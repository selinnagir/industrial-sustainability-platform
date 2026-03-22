import { useEffect, useMemo, useState } from "react"
import { Building2, Factory, Leaf, Zap, Activity, AlertTriangle, TrendingUp, Award, Download } from "lucide-react"
import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts"
import { api } from "../services/api"
import type { CompanyDashboardResponse } from "../types/company"

export default function CompanyDashboardPage() {
  const [data, setData] = useState<CompanyDashboardResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [selectedFacility, setSelectedFacility] = useState("All")
  const [selectedState, setSelectedState] = useState("All")

  const handleDownloadPdf = () => {
    const params = new URLSearchParams()
    if (selectedFacility !== "All") params.set("facility", selectedFacility)
    if (selectedState !== "All") params.set("state", selectedState)

    const query = params.toString()
    const url = `http://127.0.0.1:8000/company/report/pdf${query ? `?${query}` : ""}`
    window.open(url, "_blank")
  }

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true)
      setErrorMessage(null)

      try {
        const params: Record<string, string> = {}
        if (selectedFacility !== "All") params.facility = selectedFacility
        if (selectedState !== "All") params.state = selectedState

        const response = await api.get<CompanyDashboardResponse>("/company/dashboard", { params })
        setData(response.data)
      } catch (error: any) {
        console.error("Company dashboard verisi alınamadı:", error)
        const detail = error?.response?.data?.detail
        setErrorMessage(detail || "Company dashboard verisi alınamadı.")
      } finally {
        setLoading(false)
      }
    }

    fetchDashboard()
  }, [selectedFacility, selectedState])

  const summaryCards = useMemo(() => {
    if (!data) return []
    return [
      { title: "Toplam Enerji", value: `${data.summary.total_energy_mwh.toLocaleString()} MWh`, detail: "Yüklenen şirket verisi", icon: Zap },
      { title: "Toplam Elektrik", value: `${data.summary.total_electricity_mwh.toLocaleString()} MWh`, detail: "Elektrik tüketimi toplamı", icon: Factory },
      { title: "Direct Emisyon", value: `${data.summary.total_direct_emissions_tons.toLocaleString()} ton`, detail: "Toplam direct emissions", icon: Leaf },
      { title: "Tesis Sayısı", value: `${data.summary.total_facilities}`, detail: "Filtrelenmiş tesis sayısı", icon: Building2 },
    ]
  }, [data])

  const sustainabilityCards = useMemo(() => {
    if (!data) return []
    const metrics = data.sustainability_metrics
    return [
      { title: "Karbon Yoğunluğu", value: metrics.carbon_intensity_ton_per_mwh !== null ? `${metrics.carbon_intensity_ton_per_mwh.toLocaleString()} ton/MWh` : "—" },
      { title: "Su Yoğunluğu", value: metrics.water_intensity_per_mwh !== null ? `${metrics.water_intensity_per_mwh.toLocaleString()} /MWh` : "—" },
      { title: "Atık Yoğunluğu", value: metrics.waste_intensity_per_mwh !== null ? `${metrics.waste_intensity_per_mwh.toLocaleString()} /MWh` : "—" },
      { title: "Üretim Başına Enerji", value: metrics.energy_per_production_unit !== null ? `${metrics.energy_per_production_unit.toLocaleString()}` : "—" },
    ]
  }, [data])

  const historicalCards = useMemo(() => {
    if (!data) return []
    const h = data.historical_analysis
    return [
      { title: "İzlenen Dönem", value: `${h.period_count}`, detail: h.first_period && h.last_period ? `${h.first_period} → ${h.last_period}` : "—", icon: Activity },
      { title: "Enerji Değişimi", value: h.energy_change_percent !== null ? `%${h.energy_change_percent}` : "—", detail: h.energy_trend_label, icon: TrendingUp },
      { title: "Emisyon Değişimi", value: h.emissions_change_percent !== null ? `%${h.emissions_change_percent}` : "—", detail: h.emissions_trend_label, icon: Leaf },
      { title: "Anomali Sayısı", value: `${data.anomaly_analysis.total_anomalies}`, detail: "Tespit edilen kayıt", icon: AlertTriangle },
    ]
  }, [data])

  if (loading) return <div className="space-y-6"><div className="h-40 animate-pulse rounded-3xl bg-slate-100" /></div>

  if (errorMessage) {
    return <div className="rounded-3xl border border-amber-200 bg-amber-50 p-6 shadow-sm">{errorMessage}</div>
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">Company Dashboard</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">Yüklenen şirket verisini gerçek dashboard’a bağla</h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Bu ekran upload edilen company dataset üzerinden enerji, emisyon, geçmiş analiz,
            anomali, tahmin ve sürdürülebilirlik skorunu gösterir.
          </p>

          <div className="mt-5">
            <button
              type="button"
              onClick={handleDownloadPdf}
              className="inline-flex h-11 items-center gap-2 rounded-2xl border border-white/20 bg-white/10 px-5 text-sm font-semibold text-white transition hover:bg-white/20"
            >
              <Download size={18} />
              PDF indir
            </button>
          </div>
        </div>
      </section>

      <section className="grid gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Tesis</label>
          <select value={selectedFacility} onChange={(e) => setSelectedFacility(e.target.value)} className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none">
            <option value="All">All</option>
            {data?.filters.facilities.map((facility) => <option key={facility} value={facility}>{facility}</option>)}
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Eyalet</label>
          <select value={selectedState} onChange={(e) => setSelectedState(e.target.value)} className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none">
            <option value="All">All</option>
            {data?.filters.states.map((state) => <option key={state} value={state}>{state}</option>)}
          </select>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {summaryCards.map((item) => {
          const Icon = item.icon
          return (
            <div key={item.title} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-500">{item.title}</p>
                  <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">{item.value}</p>
                </div>
                <div className="rounded-2xl bg-teal-50 p-3 text-teal-700"><Icon size={20} /></div>
              </div>
              <p className="mt-4 text-sm leading-6 text-slate-600">{item.detail}</p>
            </div>
          )
        })}
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-amber-50 p-3 text-amber-700">
              <Award size={20} />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Sürdürülebilirlik Skoru</p>
              <p className="text-sm text-slate-500">Genel performans puanı</p>
            </div>
          </div>
          <p className="mt-5 text-5xl font-bold tracking-tight text-slate-900">
            {data?.sustainability_score.score}/100
          </p>
          <p className="mt-3 text-lg font-semibold text-slate-700">
            Grade {data?.sustainability_score.grade} • {data?.sustainability_score.label}
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">Güçlü Yönler</p>
          <div className="mt-4 space-y-3">
            {data?.sustainability_score.strengths.map((item, index) => (
              <div key={index} className="rounded-2xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
                {item}
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">Geliştirme Alanları</p>
          <div className="mt-4 space-y-3">
            {data?.sustainability_score.weaknesses.map((item, index) => (
              <div key={index} className="rounded-2xl border border-amber-100 bg-amber-50 px-4 py-3 text-sm text-amber-800">
                {item}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {historicalCards.map((item) => {
          const Icon = item.icon
          return (
            <div key={item.title} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-500">{item.title}</p>
                  <p className="mt-4 text-2xl font-bold tracking-tight text-slate-900">{item.value}</p>
                </div>
                <div className="rounded-2xl bg-amber-50 p-3 text-amber-700"><Icon size={20} /></div>
              </div>
              <p className="mt-4 text-sm leading-6 text-slate-600">{item.detail}</p>
            </div>
          )
        })}
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {sustainabilityCards.map((item) => (
          <div key={item.title} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-sm font-medium text-slate-500">{item.title}</p>
            <p className="mt-4 text-2xl font-bold tracking-tight text-slate-900">{item.value}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Tahmin Dönemi</p>
          <p className="mt-4 text-2xl font-bold tracking-tight text-slate-900">{data?.forecast_analysis.next_period ?? "—"}</p>
          <p className="mt-3 text-sm text-slate-600">Bir sonraki tahmini periyot</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Tahmini Enerji</p>
          <p className="mt-4 text-2xl font-bold tracking-tight text-slate-900">
            {data?.forecast_analysis.forecast_energy_mwh !== null ? `${data?.forecast_analysis.forecast_energy_mwh} MWh` : "—"}
          </p>
          <p className="mt-3 text-sm text-slate-600">{data?.forecast_analysis.energy_forecast_comment}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Tahmini Emisyon</p>
          <p className="mt-4 text-2xl font-bold tracking-tight text-slate-900">
            {data?.forecast_analysis.forecast_direct_emissions_tons !== null ? `${data?.forecast_analysis.forecast_direct_emissions_tons} ton` : "—"}
          </p>
          <p className="mt-3 text-sm text-slate-600">
            {data?.forecast_analysis.emissions_forecast_comment} • güven: {data?.forecast_analysis.confidence}
          </p>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
          <p className="text-sm font-semibold text-slate-900">Geçmiş Analizi</p>
          <p className="mt-1 text-sm text-slate-500">Period bazlı enerji ve direct emissions trendi</p>
          <div className="mt-6 h-[340px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data?.trend ?? []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="energy_mwh" name="Energy (MWh)" stroke="#0F766E" strokeWidth={3} />
                <Line type="monotone" dataKey="direct_emissions_tons" name="Direct Emissions (ton)" stroke="#0F172A" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">Riskli Tesisler</p>
          <p className="mt-1 text-sm text-slate-500">Anomali sayısına göre sıralama</p>

          <div className="mt-5 space-y-3">
            {data?.anomaly_analysis.risky_facilities.length ? (
              data.anomaly_analysis.risky_facilities.map((facility) => (
                <div key={`${facility.facility_name}-${facility.state_or_region}`} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <p className="text-sm font-semibold text-slate-900">{facility.facility_name}</p>
                  <p className="mt-1 text-xs text-slate-500">{facility.state_or_region} • anomaly count: {facility.anomaly_count}</p>
                </div>
              ))
            ) : (
              <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
                Şu an anomali tespit edilmedi.
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  )
}

