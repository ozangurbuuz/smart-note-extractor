from typing import Literal

from pydantic import BaseModel, model_validator

from app.core.config import SUMMARY_LENGTH_ALIASES


SummaryType = Literal["balanced", "keywords_first"]
SummaryLength = Literal["short", "medium", "long"]


class SummarizeRequest(BaseModel):
    summary_type: SummaryType = "balanced"
    summary_length: SummaryLength = "medium"

    @model_validator(mode="before")
    @classmethod
    def normalize_summary_length_aliases(cls, data: object) -> object:
        if not isinstance(data, dict):
            return data

        normalized = dict(data)
        raw_value = normalized.get("summary_length")

        if isinstance(raw_value, str):
            lower_value = raw_value.lower()
            normalized["summary_length"] = SUMMARY_LENGTH_ALIASES.get(lower_value, lower_value)

        return normalized
