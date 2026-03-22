from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"

def find_first(directory: Path, patterns: list[str]):
    if not directory.exists():
        return None
    for pattern in patterns:
        matches = sorted(directory.glob(pattern))
        if matches:
            return matches[0]
    return None

def read_file(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, nrows=5)
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path, nrows=5)
    raise ValueError(f"Desteklenmeyen uzantı: {suffix}")

def inspect_file(label: str, path: Path | None):
    print("\n" + "=" * 100)
    print(f"[{label}]")

    if path is None:
        print("Dosya bulunamadı.")
        return

    print(f"Dosya adı: {path.name}")
    print(f"Tam yol  : {path}")

    try:
        df = read_file(path)
        print(f"Önizleme boyutu: {df.shape}")
        print("\nKolonlar:")
        for col in df.columns:
            print(f" - {col}")

        print("\nVeri tipleri:")
        print(df.dtypes.to_string())

        print("\nİlk 5 satır:")
        print(df.head().to_string(index=False))
    except Exception as e:
        print(f"Okuma hatası: {e}")

def main():
    industrial = find_first(RAW_DIR, ["industrial_comb_energy*.csv", "*IndustrialCombEnergy*.csv", "*.csv"])
    ghgrp = find_first(RAW_DIR, ["ghgrp*.xlsx", "*ghgp*.xlsx", "*ghgrp*.xls", "*ghgp*.xls"])
    egrid = find_first(REF_DIR, ["egrid*.xlsx", "*egrid*.xlsx", "*egrid*.xls"])
    factors = find_first(REF_DIR, ["*emission*factors*.xlsx", "*ghg*hub*.xlsx", "*factors*.xlsx"])

    inspect_file("Industrial energy dataset", industrial)
    inspect_file("GHGRP dataset", ghgrp)
    inspect_file("eGRID reference", egrid)
    inspect_file("Emission factors reference", factors)

if __name__ == "__main__":
    main()
