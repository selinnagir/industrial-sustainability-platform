from pathlib import Path
import pandas as pd

path = Path(r".\data\reference\egrid2023.xlsx")
targets = ["ST23", "SRL23", "PLNT23", "BA23", "US23"]
keywords = ["co2", "rate", "state", "subregion", "output emission", "input emission"]

for sheet in targets:
    print("\n" + "=" * 120)
    print(f"SHEET: {sheet}")
    print("=" * 120)
    try:
        df = pd.read_excel(path, sheet_name=sheet, header=None, nrows=30)
        for idx in range(len(df)):
            row_text = " | ".join(df.iloc[idx].astype(str).fillna("").tolist()).lower()
            matched = [k for k in keywords if k in row_text]
            if matched:
                print(f"Row {idx}: MATCH -> {', '.join(matched)}")
                print(df.iloc[idx].to_string())
                print("-" * 80)
    except Exception as e:
        print("HATA:", e)
