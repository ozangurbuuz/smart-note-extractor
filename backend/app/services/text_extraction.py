from pathlib import Path

import fitz
from fastapi import HTTPException


def _extract_pdf_text(file_bytes: bytes) -> str:
    text_parts: list[str] = []
    with fitz.open(stream=file_bytes, filetype="pdf") as pdf_doc:
        for page in pdf_doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts)


def _extract_txt_text(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def extract_text(file_name: str, file_bytes: bytes) -> str:
    extension = Path(file_name).suffix.lower()

    if extension == ".pdf":
        text = _extract_pdf_text(file_bytes)
    elif extension == ".txt":
        text = _extract_txt_text(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in file")

    return text
