import pandas as pd

def preprocess_industrial_energy(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]

    text_cols = [
        "FACILITY_NAME",
        "FUEL_TYPE",
        "STATE",
        "PRIMARY_NAICS_TITLE",
        "GROUPING",
        "CENSUS_PLACE_NAME",
        "MECS_Region",
    ]
    for col in text_cols:
        if col in out.columns:
            out[col] = out[col].astype(str).str.strip()

    numeric_cols = ["REPORTING_YEAR", "MMBtu_TOTAL", "GWht_TOTAL", "LATITUDE", "LONGITUDE"]
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out.dropna(subset=["FACILITY_NAME"])
    out = out.drop_duplicates()

    if "GROUPING" in out.columns:
        out["sector"] = out["GROUPING"].fillna(out.get("PRIMARY_NAICS_TITLE"))
    else:
        out["sector"] = out.get("PRIMARY_NAICS_TITLE")

    out["facility_name"] = out["FACILITY_NAME"]
    out["state_or_region"] = out.get("STATE")
    out["energy_gwh"] = pd.to_numeric(out.get("GWht_TOTAL"), errors="coerce")
    out["energy_mmbtu"] = pd.to_numeric(out.get("MMBtu_TOTAL"), errors="coerce")
    out["reporting_year"] = pd.to_numeric(out.get("REPORTING_YEAR"), errors="coerce")

    out["energy_gwh"] = out["energy_gwh"].fillna(0)
    out["energy_mmbtu"] = out["energy_mmbtu"].fillna(0)

    keep_cols = [
        "facility_name",
        "state_or_region",
        "sector",
        "FUEL_TYPE",
        "PRIMARY_NAICS_TITLE",
        "reporting_year",
        "energy_gwh",
        "energy_mmbtu",
    ]

    keep_cols = [c for c in keep_cols if c in out.columns]
    return out[keep_cols].copy()
