from pathlib import Path
import json
import pandas as pd
from fastapi import APIRouter, UploadFile, File

from app.services.file_parsers import parse_tabular_upload, dataframe_preview
from app.services.validation_service import suggest_column_mapping, validate_dataset
from app.services.document_service import preview_pdf_upload

router = APIRouter(prefix="/upload", tags=["upload"])

BASE_DIR = Path(__file__).resolve().parents[3]
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

    for col in ["company_name", "facility_name", "state_or_region", "fuel_type"]:
        out[col] = out[col].astype(str).str.strip()
        out.loc[out[col].isin(["None", "nan", "NaN"]), col] = None

    out["state_or_region"] = out["state_or_region"].astype(str).str.upper().str.strip()
    out.loc[out["state_or_region"].isin(["NONE", "NAN"]), "state_or_region"] = None

    for col in ["energy_mwh", "electricity_mwh", "direct_emissions_tons", "water_use", "waste_tons", "production_amount"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out["date"] = pd.to_datetime(out["date"], errors="coerce")

    out = out.dropna(how="all")
    out = out.dropna(subset=["facility_name", "date"], how="any")
    out = out.drop_duplicates().reset_index(drop=True)

    return out

@router.post("/data-preview")
async def upload_data_preview(file: UploadFile = File(...)):
    df, detected_type = await parse_tabular_upload(file)
    columns = [str(c) for c in df.columns.tolist()]
    mapping = suggest_column_mapping(columns)
    validation = validate_dataset(df, mapping)

    return {
        "filename": file.filename,
        "file_type": detected_type,
        "rows": int(len(df)),
        "columns": columns,
        "preview": dataframe_preview(df),
        "suggested_mapping": mapping,
        "validation": validation,
    }

@router.post("/data-ingest")
async def upload_data_ingest(file: UploadFile = File(...)):
    df, detected_type = await parse_tabular_upload(file)
    columns = [str(c) for c in df.columns.tolist()]
    mapping = suggest_column_mapping(columns)
    validation = validate_dataset(df, mapping)

    if not validation["is_valid"]:
        return {
            "saved": False,
            "message": "Veri seti validation aşamasını geçemedi.",
            "validation": validation,
        }

    normalized_df = normalize_uploaded_dataset(df, mapping, detected_type)
    normalized_df.to_csv(LATEST_DATASET_PATH, index=False)

    metadata = {
        "filename": file.filename,
        "file_type": detected_type,
        "rows": int(len(normalized_df)),
        "columns": normalized_df.columns.tolist(),
        "mapping": mapping,
    }

    with open(LATEST_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2, default=str)

    return {
        "saved": True,
        "message": "Şirket verisi başarıyla kaydedildi.",
        "rows": int(len(normalized_df)),
        "columns": normalized_df.columns.tolist(),
        "saved_path": str(LATEST_DATASET_PATH),
    }

@router.post("/document-preview")
async def upload_document_preview(file: UploadFile = File(...)):
    return await preview_pdf_upload(file)
