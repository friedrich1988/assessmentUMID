from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def month_starts() -> list[date]:
    return [date(2025, month, 1) for month in range(1, 13)]


def build_sales_rows() -> list[list[object]]:
    configs = [
        ("BrandA", "ProductA1", "DACH", 180000, 9200, 1180, 6500, 140, 30),
        ("BrandA", "ProductA2", "DACH", 120000, 7000, 810, 2700, 110, 16),
        ("BrandB", "ProductB1", "DACH", 155000, 8600, 1010, 3100, 115, 16),
    ]

    rows: list[list[object]] = []
    for month_idx, month in enumerate(month_starts()):
        for brand, product, region, sales, units, conversions, sales_step, units_step, conv_step in configs:
            rows.append(
                [
                    month.isoformat(),
                    brand,
                    product,
                    region,
                    sales + month_idx * sales_step,
                    units + month_idx * units_step,
                    conversions + month_idx * conv_step,
                ]
            )
    return rows


def build_market_rows() -> list[list[object]]:
    configs = [
        ("BrandA", "ProductA1", "DACH", 900000, 10000, 0.018, 0.0005),
        ("BrandA", "ProductA2", "DACH", 620000, 7600, 0.014, 0.00045),
        ("BrandB", "ProductB1", "DACH", 780000, 8400, 0.013, 0.00045),
    ]

    rows: list[list[object]] = []
    for month_idx, month in enumerate(month_starts()):
        for brand, product, region, market_size, market_size_step, growth, growth_step in configs:
            rows.append(
                [
                    month.isoformat(),
                    brand,
                    product,
                    region,
                    market_size + month_idx * market_size_step,
                    round(growth + month_idx * growth_step, 4),
                ]
            )
    return rows


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    write_csv(
        DATA_DIR / "sales.csv",
        ["date", "brand", "product", "region", "sales", "units", "conversions"],
        build_sales_rows(),
    )
    write_csv(
        DATA_DIR / "market.csv",
        ["date", "brand", "product", "region", "market_size", "market_growth"],
        build_market_rows(),
    )
    print(f"Wrote fake datasets to {DATA_DIR}")


if __name__ == "__main__":
    main()
