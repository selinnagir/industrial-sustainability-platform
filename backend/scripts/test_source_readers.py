from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.source_readers import (
    read_industrial_energy,
    read_ghgrp,
    read_egrid_preview,
    read_emission_factors_gwp,
)
from app.services.schema_mapper import map_ghgrp_to_common_schema, clean_gwp_factors

def show_df(title, df, rows=5):
    print("\n" + "=" * 110)
    print(title)
    print("=" * 110)
    print("Shape:", df.shape)
    print("Columns:")
    for c in df.columns[:20]:
        print(" -", c)
    print("\nHead:")
    print(df.head(rows).to_string(index=False))

def main():
    industrial = read_industrial_energy()
    show_df("Industrial Energy Raw", industrial)

    ghgrp = read_ghgrp()
    show_df("GHGRP Raw", ghgrp)

    ghgrp_mapped = map_ghgrp_to_common_schema(ghgrp)
    show_df("GHGRP Common Schema", ghgrp_mapped)

    egrid = read_egrid_preview()
    show_df("eGRID Preview", egrid)

    gwp = read_emission_factors_gwp()
    show_df("Emission Factors Raw", gwp)

    gwp_clean = clean_gwp_factors(gwp)
    show_df("Emission Factors Cleaned", gwp_clean)

if __name__ == "__main__":
    main()
