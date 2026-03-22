export type DataPreviewValidation = {
  is_valid: boolean
  issues: string[]
  warnings: string[]
  detected_metrics: string[]
}

export type DataPreviewResponse = {
  filename: string
  file_type: string
  rows: number
  columns: string[]
  preview: Record<string, unknown>[]
  suggested_mapping: Record<string, string | null>
  validation: DataPreviewValidation
}

export type DocumentPreviewResponse = {
  filename: string
  file_type: string
  pages: number
  characters_extracted: number
  excerpt: string
  detected_keywords: string[]
}
