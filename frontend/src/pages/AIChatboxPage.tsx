import { useEffect, useState } from "react"
import { Bot, SendHorizonal } from "lucide-react"
import { api } from "../services/api"

type FiltersResponse = {
  dashboard_context: {
    filters: {
      facilities: string[]
      states: string[]
    }
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
  "Tahmine göre hangi aksiyonu önceliklendirmeliyim?",
  "Ne önerirsin?",
]

export default function AIChatboxPage() {
  const [facilities, setFacilities] = useState<string[]>([])
  const [states, setStates] = useState<string[]>([])
  const [selectedFacility, setSelectedFacility] = useState("All")
  const [selectedState, setSelectedState] = useState("All")
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(true)
  const [chatLoading, setChatLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      text: "Merhaba. Burada şirket verin üzerinden risk, anomali, trend, tahmin ve öneri sorularını cevaplayabilirim.",
    },
  ])

  useEffect(() => {
    const fetchFilters = async () => {
      setLoading(true)
      setErrorMessage(null)

      try {
        const response = await api.get<FiltersResponse>("/company/ai-insights")
        setFacilities(response.data.dashboard_context.filters.facilities || [])
        setStates(response.data.dashboard_context.filters.states || [])
      } catch (error: any) {
        console.error("Chatbox filtreleri alınamadı:", error)
        const detail = error?.response?.data?.detail
        setErrorMessage(detail || "Chatbox için gerekli filtre verisi alınamadı.")
      } finally {
        setLoading(false)
      }
    }

    fetchFilters()
  }, [])

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

  if (loading) {
    return <div className="h-40 animate-pulse rounded-3xl bg-slate-100" />
  }

  if (errorMessage) {
    return (
      <div className="rounded-3xl border border-amber-200 bg-amber-50 p-6 shadow-sm">
        <p className="text-lg font-semibold text-amber-800">AI Chatbox açılamadı</p>
        <p className="mt-3 text-sm text-amber-700">{errorMessage}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">
            AI Chatbox
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Verine soru sor, cevabı anında al
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Bu ekran company dataset üzerinden risk, anomali, tahmin, trend ve aksiyon önerilerini sohbet halinde döner.
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

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
            <Bot size={20} />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">Hazır Sorular</p>
            <p className="text-sm text-slate-500">Tek tıkla dene</p>
          </div>
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          {sampleQuestions.map((sample) => (
            <button
              key={sample}
              onClick={() => askQuestion(sample)}
              className="rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700 transition hover:bg-slate-100"
            >
              {sample}
            </button>
          ))}
        </div>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="space-y-3">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`rounded-2xl px-4 py-3 text-sm leading-7 ${
                message.role === "assistant"
                  ? "bg-slate-100 text-slate-700"
                  : "bg-teal-700 text-white"
              }`}
            >
              <div className="whitespace-pre-wrap">{message.text}</div>
            </div>
          ))}
        </div>

        <div className="mt-5 flex gap-3">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Örnek: tahmine göre hangi aksiyonu önceliklendirmeliyim?"
            className="min-h-[96px] flex-1 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none"
          />
          <button
            onClick={() => askQuestion(question)}
            disabled={chatLoading}
            className="flex h-[96px] w-24 items-center justify-center rounded-2xl bg-teal-700 text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {chatLoading ? "..." : <SendHorizonal size={20} />}
          </button>
        </div>
      </section>
    </div>
  )
}
