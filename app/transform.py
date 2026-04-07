from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
KPI_OUTPUT = OUTPUT_DIR / "kpi_data_product.csv"
FORECAST_OUTPUT = OUTPUT_DIR / "forecast_data_product.csv"


def _aggregate_brand_market_size(values: pd.Series) -> float:
    unique_values = values.dropna().unique()
    if len(unique_values) <= 1:
        return float(unique_values[0]) if len(unique_values) == 1 else 0.0
    return float(values.sum())


def load_source_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    sales_df = pd.read_csv(DATA_DIR / "sales.csv", parse_dates=["date"])
    market_df = pd.read_csv(DATA_DIR / "market.csv", parse_dates=["date"])
    return sales_df, market_df


def build_data_products() -> tuple[pd.DataFrame, pd.DataFrame]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sales_df, market_df = load_source_data()
    sales_brand_monthly = (
        sales_df.groupby(["date", "brand"], as_index=False)
        .agg(
            sales_total=("sales", "sum"),
            units=("units", "sum"),
            conversions=("conversions", "sum"),
        )
        .sort_values(["brand", "date"])
    )
    market_brand_monthly = (
        market_df.groupby(["date", "brand"], as_index=False)
        .agg(
            market_size=("market_size", _aggregate_brand_market_size),
            avg_market_growth=("market_growth", "mean"),
        )
        .sort_values(["brand", "date"])
    )
    brand_monthly = sales_brand_monthly.merge(
        market_brand_monthly,
        on=["date", "brand"],
        how="left",
        validate="one_to_one",
    )

    brand_monthly["conversion_rate"] = brand_monthly["conversions"] / brand_monthly["units"]
    brand_monthly["market_share"] = brand_monthly["sales_total"] / brand_monthly["market_size"]
    brand_monthly["sales_growth_pct"] = (
        brand_monthly.groupby("brand")["sales_total"].pct_change().fillna(0.0)
    )
    brand_monthly["period"] = brand_monthly["date"].dt.strftime("%Y-%m")
    brand_monthly.to_csv(KPI_OUTPUT, index=False)

    merged = sales_df.merge(
        market_df,
        on=["date", "brand", "product", "region"],
        how="left",
        validate="many_to_one",
    )

    product_monthly = (
        merged.groupby(["date", "brand", "product"], as_index=False)
        .agg(
            sales_total=("sales", "sum"),
            market_size=("market_size", "sum"),
            avg_market_growth=("market_growth", "mean"),
        )
        .sort_values(["product", "date"])
    )
    product_monthly["period"] = product_monthly["date"].dt.strftime("%Y-%m")
    product_monthly.to_csv(FORECAST_OUTPUT, index=False)

    return brand_monthly, product_monthly


def get_kpi_for_brand(brand: str) -> dict:
    kpi_df = pd.read_csv(KPI_OUTPUT, parse_dates=["date"])
    brand_slice = kpi_df.loc[kpi_df["brand"].str.lower() == brand.lower()].sort_values("date")
    if brand_slice.empty:
        raise ValueError(f"Unknown brand: {brand}")

    latest = brand_slice.iloc[-1]
    return {
        "brand": latest["brand"],
        "period": latest["period"],
        "sales_total": round(float(latest["sales_total"]), 2),
        "sales_growth_pct": round(float(latest["sales_growth_pct"]), 4),
        "conversion_rate": round(float(latest["conversion_rate"]), 4),
        "market_share": round(float(latest["market_share"]), 4),
        "market_growth_pct": round(float(latest["avg_market_growth"]), 4),
    }


def get_market_slide_data(brand: str) -> dict:
    kpi_df = pd.read_csv(KPI_OUTPUT, parse_dates=["date"])
    brand_slice = kpi_df.loc[kpi_df["brand"].str.lower() == brand.lower()].sort_values("date")
    if brand_slice.empty:
        raise ValueError(f"Unknown brand: {brand}")

    latest = brand_slice.iloc[-1]
    first = brand_slice.iloc[0]
    market_size_growth = (float(latest["market_size"]) - float(first["market_size"])) / float(
        first["market_size"]
    )
    return {
        "brand": latest["brand"],
        "latest_market_size": round(float(latest["market_size"]), 2),
        "market_size_growth_pct": round(market_size_growth, 4),
        "latest_market_growth_pct": round(float(latest["avg_market_growth"]), 4),
    }
