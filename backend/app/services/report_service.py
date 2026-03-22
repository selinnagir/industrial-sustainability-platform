from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def _fmt(value, digits=3):
    if value is None:
        return "-"
    try:
        return f"{float(value):,.{digits}f}"
    except Exception:
        return str(value)


def _safe_text(value):
    if value is None:
        return "-"
    return str(value)


def build_company_pdf_bytes(payload: dict, facility: str | None = None, state: str | None = None) -> bytes:
    summary = payload.get("summary", {})
    sustainability = payload.get("sustainability_metrics", {})
    score = payload.get("sustainability_score", {})
    benchmark = payload.get("benchmark_analysis", {})
    anomaly = payload.get("anomaly_analysis", {})
    forecast = payload.get("forecast_analysis", {})

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    small_style = ParagraphStyle(
        "Small",
        parent=normal_style,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4B5563"),
    )

    story = []

    report_title = "Industrial Sustainability Report"
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 6))

    filter_lines = [
        f"Generated at: {report_time}",
        f"Facility filter: {_safe_text(facility)}",
        f"State filter: {_safe_text(state)}",
    ]
    for line in filter_lines:
        story.append(Paragraph(line, small_style))

    story.append(Spacer(1, 14))

    story.append(Paragraph("1. Executive Summary", heading_style))
    summary_data = [
        ["Metric", "Value"],
        ["Total Energy (MWh)", _fmt(summary.get("total_energy_mwh"))],
        ["Total Direct Emissions (tons)", _fmt(summary.get("total_direct_emissions_tons"))],
        ["Average Energy / Period", _fmt(summary.get("avg_energy_per_period"))],
        ["Average Emissions / Period", _fmt(summary.get("avg_emissions_per_period"))],
        ["Carbon Intensity", _fmt(sustainability.get("carbon_intensity_ton_per_mwh"), 6)],
        ["Water Intensity", _fmt(sustainability.get("water_intensity_per_mwh"), 6)],
        ["Waste Intensity", _fmt(sustainability.get("waste_intensity_per_mwh"), 6)],
    ]

    summary_table = Table(summary_data, colWidths=[70 * mm, 80 * mm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("2. Sustainability Score", heading_style))
    score_data = [
        ["Score", _safe_text(score.get("score"))],
        ["Grade", _safe_text(score.get("grade"))],
        ["Label", _safe_text(score.get("label"))],
    ]
    score_table = Table(score_data, colWidths=[70 * mm, 80 * mm])
    score_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 8))

    strengths = score.get("strengths", []) or []
    weaknesses = score.get("weaknesses", []) or []
    drivers = score.get("drivers", []) or []

    story.append(Paragraph("Top Strengths", styles["Heading3"]))
    for item in strengths[:5]:
        story.append(Paragraph(f"- {_safe_text(item)}", normal_style))
    if not strengths:
        story.append(Paragraph("- No strength item available.", normal_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Top Weaknesses", styles["Heading3"]))
    for item in weaknesses[:5]:
        story.append(Paragraph(f"- {_safe_text(item)}", normal_style))
    if not weaknesses:
        story.append(Paragraph("- No weakness item available.", normal_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Key Drivers", styles["Heading3"]))
    for item in drivers[:5]:
        story.append(Paragraph(f"- {_safe_text(item)}", normal_style))
    if not drivers:
        story.append(Paragraph("- No driver item available.", normal_style))

    story.append(Spacer(1, 14))

    story.append(Paragraph("3. Benchmark Analysis", heading_style))
    company_context = benchmark.get("company_context", {}) or {}
    state_benchmark = benchmark.get("state_benchmark", {}) or {}
    state_reference = benchmark.get("state_reference", {}) or {}
    sector_benchmark = benchmark.get("sector_benchmark", {}) or {}

    benchmark_data = [
        ["Field", "Value"],
        ["Selected State", _safe_text(company_context.get("selected_state"))],
        ["Sector Column", _safe_text(company_context.get("sector_column_detected"))],
        ["Company Carbon Intensity", _fmt(company_context.get("carbon_intensity_ton_per_mwh"), 6)],
        ["State Benchmark Status", _safe_text(state_benchmark.get("status"))],
        ["State Benchmark Gap", _fmt(state_benchmark.get("gap_ton_per_mwh"), 6)],
        ["State Ref Avg Direct Emissions", _fmt(state_reference.get("reference_avg_direct_emissions_tons"))],
        ["Sector Ref Avg Direct Emissions", _fmt(sector_benchmark.get("reference_avg_direct_emissions_tons"))],
    ]
    benchmark_table = Table(benchmark_data, colWidths=[70 * mm, 80 * mm])
    benchmark_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(benchmark_table)

    commentary = benchmark.get("commentary", []) or []
    story.append(Spacer(1, 8))
    story.append(Paragraph("Benchmark Commentary", styles["Heading3"]))
    for item in commentary[:6]:
        story.append(Paragraph(f"- {_safe_text(item)}", normal_style))
    if not commentary:
        story.append(Paragraph("- No benchmark commentary available.", normal_style))

    story.append(Spacer(1, 14))

    story.append(Paragraph("4. Risk and Forecast", heading_style))
    risk_data = [
        ["Field", "Value"],
        ["Total Anomalies", _safe_text(anomaly.get("total_anomalies"))],
        ["Risk Level", _safe_text(anomaly.get("risk_level"))],
        ["Forecast Energy", _fmt(forecast.get("forecast_energy_mwh"))],
        ["Forecast Direct Emissions", _fmt(forecast.get("forecast_direct_emissions_tons"))],
        ["Forecast Carbon Intensity", _fmt(forecast.get("forecast_carbon_intensity_ton_per_mwh"), 6)],
    ]
    risk_table = Table(risk_data, colWidths=[70 * mm, 80 * mm])
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#065F46")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(risk_table)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
