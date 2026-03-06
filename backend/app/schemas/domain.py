from pydantic import BaseModel


class ChunkMetadata(BaseModel):
    chunk_id: str
    text: str
    start_char: int
    end_char: int
    char_count: int
    sentence_start_index: int
    sentence_end_index: int


class PipelineArtifacts(BaseModel):
    doc_id: str
    file_name: str
    summary_type: str
    summary_length: str
    summary: str
    notes: list[str]
    keywords: list[str]
    language: str
    sentence_count: int
    chunks: list[ChunkMetadata]
    chunk_count: int
