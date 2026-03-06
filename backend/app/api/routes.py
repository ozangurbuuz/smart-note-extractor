from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import ValidationError

from app.core.logging import get_logger
from app.pipeline.orchestrator import run_analysis_pipeline
from app.schemas.request import SummarizeRequest
from app.schemas.response import SummarizeResponse
from app.services.file_validation import validate_file


router = APIRouter()
logger = get_logger(__name__)


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(
    file: UploadFile = File(...),
    summary_type: str = Form("balanced"),
    summary_length: str = Form("medium"),
) -> SummarizeResponse:
    try:
        request_data = SummarizeRequest(
            summary_type=summary_type,
            summary_length=summary_length,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid request values: {exc.errors()}") from exc

    file_bytes = await file.read()
    validate_file(file_name=file.filename or "", file_bytes=file_bytes)

    try:
        return run_analysis_pipeline(
            file_name=file.filename or "",
            file_bytes=file_bytes,
            request=request_data,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected processing failure")
        # Return a clean API error message for unexpected failures.
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}") from exc
