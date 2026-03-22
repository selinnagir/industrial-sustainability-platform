import { useState } from "react"
import { Upload, Table2 } from "lucide-react"
import { api } from "../../services/api"
import type { DataPreviewResponse } from "../../types/upload"

export default function DataUploadTab() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [result, setResult] = useState<DataPreviewResponse | null>(null)

  const handlePreview = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    setLoading(true)
    try {
      const response = await api.post<DataPreviewResponse>("/upload/data-preview", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      setResult(response.data)
    } catch (error: any) {
      console.error("Veri önizleme hatası:", error)
      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Dosya önizleme sırasında hata oluştu."
      alert(String(message))
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    setSaving(true)
    try {
      const response = await api.post("/upload/data-ingest", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      alert(response.data.message || "Şirket verisi kaydedildi.")
    } catch (error: any) {
      console.error("Veri kaydetme hatası:", error)
      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Veri kaydetme sırasında hata oluştu."
      alert(String(message))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
            <Upload size={20} />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">Veri Yükle</p>
            <p className="text-sm text-slate-500">CSV, Excel ve JSON desteklenir</p>
          </div>
        </div>

        <div className="mt-5 flex flex-col gap-3 md:flex-row">
          <input
            type="file"
            accept=".csv,.xlsx,.xls,.json"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="block w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm"
          />
          <button
            onClick={handlePreview}
            disabled={!file || loading}
            className="rounded-2xl bg-teal-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "İnceleniyor..." : "Önizleme Oluştur"}
          </button>
        </div>

        {file && (
          <p className="mt-3 text-sm text-slate-600">
            Seçilen dosya: <span className="font-medium">{file.name}</span>
          </p>
        )}

        {result?.validation?.is_valid && file && (
          <div className="mt-4">
            <button
              onClick={handleSave}
              disabled={saving}
              className="rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {saving ? "Kaydediliyor..." : "Sisteme Kaydet"}
            </button>
          </div>
        )}
      </div>

      {result && (
        <>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Dosya Türü</p>
              <p className="mt-2 text-2xl font-semibold">{result.file_type.toUpperCase()}</p>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Satır</p>
              <p className="mt-2 text-2xl font-semibold">{result.rows}</p>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Kolon</p>
              <p className="mt-2 text-2xl font-semibold">{result.columns.length}</p>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Doğrulama</p>
              <p className="mt-2 text-2xl font-semibold">
                {result.validation.is_valid ? "Geçti" : "Sorunlu"}
              </p>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-teal-50 p-3 text-teal-700">
                <Table2 size={20} />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-900">İlk Satırlar</p>
                <p className="text-sm text-slate-500">Önizleme tablosu</p>
              </div>
            </div>

            <div className="mt-5 overflow-x-auto">
              <table className="min-w-full border-separate border-spacing-y-2 text-sm">
                <thead>
                  <tr>
                    {result.columns.map((col) => (
                      <th
                        key={col}
                        className="whitespace-nowrap rounded-2xl bg-slate-100 px-4 py-3 text-left font-medium text-slate-700"
                      >
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.preview.map((row, index) => (
                    <tr key={index}>
                      {result.columns.map((col) => (
                        <td
                          key={col}
                          className="whitespace-nowrap rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-600"
                        >
                          {String(row[col] ?? "—")}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
