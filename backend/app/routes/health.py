"""
Health check route.
"""

from fastapi import APIRouter
from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint returning system status and service name.
    """
    return HealthResponse(status="ok", service="eduvision-api")
