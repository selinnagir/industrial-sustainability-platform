from fastapi import APIRouter, Query, HTTPException, Body, Response

from app.services.company_dashboard_service import (
    company_dataset_exists,
    load_company_dataset,
    preprocess_company_dataset,
    apply_company_filters,
    build_company_summary,
    build_company_trend,
    build_top_facilities,
    build_filter_options,
    build_sustainability_metrics,
    build_historical_analysis,
    build_anomaly_analysis,
)
from app.services.company_ai_service import build_company_ai_insights, answer_company_question
from app.services.forecast_service import build_forecast_analysis
from app.services.scenario_service import build_scenario_simulation
from app.services.sustainability_score_service import build_sustainability_score
from app.services.benchmark_service import build_benchmark_analysis
from app.services.egrid_mapper import read_egrid_state_factors
from app.services.report_service import build_company_pdf_bytes

router = APIRouter(prefix="/company", tags=["company"])

def _build_company_payload(facility: str | None = None, state: str | None = None) -> dict:
    if not company_dataset_exists():
        raise HTTPException(status_code=404, detail="Henüz kaydedilmiş şirket verisi bulunamadı.")

    df = load_company_dataset()
    df = preprocess_company_dataset(df)
    filtered = apply_company_filters(df, facility=facility, state=state)

    egrid_df = read_egrid_state_factors()
    relevant_states = sorted(filtered["state_or_region"].dropna().astype(str).str.upper().unique().tolist()) if "state_or_region" in filtered.columns else []
    egrid_reference = egrid_df[egrid_df["state_abbr"].isin(relevant_states)].copy()

    payload = {
        "summary": build_company_summary(filtered),
        "trend": build_company_trend(filtered),
        "top_facilities": build_top_facilities(filtered),
        "filters": build_filter_options(df),
        "sustainability_metrics": build_sustainability_metrics(filtered),
        "historical_analysis": build_historical_analysis(filtered),
        "anomaly_analysis": build_anomaly_analysis(filtered),
        "forecast_analysis": build_forecast_analysis(filtered),
        "egrid_reference": egrid_reference[["state_abbr", "co2e_ton_per_mwh", "co2_ton_per_mwh"]].to_dict(orient="records"),
    }

    payload["sustainability_score"] = build_sustainability_score(payload)
    payload["benchmark_analysis"] = build_benchmark_analysis(filtered, payload)
    return payload

@router.get("/dashboard")
def get_company_dashboard(
    facility: str | None = Query(default=None),
    state: str | None = Query(default=None),
):
    return _build_company_payload(facility=facility, state=state)

@router.get("/ai-insights")
def get_company_ai_insights(
    facility: str | None = Query(default=None),
    state: str | None = Query(default=None),
):
    payload = _build_company_payload(facility=facility, state=state)
    insights = build_company_ai_insights(payload)

    return {
        "dashboard_context": payload,
        "insights": insights,
    }

@router.get("/benchmark")
def get_company_benchmark(
    facility: str | None = Query(default=None),
    state: str | None = Query(default=None),
):
    payload = _build_company_payload(facility=facility, state=state)
    return payload["benchmark_analysis"]

@router.post("/chat")
def company_chat(body: dict = Body(...)):
    question = (body.get("question") or "").strip()
    facility = body.get("facility")
    state = body.get("state")

    payload = _build_company_payload(facility=facility, state=state)
    response = answer_company_question(question, payload)

    return {
        "question": question,
        "question_type": response["question_type"],
        "answer": response["answer"],
        "used_filters": {
            "facility": facility,
            "state": state,
        },
    }

@router.post("/scenario-simulate")
def company_scenario_simulate(body: dict = Body(...)):
    facility = body.get("facility")
    state = body.get("state")
    energy_reduction_pct = body.get("energy_reduction_pct", 0)
    emissions_reduction_pct = body.get("emissions_reduction_pct", 0)

    payload = _build_company_payload(facility=facility, state=state)
    result = build_scenario_simulation(
        payload,
        energy_reduction_pct=energy_reduction_pct,
        emissions_reduction_pct=emissions_reduction_pct,
    )

    return {
        "used_filters": {
            "facility": facility,
            "state": state,
        },
        "result": result,
    }

@router.get("/report/pdf")
def get_company_report_pdf(
    facility: str | None = Query(default=None),
    state: str | None = Query(default=None),
):
    payload = _build_company_payload(facility=facility, state=state)
    pdf_bytes = build_company_pdf_bytes(payload, facility=facility, state=state)

    filename_parts = ["company_report"]
    if facility:
        filename_parts.append(str(facility).replace(" ", "_"))
    if state:
        filename_parts.append(str(state).replace(" ", "_"))

    filename = "_".join(filename_parts) + ".pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
