from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
EGRID_PATH = BASE_DIR / "data" / "reference" / "egrid2023.xlsx"

def print_title(title: str):
    print("\n" + "=" * 120)
    print(title)
    print("=" * 120)

def main():
    if not EGRID_PATH.exists():
        print(f"Dosya bulunamadı: {EGRID_PATH}")
        return

    xls = pd.ExcelFile(EGRID_PATH)
    print_title("eGRID SHEET LISTESI")
    for i, sheet in enumerate(xls.sheet_names, start=1):
        print(f"{i}. {sheet}")

    for sheet in xls.sheet_names:
        print_title(f"SHEET PREVIEW -> {sheet}")
        try:
            df = pd.read_excel(EGRID_PATH, sheet_name=sheet, header=None, nrows=15)
            print(df.to_string(index=False, header=False))
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    main()
