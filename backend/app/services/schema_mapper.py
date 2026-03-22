import pandas as pd

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(col).strip() for col in out.columns]
    return out

def map_ghgrp_to_common_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)

    column_map = {
        "Facility Name": "facility_name",
        "City": "city",
        "State": "state_or_region",
        "Primary NAICS Code": "primary_naics_code",
        "Industry Type (sectors)": "sector",
        "Total reported direct emissions": "reported_emissions_co2e",
    }

    available = {k: v for k, v in column_map.items() if k in df.columns}
    mapped = df[list(available.keys())].rename(columns=available).copy()

    mapped["source_dataset"] = "ghgrp_2023"
    mapped["year"] = 2023

    return mapped

def clean_gwp_factors(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]

    keep_cols = [c for c in out.columns if c in ["Gas", "100-Year GWP"]]
    out = out[keep_cols].copy()

    out = out.dropna(how="all")
    out["Gas"] = out["Gas"].astype(str).str.strip()
    out["100-Year GWP"] = pd.to_numeric(out["100-Year GWP"], errors="coerce")
    out = out.dropna(subset=["Gas", "100-Year GWP"])

    return out
