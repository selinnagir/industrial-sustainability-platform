import { useEffect, useState } from "react"
import { FlaskConical, TrendingDown, Leaf, Gauge } from "lucide-react"
import { api } from "../services/api"

type FiltersResponse = {
  dashboard_context: {
    filters: {
      facilities: string[]
      states: string[]
    }
  }
}

type ScenarioResponse = {
  used_filters: {
    facility: string | null
    state: string | null
  }
  result: {
    inputs: {
      energy_reduction_pct: number
      emissions_reduction_pct: number
    }
    baseline: {
      total_energy_mwh: number
      total_direct_emissions_tons: number
      carbon_intensity_ton_per_mwh: number | null
    }
    simulation: {
      total_energy_mwh: number
      total_direct_emissions_tons: number
      carbon_intensity_ton_per_mwh: number | null
      energy_saved_mwh: number
      emissions_saved_tons: number
    }
    forecast_effect: {
      next_period: string | null
      baseline_forecast_energy_mwh: number | null
      baseline_forecast_direct_emissions_tons: number | null
      simulated_forecast_energy_mwh: number | null
      simulated_forecast_direct_emissions_tons: number | null
    }
    commentary: string[]
    recommendations: string[]
  }
}

export default function ScenarioSimulationPage() {
  const [facilities, setFacilities] = useState<string[]>([])
  const [states, setStates] = useState<string[]>([])
  const [selectedFacility, setSelectedFacility] = useState("All")
  const [selectedState, setSelectedState] = useState("All")
  const [energyReduction, setEnergyReduction] = useState(10)
  const [emissionsReduction, setEmissionsReduction] = useState(10)
  const [loading, setLoading] = useState(true)
  const [simLoading, setSimLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [data, setData] = useState<ScenarioResponse | null>(null)

  useEffect(() => {
    const loadFilters = async () => {
      setLoading(true)
      setErrorMessage(null)

      try {
        const response = await api.get<FiltersResponse>("/company/ai-insights")
        setFacilities(response.data.dashboard_context.filters.facilities || [])
        setStates(response.data.dashboard_context.filters.states || [])
      } catch (error: any) {
        console.error("Scenario filtreleri alınamadı:", error)
        const detail = error?.response?.data?.detail
        setErrorMessage(detail || "Scenario simulation için filtre verisi alınamadı.")
      } finally {
        setLoading(false)
      }
    }

    loadFilters()
  }, [])

  const runSimulation = async () => {
    setSimLoading(true)
    setErrorMessage(null)

    try {
      const response = await api.post<ScenarioResponse>("/company/scenario-simulate", {
        facility: selectedFacility !== "All" ? selectedFacility : null,
        state: selectedState !== "All" ? selectedState : null,
        energy_reduction_pct: energyReduction,
        emissions_reduction_pct: emissionsReduction,
      })

      setData(response.data)
    } catch (error: any) {
      console.error("Scenario simulation hatası:", error)
      const detail = error?.response?.data?.detail
      setErrorMessage(detail || "Scenario simulation çalıştırılamadı.")
    } finally {
      setSimLoading(false)
    }
  }

  if (loading) {
    return <div className="h-40 animate-pulse rounded-3xl bg-slate-100" />
  }

  if (errorMessage && !data) {
    return (
      <div className="rounded-3xl border border-amber-200 bg-amber-50 p-6 shadow-sm">
        <p className="text-lg font-semibold text-amber-800">Scenario Simulation açılamadı</p>
        <p className="mt-3 text-sm text-amber-700">{errorMessage}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">
            Scenario Simulation
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Azaltım senaryolarını test et
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Enerji ve emisyon azaltım yüzdesi gir, mevcut durum ile simüle edilen sonucu karşılaştır.
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

      <section className="grid gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Enerji azaltımı (%)
          </label>
          <input
            type="range"
            min="0"
            max="50"
            value={energyReduction}
            onChange={(e) => setEnergyReduction(Number(e.target.value))}
            className="w-full"
          />
          <p className="mt-2 text-sm text-slate-600">{energyReduction}%</p>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Emisyon azaltımı (%)
          </label>
          <input
            type="range"
            min="0"
            max="50"
            value={emissionsReduction}
            onChange={(e) => setEmissionsReduction(Number(e.target.value))}
            className="w-full"
          />
          <p className="mt-2 text-sm text-slate-600">{emissionsReduction}%</p>
        </div>

        <div className="md:col-span-2">
          <button
            onClick={runSimulation}
            disabled={simLoading}
            className="rounded-2xl bg-teal-700 px-5 py-3 text-white transition hover:bg-teal-800 disabled:opacity-60"
          >
            {simLoading ? "Hesaplanıyor..." : "Senaryoyu Çalıştır"}
          </button>
        </div>
      </section>

      {errorMessage && data && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
          {errorMessage}
        </div>
      )}

      {data && (
        <>
          <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm font-medium text-slate-500">Mevcut Enerji</p>
              <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
                {data.result.baseline.total_energy_mwh} MWh
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm font-medium text-slate-500">Simüle Enerji</p>
              <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
                {data.result.simulation.total_energy_mwh} MWh
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm font-medium text-slate-500">Enerji Tasarrufu</p>
              <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
                {data.result.simulation.energy_saved_mwh} MWh
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm font-medium text-slate-500">Emisyon Tasarrufu</p>
              <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
                {data.result.simulation.emissions_saved_tons} ton
              </p>
            </div>
          </section>

          <section className="grid gap-4 md:grid-cols-3">
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-slate-100 p-3 text-slate-700">
                  <FlaskConical size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-900">Karbon Yoğunluğu</p>
                  <p className="text-sm text-slate-500">Önce / sonra</p>
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-700">
                Mevcut: {data.result.baseline.carbon_intensity_ton_per_mwh ?? "—"} ton/MWh
              </p>
              <p className="mt-2 text-sm text-slate-700">
                Simüle: {data.result.simulation.carbon_intensity_ton_per_mwh ?? "—"} ton/MWh
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-emerald-50 p-3 text-emerald-700">
                  <TrendingDown size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-900">Tahmin Etkisi</p>
                  <p className="text-sm text-slate-500">Bir sonraki dönem</p>
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-700">
                Dönem: {data.result.forecast_effect.next_period ?? "—"}
              </p>
              <p className="mt-2 text-sm text-slate-700">
                Enerji: {data.result.forecast_effect.baseline_forecast_energy_mwh ?? "—"} → {data.result.forecast_effect.simulated_forecast_energy_mwh ?? "—"}
              </p>
              <p className="mt-2 text-sm text-slate-700">
                Emisyon: {data.result.forecast_effect.baseline_forecast_direct_emissions_tons ?? "—"} → {data.result.forecast_effect.simulated_forecast_direct_emissions_tons ?? "—"}
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
                  <Gauge size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-900">Senaryo Girdileri</p>
                  <p className="text-sm text-slate-500">Uygulanan azaltımlar</p>
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-700">
                Enerji azaltımı: {data.result.inputs.energy_reduction_pct}%
              </p>
              <p className="mt-2 text-sm text-slate-700">
                Emisyon azaltımı: {data.result.inputs.emissions_reduction_pct}%
              </p>
            </div>
          </section>

          <section className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
                  <Leaf size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-900">Senaryo Yorumu</p>
                  <p className="text-sm text-slate-500">Simülasyon sonucu</p>
                </div>
              </div>

              <div className="mt-5 space-y-3">
                {data.result.commentary.map((item, index) => (
                  <div key={index} className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
                    {item}
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-emerald-50 p-3 text-emerald-700">
                  <Leaf size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-900">Önerilen Aksiyonlar</p>
                  <p className="text-sm text-slate-500">Senaryoya göre öneriler</p>
                </div>
              </div>

              <div className="mt-5 space-y-3">
                {data.result.recommendations.map((item, index) => (
                  <div key={index} className="rounded-2xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  )
}
