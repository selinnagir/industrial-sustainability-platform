import pandas as pd

def preprocess_ghgrp_common(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["facility_name"] = out["facility_name"].astype(str).str.strip()
    out["city"] = out["city"].astype(str).str.strip()
    out["state_or_region"] = out["state_or_region"].astype(str).str.strip().str.upper()
    out["sector"] = out["sector"].astype(str).str.strip()

    out["reported_emissions_co2e"] = pd.to_numeric(out["reported_emissions_co2e"], errors="coerce")
    out["primary_naics_code"] = pd.to_numeric(out["primary_naics_code"], errors="coerce")

    out = out.dropna(subset=["facility_name", "state_or_region", "reported_emissions_co2e"])
    out = out.drop_duplicates()

    return out

def apply_carbon_filters(
    df: pd.DataFrame,
    state: str | None = None,
    sector: str | None = None,
) -> pd.DataFrame:
    out = df.copy()

    if state and state != "All":
        out = out[out["state_or_region"] == state]

    if sector and sector != "All":
        out = out[out["sector"] == sector]

    return out

def build_carbon_summary(df: pd.DataFrame) -> dict:
    total_direct = float(df["reported_emissions_co2e"].sum()) if not df.empty else 0.0
    total_facilities = int(df["facility_name"].nunique()) if not df.empty else 0
    total_states = int(df["state_or_region"].nunique()) if not df.empty else 0

    avg_facility = (
        float(df.groupby("facility_name")["reported_emissions_co2e"].sum().mean())
        if not df.empty else 0.0
    )

    return {
        "total_direct_emissions_co2e_tons": round(total_direct, 3),
        "total_facilities": total_facilities,
        "total_states": total_states,
        "avg_facility_direct_emissions_tons": round(avg_facility, 3),
    }

def build_top_carbon_facilities(df: pd.DataFrame) -> list[dict]:
    grouped = (
        df.groupby(["facility_name", "state_or_region", "sector"], as_index=False)["reported_emissions_co2e"]
        .sum()
        .sort_values("reported_emissions_co2e", ascending=False)
        .head(10)
    )

    return [
        {
            "facility_name": row["facility_name"],
            "state_or_region": row["state_or_region"],
            "sector": row["sector"],
            "reported_emissions_co2e": round(float(row["reported_emissions_co2e"]), 3),
        }
        for _, row in grouped.iterrows()
    ]

def build_state_carbon_breakdown(df: pd.DataFrame, egrid_df: pd.DataFrame) -> list[dict]:
    grouped = (
        df.groupby("state_or_region", as_index=False)["reported_emissions_co2e"]
        .sum()
        .rename(columns={"state_or_region": "state_abbr"})
        .sort_values("reported_emissions_co2e", ascending=False)
    )

    merged = grouped.merge(
        egrid_df[["state_abbr", "co2e_ton_per_mwh"]],
        on="state_abbr",
        how="left",
    )

    return [
        {
            "state_abbr": row["state_abbr"],
            "reported_emissions_co2e": round(float(row["reported_emissions_co2e"]), 3),
            "egrid_co2e_ton_per_mwh": round(float(row["co2e_ton_per_mwh"]), 6) if pd.notna(row["co2e_ton_per_mwh"]) else None,
        }
        for _, row in merged.head(15).iterrows()
    ]

def build_carbon_filter_options(df: pd.DataFrame) -> dict:
    return {
        "states": sorted(df["state_or_region"].dropna().unique().tolist()),
        "sectors": sorted(df["sector"].dropna().unique().tolist()),
    }
