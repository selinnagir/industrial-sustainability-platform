from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = BASE_DIR / "data" / "company" / "latest_company_dataset.csv"

def company_dataset_exists() -> bool:
    return DATASET_PATH.exists()

def load_company_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError("Kaydedilmiş şirket verisi bulunamadı.")
    df = pd.read_csv(DATASET_PATH)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

def preprocess_company_dataset(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"], errors="coerce")

    numeric_cols = [
        "energy_mwh",
        "electricity_mwh",
        "direct_emissions_tons",
        "water_use",
        "waste_tons",
        "production_amount",
    ]
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    text_cols = ["company_name", "facility_name", "state_or_region", "fuel_type"]
    for col in text_cols:
        if col in out.columns:
            out[col] = out[col].astype(str).str.strip()
            out.loc[out[col].isin(["None", "nan", "NaN"]), col] = None

    out = out.dropna(subset=["facility_name", "date"], how="any")
    out = out.reset_index(drop=True)
    return out

def apply_company_filters(df: pd.DataFrame, facility: str | None = None, state: str | None = None) -> pd.DataFrame:
    out = df.copy()

    if facility and facility != "All":
        out = out[out["facility_name"] == facility]

    if state and state != "All":
        out = out[out["state_or_region"] == state]

    return out

def build_company_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_energy_mwh": 0.0,
            "total_electricity_mwh": 0.0,
            "total_direct_emissions_tons": 0.0,
            "total_facilities": 0,
            "date_range_start": None,
            "date_range_end": None,
        }

    return {
        "total_energy_mwh": round(float(df["energy_mwh"].fillna(0).sum()), 3),
        "total_electricity_mwh": round(float(df["electricity_mwh"].fillna(0).sum()), 3),
        "total_direct_emissions_tons": round(float(df["direct_emissions_tons"].fillna(0).sum()), 3),
        "total_facilities": int(df["facility_name"].nunique()),
        "date_range_start": str(df["date"].min().date()) if df["date"].notna().any() else None,
        "date_range_end": str(df["date"].max().date()) if df["date"].notna().any() else None,
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

def build_top_facilities(df: pd.DataFrame) -> list[dict]:
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

def build_filter_options(df: pd.DataFrame) -> dict:
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
    energy_per_production = (total_energy / total_production) if total_production > 0 else None

    return {
        "carbon_intensity_ton_per_mwh": round(carbon_intensity, 6) if carbon_intensity is not None else None,
        "water_intensity_per_mwh": round(water_intensity, 6) if water_intensity is not None else None,
        "waste_intensity_per_mwh": round(waste_intensity, 6) if waste_intensity is not None else None,
        "energy_per_production_unit": round(energy_per_production, 6) if energy_per_production is not None else None,
    }

def _calculate_change_percent(first_value: float, last_value: float) -> float | None:
    if first_value == 0:
        return None
    return ((last_value - first_value) / first_value) * 100

def _trend_label(change_percent: float | None) -> str:
    if change_percent is None:
        return "yetersiz veri"
    if change_percent > 3:
        return "artıyor"
    if change_percent < -3:
        return "azalıyor"
    return "stabil"

def build_historical_analysis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "period_count": 0,
            "first_period": None,
            "last_period": None,
            "energy_change_percent": None,
            "emissions_change_percent": None,
            "energy_trend_label": "yetersiz veri",
            "emissions_trend_label": "yetersiz veri",
        }

    trend_df = (
        df.assign(period=df["date"].dt.strftime("%Y-%m"))
        .groupby("period", as_index=False)[["energy_mwh", "direct_emissions_tons"]]
        .sum()
        .sort_values("period")
    )

    if trend_df.empty:
        return {
            "period_count": 0,
            "first_period": None,
            "last_period": None,
            "energy_change_percent": None,
            "emissions_change_percent": None,
            "energy_trend_label": "yetersiz veri",
            "emissions_trend_label": "yetersiz veri",
        }

    first_row = trend_df.iloc[0]
    last_row = trend_df.iloc[-1]

    energy_change = _calculate_change_percent(float(first_row["energy_mwh"]), float(last_row["energy_mwh"]))
    emissions_change = _calculate_change_percent(float(first_row["direct_emissions_tons"]), float(last_row["direct_emissions_tons"]))

    return {
        "period_count": int(len(trend_df)),
        "first_period": first_row["period"],
        "last_period": last_row["period"],
        "energy_change_percent": round(float(energy_change), 3) if energy_change is not None else None,
        "emissions_change_percent": round(float(emissions_change), 3) if emissions_change is not None else None,
        "energy_trend_label": _trend_label(energy_change),
        "emissions_trend_label": _trend_label(emissions_change),
    }

def _iqr_bounds(series: pd.Series) -> tuple[float | None, float | None]:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if len(clean) < 4:
        return None, None

    q1 = clean.quantile(0.25)
    q3 = clean.quantile(0.75)
    iqr = q3 - q1

    if iqr == 0:
        return None, None

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return float(lower), float(upper)

def build_anomaly_analysis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_anomalies": 0,
            "anomalous_records": [],
            "risky_facilities": [],
        }

    working = df.copy()
    working["period"] = working["date"].dt.strftime("%Y-%m")

    energy_lower, energy_upper = _iqr_bounds(working["energy_mwh"])
    emissions_lower, emissions_upper = _iqr_bounds(working["direct_emissions_tons"])

    anomaly_records = []

    for _, row in working.iterrows():
        reasons = []

        energy_value = row.get("energy_mwh")
        emissions_value = row.get("direct_emissions_tons")

        if energy_upper is not None and pd.notna(energy_value):
            if float(energy_value) > energy_upper or float(energy_value) < energy_lower:
                reasons.append("enerji anomalisi")

        if emissions_upper is not None and pd.notna(emissions_value):
            if float(emissions_value) > emissions_upper or float(emissions_value) < emissions_lower:
                reasons.append("emisyon anomalisi")

        if reasons:
            anomaly_records.append(
                {
                    "facility_name": row.get("facility_name"),
                    "state_or_region": row.get("state_or_region"),
                    "period": row.get("period"),
                    "energy_mwh": round(float(energy_value), 3) if pd.notna(energy_value) else None,
                    "direct_emissions_tons": round(float(emissions_value), 3) if pd.notna(emissions_value) else None,
                    "reasons": reasons,
                }
            )

    risky_facilities = []
    if anomaly_records:
        anomaly_df = pd.DataFrame(anomaly_records)
        grouped = (
            anomaly_df.groupby(["facility_name", "state_or_region"], as_index=False)
            .size()
            .rename(columns={"size": "anomaly_count"})
            .sort_values("anomaly_count", ascending=False)
        )

        risky_facilities = [
            {
                "facility_name": row["facility_name"],
                "state_or_region": row["state_or_region"],
                "anomaly_count": int(row["anomaly_count"]),
            }
            for _, row in grouped.iterrows()
        ]

    return {
        "total_anomalies": len(anomaly_records),
        "anomalous_records": anomaly_records[:20],
        "risky_facilities": risky_facilities[:10],
    }
