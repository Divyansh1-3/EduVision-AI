"""
Study endpoints for EduVision AI.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from app.schemas import StudyRequest, StudyResponse
from app.services.gemma_service import (
    gemma_service,
    validate_image_bytes,
    GemmaConfigurationError,
    GemmaAPIError,
)

router = APIRouter(tags=["study"])


@router.post(
    "/study",
    response_model=StudyResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate AI study assistance (Text Query)",
    description="Generates explanations, revision notes, or practice quizzes using Gemma 4."
)
async def generate_study_response(request: StudyRequest):
    """
    POST /api/study endpoint for text-based queries.
    Receives a question and study mode ('explain', 'revision', or 'quiz').
    Returns structured study response.
    """
    # Defensive check for empty or whitespace-only question
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'question' field cannot be empty or contain only whitespace."
        )

    try:
        answer = gemma_service.generate_study_content(
            question=request.question,
            mode=request.mode
        )
        return StudyResponse(mode=request.mode, answer=answer)

    except GemmaConfigurationError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Service Configuration Error: {str(err)}"
        )

    except GemmaAPIError as err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI Upstream Error: {str(err)}"
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the study response."
        )


@router.post(
    "/study/image",
    response_model=StudyResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate AI study assistance from Image (Multimodal)",
    description="Accepts an image (JPG, PNG, or WEBP up to 5 MB) with an optional text question and study mode."
)
async def generate_study_from_image(
    file: UploadFile = File(..., description="Uploaded diagram or study material image"),
    mode: str = Form(default="explain", description="Study mode: explain, revision, or quiz"),
    question: Optional[str] = Form(default=None, description="Optional question or topic regarding the image"),
):
    """
    POST /api/study/image multipart/form-data endpoint.
    Validates MIME type via binary magic bytes and max size (5 MB).
    Calls Gemma 4 with image Part and returns structured study response.
    """
    mode_clean = mode.lower().strip()
    if mode_clean not in ("explain", "revision", "quiz"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Input 'mode' should be 'explain', 'revision' or 'quiz'"
        )

    # Read uploaded bytes and enforce immediate stream cleanup
    try:
        image_bytes = await file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read the uploaded image file."
        )
    finally:
        await file.close()

    # Validate image content type using binary inspection (never trust file extension alone)
    try:
        resolved_mime = validate_image_bytes(image_bytes)
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )

    try:
        answer = gemma_service.generate_study_content(
            question=question,
            mode=mode_clean,
            image_bytes=image_bytes,
            mime_type=resolved_mime,
        )
        return StudyResponse(mode=mode_clean, answer=answer)

    except GemmaConfigurationError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Service Configuration Error: {str(err)}"
        )

    except GemmaAPIError as err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI Upstream Error: {str(err)}"
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the multimodal study request."
        )
