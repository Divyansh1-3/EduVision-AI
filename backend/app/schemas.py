"""
Pydantic schemas and data models for EduVision AI.
"""

from typing import Literal
from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(default="ok", description="Service status")
    service: str = Field(default="eduvision-api", description="Service identifier")


class StudyRequest(BaseModel):
    """Schema for study query requests."""
    question: str = Field(..., description="The student's study question or topic")
    mode: Literal["explain", "revision", "quiz"] = Field(
        default="explain",
        description="Study mode: explain, revision, or quiz"
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Question cannot be empty or contain only whitespace.")
        return value.strip()


class StudyResponse(BaseModel):
    """Schema for study query responses."""
    mode: str = Field(..., description="The study mode used")
    answer: str = Field(..., description="The AI-generated study response")
