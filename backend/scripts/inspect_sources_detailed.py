from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"

def print_title(title: str):
    print("\n" + "=" * 110)
    print(title)
    print("=" * 110)

def inspect_csv_encodings(path: Path):
    print_title(f"CSV Encoding Test -> {path.name}")

    encodings = ["utf-8", "utf-8-sig", "utf-16", "latin1", "cp1252"]
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, nrows=5)
            print(f"\n[OK] encoding = {enc}")
            print("Kolonlar:")
            for col in df.columns:
                print(f" - {col}")
            print("\nİlk 5 satır:")
            print(df.head().to_string(index=False))
            return enc
        except Exception as e:
            print(f"[FAIL] encoding = {enc} -> {e}")

    return None

def inspect_excel_sheets(path: Path):
    print_title(f"Excel Sheet Inspection -> {path.name}")

    try:
        xls = pd.ExcelFile(path)
        print("Sheet'ler:")
        for sheet in xls.sheet_names:
            print(f" - {sheet}")

        for sheet in xls.sheet_names[:5]:
            print("\n" + "-" * 100)
            print(f"Sheet preview: {sheet}")
            try:
                df = pd.read_excel(path, sheet_name=sheet, nrows=8, header=None)
                print(df.to_string(index=False, header=False))
            except Exception as e:
                print(f"Sheet okunamadı: {e}")

    except Exception as e:
        print(f"Excel inceleme hatası: {e}")

def main():
    industrial = RAW_DIR / "industrial_comb_energy_2014.csv"
    ghgrp = RAW_DIR / "ghgrp_data_2023.xlsx"
    egrid = REF_DIR / "egrid2023.xlsx"
    factors = REF_DIR / "epa_ghg_emission_factors_hub_2025.xlsx"

    if industrial.exists():
        inspect_csv_encodings(industrial)
    else:
        print(f"Industrial dosyası bulunamadı: {industrial}")

    if ghgrp.exists():
        inspect_excel_sheets(ghgrp)
    else:
        print(f"GHGRP dosyası bulunamadı: {ghgrp}")

    if egrid.exists():
        inspect_excel_sheets(egrid)
    else:
        print(f"eGRID dosyası bulunamadı: {egrid}")

    if factors.exists():
        inspect_excel_sheets(factors)
    else:
        print(f"Emission factors dosyası bulunamadı: {factors}")

if __name__ == "__main__":
    main()
