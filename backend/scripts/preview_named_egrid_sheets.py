from pathlib import Path
import pandas as pd

path = Path(r".\data\reference\egrid2023.xlsx")
xls = pd.ExcelFile(path)

targets = [
    "PLNT23",
    "GEN23",
    "UNT23",
    "BA23",
    "SRL23",
    "SRCO2RTA23",
    "ST23",
    "US23",
]

for sheet in targets:
    if sheet in xls.sheet_names:
        print("\n" + "=" * 120)
        print(f"SHEET: {sheet}")
        print("=" * 120)
        try:
            df = pd.read_excel(path, sheet_name=sheet, header=None, nrows=12)
            print(df.to_string(index=False, header=False))
        except Exception as e:
            print("HATA:", e)
