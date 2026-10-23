"""Transcript schemas"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TranscriptSegment(BaseModel):
    """Transcript segment with timestamp"""
    start_time: float
    end_time: float
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None


class TranscriptResponse(BaseModel):
    """Transcript response"""
    id: str
    media_asset_id: str
    content: Optional[str] = None
    segments: Optional[List[TranscriptSegment]] = None
    language: str
    duration: Optional[float] = None
    status: str
    created_at: str

    class Config:
        from_attributes = True


class TranscriptUpdateRequest(BaseModel):
    """Update transcript content"""
    content: Optional[str] = None
    segments: Optional[List[TranscriptSegment]] = None


class TranscriptExportRequest(BaseModel):
    """Export transcript"""
    format: str = "srt"  # srt, vtt, json


class SilenceSegment(BaseModel):
    """Silence segment"""
    start_time: float
    end_time: float
    duration: float


class VideoAnalysisResponse(BaseModel):
    """Video analysis results"""
    id: str
    media_asset_id: str
    silence_segments: Optional[List[SilenceSegment]] = None
    suggested_cuts: Optional[List[dict]] = None
    highlights: Optional[List[dict]] = None
    status: str
    confidence_score: Optional[float] = None

    class Config:
        from_attributes = True


class BrandTemplateResponse(BaseModel):
    """Brand template response"""
    id: str
    name: str
    logo_url: Optional[str] = None
    colors: Optional[dict] = None
    fonts: Optional[dict] = None
    is_active: bool

    class Config:
        from_attributes = True
