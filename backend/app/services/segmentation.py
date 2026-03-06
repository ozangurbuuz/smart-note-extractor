from app.schemas.domain import ChunkMetadata
from app.services.sentence_splitter import split_sentences


def _compute_sentence_offsets(sentences: list[str]) -> list[tuple[int, int]]:
    offsets: list[tuple[int, int]] = []
    cursor = 0

    for sentence in sentences:
        start = cursor
        end = start + len(sentence)
        offsets.append((start, end))
        # Simulate normalized join with single spaces between sentences.
        cursor = end + 1

    return offsets


def _build_chunk(
    *,
    chunk_index: int,
    sentence_start_index: int,
    sentence_end_index: int,
    sentences: list[str],
    sentence_offsets: list[tuple[int, int]],
) -> ChunkMetadata:
    start_char = sentence_offsets[sentence_start_index][0]
    end_char = sentence_offsets[sentence_end_index][1]
    text = " ".join(sentences[sentence_start_index : sentence_end_index + 1])

    return ChunkMetadata(
        chunk_id=f"chunk_{chunk_index:04d}",
        text=text,
        start_char=start_char,
        end_char=end_char,
        char_count=max(end_char - start_char, 0),
        sentence_start_index=sentence_start_index,
        sentence_end_index=sentence_end_index,
    )


def build_chunks(sentences: list[str], max_chars: int = 900) -> list[ChunkMetadata]:
    if not sentences:
        return []

    sentence_offsets = _compute_sentence_offsets(sentences)
    chunks: list[ChunkMetadata] = []
    chunk_index = 1
    current_start = 0
    current_len = 0

    for sentence_index, sentence in enumerate(sentences):
        sentence_len = len(sentence)

        # Keep very long sentences as standalone chunks.
        if sentence_len >= max_chars:
            if current_len > 0:
                chunks.append(
                    _build_chunk(
                        chunk_index=chunk_index,
                        sentence_start_index=current_start,
                        sentence_end_index=sentence_index - 1,
                        sentences=sentences,
                        sentence_offsets=sentence_offsets,
                    )
                )
                chunk_index += 1
                current_len = 0

            chunks.append(
                _build_chunk(
                    chunk_index=chunk_index,
                    sentence_start_index=sentence_index,
                    sentence_end_index=sentence_index,
                    sentences=sentences,
                    sentence_offsets=sentence_offsets,
                )
            )
            chunk_index += 1
            current_start = sentence_index + 1
            continue

        projected_len = sentence_len if current_len == 0 else current_len + 1 + sentence_len
        if projected_len > max_chars and current_len > 0:
            chunks.append(
                _build_chunk(
                    chunk_index=chunk_index,
                    sentence_start_index=current_start,
                    sentence_end_index=sentence_index - 1,
                    sentences=sentences,
                    sentence_offsets=sentence_offsets,
                )
            )
            chunk_index += 1
            current_start = sentence_index
            current_len = sentence_len
            continue

        current_len = projected_len

    if current_start < len(sentences):
        chunks.append(
            _build_chunk(
                chunk_index=chunk_index,
                sentence_start_index=current_start,
                sentence_end_index=len(sentences) - 1,
                sentences=sentences,
                sentence_offsets=sentence_offsets,
            )
        )

    return chunks


def segment_text(text: str, max_chunk_chars: int = 900) -> tuple[list[str], list[ChunkMetadata]]:
    sentences = split_sentences(text)
    chunks = build_chunks(sentences, max_chars=max_chunk_chars)
    return sentences, chunks
