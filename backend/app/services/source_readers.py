from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"

def _find_header_row_excel(path: Path, sheet_name: str, expected_text: str, scan_rows: int = 50) -> int:
    preview = pd.read_excel(path, sheet_name=sheet_name, header=None, nrows=scan_rows)
    for i in range(len(preview)):
        row_values = preview.iloc[i].astype(str).str.strip().tolist()
        if any(expected_text.lower() == str(v).strip().lower() for v in row_values):
            return i
    raise ValueError(f"'{expected_text}' başlığı bulunamadı -> {path.name} / {sheet_name}")

def read_industrial_energy() -> pd.DataFrame:
    path = RAW_DIR / "industrial_comb_energy_2014.csv"
    encodings = ["utf-16", "utf-8", "utf-8-sig", "cp1252", "latin1"]

    last_error = None
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            return df
        except Exception as e:
            last_error = e

    raise ValueError(f"Industrial enerji dosyası okunamadı: {last_error}")

def read_ghgrp() -> pd.DataFrame:
    path = RAW_DIR / "ghgrp_data_2023.xlsx"
    xls = pd.ExcelFile(path)
    sheet = xls.sheet_names[0]

    header_row = _find_header_row_excel(path, sheet, "Facility Id", scan_rows=20)
    df = pd.read_excel(path, sheet_name=sheet, header=header_row)
    return df

def read_egrid_preview() -> pd.DataFrame:
    path = REF_DIR / "egrid2023.xlsx"
    xls = pd.ExcelFile(path)

    best_sheet = None
    for sheet in xls.sheet_names:
        try:
            preview = pd.read_excel(path, sheet_name=sheet, header=None, nrows=20)
            flat = " | ".join(preview.astype(str).fillna("").stack().tolist()).lower()
            if "subregion" in flat or "state" in flat or "plant" in flat:
                best_sheet = sheet
                break
        except Exception:
            continue

    if best_sheet is None:
        best_sheet = xls.sheet_names[0]

    df = pd.read_excel(path, sheet_name=best_sheet, nrows=50)
    return df

def read_emission_factors_gwp() -> pd.DataFrame:
    path = REF_DIR / "epa_ghg_emission_factors_hub_2025.xlsx"
    xls = pd.ExcelFile(path)
    sheet = xls.sheet_names[0]

    header_row = _find_header_row_excel(path, sheet, "Gas", scan_rows=40)
    df = pd.read_excel(path, sheet_name=sheet, header=header_row)

    df.columns = [str(c).strip() for c in df.columns]
    return df
