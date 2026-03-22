import { useState } from "react"
import DataUploadTab from "../components/upload/DataUploadTab"
import DocumentUploadTab from "../components/upload/DocumentUploadTab"

export default function UploadCenterPage() {
  const [activeTab, setActiveTab] = useState<"data" | "document">("data")

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-r from-[#0F172A] via-[#0F172A] to-[#0F766E] p-8 text-white shadow-sm">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-200">
            Upload Center
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Şirket verilerini ve sürdürülebilirlik dokümanlarını yükle
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-200">
            Veri yükleme alanı analiz ve tahmin için; doküman yükleme alanı ise
            sürdürülebilirlik raporları ve PDF içerikleri için kullanılır.
          </p>
        </div>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => setActiveTab("data")}
            className={`rounded-2xl px-4 py-3 text-sm font-semibold transition ${
              activeTab === "data"
                ? "bg-teal-700 text-white"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            Veri Yükle
          </button>

          <button
            onClick={() => setActiveTab("document")}
            className={`rounded-2xl px-4 py-3 text-sm font-semibold transition ${
              activeTab === "document"
                ? "bg-teal-700 text-white"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            Doküman Yükle
          </button>
        </div>
      </section>

      {activeTab === "data" ? <DataUploadTab /> : <DocumentUploadTab />}
    </div>
  )
}
