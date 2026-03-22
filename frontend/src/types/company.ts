export type CompanySummary = {
  total_energy_mwh: number
  total_electricity_mwh: number
  total_direct_emissions_tons: number
  total_facilities: number
  date_range_start: string | null
  date_range_end: string | null
}

export type CompanyTrendItem = {
  period: string
  energy_mwh: number
  direct_emissions_tons: number
}

export type CompanyTopFacility = {
  facility_name: string
  state_or_region: string
  energy_mwh: number
  direct_emissions_tons: number
}

export type CompanyFilters = {
  facilities: string[]
  states: string[]
}

export type CompanySustainabilityMetrics = {
  carbon_intensity_ton_per_mwh: number | null
  water_intensity_per_mwh: number | null
  waste_intensity_per_mwh: number | null
  energy_per_production_unit: number | null
}

export type CompanyHistoricalAnalysis = {
  period_count: number
  first_period: string | null
  last_period: string | null
  energy_change_percent: number | null
  emissions_change_percent: number | null
  energy_trend_label: string
  emissions_trend_label: string
}

export type CompanyAnomalousRecord = {
  facility_name: string
  state_or_region: string
  period: string
  energy_mwh: number | null
  direct_emissions_tons: number | null
  reasons: string[]
}

export type CompanyRiskyFacility = {
  facility_name: string
  state_or_region: string
  anomaly_count: number
}

export type CompanyAnomalyAnalysis = {
  total_anomalies: number
  anomalous_records: CompanyAnomalousRecord[]
  risky_facilities: CompanyRiskyFacility[]
}

export type CompanyForecastAnalysis = {
  next_period: string | null
  forecast_energy_mwh: number | null
  forecast_direct_emissions_tons: number | null
  energy_forecast_comment: string
  emissions_forecast_comment: string
  confidence: string
}

export type CompanySustainabilityScore = {
  score: number
  grade: string
  label: string
  strengths: string[]
  weaknesses: string[]
  drivers: string[]
}

export type CompanyDashboardResponse = {
  summary: CompanySummary
  trend: CompanyTrendItem[]
  top_facilities: CompanyTopFacility[]
  filters: CompanyFilters
  sustainability_metrics: CompanySustainabilityMetrics
  historical_analysis: CompanyHistoricalAnalysis
  anomaly_analysis: CompanyAnomalyAnalysis
  forecast_analysis: CompanyForecastAnalysis
  sustainability_score: CompanySustainabilityScore
}
