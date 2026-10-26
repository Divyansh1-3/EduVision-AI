"""
EduVision AI FastAPI Application Entrypoint.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, study

app = FastAPI(
    title="EduVision AI API",
    description="Backend API for EduVision AI - Multimodal Educational Companion",
    version="0.1.0",
)

# CORS configuration for local Vite development server
allowed_origins_env = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)
origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(health.router, prefix="/api")
app.include_router(study.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint verifying API availability."""
    return {
        "message": "Welcome to EduVision AI API",
        "docs_url": "/docs",
        "health_url": "/api/health",
        "study_url": "/api/study",
        "study_image_url": "/api/study/image",
    }
