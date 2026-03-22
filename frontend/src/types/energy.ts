export type EnergySummary = {
  total_energy_gwh: number
  total_energy_mmbtu: number
  total_facilities: number
  total_states: number
  avg_facility_energy_gwh: number
}

export type SectorBreakdownItem = {
  sector: string
  energy_gwh: number
}

export type TopFacilityItem = {
  facility_name: string
  state_or_region: string
  energy_gwh: number
}

export type EnergyFilters = {
  facilities: string[]
  sectors: string[]
  states: string[]
}

export type EnergyDashboardResponse = {
  summary: EnergySummary
  sector_breakdown: SectorBreakdownItem[]
  top_facilities: TopFacilityItem[]
  filters: EnergyFilters
}
