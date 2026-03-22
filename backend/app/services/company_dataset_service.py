from pathlib import Path
import json
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
COMPANY_DIR = BASE_DIR / "data" / "company"
COMPANY_DIR.mkdir(parents=True, exist_ok=True)

LATEST_DATASET_PATH = COMPANY_DIR / "latest_company_dataset.csv"
LATEST_METADATA_PATH = COMPANY_DIR / "latest_company_metadata.json"

TARGET_COLUMNS = [
    "company_name",
    "facility_name",
    "state_or_region",
    "date",
    "energy_mwh",
    "electricity_mwh",
    "fuel_type",
    "direct_emissions_tons",
    "water_use",
    "waste_tons",
    "production_amount",
    "source_file_type",
]

def normalize_uploaded_dataset(df: pd.DataFrame, mapping: dict, source_file_type: str) -> pd.DataFrame:
    out = pd.DataFrame()

    for target in TARGET_COLUMNS:
        source_col = mapping.get(target)
        if source_col and source_col in df.columns:
            out[target] = df[source_col]
        else:
            out[target] = None

    out["source_file_type"] = source_file_type

    text_cols = ["company_name", "facility_name", "state_or_region", "fuel_type"]
    for col in text_cols:
        out[col] = out[col].astype(str).str.strip()
        out.loc[out[col].isin(["None", "nan", "NaN"]), col] = None

    out["state_or_region"] = out["state_or_region"].astype(str).str.upper().str.strip()
    out.loc[out["state_or_region"].isin(["NONE", "NAN"]), "state_or_region"] = None

    numeric_cols = [
        "energy_mwh",
        "electricity_mwh",
        "direct_emissions_tons",
        "water_use",
        "waste_tons",
        "production_amount",
    ]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out["date"] = pd.to_datetime(out["date"], errors="coerce")

    out = out.dropna(how="all")
    out = out.dropna(subset=["facility_name", "date"], how="any")
    out = out.drop_duplicates().reset_index(drop=True)

    return out

def save_company_dataset(df: pd.DataFrame, metadata: dict) -> None:
    df.to_csv(LATEST_DATASET_PATH, index=False)
    with open(LATEST_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2, default=str)

def load_company_dataset() -> pd.DataFrame:
    if not LATEST_DATASET_PATH.exists():
        raise FileNotFoundError("Yüklenmiş şirket verisi bulunamadı.")
    df = pd.read_csv(LATEST_DATASET_PATH)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

def company_dataset_exists() -> bool:
    return LATEST_DATASET_PATH.exists()

def load_company_metadata() -> dict:
    if not LATEST_METADATA_PATH.exists():
        return {}
    with open(LATEST_METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
