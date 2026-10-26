"""
Pydantic schemas and data models for EduVision AI.
"""

from typing import Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(default="ok", description="Service status")
    service: str = Field(default="eduvision-api", description="Service identifier")


# --- Future Schemas (Placeholders for incremental expansion) ---

class StudyRequestPlaceholder(BaseModel):
    """Placeholder schema for future visual/textual study requests."""
    mode: str = Field(description="Study mode: explain, revision, or quiz")
    prompt: str = Field(description="User question or text prompt")
    image_base64: Optional[str] = Field(default=None, description="Optional base64 image data")


class StudyResponsePlaceholder(BaseModel):
    """Placeholder schema for future AI response output."""
    mode: str
    content: str
