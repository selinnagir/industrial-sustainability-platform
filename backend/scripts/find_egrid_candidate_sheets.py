from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
EGRID_PATH = BASE_DIR / "data" / "reference" / "egrid2023.xlsx"

KEYWORDS = [
    "state",
    "subregion",
    "plant",
    "output emission rate",
    "co2",
    "co2 equivalent",
    "grid gross loss",
    "balancing authority",
]

def print_title(title: str):
    print("\n" + "=" * 120)
    print(title)
    print("=" * 120)

def main():
    xls = pd.ExcelFile(EGRID_PATH)

    print_title("eGRID ADAY SHEET TARAMASI")
    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(EGRID_PATH, sheet_name=sheet, header=None, nrows=40)
            text = " | ".join(df.astype(str).fillna("").stack().tolist()).lower()

            matched = [kw for kw in KEYWORDS if kw in text]
            if matched:
                print(f"\nSheet: {sheet}")
                print("Eşleşen kelimeler:", ", ".join(matched))

                preview = pd.read_excel(EGRID_PATH, sheet_name=sheet, header=None, nrows=12)
                print(preview.to_string(index=False, header=False))
        except Exception as e:
            print(f"\nSheet: {sheet} -> Hata: {e}")

if __name__ == "__main__":
    main()
