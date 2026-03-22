from pathlib import Path
import pandas as pd

path = Path(r".\data\reference\egrid2023.xlsx")
targets = ["ST23", "SRL23", "PLNT23", "BA23", "US23"]

for sheet in targets:
    print("\n" + "=" * 120)
    print(f"SHEET: {sheet}")
    print("=" * 120)
    try:
        df = pd.read_excel(path, sheet_name=sheet, header=None, nrows=15)
        print(df.to_string(index=False, header=False))
    except Exception as e:
        print("HATA:", e)
