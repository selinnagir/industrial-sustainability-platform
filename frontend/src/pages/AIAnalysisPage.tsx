import { useEffect, useState } from "react"
import { Bot, Sparkles, WandSparkles, AlertTriangle, TrendingUp, SendHorizonal } from "lucide-react"
import { api } from "../services/api"

type AIInsightsResponse = {
  dashboard_context: {
    filters: {
      facilities: string[]
      states: string[]
    }
  }
  insights: {
    overview: {
      total_energy_mwh: number
      total_direct_emissions_tons: number
      facility_count: number
      risk_level: string
      risk_score: number
    }
    risk_assessment: {
      score: number
      level: string
      drivers: string[]
      reason_text: string
    }
    historical_commentary: {
      energy_change_percent: number | null
      emissions_change_percent: number | null
      energy_comment: string
      emissions_comment: string
    }
    anomaly_commentary: {
      total_anomalies: number
      comment: string
      risky_facilities: {
        facility_name: string
        state_or_region: string
        anomaly_count: number
      }[]
    }
    sustainability_commentary: {
      carbon_intensity_ton_per_mwh: number | null
      comment: string
    }
    forecast_commentary: {
      next_period: string | null
      forecast_energy_mwh: number | null
      forecast_direct_emissions_tons: number | null
      confidence: string
      energy_forecast_comment: string
      emissions_forecast_comment: string
    }
    recommendations: string[]
    executive_summary: string
  }
}

type ChatResponse = {
  question: string
  question_type: string
  answer: string
  used_filters: {
    facility: string | null
    state: string | null
  }
}

type ChatMessage = {
  role: "user" | "assistant"
  text: string
}

const sampleQuestions = [
  "Risk seviyem neden yüksek?",
  "Hangi tesis daha problemli?",
  "Emisyonlarım artıyor mu?",
  "Anomali var mı?",
  "Gelecek ay ne bekleniyor?",
  "Ne önerirsin?",
]

export default function AIAnalysisPage() {
  const [data, setData] = useState<AIInsightsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedFacility, setSelectedFacility] = useState("All")
  const [selectedState, setSelectedState] = useState("All")
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [question, setQuestion] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      text: "Merhaba. Company data üzerinden risk, anomali, trend, tahmin ve öneri sorularını cevaplayabilirim.",
    },
  ])

  useEffect(() => {
    const fetchAIInsights = async () => {
      setLoading(true)
      setErrorMessage(null)

      try {
        const params: Record<string, string> = {}
        if (selectedFacility !== "All") params.facility = selectedFacility
        if (selectedState !== "All") params.state = selectedState

        const response = await api.get<AIInsightsResponse>("/company/ai-insights", { params })
        setData(response.data)
      } catch (error: any) {
        console.error("AI insights alınamadı:", error)
        const detail = error?.response?.data?.detail
        setErrorMessage(detail || "AI analiz verisi alınamadı.")
      } finally {
        setLoading(false)
      }
    }

    fetchAIInsights()
  }, [selectedFacility, selectedState])

  const askQuestion = async (text: string) => {
    const clean = text.trim()
    if (!clean) return

    setMessages((prev) => [...prev, { role: "user", text: clean }])
    setQuestion("")
    setChatLoading(true)

    try {
      const response = await api.post<ChatResponse>("/company/chat", {
        question: clean,
        facility: selectedFacility !== "All" ? selectedFacility : null,
        state: selectedState !== "All" ? selectedState : null,
      })

      setMessages((prev) => [...prev, { role: "assistant", text: response.data.answer }])
    } catch (error: any) {
      console.error("Chat hatası:", error)
      const detail = error?.response?.data?.detail || "Soru cevaplanırken hata oluştu."
      setMessages((prev) => [...prev, { role: "assistant", text: String(detail) }])
    } finally {
      setChatLoading(false)
    }
  }

  if (loading) return <div className="space-y-6"><div className="h-40 animate-pulse rounded-3xl bg-slate-100" /></div>

  if (errorMessage) {
    return <div className="rounded-3xl border border-amber-200 bg-amber-50 p-6 shadow-sm">{errorMessage}</div>
  }

  const insights = data?.insights

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">AI Analiz</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">Şirket verisini yorumla ve öneriler üret</h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Bu ekran company dataset üzerinden risk, anomali, geçmiş analiz, tahmin ve öneri üretir.
          </p>
        </div>
      </section>

      <section className="grid gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Tesis</label>
          <select value={selectedFacility} onChange={(e) => setSelectedFacility(e.target.value)} className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none">
            <option value="All">All</option>
            {data?.dashboard_context.filters.facilities.map((facility) => <option key={facility} value={facility}>{facility}</option>)}
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">Eyalet</label>
          <select value={selectedState} onChange={(e) => setSelectedState(e.target.value)} className="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 outline-none">
            <option value="All">All</option>
            {data?.dashboard_context.filters.states.map((state) => <option key={state} value={state}>{state}</option>)}
          </select>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Risk Seviyesi</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">{insights?.overview.risk_level}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Risk Skoru</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">{insights?.overview.risk_score}/100</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Toplam Enerji</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">{insights?.overview.total_energy_mwh.toLocaleString()} MWh</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Toplam Emisyon</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">{insights?.overview.total_direct_emissions_tons.toLocaleString()} ton</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Tahmin Dönemi</p>
          <p className="mt-4 text-3xl font-bold tracking-tight text-slate-900">{insights?.forecast_commentary.next_period ?? "—"}</p>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-teal-50 p-3 text-teal-700"><Bot size={20} /></div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Yönetici Özeti</p>
              <p className="text-sm text-slate-500">AI tarafından oluşturulan kısa değerlendirme</p>
            </div>
          </div>
          <p className="mt-5 text-sm leading-7 text-slate-700">{insights?.executive_summary}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-rose-50 p-3 text-rose-700"><AlertTriangle size={20} /></div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Risk Nedenleri</p>
              <p className="text-sm text-slate-500">Skoru yükselten sürücüler</p>
            </div>
          </div>

          <div className="mt-5 space-y-3">
            {insights?.risk_assessment.drivers.length ? (
              insights.risk_assessment.drivers.map((driver, index) => (
                <div key={index} className="rounded-2xl bg-rose-50 px-4 py-3 text-sm text-rose-700">{driver}</div>
              ))
            ) : (
              <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">Belirgin risk sürücüsü görünmüyor.</div>
            )}
          </div>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-slate-100 p-3 text-slate-700"><TrendingUp size={20} /></div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Geçmiş Analizi</p>
              <p className="text-sm text-slate-500">Trend bazlı değerlendirme</p>
            </div>
          </div>
          <div className="mt-5 space-y-4">
            <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">{insights?.historical_commentary.energy_comment}</div>
            <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">{insights?.historical_commentary.emissions_comment}</div>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-emerald-50 p-3 text-emerald-700"><Sparkles size={20} /></div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Karbon Yorumu</p>
              <p className="text-sm text-slate-500">Sürdürülebilirlik değerlendirmesi</p>
            </div>
          </div>
          <p className="mt-5 text-sm leading-7 text-slate-700">{insights?.sustainability_commentary.comment}</p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-indigo-50 p-3 text-indigo-700"><TrendingUp size={20} /></div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Tahmin Yorumu</p>
              <p className="text-sm text-slate-500">Gelecek dönem beklentisi</p>
            </div>
          </div>
          <div className="mt-5 space-y-4">
            <div className="rounded-2xl bg-indigo-50 px-4 py-3 text-sm text-indigo-700">{insights?.forecast_commentary.energy_forecast_comment}</div>
            <div className="rounded-2xl bg-indigo-50 px-4 py-3 text-sm text-indigo-700">{insights?.forecast_commentary.emissions_forecast_comment}</div>
            <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
              {insights?.forecast_commentary.next_period} • enerji {insights?.forecast_commentary.forecast_energy_mwh} MWh • emisyon {insights?.forecast_commentary.forecast_direct_emissions_tons} ton • güven {insights?.forecast_commentary.confidence}
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-emerald-50 p-3 text-emerald-700"><WandSparkles size={20} /></div>
          <div>
            <p className="text-sm font-semibold text-slate-900">Önerilen Aksiyonlar</p>
            <p className="text-sm text-slate-500">AI destekli temel önlem önerileri</p>
          </div>
        </div>

        <div className="mt-5 space-y-3">
          {insights?.recommendations.map((rec, index) => (
            <div key={index} className="rounded-2xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">{rec}</div>
          ))}
        </div>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-teal-50 p-3 text-teal-700"><Bot size={20} /></div>
          <div>
            <p className="text-sm font-semibold text-slate-900">AI Sustainability Analyst</p>
            <p className="text-sm text-slate-500">Şirket verin üzerinden soru sor</p>
          </div>
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          {sampleQuestions.map((sample) => (
            <button key={sample} onClick={() => askQuestion(sample)} className="rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700 transition hover:bg-slate-100">
              {sample}
            </button>
          ))}
        </div>

        <div className="mt-5 space-y-3">
          {messages.map((message, index) => (
            <div key={index} className={`rounded-2xl px-4 py-3 text-sm leading-7 ${message.role === "assistant" ? "bg-slate-100 text-slate-700" : "bg-teal-700 text-white"}`}>
              <div className="whitespace-pre-wrap">{message.text}</div>
            </div>
          ))}
        </div>

        <div className="mt-5 flex gap-3">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Örnek: Son veriye göre gelecek dönem enerji ve emisyon tahmini yap, risk artar mı söyle ve bana 3 aksiyon öner."
            className="min-h-[96px] flex-1 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none"
          />
          <button onClick={() => askQuestion(question)} disabled={chatLoading} className="flex h-[96px] w-24 items-center justify-center rounded-2xl bg-teal-700 text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60">
            {chatLoading ? "..." : <SendHorizonal size={20} />}
          </button>
        </div>
      </section>
    </div>
  )
}
