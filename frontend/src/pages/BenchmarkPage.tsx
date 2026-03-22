import { useEffect, useState } from "react"
import { BarChart3, Scale, Globe2, Building2 } from "lucide-react"
import { api } from "../services/api"

type FiltersResponse = {
  dashboard_context: {
    filters: {
      facilities: string[]
      states: string[]
    }
  }
}

type BenchmarkResponse = {
  company_context: {
    total_energy_mwh: number
    total_direct_emissions_tons: number
    carbon_intensity_ton_per_mwh: number | null
    selected_state: string | null
    sector_column_detected: string | null
  }
  state_benchmark: {
    state: string
    company_carbon_intensity_ton_per_mwh: number
    reference_carbon_intensity_ton_per_mwh: number
    gap_ton_per_mwh: number
    status: string
  } | null
  state_reference: {
    state: string
    reference_facility_count: number
    reference_avg_direct_emissions_tons: number
    reference_total_direct_emissions_tons: number
  } | null
  sector_benchmark: {
    sector: string
    reference_facility_count: number
    reference_avg_direct_emissions_tons: number
    reference_total_direct_emissions_tons: number
    company_total_direct_emissions_tons: number
  } | null
  commentary: string[]
}

export default function BenchmarkPage() {
  const [facilities, setFacilities] = useState<string[]>([])
  const [states, setStates] = useState<string[]>([])
  const [selectedFacility, setSelectedFacility] = useState("All")
  const [selectedState, setSelectedState] = useState("All")
  const [data, setData] = useState<BenchmarkResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  useEffect(() => {
    const loadFilters = async () => {
      try {
        const response = await api.get<FiltersResponse>("/company/ai-insights")
        setFacilities(response.data.dashboard_context.filters.facilities || [])
        setStates(response.data.dashboard_context.filters.states || [])
      } catch (error) {
        console.error(error)
      }
    }

    loadFilters()
  }, [])

  useEffect(() => {
    const loadBenchmark = async () => {
      setLoading(true)
      setErrorMessage(null)

      try {
        const params: Record<string, string> = {}
        if (selectedFacility !== "All") params.facility = selectedFacility
        if (selectedState !== "All") params.state = selectedState

        const response = await api.get<BenchmarkResponse>("/company/benchmark", { params })
        setData(response.data)
      } catch (error: any) {
        console.error("Benchmark verisi alınamadı:", error)
        const detail = error?.response?.data?.detail
        setErrorMessage(detail || "Benchmark verisi alınamadı.")
      } finally {
        setLoading(false)
      }
    }

    loadBenchmark()
  }, [selectedFacility, selectedState])

  if (loading) {
    return <div className="h-40 animate-pulse rounded-3xl bg-slate-100" />
  }

  if (errorMessage) {
    return (
      <div className="rounded-3xl border border-amber-200 bg-amber-50 p-6 shadow-sm">
        {errorMessage}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">
            Benchmark
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Şirket verini referans veriyle kıyasla
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            eGRID eyalet referansı ve GHGRP referanslarıyla temel kıyaslama yapılır.
          </p>
        </div>
      </section>

      <section className="grid gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Tesis</label>
          <select
            value={selectedFacility}
            onChange={(e) => setSelectedFacility(e.target.value)}
            className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none"
          >
            <option value="All">All</option>
            {facilities.map((facility) => (
              <option key={facility} value={facility}>
                {facility}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Eyalet</label>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none"
          >
            <option value="All">All</option>
            {states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Company Carbon Intensity</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
            {data?.company_context.carbon_intensity_ton_per_mwh ?? "—"}
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Selected State</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
            {data?.company_context.selected_state ?? "—"}
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">State Status</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
            {data?.state_benchmark?.status ?? "—"}
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Sector Column</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
            {data?.company_context.sector_column_detected ?? "Yok"}
          </p>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
              <Scale size={20} />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900">eGRID State Benchmark</p>
              <p className="text-sm text-slate-500">Karbon yoğunluğu kıyası</p>
            </div>
          </div>

          {data?.state_benchmark ? (
            <div className="mt-5 space-y-3 text-sm text-slate-700">
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Company: {data.state_benchmark.company_carbon_intensity_ton_per_mwh}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Reference: {data.state_benchmark.reference_carbon_intensity_ton_per_mwh}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Gap: {data.state_benchmark.gap_ton_per_mwh}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Status: {data.state_benchmark.status}
              </div>
            </div>
          ) : (
            <div className="mt-5 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
              State benchmark için tek eyalet seçmek daha anlamlı.
            </div>
          )}
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-indigo-50 p-3 text-indigo-700">
              <Globe2 size={20} />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900">GHGRP State Reference</p>
              <p className="text-sm text-slate-500">Eyalet referans emisyonları</p>
            </div>
          </div>

          {data?.state_reference ? (
            <div className="mt-5 space-y-3 text-sm text-slate-700">
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Facility count: {data.state_reference.reference_facility_count}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Avg emissions: {data.state_reference.reference_avg_direct_emissions_tons}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Total emissions: {data.state_reference.reference_total_direct_emissions_tons}
              </div>
            </div>
          ) : (
            <div className="mt-5 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
              State reference üretilemedi.
            </div>
          )}
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-amber-50 p-3 text-amber-700">
              <Building2 size={20} />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Sector Benchmark</p>
              <p className="text-sm text-slate-500">Sektör varsa aktif</p>
            </div>
          </div>

          {data?.sector_benchmark ? (
            <div className="mt-5 space-y-3 text-sm text-slate-700">
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Sector: {data.sector_benchmark.sector}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Ref facility count: {data.sector_benchmark.reference_facility_count}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Ref avg emissions: {data.sector_benchmark.reference_avg_direct_emissions_tons}
              </div>
              <div className="rounded-2xl bg-slate-50 px-4 py-3">
                Company emissions: {data.sector_benchmark.company_total_direct_emissions_tons}
              </div>
            </div>
          ) : (
            <div className="mt-5 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
              Sector benchmark için company dataset içinde sektör kolonu gerekli.
            </div>
          )}
        </div>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
            <BarChart3 size={20} />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">Benchmark Yorumu</p>
            <p className="text-sm text-slate-500">Otomatik yorumlar</p>
          </div>
        </div>

        <div className="mt-5 space-y-3">
          {data?.commentary.map((item, index) => (
            <div key={index} className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
              {item}
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
