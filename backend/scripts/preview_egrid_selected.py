from pathlib import Path
import pandas as pd

path = Path(r".\data\reference\egrid2023.xlsx")
xls = pd.ExcelFile(path)

print("SHEET LIST:")
for s in xls.sheet_names:
    print(" -", s)

print("\n" + "="*100)
targets = xls.sheet_names

for sheet in targets:
    print("\n" + "="*120)
    print(f"SHEET: {sheet}")
    print("="*120)
    try:
        df = pd.read_excel(path, sheet_name=sheet, header=None, nrows=8)
        print(df.to_string(index=False, header=False))
    except Exception as e:
        print("HATA:", e)
