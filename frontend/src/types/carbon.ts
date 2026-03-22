export type CarbonSummary = {
  total_direct_emissions_co2e_tons: number
  total_facilities: number
  total_states: number
  avg_facility_direct_emissions_tons: number
}

export type CarbonTopFacility = {
  facility_name: string
  state_or_region: string
  sector: string
  reported_emissions_co2e: number
}

export type CarbonStateBreakdown = {
  state_abbr: string
  reported_emissions_co2e: number
  egrid_co2e_ton_per_mwh: number | null
}

export type CarbonFilters = {
  states: string[]
  sectors: string[]
}

export type CarbonDashboardResponse = {
  summary: CarbonSummary
  top_facilities: CarbonTopFacility[]
  state_breakdown: CarbonStateBreakdown[]
  filters: CarbonFilters
  methodology: {
    direct_emissions_source: string
    state_factor_source: string
    note: string
  }
}
