import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def _candidate_ghgrp_paths() -> list[Path]:
    return [
        BASE_DIR / "data" / "raw" / "ghgrp_data_2023.xlsx",
        BASE_DIR / "data" / "reference" / "ghgrp_data_2023.xlsx",
        BASE_DIR / "data" / "raw" / "GHGRP_data_2023.xlsx",
        BASE_DIR / "data" / "reference" / "GHGRP_data_2023.xlsx",
        BASE_DIR / "data" / "raw" / "ghgrp_2023.xlsx",
        BASE_DIR / "data" / "reference" / "ghgrp_2023.xlsx",
    ]

def _resolve_ghgrp_path() -> Path | None:
    for path in _candidate_ghgrp_paths():
        if path.exists():
            return path

    data_dir = BASE_DIR / "data"
    if data_dir.exists():
        matches = list(data_dir.rglob("*ghgrp*.xlsx"))
        if matches:
            return matches[0]

    return None

def _empty_ghgrp_df() -> pd.DataFrame:
    return pd.DataFrame(columns=[
        "facility_name",
        "state_or_region",
        "sector",
        "reported_emissions_co2e",
    ])

def _read_ghgrp_reference() -> pd.DataFrame:
    ghgrp_path = _resolve_ghgrp_path()
    if ghgrp_path is None:
        return _empty_ghgrp_df()

    try:
        df = pd.read_excel(ghgrp_path)
    except Exception:
        return _empty_ghgrp_df()

    rename_map = {
        "Facility Name": "facility_name",
        "State": "state_or_region",
        "Industry Type (sectors)": "sector",
        "Total reported direct emissions": "reported_emissions_co2e",
    }

    existing = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=existing)

    keep_cols = [c for c in ["facility_name", "state_or_region", "sector", "reported_emissions_co2e"] if c in df.columns]
    if not keep_cols:
        return _empty_ghgrp_df()

    df = df[keep_cols].copy()

    if "state_or_region" in df.columns:
        df["state_or_region"] = df["state_or_region"].astype(str).str.strip().str.upper()

    if "sector" in df.columns:
        df["sector"] = df["sector"].astype(str).str.strip()
        df.loc[df["sector"].isin(["nan", "None", ""]), "sector"] = None

    if "reported_emissions_co2e" in df.columns:
        df["reported_emissions_co2e"] = pd.to_numeric(df["reported_emissions_co2e"], errors="coerce")

    if "state_or_region" not in df.columns:
        return _empty_ghgrp_df()

    return df.dropna(subset=["state_or_region"], how="any")

def _detect_company_sector_column(df: pd.DataFrame) -> str | None:
    candidates = [
        "sector",
        "industry_type",
        "industry",
        "category",
        "business_sector",
        "sector_name",
    ]
    for col in candidates:
        if col in df.columns:
            return col
    return None

def build_benchmark_analysis(company_df: pd.DataFrame, company_payload: dict) -> dict:
    summary = company_payload.get("summary", {})
    sustainability_metrics = company_payload.get("sustainability_metrics", {})
    company_carbon_intensity = sustainability_metrics.get("carbon_intensity_ton_per_mwh")
    company_total_emissions = summary.get("total_direct_emissions_tons", 0)
    company_total_energy = summary.get("total_energy_mwh", 0)

    states = (
        company_df["state_or_region"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .unique()
        .tolist()
        if "state_or_region" in company_df.columns
        else []
    )
    selected_state = states[0] if len(states) == 1 else None

    egrid_reference = company_payload.get("egrid_reference", [])
    state_benchmark = None

    if selected_state and company_carbon_intensity is not None:
        match = next((x for x in egrid_reference if x.get("state_abbr") == selected_state), None)
        if match:
            ref_value = match.get("co2e_ton_per_mwh")
            if ref_value is not None:
                gap = round(company_carbon_intensity - ref_value, 6)
                status = "better" if company_carbon_intensity < ref_value else "worse" if company_carbon_intensity > ref_value else "equal"

                state_benchmark = {
                    "state": selected_state,
                    "company_carbon_intensity_ton_per_mwh": company_carbon_intensity,
                    "reference_carbon_intensity_ton_per_mwh": ref_value,
                    "gap_ton_per_mwh": gap,
                    "status": status,
                }

    ghgrp_df = _read_ghgrp_reference()

    state_reference = None
    if selected_state and not ghgrp_df.empty:
        state_slice = ghgrp_df[ghgrp_df["state_or_region"] == selected_state].copy()
        if not state_slice.empty and "reported_emissions_co2e" in state_slice.columns:
            state_reference = {
                "state": selected_state,
                "reference_facility_count": int(state_slice["facility_name"].nunique()) if "facility_name" in state_slice.columns else int(len(state_slice)),
                "reference_avg_direct_emissions_tons": round(float(state_slice["reported_emissions_co2e"].dropna().mean()), 3),
                "reference_total_direct_emissions_tons": round(float(state_slice["reported_emissions_co2e"].dropna().sum()), 3),
            }

    sector_col = _detect_company_sector_column(company_df)
    sector_benchmark = None

    if sector_col and not ghgrp_df.empty:
        company_sector_values = (
            company_df[sector_col]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .unique()
            .tolist()
        )

        if len(company_sector_values) == 1 and "sector" in ghgrp_df.columns:
            selected_sector = company_sector_values[0]
            sector_slice = ghgrp_df[
                ghgrp_df["sector"].astype(str).str.contains(selected_sector, case=False, na=False)
            ].copy()

            if not sector_slice.empty and "reported_emissions_co2e" in sector_slice.columns:
                sector_benchmark = {
                    "sector": selected_sector,
                    "reference_facility_count": int(sector_slice["facility_name"].nunique()) if "facility_name" in sector_slice.columns else int(len(sector_slice)),
                    "reference_avg_direct_emissions_tons": round(float(sector_slice["reported_emissions_co2e"].dropna().mean()), 3),
                    "reference_total_direct_emissions_tons": round(float(sector_slice["reported_emissions_co2e"].dropna().sum()), 3),
                    "company_total_direct_emissions_tons": round(float(company_total_emissions), 3),
                }

    commentary = []

    if state_benchmark:
        if state_benchmark["status"] == "better":
            commentary.append(f"Şirket karbon yoğunluğu {state_benchmark['state']} eGRID referansından daha iyi.")
        elif state_benchmark["status"] == "worse":
            commentary.append(f"Şirket karbon yoğunluğu {state_benchmark['state']} eGRID referansından daha kötü.")
        else:
            commentary.append(f"Şirket karbon yoğunluğu {state_benchmark['state']} eGRID referansına yakın.")

    if state_reference:
        commentary.append(
            f"{state_reference['state']} için GHGRP referansında ortalama tesis emisyonu "
            f"{state_reference['reference_avg_direct_emissions_tons']} ton."
        )

    if sector_benchmark:
        commentary.append(
            f"{sector_benchmark['sector']} sektörü için GHGRP referans ortalama emisyonu "
            f"{sector_benchmark['reference_avg_direct_emissions_tons']} ton."
        )

    if ghgrp_df.empty:
        commentary.append("GHGRP referans dosyası bulunamadı ya da okunamadı. Bu yüzden sadece mevcut referanslar gösteriliyor.")

    if not sector_col:
        commentary.append("Company dataset içinde sektör kolonu olmadığı için sektör benchmarkı hesaplanamadı.")

    return {
        "company_context": {
            "total_energy_mwh": round(float(company_total_energy), 3),
            "total_direct_emissions_tons": round(float(company_total_emissions), 3),
            "carbon_intensity_ton_per_mwh": company_carbon_intensity,
            "selected_state": selected_state,
            "sector_column_detected": sector_col,
        },
        "state_benchmark": state_benchmark,
        "state_reference": state_reference,
        "sector_benchmark": sector_benchmark,
        "commentary": commentary,
    }

