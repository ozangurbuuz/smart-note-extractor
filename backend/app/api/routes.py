from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.config import SUMMARY_LENGTH_MAP
from app.schemas.response import SummarizeResponse
from app.services.file_validation import validate_file
from app.services.keyword_extraction import extract_keywords
from app.services.sentence_scoring import score_sentences
from app.services.sentence_splitter import split_sentences
from app.services.summary_generation import build_notes, build_summary
from app.services.text_cleaning import clean_text
from app.services.text_extraction import extract_text


router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(
    file: UploadFile = File(...),
    summary_type: str = Form("balanced"),
    summary_length: str = Form("medium"),
) -> SummarizeResponse:
    if summary_type not in {"balanced", "keywords_first"}:
        raise HTTPException(status_code=400, detail="Invalid summary_type value")

    if summary_length not in SUMMARY_LENGTH_MAP:
        raise HTTPException(status_code=400, detail="Invalid summary_length value")

    file_bytes = await file.read()
    validate_file(file_name=file.filename or "", file_bytes=file_bytes)

    try:
        raw_text = extract_text(file_name=file.filename or "", file_bytes=file_bytes)
        cleaned_text = clean_text(raw_text)
        sentences = split_sentences(cleaned_text)

        if not sentences:
            raise HTTPException(status_code=400, detail="No valid sentence found in file")

        scored_sentences = score_sentences(sentences)
        length_ratio = SUMMARY_LENGTH_MAP[summary_length]

        summary = build_summary(scored_sentences=scored_sentences, length_ratio=length_ratio)
        notes = build_notes(scored_sentences=scored_sentences, length_ratio=length_ratio)
        keywords = extract_keywords(cleaned_text, top_k=10 if summary_type == "keywords_first" else 7)

        return SummarizeResponse(
            summary=summary,
            notes=notes,
            keywords=keywords,
            metadata={
                "file_name": file.filename or "unknown",
                "summary_type": summary_type,
                "summary_length": summary_length,
                "sentence_count": len(sentences),
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        # Return a clean API error message for unexpected failures.
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}") from exc
