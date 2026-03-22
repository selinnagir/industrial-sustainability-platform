import pandas as pd

def apply_filters(
    df: pd.DataFrame,
    facility: str | None = None,
    sector: str | None = None,
    state: str | None = None,
):
    out = df.copy()

    if facility and facility != "All":
        out = out[out["facility_name"] == facility]

    if sector and sector != "All":
        out = out[out["sector"] == sector]

    if state and state != "All":
        out = out[out["state_or_region"] == state]

    return out

def build_summary(df: pd.DataFrame) -> dict:
    return {
        "total_energy_gwh": round(float(df["energy_gwh"].sum()), 3),
        "total_energy_mmbtu": round(float(df["energy_mmbtu"].sum()), 3),
        "total_facilities": int(df["facility_name"].nunique()),
        "total_states": int(df["state_or_region"].nunique()),
        "avg_facility_energy_gwh": round(float(df.groupby("facility_name")["energy_gwh"].sum().mean()), 3) if not df.empty else 0.0,
    }

def build_sector_breakdown(df: pd.DataFrame) -> list[dict]:
    grouped = (
        df.groupby("sector", as_index=False)["energy_gwh"]
        .sum()
        .sort_values("energy_gwh", ascending=False)
        .head(10)
    )
    return [
        {"sector": row["sector"], "energy_gwh": round(float(row["energy_gwh"]), 3)}
        for _, row in grouped.iterrows()
    ]

def build_top_facilities(df: pd.DataFrame) -> list[dict]:
    grouped = (
        df.groupby(["facility_name", "state_or_region"], as_index=False)["energy_gwh"]
        .sum()
        .sort_values("energy_gwh", ascending=False)
        .head(10)
    )
    return [
        {
            "facility_name": row["facility_name"],
            "state_or_region": row["state_or_region"],
            "energy_gwh": round(float(row["energy_gwh"]), 3),
        }
        for _, row in grouped.iterrows()
    ]

def build_filter_options(df: pd.DataFrame) -> dict:
    return {
        "facilities": sorted(df["facility_name"].dropna().unique().tolist()),
        "sectors": sorted(df["sector"].dropna().unique().tolist()),
        "states": sorted(df["state_or_region"].dropna().unique().tolist()),
    }
