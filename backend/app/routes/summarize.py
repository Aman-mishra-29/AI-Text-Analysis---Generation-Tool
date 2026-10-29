import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.models.request_models import SummarizeRequest
from app.models.response_models import SummarizeResponse, SummarizeData


# Import service layer
from app.services.summarizer import summarize_text

# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("summarize")

# ---------------------------------------------------
# Router Initialization
# ---------------------------------------------------
router = APIRouter()

# ---------------------------------------------------
# Request Schema
# ---------------------------------------------------
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Input text to summarize")
    max_length: Optional[int] = Field(130, ge=30, le=500)
    min_length: Optional[int] = Field(30, ge=10, le=200)

# ---------------------------------------------------
# Response Schema
# ---------------------------------------------------

# ---------------------------------------------------
# Route: Summarize Text
# ---------------------------------------------------
@router.post("/", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    try:
        logger.info("Summarization request received")

        input_text = request.text.strip()

        # Basic validation
        if len(input_text.split()) < 20:
            raise HTTPException(
                status_code=400,
                detail="Input text is too short for summarization"
            )

        # Call service layer
        summary = summarize_text(
            text=input_text,
            max_length=request.max_length,
            min_length=request.min_length
        )

        if not summary:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate summary"
            )

        logger.info("Summarization successful")

        return SummarizeResponse(
            success=True,
            message="Summarization successful",
            data=SummarizeData(
                summary=summary,
                input_length=len(input_text),
                summary_length=len(summary)
            )
        )


    except HTTPException as http_err:
        logger.warning(f"Client error: {http_err.detail}")
        raise http_err

    except Exception as e:
        logger.exception(f"Server error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during summarization"
        )