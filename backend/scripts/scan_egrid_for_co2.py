from pathlib import Path
import pandas as pd

path = Path(r".\data\reference\egrid2023.xlsx")
xls = pd.ExcelFile(path)

keywords = ["co2", "emission rate", "output emission", "subregion", "state abbreviation", "pstatabb", "subrgn"]

for sheet in xls.sheet_names:
    try:
        df = pd.read_excel(path, sheet_name=sheet, header=None, nrows=25)
        text = " | ".join(df.astype(str).fillna("").stack().tolist()).lower()
        matched = [k for k in keywords if k in text]
        if matched:
            print("\n" + "=" * 120)
            print(f"SHEET: {sheet}")
            print("MATCH:", ", ".join(matched))
            print(df.head(10).to_string(index=False, header=False))
    except Exception as e:
        print(f"{sheet} -> HATA: {e}")
