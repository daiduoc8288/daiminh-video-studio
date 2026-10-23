"""
Configuration module for FastAPI app
"""

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """Application settings"""

    # API
    APP_NAME: str = "DaiMinh AI Video Studio"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Server
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://daiminh:daiminh123@localhost:5432/daiminh_video_studio"
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Storage (S3)
    S3_BUCKET: str = os.getenv("S3_BUCKET", "daiminh-videos")
    S3_ENDPOINT_URL: str = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "minioadmin")
    S3_REGION: str = os.getenv("S3_REGION", "us-east-1")

    # Whisper API
    WHISPER_API_KEY: str = os.getenv("WHISPER_API_KEY", "")

    # File Upload
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024 * 1024  # 100GB
    ALLOWED_VIDEO_FORMATS: list = ["mp4", "mov", "avi", "webm", "mkv"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
