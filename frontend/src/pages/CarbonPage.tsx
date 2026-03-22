import { useEffect, useMemo, useState } from "react"
import { Factory, Globe2, Leaf, Scale } from "lucide-react"
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
import type { CarbonDashboardResponse } from "../types/carbon"

export default function CarbonPage() {
  const [data, setData] = useState<CarbonDashboardResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedState, setSelectedState] = useState("All")
  const [selectedSector, setSelectedSector] = useState("All")

  useEffect(() => {
    const fetchCarbon = async () => {
      setLoading(true)
      try {
        const params: Record<string, string> = {}

        if (selectedState !== "All") params.state = selectedState
        if (selectedSector !== "All") params.sector = selectedSector

        const response = await api.get<CarbonDashboardResponse>("/analytics/carbon", {
          params,
        })

        setData(response.data)
      } catch (error) {
        console.error("Karbon verisi alınamadı:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchCarbon()
  }, [selectedState, selectedSector])

  const summaryCards = useMemo(() => {
    if (!data) return []

    return [
      {
        title: "Toplam Direct Emisyon",
        value: `${data.summary.total_direct_emissions_co2e_tons.toLocaleString()} ton CO2e`,
        detail: "GHGRP 2023 toplamı",
        icon: Leaf,
      },
      {
        title: "Toplam Tesis",
        value: `${data.summary.total_facilities}`,
        detail: "Filtrelenmiş tesis sayısı",
        icon: Factory,
      },
      {
        title: "Toplam Eyalet",
        value: `${data.summary.total_states}`,
        detail: "Filtrelenmiş eyalet sayısı",
        icon: Globe2,
      },
      {
        title: "Tesis Başına Ortalama",
        value: `${data.summary.avg_facility_direct_emissions_tons.toLocaleString()} ton`,
        detail: "Ortalama direct emisyon",
        icon: Scale,
      },
    ]
  }, [data])

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">
            Carbon
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Direct emisyonları ve eyalet bazlı karbon bağlamını izle
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Bu ekran GHGRP direct emissions verisini gösterir. eGRID state faktörleri ise
            bağlamsal karbon referansı olarak sunulur.
          </p>
        </div>
      </section>

      <section className="grid gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-2">
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
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {loading
          ? [1, 2, 3, 4].map((item) => (
              <div key={item} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
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
              <p className="text-sm font-semibold text-slate-900">Eyalet Bazlı Emisyon Kırılımı</p>
              <p className="mt-1 text-sm text-slate-500">
                GHGRP direct emissions + eGRID state context
              </p>
            </div>
          </div>

          <div className="mt-6 h-[340px]">
            {loading ? (
              <div className="h-full animate-pulse rounded-2xl bg-slate-100" />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data?.state_breakdown ?? []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="state_abbr" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="reported_emissions_co2e" fill="#0F766E" radius={[10, 10, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">En Yüksek Emisyonlu Tesisler</p>

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
                    {facility.state_or_region} • {facility.reported_emissions_co2e.toLocaleString()} ton CO2e
                  </p>
                </div>
              ))
            )}
          </div>

          <div className="mt-6 rounded-3xl border border-emerald-100 bg-emerald-50 p-4">
            <p className="text-sm font-semibold text-emerald-800">Metodoloji</p>
            <p className="mt-2 text-sm leading-6 text-emerald-700">
              {data?.methodology.note}
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}
