from pydantic import BaseModel, Field

from app.schemas.request import SummaryLength, SummaryType


class ResponseChunkMetadata(BaseModel):
    chunk_id: str
    start_char: int
    end_char: int
    char_count: int
    sentence_start_index: int
    sentence_end_index: int


class SummarizeMetadata(BaseModel):
    doc_id: str
    file_name: str
    summary_type: SummaryType
    summary_length: SummaryLength
    language: str = "unknown"
    sentence_count: int
    chunk_count: int = 0


class SummarizeResponse(BaseModel):
    summary: str
    notes: list[str]
    keywords: list[str]
    metadata: SummarizeMetadata
    chunks: list[ResponseChunkMetadata] = Field(default_factory=list)
