# Galderma Deck Generation MVP

This repository contains a small working end-to-end MVP for automated business presentation generation.

The MVP simulates the target architecture from the case:

- `CSV files` represent incoming sales and market data from the enterprise data platform.
- `Transformation logic` creates two local data products:
  - `KPI Data Product`
  - `Forecast Data Product`
- `FastAPI` represents the governed API layer that would later sit in front of Snowflake.
- `Prompt parsing` acts as a deterministic Copilot stub.
- `python-pptx` generates a PowerPoint deck automatically.

## Architecture Mapping

Target architecture in the case:

- Azure Data Factory -> ingestion/orchestration
- Azure-based Data Platform -> raw and harmonized enterprise data
- Snowflake -> curated analytics-ready storage
- Classic data products -> reusable sales and business datasets
- Copilot -> prompt-driven orchestration

Local MVP implementation:

- `data/*.csv` -> source extracts
- `app/transform.py` -> harmonization and data product creation
- `output/kpi_data_product.csv` -> KPI data product
- `output/forecast_data_product.csv` -> forecast data product
- `app/main.py` -> API endpoints
- `app/prompt_parser.py` -> dummy AI orchestration
- `app/ppt_generator.py` -> automated slide deck generation

## MVP Scope

Implemented:

1. Load sample datasets (`sales.csv`, `market.csv`)
2. Transform to KPI data
3. Run a simple forecast model using linear regression
4. Expose API endpoints
   - `GET /kpi?brand=BrandA`
   - `GET /forecast?product=ProductA1`
   - `POST /ask`
5. Parse a natural-language request via a rule-based prompt parser
6. Generate a PowerPoint presentation with:
   - Title slide
   - KPI slide
   - Forecast slide
   - Market development slide

## KPI Logic

The MVP uses simple, explicit KPI definitions:

- `sales_total = sum(sales)`
- `sales_growth_pct = month-over-month growth`
- `conversion_rate = conversions / units`
- `market_share = sales_total / market_size`

## Forecast Logic

For the MVP, forecasting uses linear regression on:

- month index
- market size
- market growth

Output includes:

- next month forecast (`Forecast EoM`)
- next quarter total (`Forecast Tercial`)
- 95% confidence interval approximation based on residual standard deviation

In production this could be replaced with Prophet, ARIMA, or a dedicated forecasting service.

## Setup

Tested runtime for this repository:

- `Python 3.14`

Install dependencies in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Regenerate fake input data if needed:

```bash
python scripts/generate_fake_data.py
```

## Run The API

```bash
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`

## Quick Smoke Test

Verify the main MVP flow step by step:

```bash
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/kpi?brand=BrandA"
curl "http://127.0.0.1:8000/forecast?product=ProductA1"
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Create a presentation for BrandA with forecast for the next quarter and include product ProductA1"}'
```

Expected result:

- health endpoint returns `{"status":"ok"}`
- KPI endpoint returns the latest KPI snapshot for `BrandA`
- forecast endpoint returns the next three forecast months for `ProductA1`
- ask endpoint returns KPI + forecast JSON and writes a PowerPoint file to `output/BrandA_business_review.pptx`

## Example Calls

Get KPI data:

```bash
curl "http://127.0.0.1:8000/kpi?brand=BrandA"
```

Get forecast:

```bash
curl "http://127.0.0.1:8000/forecast?product=ProductA1"
```

Ask the Copilot stub to generate a deck:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Create a presentation for BrandA with forecast for the next quarter and include product ProductA1"}'
```

Output:

- PowerPoint deck written to `output/BrandA_business_review.pptx`

Note:

- If the prompt does not explicitly mention a product, the parser defaults to `ProductA1` and returns that choice in `parser_warnings`

## Governance Perspective

Even in this MVP, the design follows the intended governance model:

- only curated data products are exposed to the API
- KPI definitions are centralized in code
- generated outputs are reproducible
- prompt handling is deterministic and auditable
- versioning and audit trail can be handled via GitHub history

## Limitations

- No real Azure Data Factory integration
- No real Snowflake integration
- No real semantic layer product
- No authentication / RBAC
- No production-grade forecast model lifecycle
- No real LLM integration

These are intentionally replaced with local stand-ins so the end-to-end product flow can be demonstrated quickly within interview constraints.
