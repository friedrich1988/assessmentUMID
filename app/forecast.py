from __future__ import annotations

from math import sqrt

import pandas as pd

from app.transform import FORECAST_OUTPUT


def _load_product_history(product: str) -> pd.DataFrame:
    forecast_df = pd.read_csv(FORECAST_OUTPUT, parse_dates=["date"])
    product_slice = forecast_df.loc[
        forecast_df["product"].str.lower() == product.lower()
    ].sort_values("date")
    if product_slice.empty:
        raise ValueError(f"Unknown product: {product}")
    product_slice = product_slice.reset_index(drop=True)
    product_slice["month_index"] = range(len(product_slice))
    return product_slice


def _solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    augmented = [row[:] + [vector[idx]] for idx, row in enumerate(matrix)]

    for pivot in range(size):
        max_row = max(range(pivot, size), key=lambda row: abs(augmented[row][pivot]))
        augmented[pivot], augmented[max_row] = augmented[max_row], augmented[pivot]
        pivot_value = augmented[pivot][pivot]
        if abs(pivot_value) < 1e-12:
            raise ValueError("Regression matrix is singular")

        for column in range(pivot, size + 1):
            augmented[pivot][column] /= pivot_value

        for row in range(size):
            if row == pivot:
                continue
            factor = augmented[row][pivot]
            for column in range(pivot, size + 1):
                augmented[row][column] -= factor * augmented[pivot][column]

    return [augmented[row][size] for row in range(size)]


def _fit_linear_regression(features: list[list[float]], target: list[float]) -> list[float]:
    feature_count = len(features[0])
    design_matrix = [[1.0, *row] for row in features]
    parameter_count = feature_count + 1
    ridge_lambda = 1e-6

    xtx = [[0.0 for _ in range(parameter_count)] for _ in range(parameter_count)]
    xty = [0.0 for _ in range(parameter_count)]

    for row, y_value in zip(design_matrix, target, strict=True):
        for left in range(parameter_count):
            xty[left] += row[left] * y_value
            for right in range(parameter_count):
                xtx[left][right] += row[left] * row[right]

    for index in range(1, parameter_count):
        xtx[index][index] += ridge_lambda

    return _solve_linear_system(xtx, xty)


def _predict(coefficients: list[float], features: list[float]) -> float:
    return coefficients[0] + sum(
        coefficient * value for coefficient, value in zip(coefficients[1:], features, strict=True)
    )


def forecast_product(product: str, periods: int = 3) -> dict:
    history = _load_product_history(product)

    feature_rows = history[["month_index", "market_size", "avg_market_growth"]].astype(float)
    features = feature_rows.values.tolist()
    target = history["sales_total"].astype(float).tolist()
    coefficients = _fit_linear_regression(features, target)

    history_pred = [_predict(coefficients, row) for row in features]
    if len(target) > 1:
        squared_error = sum((actual - predicted) ** 2 for actual, predicted in zip(target, history_pred, strict=True))
        residual_std = sqrt(squared_error / (len(target) - 1))
    else:
        residual_std = 0.0

    last_row = history.iloc[-1]
    last_date = pd.Timestamp(last_row["date"])
    last_market_size = float(last_row["market_size"])
    last_market_growth = float(last_row["avg_market_growth"])
    market_size_step = history["market_size"].pct_change().dropna().mean()
    if pd.isna(market_size_step):
        market_size_step = 0.01

    forecasts = []
    for step in range(1, periods + 1):
        future_date = last_date + pd.DateOffset(months=step)
        future_market_size = last_market_size * ((1 + market_size_step) ** step)
        future_market_growth = last_market_growth
        future_month_index = int(last_row["month_index"]) + step

        prediction = float(
            _predict(coefficients, [future_month_index, future_market_size, future_market_growth])
        )
        lower_ci = prediction - 1.96 * residual_std
        upper_ci = prediction + 1.96 * residual_std
        forecasts.append(
            {
                "month": future_date.strftime("%Y-%m"),
                "forecast_sales": round(prediction, 2),
                "lower_ci": round(lower_ci, 2),
                "upper_ci": round(upper_ci, 2),
            }
        )

    return {
        "product": history.iloc[-1]["product"],
        "brand": history.iloc[-1]["brand"],
        "history_months": history["period"].tolist(),
        "forecast_months": forecasts,
        "forecast_eom": forecasts[0]["forecast_sales"],
        "forecast_tercial": round(sum(item["forecast_sales"] for item in forecasts), 2),
        "forecast_next_quarter_total": round(sum(item["forecast_sales"] for item in forecasts), 2),
        "confidence_interval_method": "95% interval derived from linear-regression residual standard deviation",
    }
