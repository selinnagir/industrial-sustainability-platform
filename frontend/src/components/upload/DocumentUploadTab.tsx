import { useState } from "react"
import { FileText } from "lucide-react"
import { api } from "../../services/api"
import type { DocumentPreviewResponse } from "../../types/upload"

export default function DocumentUploadTab() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<DocumentPreviewResponse | null>(null)

  const handlePreview = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    setLoading(true)
    try {
      const response = await api.post<DocumentPreviewResponse>("/upload/document-preview", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      setResult(response.data)
    } catch (error) {
      console.error("Doküman önizleme hatası:", error)
      alert("PDF önizleme sırasında hata oluştu.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
            <FileText size={20} />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">Doküman Yükle</p>
            <p className="text-sm text-slate-500">PDF sürdürülebilirlik raporları ve dokümanlar</p>
          </div>
        </div>

        <div className="mt-5 flex flex-col gap-3 md:flex-row">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="block w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm"
          />
          <button
            onClick={handlePreview}
            disabled={!file || loading}
            className="rounded-2xl bg-teal-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "İnceleniyor..." : "Doküman Önizle"}
          </button>
        </div>
      </div>

      {result && (
        <>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Sayfa Sayısı</p>
              <p className="mt-2 text-2xl font-semibold">{result.pages}</p>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Çıkarılan Karakter</p>
              <p className="mt-2 text-2xl font-semibold">{result.characters_extracted}</p>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Anahtar Kelime</p>
              <p className="mt-2 text-2xl font-semibold">{result.detected_keywords.length}</p>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-slate-900">Algılanan Temalar</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {result.detected_keywords.length === 0 ? (
                <span className="rounded-2xl bg-slate-100 px-3 py-2 text-sm text-slate-600">
                  Tema bulunamadı
                </span>
              ) : (
                result.detected_keywords.map((kw) => (
                  <span key={kw} className="rounded-2xl bg-teal-50 px-3 py-2 text-sm text-teal-700">
                    {kw}
                  </span>
                ))
              )}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-slate-900">Doküman Özeti / Excerpt</p>
            <p className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-600">
              {result.excerpt}
            </p>
          </div>
        </>
      )}
    </div>
  )
}
