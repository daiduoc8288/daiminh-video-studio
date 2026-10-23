"""Media and Project schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class MediaAssetResponse(BaseModel):
    id: str
    project_id: str
    original_filename: str
    file_size: int
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    status: str
    thumbnail_path: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class UploadCompleteRequest(BaseModel):
    """Complete upload after all chunks uploaded"""
    upload_session_id: str
    filename: str
    total_size: int


class UploadUrlResponse(BaseModel):
    """Presigned URL for chunk upload"""
    upload_url: str
    upload_session_id: str
    chunk_number: int
    expires_in: int  # seconds
