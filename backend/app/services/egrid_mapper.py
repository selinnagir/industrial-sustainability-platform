import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
EGRID_PATH = BASE_DIR / "data" / "reference" / "egrid2023.xlsx"

def read_egrid_state_factors() -> pd.DataFrame:
    df = pd.read_excel(EGRID_PATH, sheet_name="ST23", header=0)

    keep_cols = [
        "Data Year",
        "State abbreviation",
        "State annual net generation (MWh)",
        "State annual CO2 emissions (tons)",
        "State annual CO2 equivalent emissions (tons)",
        "State annual CO2 total output emission rate (lb/MWh)",
        "State annual CO2 equivalent total output emission rate (lb/MWh)",
        "State annual CO2 input emission rate (lb/MMBtu)",
        "State annual CO2 equivalent input emission rate (lb/MMBtu)",
    ]

    df = df[keep_cols].copy()

    df = df.rename(columns={
        "Data Year": "data_year",
        "State abbreviation": "state_abbr",
        "State annual net generation (MWh)": "annual_net_generation_mwh",
        "State annual CO2 emissions (tons)": "annual_co2_tons",
        "State annual CO2 equivalent emissions (tons)": "annual_co2e_tons",
        "State annual CO2 total output emission rate (lb/MWh)": "co2_lb_per_mwh",
        "State annual CO2 equivalent total output emission rate (lb/MWh)": "co2e_lb_per_mwh",
        "State annual CO2 input emission rate (lb/MMBtu)": "co2_lb_per_mmbtu",
        "State annual CO2 equivalent input emission rate (lb/MMBtu)": "co2e_lb_per_mmbtu",
    })

    df["state_abbr"] = df["state_abbr"].astype(str).str.strip().str.upper()

    numeric_cols = [
        "annual_net_generation_mwh",
        "annual_co2_tons",
        "annual_co2e_tons",
        "co2_lb_per_mwh",
        "co2e_lb_per_mwh",
        "co2_lb_per_mmbtu",
        "co2e_lb_per_mmbtu",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["state_abbr"])
    df = df.drop_duplicates(subset=["state_abbr"])

    df["co2_kg_per_mwh"] = df["co2_lb_per_mwh"] * 0.45359237
    df["co2e_kg_per_mwh"] = df["co2e_lb_per_mwh"] * 0.45359237

    df["co2_ton_per_mwh"] = df["co2_kg_per_mwh"] / 1000
    df["co2e_ton_per_mwh"] = df["co2e_kg_per_mwh"] / 1000

    return df.sort_values("state_abbr").reset_index(drop=True)
