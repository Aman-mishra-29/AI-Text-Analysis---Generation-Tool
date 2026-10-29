import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Import service
from app.services.autocorrect_engine import correct_text

# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("autocorrect_route")

# ---------------------------------------------------
# Router
# ---------------------------------------------------
router = APIRouter()

# ---------------------------------------------------
# Request Schema
# ---------------------------------------------------
class AutocorrectRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Input text for correction")

# ---------------------------------------------------
# Response Schema
# ---------------------------------------------------
class CorrectionItem(BaseModel):
    original: str
    corrected: str
    message: str

class AutocorrectResponse(BaseModel):
    success: bool
    corrected_text: str
    corrections: List[CorrectionItem]

# ---------------------------------------------------
# Route
# ---------------------------------------------------
@router.post("/", response_model=AutocorrectResponse)
async def autocorrect(request: AutocorrectRequest):
    try:
        logger.info("Autocorrect request received")

        input_text = request.text.strip()

        if len(input_text.split()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Text too short for meaningful correction"
            )

        result = correct_text(input_text)

        logger.info("Autocorrect completed successfully")

        return AutocorrectResponse(
            success=True,
            corrected_text=result["corrected_text"],
            corrections=result["corrections"]
        )

    except HTTPException as http_err:
        logger.warning(f"Client error: {http_err.detail}")
        raise http_err

    except Exception as e:
        logger.exception(f"Server error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error during autocorrect processing"
        )