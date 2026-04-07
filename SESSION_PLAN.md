# Session Continuation Plan

## Current State

- Repository scaffolded for the interview MVP.
- Implemented files:
  - `app/main.py`
  - `app/transform.py`
  - `app/forecast.py`
  - `app/prompt_parser.py`
  - `app/ppt_generator.py`
  - `app/models.py`
  - `scripts/generate_fake_data.py`
  - `data/sales.csv`
  - `data/market.csv`
  - `README.md`
  - `requirements.txt`
- Fake source datasets exist and can be regenerated with:
  - `python scripts/generate_fake_data.py`

## Environment Constraint

- Only these Python executables are currently on `PATH`:
  - `python`
  - `python3`
  - `python3.14`
- `python3.12` is not installed on this machine.

## Main Risk

- The current dependency set includes `pandas` and `scikit-learn`.
- On Python 3.14 this may trigger source builds or wheel availability issues, which is risky for a fast interview demo.

## Recommended Next Step

Choose one of these two paths:

1. Preferred if possible:
   - Install Python 3.12 and recreate the virtualenv with it.
   - Reuse the current code with minimal changes.

2. Fallback if staying on Python 3.14:
   - Remove `pandas` and `scikit-learn` from the MVP.
   - Rewrite transformation and forecast logic using only:
     - `csv`
     - `datetime`
     - `statistics`
     - simple hand-rolled linear regression
   - Keep `fastapi`, `uvicorn`, and `python-pptx`.

## Concrete Resume Checklist

1. Decide runtime strategy:
   - use Python 3.12 if installed later
   - or simplify dependencies for Python 3.14
2. Create or recreate virtualenv
3. Install dependencies
4. Run:
   - `python scripts/generate_fake_data.py`
5. Start API:
   - `uvicorn app.main:app --reload`
6. Verify endpoints:
   - `GET /health`
   - `GET /kpi?brand=BrandA`
   - `GET /forecast?product=ProductA1`
   - `POST /ask`
7. Confirm PPT output is generated in `output/`
8. If needed, tighten README wording for interview presentation

## Suggested Talking Point

If the demo is discussed before verification is complete:

"The MVP is structured end to end already. The remaining work is environment-hardening for the chosen Python runtime and then a final smoke test of API plus PowerPoint generation."
