from fastapi import APIRouter, Query

from app.services.source_readers import read_industrial_energy, read_ghgrp
from app.services.preprocessing import preprocess_industrial_energy
from app.services.energy_analytics import (
    apply_filters as apply_energy_filters,
    build_summary as build_energy_summary,
    build_sector_breakdown,
    build_top_facilities,
    build_filter_options as build_energy_filter_options,
)
from app.services.schema_mapper import map_ghgrp_to_common_schema
from app.services.egrid_mapper import read_egrid_state_factors
from app.services.carbon_analytics import (
    preprocess_ghgrp_common,
    apply_carbon_filters,
    build_carbon_summary,
    build_top_carbon_facilities,
    build_state_carbon_breakdown,
    build_carbon_filter_options,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/energy")
def get_energy_dashboard(
    facility: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    state: str | None = Query(default=None),
):
    df = read_industrial_energy()
    df = preprocess_industrial_energy(df)
    filtered = apply_energy_filters(df, facility=facility, sector=sector, state=state)

    return {
        "summary": build_energy_summary(filtered),
        "sector_breakdown": build_sector_breakdown(filtered),
        "top_facilities": build_top_facilities(filtered),
        "filters": build_energy_filter_options(df),
    }

@router.get("/carbon")
def get_carbon_dashboard(
    state: str | None = Query(default=None),
    sector: str | None = Query(default=None),
):
    ghgrp_raw = read_ghgrp()
    ghgrp_common = map_ghgrp_to_common_schema(ghgrp_raw)
    ghgrp_clean = preprocess_ghgrp_common(ghgrp_common)

    filtered = apply_carbon_filters(ghgrp_clean, state=state, sector=sector)
    egrid_df = read_egrid_state_factors()

    return {
        "summary": build_carbon_summary(filtered),
        "top_facilities": build_top_carbon_facilities(filtered),
        "state_breakdown": build_state_carbon_breakdown(filtered, egrid_df),
        "filters": build_carbon_filter_options(ghgrp_clean),
        "methodology": {
            "direct_emissions_source": "GHGRP 2023",
            "state_factor_source": "eGRID ST23",
            "note": "Direct facility emissions come from GHGRP. State electricity carbon factors come from eGRID and are provided as contextual reference."
        },
    }
