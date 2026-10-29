import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# Import service
from app.services.plagiarism_engine import check_plagiarism

# ---------------------------------------------------
# Logger
# ---------------------------------------------------
logger = logging.getLogger("plagiarism_route")

# ---------------------------------------------------
# Router
# ---------------------------------------------------
router = APIRouter()

# ---------------------------------------------------
# Request Schema
# ---------------------------------------------------
class PlagiarismRequest(BaseModel):
    text: str = Field(..., min_length=20)
    compare_texts: Optional[List[str]] = Field(
        None,
        description="List of texts to compare against"
    )

# ---------------------------------------------------
# Response Schema
# ---------------------------------------------------
class MatchResult(BaseModel):
    compared_text: str
    similarity_score: float

class PlagiarismResponse(BaseModel):
    success: bool
    overall_similarity: float
    matches: List[MatchResult]

# ---------------------------------------------------
# Route
# ---------------------------------------------------
@router.post("/", response_model=PlagiarismResponse)
async def plagiarism_check(request: PlagiarismRequest):
    try:
        logger.info("Plagiarism check request received")

        if not request.compare_texts:
            raise HTTPException(
                status_code=400,
                detail="compare_texts list cannot be empty"
            )

        results = check_plagiarism(
            input_text=request.text,
            comparison_texts=request.compare_texts
        )

        logger.info("Plagiarism check completed")

        return PlagiarismResponse(
            success=True,
            overall_similarity=results["overall_similarity"],
            matches=results["matches"]
        )

    except HTTPException as http_err:
        logger.warning(f"Client error: {http_err.detail}")
        raise http_err

    except Exception as e:
        logger.exception(f"Server error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error during plagiarism detection"
        )