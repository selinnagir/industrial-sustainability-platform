from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.egrid_mapper import read_egrid_state_factors

df = read_egrid_state_factors()

print("Shape:", df.shape)
print("\nColumns:")
for c in df.columns:
    print(" -", c)

print("\nHead:")
print(df.head(10).to_string(index=False))
