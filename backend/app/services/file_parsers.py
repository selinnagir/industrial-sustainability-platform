from io import BytesIO
from pathlib import Path
import json
import pandas as pd
from fastapi import HTTPException, UploadFile

SUPPORTED_DATA_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}
SUPPORTED_DOCUMENT_EXTENSIONS = {".pdf"}

def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    out = out.dropna(how="all")
    out = out.reset_index(drop=True)
    return out

async def parse_tabular_upload(file: UploadFile) -> tuple[pd.DataFrame, str]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Dosya adı bulunamadı.")

    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_DATA_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Desteklenmeyen veri dosyası: {ext}")

    content = await file.read()

    try:
        if ext == ".csv":
            last_error = None
            for encoding in ["utf-8-sig", "utf-8", "utf-16", "cp1252", "latin1"]:
                try:
                    df = pd.read_csv(BytesIO(content), encoding=encoding)
                    return _clean_dataframe(df), "csv"
                except Exception as e:
                    last_error = e
            raise HTTPException(status_code=400, detail=f"CSV okunamadı: {last_error}")

        if ext in {".xlsx", ".xls"}:
            df = pd.read_excel(BytesIO(content))
            return _clean_dataframe(df), "excel"

        if ext == ".json":
            raw = json.loads(content.decode("utf-8-sig"))

            if isinstance(raw, list):
                df = pd.DataFrame(raw)
            elif isinstance(raw, dict):
                if "data" in raw and isinstance(raw["data"], list):
                    df = pd.DataFrame(raw["data"])
                else:
                    df = pd.json_normalize(raw)
            else:
                raise HTTPException(status_code=400, detail="JSON yapısı desteklenmiyor.")

            return _clean_dataframe(df), "json"

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Dosya okunamadı: {e}")

    raise HTTPException(status_code=400, detail="Dosya tipi çözümlenemedi.")

def dataframe_preview(df: pd.DataFrame, max_rows: int = 10) -> list[dict]:
    preview_df = df.head(max_rows).copy()
    preview_df = preview_df.where(pd.notnull(preview_df), None)
    return preview_df.to_dict(orient="records")
