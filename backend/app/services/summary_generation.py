def _select_top_sentences(
    scored_sentences: list[tuple[int, str, float]],
    length_ratio: float,
    min_count: int,
    max_count: int,
) -> list[str]:
    sentence_count = len(scored_sentences)
    target_count = max(min_count, int(round(sentence_count * length_ratio)))
    target_count = min(target_count, max_count, sentence_count)

    top_scored = sorted(scored_sentences, key=lambda item: item[2], reverse=True)[:target_count]
    ordered = sorted(top_scored, key=lambda item: item[0])
    return [sentence for _, sentence, _ in ordered]


def build_summary(scored_sentences: list[tuple[int, str, float]], length_ratio: float) -> str:
    selected = _select_top_sentences(scored_sentences, length_ratio, min_count=1, max_count=8)
    return " ".join(selected)


def build_notes(scored_sentences: list[tuple[int, str, float]], length_ratio: float) -> list[str]:
    return _select_top_sentences(scored_sentences, length_ratio, min_count=3, max_count=10)
