from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "sample_energy_data.csv"

def load_energy_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)
