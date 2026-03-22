from io import BytesIO
from pathlib import Path
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

SUPPORTED_DOCUMENT_EXTENSIONS = {".pdf"}

KEYWORDS = [
    "sustainability",
    "carbon",
    "emission",
    "energy",
    "net zero",
    "climate",
    "renewable",
    "waste",
    "water",
    "scope",
    "esg",
]

async def preview_pdf_upload(file: UploadFile) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Dosya adı bulunamadı.")

    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_DOCUMENT_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Sadece PDF destekleniyor.")

    content = await file.read()

    try:
        reader = PdfReader(BytesIO(content))
        pages = len(reader.pages)

        extracted_parts = []
        for page in reader.pages[:3]:
            text = page.extract_text() or ""
            if text.strip():
                extracted_parts.append(text.strip())

        full_text = "\n".join(extracted_parts).strip()
        excerpt = full_text[:1500] if full_text else "PDF içinden metin çıkarılamadı."

        lowered = excerpt.lower()
        found_keywords = [kw for kw in KEYWORDS if kw in lowered]

        return {
            "filename": file.filename,
            "file_type": "pdf",
            "pages": pages,
            "characters_extracted": len(full_text),
            "excerpt": excerpt,
            "detected_keywords": found_keywords,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF okunamadı: {e}")
