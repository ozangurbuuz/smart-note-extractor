import re


def clean_text(raw_text: str) -> str:
    # Keep plain text while normalizing noisy spacing.
    text = re.sub(r"\s+", " ", raw_text)
    text = re.sub(r"[^\x20-\x7E\n\r\t]", "", text)
    return text.strip()
