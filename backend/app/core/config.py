ALLOWED_EXTENSIONS = {".pdf", ".txt"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB limit for MVP

# Sentence selection ratios by desired output length.
SUMMARY_LENGTH_MAP = {
    "short": 0.2,
    "medium": 0.35,
    "long": 0.5,
}
