import pandas as pd

def preprocess_company_dataset(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"], errors="coerce")

    for col in ["energy_mwh", "electricity_mwh", "direct_emissions_tons", "water_use", "waste_tons", "production_amount"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    for col in ["company_name", "facility_name", "state_or_region", "fuel_type"]:
        if col in out.columns:
            out[col] = out[col].astype(str).str.strip()
            out.loc[out[col].isin(["None", "nan", "NaN"]), col] = None

    out = out.dropna(subset=["facility_name", "date"], how="any")
    out = out.reset_index(drop=True)
    return out

def apply_company_filters(df: pd.DataFrame, facility: str | None = None, state: str | None = None):
    out = df.copy()

    if facility and facility != "All":
        out = out[out["facility_name"] == facility]

    if state and state != "All":
        out = out[out["state_or_region"] == state]

    return out

def build_company_summary(df: pd.DataFrame) -> dict:
    return {
        "total_energy_mwh": round(float(df["energy_mwh"].fillna(0).sum()), 3),
        "total_electricity_mwh": round(float(df["electricity_mwh"].fillna(0).sum()), 3),
        "total_direct_emissions_tons": round(float(df["direct_emissions_tons"].fillna(0).sum()), 3),
        "total_facilities": int(df["facility_name"].nunique()) if not df.empty else 0,
        "date_range_start": str(df["date"].min().date()) if not df.empty and df["date"].notna().any() else None,
        "date_range_end": str(df["date"].max().date()) if not df.empty and df["date"].notna().any() else None,
    }

def build_company_trend(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []

    trend = (
        df.assign(period=df["date"].dt.strftime("%Y-%m"))
        .groupby("period", as_index=False)[["energy_mwh", "direct_emissions_tons"]]
        .sum()
        .sort_values("period")
    )

    return [
        {
            "period": row["period"],
            "energy_mwh": round(float(row["energy_mwh"]), 3),
            "direct_emissions_tons": round(float(row["direct_emissions_tons"]), 3),
        }
        for _, row in trend.iterrows()
    ]

def build_top_company_facilities(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []

    grouped = (
        df.groupby(["facility_name", "state_or_region"], as_index=False)[["energy_mwh", "direct_emissions_tons"]]
        .sum()
        .sort_values("energy_mwh", ascending=False)
        .head(10)
    )

    return [
        {
            "facility_name": row["facility_name"],
            "state_or_region": row["state_or_region"],
            "energy_mwh": round(float(row["energy_mwh"]), 3),
            "direct_emissions_tons": round(float(row["direct_emissions_tons"]), 3),
        }
        for _, row in grouped.iterrows()
    ]

def build_company_filters(df: pd.DataFrame) -> dict:
    return {
        "facilities": sorted([x for x in df["facility_name"].dropna().unique().tolist() if str(x).strip()]),
        "states": sorted([x for x in df["state_or_region"].dropna().unique().tolist() if str(x).strip()]),
    }

def build_sustainability_metrics(df: pd.DataFrame) -> dict:
    total_energy = float(df["energy_mwh"].fillna(0).sum())
    total_direct = float(df["direct_emissions_tons"].fillna(0).sum())
    total_water = float(df["water_use"].fillna(0).sum())
    total_waste = float(df["waste_tons"].fillna(0).sum())
    total_production = float(df["production_amount"].fillna(0).sum())

    carbon_intensity = (total_direct / total_energy) if total_energy > 0 else None
    water_intensity = (total_water / total_energy) if total_energy > 0 else None
    waste_intensity = (total_waste / total_energy) if total_energy > 0 else None
    production_energy_intensity = (total_energy / total_production) if total_production > 0 else None

    return {
        "carbon_intensity_ton_per_mwh": round(carbon_intensity, 6) if carbon_intensity is not None else None,
        "water_intensity_per_mwh": round(water_intensity, 6) if water_intensity is not None else None,
        "waste_intensity_per_mwh": round(waste_intensity, 6) if waste_intensity is not None else None,
        "energy_per_production_unit": round(production_energy_intensity, 6) if production_energy_intensity is not None else None,
    }
