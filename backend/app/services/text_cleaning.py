import re


def clean_text(raw_text: str) -> str:
    # Remove non-printable control chars but keep Unicode letters (e.g. Turkish chars).
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", raw_text)
    # Normalize line breaks first, then collapse spaces.
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()
