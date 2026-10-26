"""
Gemma AI Service for EduVision AI.

Handles multimodal text and image interactions with Gemma 4 using the official google-genai Python SDK.
Loads GEMINI_API_KEY from backend/.env with explicit path resolution.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve backend/.env path relative to this file's location
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BACKEND_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()


class GemmaConfigurationError(Exception):
    """Raised when the Gemma AI service is misconfigured (e.g. missing API key)."""
    pass


class GemmaAPIError(Exception):
    """Raised when the model generation request fails."""
    pass


def validate_image_bytes(file_bytes: bytes) -> str:
    """
    Validates uploaded image by inspecting actual binary magic bytes and enforcing a 5 MB maximum size.
    Never trusts file extensions alone.
    Returns the resolved MIME type ('image/png', 'image/jpeg', or 'image/webp').
    Raises ValueError if invalid or exceeding size.
    """
    MAX_SIZE = 5 * 1024 * 1024  # 5 MB
    if not file_bytes or len(file_bytes) == 0:
        raise ValueError("Uploaded image file is empty.")

    if len(file_bytes) > MAX_SIZE:
        size_mb = len(file_bytes) / (1024 * 1024)
        raise ValueError(f"Image file size ({size_mb:.2f} MB) exceeds the 5 MB limit.")

    # Inspect binary signatures (magic bytes)
    # PNG signature: 89 50 4E 47 0D 0A 1A 0A
    if len(file_bytes) >= 8 and file_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"

    # JPEG / JPG signature: FF D8 FF
    if len(file_bytes) >= 3 and file_bytes[:3] == b"\xff\xd8\xff":
        return "image/jpeg"

    # WEBP signature: 'RIFF' .... 'WEBP'
    if len(file_bytes) >= 12 and file_bytes[:4] == b"RIFF" and file_bytes[8:12] == b"WEBP":
        return "image/webp"

    raise ValueError(
        "Invalid or unsupported image format. Only authentic JPG, PNG, and WEBP files are accepted."
    )


class GemmaService:
    """Service wrapper for Gemma 4 generation using google-genai SDK."""

    MODEL_NAME = "gemma-4-26b-a4b-it"

    def __init__(self):
        # Refresh environment on initialization to catch updated keys
        if ENV_PATH.exists():
            load_dotenv(dotenv_path=ENV_PATH, override=True)
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _get_client(self):
        """Initializes and returns the google-genai client."""
        api_key = os.getenv("GEMINI_API_KEY") or self.api_key
        if not api_key or api_key.strip() in ("", "your_key_here", "your_gemini_api_key_here"):
            raise GemmaConfigurationError(
                "GEMINI_API_KEY is not configured. Please set your API key in backend/.env."
            )
        try:
            from google import genai
            return genai.Client(api_key=api_key.strip())
        except ImportError as e:
            raise GemmaConfigurationError(
                "google-genai library is not installed in the environment."
            ) from e

    def build_prompt(self, question: str | None, mode: str, has_image: bool = False) -> str:
        """
        Constructs mode-specific educational prompts.
        - explain: beginner-friendly explanation with steps and an example.
        - revision: concise revision notes and key concepts.
        - quiz: five practice questions and an answer key clearly separated.
        Supports both text-only and image-multimodal contexts.
        """
        mode_lower = mode.lower().strip()
        clean_question = question.strip() if question and question.strip() else None

        if has_image:
            image_context = "Refer directly to the attached study image (diagram, chart, textbook figure, or notes)."
            if clean_question:
                topic_line = f"Question/Topic regarding the image: {clean_question}"
            else:
                topic_line = "Explain the concepts and material depicted in the image."
        else:
            image_context = ""
            topic_line = f"Topic/Question: {clean_question or 'Study material'}"

        if mode_lower == "explain":
            prompt_parts = [
                "You are an expert tutor. Provide a clear, beginner-friendly explanation.",
                image_context,
                "Structure your explanation with clear steps and include a concrete real-world example to illustrate the concept.",
                "",
                topic_line,
                "",
                "Format your response cleanly with:",
                "1. Overview & Core Concept",
                "2. Step-by-Step Breakdown",
                "3. Real-World Example",
                "4. Summary / Key Takeaway",
            ]
            return "\n".join([p for p in prompt_parts if p is not None])

        elif mode_lower == "revision":
            prompt_parts = [
                "You are an expert tutor. Provide concise, high-yield revision notes.",
                image_context,
                "Focus on essential concepts, core definitions, and quick summary points ideal for rapid exam review.",
                "",
                topic_line,
                "",
                "Format your response cleanly with:",
                "• Key Concepts & Definitions",
                "• High-Yield Summary Points",
                "• Quick Memory Anchors / Formulas (if applicable)",
            ]
            return "\n".join([p for p in prompt_parts if p is not None])

        elif mode_lower == "quiz":
            prompt_parts = [
                "You are an expert tutor. Create an active-recall practice quiz.",
                image_context,
                "Generate exactly five practice questions to test understanding, followed by an answer key clearly separated from the questions.",
                "",
                topic_line,
                "",
                "Format your response strictly as:",
                "## Practice Questions",
                "1. [Question 1]",
                "2. [Question 2]",
                "3. [Question 3]",
                "4. [Question 4]",
                "5. [Question 5]",
                "",
                "---",
                "## Answer Key & Explanations",
                "1. [Answer and brief explanation]",
                "2. [Answer and brief explanation]",
                "3. [Answer and brief explanation]",
                "4. [Answer and brief explanation]",
                "5. [Answer and brief explanation]",
            ]
            return "\n".join([p for p in prompt_parts if p is not None])

        else:
            raise ValueError(f"Unsupported study mode '{mode}'. Choose 'explain', 'revision', or 'quiz'.")

    def generate_study_content(
        self,
        question: str | None = None,
        mode: str = "explain",
        image_bytes: bytes | None = None,
        mime_type: str | None = None,
    ) -> str:
        """
        Executes synchronous content generation using Gemma 4.
        Supports both text-only and image-multimodal requests.
        Never prints or exposes the API key.
        """
        client = self._get_client()
        has_image = bool(image_bytes and mime_type)
        prompt = self.build_prompt(question, mode, has_image=has_image)

        try:
            from google.genai import types

            if has_image:
                image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                contents = [prompt, image_part]
            else:
                contents = prompt

            response = client.models.generate_content(
                model=self.MODEL_NAME,
                contents=contents,
            )
            if response and response.text:
                return response.text.strip()
            raise GemmaAPIError("The model returned an empty response.")

        except Exception as exc:
            err_text = str(exc)
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key and api_key in err_text:
                err_text = err_text.replace(api_key, "[REDACTED]")
            raise GemmaAPIError(f"Model generation error: {err_text}") from None


# Global singleton instance for injection into routes
gemma_service = GemmaService()
