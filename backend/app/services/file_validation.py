from pathlib import Path

from fastapi import HTTPException

from app.core.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES


def validate_file(file_name: str, file_bytes: bytes) -> None:
    extension = Path(file_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File is too large. Maximum size is 5 MB")
