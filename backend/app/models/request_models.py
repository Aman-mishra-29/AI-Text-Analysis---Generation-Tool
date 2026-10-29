from pydantic import BaseModel, Field, validator
from typing import List, Optional


# ---------------------------------------------------
# Base Model (Common Config)
# ---------------------------------------------------
class BaseRequestModel(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True


# ---------------------------------------------------
# Summarization Request
# ---------------------------------------------------
class SummarizeRequest(BaseRequestModel):
    text: str = Field(
        ...,
        min_length=20,
        description="Input text to summarize"
    )
    max_length: Optional[int] = Field(
        500,
        ge=30,
        le=500,
        description="Maximum length of summary"
    )
    min_length: Optional[int] = Field(
        20,
        ge=10,
        le=200,
        description="Minimum length of summary"
    )

    @validator("text")
    def validate_text(cls, value):
        if len(value.split()) < 20:
            raise ValueError("Text must contain at least 20 words for summarization")
        return value


# ---------------------------------------------------
# Plagiarism Request
# ---------------------------------------------------
class PlagiarismRequest(BaseRequestModel):
    text: str = Field(
        ...,
        min_length=20,
        description="Input text to check plagiarism"
    )
    compare_texts: List[str] = Field(
        ...,
        min_items=1,
        description="List of texts to compare against"
    )

    @validator("compare_texts")
    def validate_compare_texts(cls, value):
        if not value:
            raise ValueError("compare_texts cannot be empty")

        for text in value:
            if len(text.split()) < 5:
                raise ValueError("Each comparison text must have at least 5 words")

        return value


# ---------------------------------------------------
# Autocorrect Request
# ---------------------------------------------------
class AutocorrectRequest(BaseRequestModel):
    text: str = Field(
        ...,
        min_length=5,
        description="Input text for autocorrection"
    )

    @validator("text")
    def validate_text(cls, value):
        if len(value.split()) < 2:
            raise ValueError("Text must contain at least 2 words for correction")
        return value


# ---------------------------------------------------
# Optional: Batch Requests (Advanced Feature)
# ---------------------------------------------------
class BatchSummarizeRequest(BaseRequestModel):
    texts: List[str] = Field(
        ...,
        min_items=1,
        description="List of texts to summarize"
    )

    @validator("texts")
    def validate_texts(cls, value):
        for text in value:
            if len(text.split()) < 20:
                raise ValueError("Each text must have at least 20 words")
        return value


class BatchAutocorrectRequest(BaseRequestModel):
    texts: List[str] = Field(
        ...,
        min_items=1,
        description="List of texts to correct"
    )