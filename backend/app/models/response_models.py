from pydantic import BaseModel, Field
from typing import Any, List, Optional, Generic, TypeVar
from datetime import datetime

# Generic Type for flexible responses
T = TypeVar("T")


# ---------------------------------------------------
# Base Response Model
# ---------------------------------------------------
class BaseResponse(BaseModel):
    success: bool = Field(..., description="Status of the response")
    message: str = Field(..., description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


# ---------------------------------------------------
# Generic Success Response
# ---------------------------------------------------
class SuccessResponse(BaseResponse, Generic[T]):
    data: Optional[T] = Field(None, description="Payload data")


# ---------------------------------------------------
# Error Response Model
# ---------------------------------------------------
class ErrorResponse(BaseResponse):
    error_code: Optional[str] = Field(None, description="Error identifier")
    details: Optional[Any] = Field(None, description="Additional error details")


# ---------------------------------------------------
# Summarization Response
# ---------------------------------------------------
class SummarizeData(BaseModel):
    summary: str
    input_length: int
    summary_length: int


class SummarizeResponse(SuccessResponse[SummarizeData]):
    pass


# ---------------------------------------------------
# Plagiarism Response
# ---------------------------------------------------
class MatchResult(BaseModel):
    compared_text: str
    similarity_score: float


class PlagiarismData(BaseModel):
    overall_similarity: float
    matches: List[MatchResult]


class PlagiarismResponse(SuccessResponse[PlagiarismData]):
    pass


# ---------------------------------------------------
# Autocorrect Response
# ---------------------------------------------------
class CorrectionItem(BaseModel):
    original: str
    corrected: str
    message: str


class AutocorrectData(BaseModel):
    corrected_text: str
    corrections: List[CorrectionItem]


class AutocorrectResponse(SuccessResponse[AutocorrectData]):
    pass


# ---------------------------------------------------
# Health Check Response
# ---------------------------------------------------
class HealthResponse(BaseResponse):
    status: str


# ---------------------------------------------------
# Pagination (Future Use)
# ---------------------------------------------------
class PaginatedResponse(BaseResponse, Generic[T]):
    data: List[T]
    total: int
    page: int
    page_size: int


# ---------------------------------------------------
# Utility Functions (Optional)
# ---------------------------------------------------
def build_success_response(
    message: str,
    data: Any = None
) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow()
    }


def build_error_response(
    message: str,
    error_code: Optional[str] = None,
    details: Any = None
) -> dict:
    return {
        "success": False,
        "message": message,
        "error_code": error_code,
        "details": details,
        "timestamp": datetime.utcnow()
    }