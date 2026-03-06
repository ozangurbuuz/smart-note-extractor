def detect_language(text: str) -> str:
    lowered = text.lower()

    turkish_markers = [" ve ", " bir ", " için ", " olarak ", " bu ", "ş", "ğ", "ı", "ö", "ü", "ç"]
    english_markers = [" the ", " and ", " of ", " with ", " is ", " are "]

    turkish_score = sum(lowered.count(marker) for marker in turkish_markers)
    english_score = sum(lowered.count(marker) for marker in english_markers)

    if turkish_score > english_score:
        return "tr"
    if english_score > turkish_score:
        return "en"
    return "unknown"
