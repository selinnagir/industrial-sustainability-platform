import { useEffect, useMemo, useState } from "react"
import { Building2, Factory, Globe2, Gauge } from "lucide-react"
import {
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts"
import { api } from "../services/api"
import type { EnergyDashboardResponse } from "../types/energy"

export default function DashboardPage() {
  const [data, setData] = useState<EnergyDashboardResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedFacility, setSelectedFacility] = useState("All")
  const [selectedSector, setSelectedSector] = useState("All")
  const [selectedState, setSelectedState] = useState("All")

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true)
      try {
        const params: Record<string, string> = {}

        if (selectedFacility !== "All") params.facility = selectedFacility
        if (selectedSector !== "All") params.sector = selectedSector
        if (selectedState !== "All") params.state = selectedState

        const response = await api.get<EnergyDashboardResponse>("/analytics/energy", {
          params,
        })

        setData(response.data)
      } catch (error) {
        console.error("Dashboard verisi alınamadı:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboard()
  }, [selectedFacility, selectedSector, selectedState])

  const summaryCards = useMemo(() => {
    if (!data) return []

    return [
      {
        title: "Toplam Enerji",
        value: `${data.summary.total_energy_gwh.toLocaleString()} GWh`,
        detail: "Filtrelenmiş toplam enerji",
        icon: Gauge,
      },
      {
        title: "Toplam Tesis",
        value: `${data.summary.total_facilities}`,
        detail: "Seçilen filtredeki tesis sayısı",
        icon: Building2,
      },
      {
        title: "Toplam Eyalet",
        value: `${data.summary.total_states}`,
        detail: "Verideki eyalet/bölge sayısı",
        icon: Globe2,
      },
      {
        title: "Ortalama Tesis Enerjisi",
        value: `${data.summary.avg_facility_energy_gwh.toLocaleString()} GWh`,
        detail: "Tesis başına ortalama enerji",
        icon: Factory,
      },
    ]
  }, [data])

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">
            Dashboard
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Endüstriyel enerji kullanımını gerçek veriyle izle
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Bu sürüm, gerçek industrial dataset üzerinden enerji özeti, sektör kırılımı
            ve en yüksek enerji kullanan tesisleri gösterir.
          </p>
        </div>
      </section>

      <section className="grid gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-3">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Tesis</label>
          <select
            value={selectedFacility}
            onChange={(e) => setSelectedFacility(e.target.value)}
            className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none"
          >
            <option value="All">All</option>
            {data?.filters.facilities.map((facility) => (
              <option key={facility} value={facility}>
                {facility}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Sektör</label>
          <select
            value={selectedSector}
            onChange={(e) => setSelectedSector(e.target.value)}
            className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none"
          >
            <option value="All">All</option>
            {data?.filters.sectors.map((sector) => (
              <option key={sector} value={sector}>
                {sector}
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
            {data?.filters.states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {loading
          ? [1, 2, 3, 4].map((item) => (
              <div
                key={item}
                className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm"
              >
                <div className="h-24 animate-pulse rounded-2xl bg-slate-100" />
              </div>
            ))
          : summaryCards.map((item) => {
              const Icon = item.icon
              return (
                <div
                  key={item.title}
                  className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-500">{item.title}</p>
                      <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
                        {item.value}
                      </p>
                    </div>
                    <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
                      <Icon size={20} />
                    </div>
                  </div>
                  <p className="mt-4 text-sm leading-6 text-slate-600">{item.detail}</p>
                </div>
              )
            })}
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-slate-900">Sektör Bazlı Enerji Kırılımı</p>
              <p className="mt-1 text-sm text-slate-500">
                En yüksek enerji kullanan sektörler
              </p>
            </div>
          </div>

          <div className="mt-6 h-[340px]">
            {loading ? (
              <div className="h-full animate-pulse rounded-2xl bg-slate-100" />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data?.sector_breakdown ?? []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="sector" hide />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="energy_gwh" fill="#0F766E" radius={[10, 10, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">En Yüksek Enerji Kullanan Tesisler</p>

          <div className="mt-5 space-y-3">
            {loading ? (
              [1, 2, 3, 4, 5].map((item) => (
                <div key={item} className="h-16 animate-pulse rounded-2xl bg-slate-100" />
              ))
            ) : (
              data?.top_facilities.slice(0, 5).map((facility) => (
                <div
                  key={`${facility.facility_name}-${facility.state_or_region}`}
                  className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3"
                >
                  <p className="text-sm font-semibold text-slate-900">
                    {facility.facility_name}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    {facility.state_or_region} • {facility.energy_gwh.toLocaleString()} GWh
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </section>
    </div>
  )
}
