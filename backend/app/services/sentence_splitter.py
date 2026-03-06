import re

import nltk
from nltk.tokenize import sent_tokenize


def _ensure_punkt() -> None:
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)


def split_sentences(text: str) -> list[str]:
    _ensure_punkt()

    try:
        sentences = sent_tokenize(text)
    except Exception:
        # Fallback keeps the API functional in edge cases.
        sentences = re.split(r"(?<=[.!?])\s+", text)

    return [sentence.strip() for sentence in sentences if sentence.strip()]
