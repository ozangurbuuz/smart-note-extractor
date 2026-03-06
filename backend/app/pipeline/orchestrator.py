from uuid import uuid4

from app.core.config import KEYWORD_COUNT_MAP, SUMMARY_LENGTH_MAP
from app.schemas.domain import PipelineArtifacts
from app.schemas.request import SummarizeRequest
from app.schemas.response import ResponseChunkMetadata, SummarizeMetadata, SummarizeResponse
from app.services.keyword_extraction import extract_keywords
from app.services.language_detection import detect_language
from app.services.sentence_scoring import score_sentences
from app.services.segmentation import segment_text
from app.services.summary_generation import build_notes, build_summary
from app.services.text_cleaning import clean_text
from app.services.text_extraction import extract_text


def run_analysis_pipeline(
    *,
    file_name: str,
    file_bytes: bytes,
    request: SummarizeRequest,
) -> SummarizeResponse:
    normalized_file_name = file_name or "unknown"

    raw_text = extract_text(file_name=file_name, file_bytes=file_bytes)
    cleaned_text = clean_text(raw_text)
    language = detect_language(cleaned_text)
    sentences, chunks = segment_text(cleaned_text)

    if not sentences:
        raise ValueError("No valid sentence found in file")

    scored_sentences = score_sentences(sentences)
    length_ratio = SUMMARY_LENGTH_MAP[request.summary_length]

    summary = build_summary(scored_sentences=scored_sentences, length_ratio=length_ratio)
    notes = build_notes(scored_sentences=scored_sentences, length_ratio=length_ratio)
    keywords = extract_keywords(cleaned_text, top_k=KEYWORD_COUNT_MAP[request.summary_type])

    # Keeping this object now makes chunk metadata additions easy in RAG phase.
    artifacts = PipelineArtifacts(
        doc_id=str(uuid4()),
        file_name=normalized_file_name,
        summary_type=request.summary_type,
        summary_length=request.summary_length,
        summary=summary,
        notes=notes,
        keywords=keywords,
        language=language,
        sentence_count=len(sentences),
        chunks=chunks,
        chunk_count=len(chunks),
    )

    return SummarizeResponse(
        summary=artifacts.summary,
        notes=artifacts.notes,
        keywords=artifacts.keywords,
        metadata=SummarizeMetadata(
            doc_id=artifacts.doc_id,
            file_name=artifacts.file_name,
            summary_type=artifacts.summary_type,
            summary_length=artifacts.summary_length,
            language=artifacts.language,
            sentence_count=artifacts.sentence_count,
            chunk_count=artifacts.chunk_count,
        ),
        chunks=[
            ResponseChunkMetadata(
                chunk_id=chunk.chunk_id,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
                char_count=chunk.char_count,
                sentence_start_index=chunk.sentence_start_index,
                sentence_end_index=chunk.sentence_end_index,
            )
            for chunk in artifacts.chunks
        ],
    )
