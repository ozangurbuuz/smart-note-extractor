ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB limit for MVP

SUMMARY_TYPE_VALUES = {"balanced", "keywords_first"}
SUMMARY_LENGTH_VALUES = {"short", "medium", "long"}

SUMMARY_LENGTH_ALIASES = {
    "small": "short",
    "large": "long",
}

KEYWORD_COUNT_MAP = {
    "balanced": 7,
    "keywords_first": 10,
}

# Sentence selection ratios by desired output length.
SUMMARY_LENGTH_MAP = {
    "short": 0.2,
    "medium": 0.35,
    "long": 0.5,
}
