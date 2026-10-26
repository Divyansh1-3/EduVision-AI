"""
Standalone test script for Gemma 4 using the official google-genai SDK.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Load backend/.env whether script is run from repo root or backend directory
    script_dir = Path(__file__).resolve().parent
    env_file = script_dir / ".env"

    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() in ("", "your_key_here", "your_gemini_api_key_here"):
        print("Configuration Error: GEMINI_API_KEY is missing or contains placeholder in backend/.env.")
        print("Please set your real API key in backend/.env before running this test.")
        sys.exit(1)

    try:
        from google import genai
    except ImportError:
        print("Import Error: google-genai is not installed in the active environment.")
        sys.exit(1)

    try:
        client = genai.Client(api_key=api_key.strip())
        model_name = "gemma-4-26b-a4b-it"
        prompt = "Explain photosynthesis to a first-year college student in three bullet points."

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        if response and response.text:
            print(response.text)
        else:
            print("Received empty response from model.")

    except Exception as exc:
        # Safe error reporting: never print credentials or raw query strings containing keys
        err_msg = str(exc)
        if api_key and api_key in err_msg:
            err_msg = err_msg.replace(api_key, "[REDACTED_KEY]")
        print(f"Generation Error ({type(exc).__name__}): {err_msg}")
        sys.exit(1)

if __name__ == "__main__":
    main()
