from io import BytesIO
from pathlib import Path

import fitz
from docx import Document
from fastapi import HTTPException


def _extract_pdf_text(file_bytes: bytes) -> str:
    text_parts: list[str] = []
    with fitz.open(stream=file_bytes, filetype="pdf") as pdf_doc:
        for page in pdf_doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts)


def _extract_txt_text(file_bytes: bytes) -> str:
    candidate_encodings = ("utf-8-sig", "utf-8", "cp1254", "iso-8859-9", "latin-1")

    def score_decoding(decoded_text: str) -> tuple[int, int]:
        replacement_count = decoded_text.count("\ufffd")
        mojibake_markers = decoded_text.count("Ã") + decoded_text.count("Â") + decoded_text.count("├")
        return (replacement_count, mojibake_markers)

    best_text = ""
    best_score: tuple[int, int] | None = None

    for encoding in candidate_encodings:
        decoded = file_bytes.decode(encoding, errors="replace")
        current_score = score_decoding(decoded)

        if best_score is None or current_score < best_score:
            best_text = decoded
            best_score = current_score

        if current_score == (0, 0):
            return decoded

    return best_text


def _extract_docx_text(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)


def extract_text(file_name: str, file_bytes: bytes) -> str:
    extension = Path(file_name).suffix.lower()

    if extension == ".pdf":
        text = _extract_pdf_text(file_bytes)
    elif extension == ".txt":
        text = _extract_txt_text(file_bytes)
    elif extension == ".docx":
        text = _extract_docx_text(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in file")

    return text
