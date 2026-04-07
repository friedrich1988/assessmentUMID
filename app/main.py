from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from app.forecast import forecast_product
from app.frontend import render_frontend
from app.models import AskRequest
from app.ppt_generator import build_presentation
from app.prompt_parser import parse_question
from app.transform import build_data_products, get_kpi_for_brand, get_market_slide_data

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"


@asynccontextmanager
async def lifespan(_: FastAPI):
    build_data_products()
    yield


app = FastAPI(
    title="Galderma Presentation MVP",
    description="Interview MVP for KPI, forecast, prompt parsing, and PowerPoint generation",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return render_frontend()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/kpi")
def get_kpi(brand: str) -> dict:
    try:
        return get_kpi_for_brand(brand)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/forecast")
def get_forecast(product: str) -> dict:
    try:
        return forecast_product(product)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/ask")
def ask_copilot(request: AskRequest) -> dict:
    parsed = parse_question(request.question)
    try:
        kpi = get_kpi_for_brand(parsed["brand"])
        forecast = forecast_product(parsed["product"])
        market = get_market_slide_data(parsed["brand"])
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    presentation_file = None
    if parsed["intent"] == "generate_presentation":
        presentation_file = build_presentation(kpi, forecast, market)

    return {
        "intent": parsed["intent"],
        "question": parsed["original_question"],
        "parser_warnings": parsed["warnings"],
        "brand": kpi["brand"],
        "product": forecast["product"],
        "period": parsed["period"],
        "kpi": kpi,
        "forecast": forecast if parsed["wants_forecast"] else None,
        "presentation_file": presentation_file,
    }


@app.get("/presentation/{brand}")
def download_presentation(brand: str) -> FileResponse:
    presentation_path = OUTPUT_DIR / f"{brand}_business_review.pptx"
    if not presentation_path.exists():
        raise HTTPException(status_code=404, detail=f"No presentation found for brand: {brand}")
    return FileResponse(
        presentation_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=presentation_path.name,
    )
