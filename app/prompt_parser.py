from __future__ import annotations

import re


BRAND_PATTERN = re.compile(r"\b(?:brand\s+)?(Brand[a-z0-9_-]*)\b", re.IGNORECASE)
PRODUCT_PATTERN = re.compile(r"\b(?:product\s+)?(Product[a-z0-9_-]*)\b", re.IGNORECASE)


def parse_question(question: str) -> dict:
    normalized = question.strip()
    lowered = normalized.lower()

    brand_match = BRAND_PATTERN.search(normalized)
    product_match = PRODUCT_PATTERN.search(normalized)

    period = "next_quarter" if "next quarter" in lowered else "latest"
    intent = "generate_presentation" if "presentation" in lowered or "deck" in lowered else "get_kpi"
    wants_forecast = "forecast" in lowered
    warnings: list[str] = []

    if not brand_match:
        warnings.append("No brand found in question. Defaulted to BrandA.")
    if not product_match:
        warnings.append("No product found in question. Defaulted to ProductA1.")

    return {
        "intent": intent,
        "brand": brand_match.group(1) if brand_match else "BrandA",
        "product": product_match.group(1) if product_match else "ProductA1",
        "period": period,
        "wants_forecast": wants_forecast,
        "original_question": normalized,
        "warnings": warnings,
    }
