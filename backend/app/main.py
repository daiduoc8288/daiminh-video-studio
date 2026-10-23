"""
FastAPI application factory
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.v1 import auth, videos, transcripts, analysis, editor, auto_studio, ai_features

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title="DaiMinh AI Video Studio",
        description="Hệ thống sản xuất video bằng AI cho Nhà thuốc Đại Minh",
        version="0.2.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/api/health")
    async def health():
        return {
            "status": "healthy",
            "version": "0.5.0",
            "phase": "Phase 5 - Complete with AI Features",
            "service": "daiminh-video-studio-api"
        }

    # API routes
    @app.get("/api/v1/")
    async def api_root():
        return {
            "message": "Chào mừng đến DAIMINH AI VIDEO STUDIO API",
            "version": "0.2.0",
            "phase": "Phase 2 - AI Video MVP",
            "docs": "/api/docs",
            "endpoints": {
                "auth": "/api/v1/auth/",
                "videos": "/api/v1/videos/",
                "transcripts": "/api/v1/transcripts/",
            }
        }

    # Include routers
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(videos.router, prefix="/api/v1")
    app.include_router(transcripts.router, prefix="/api/v1")
    app.include_router(analysis.router, prefix="/api/v1")
    app.include_router(editor.router, prefix="/api/v1")
    app.include_router(auto_studio.router, prefix="/api/v1")
    app.include_router(ai_features.router, prefix="/api/v1")

    return app
