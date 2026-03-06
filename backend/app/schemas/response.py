from typing import Any

from pydantic import BaseModel


class SummarizeResponse(BaseModel):
    summary: str
    notes: list[str]
    keywords: list[str]
    metadata: dict[str, Any]
