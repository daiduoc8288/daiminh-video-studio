"""Timeline schemas"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class TimelineClip(BaseModel):
    """Timeline clip"""
    id: str
    asset_id: str
    start: float  # Start time in timeline
    duration: float
    offset: float  # Offset in source file
    effects: Optional[List[Dict[str, Any]]] = None


class TimelineTrack(BaseModel):
    """Timeline track"""
    id: str
    type: str  # video, audio, text, effects
    clips: List[TimelineClip]


class TimelineData(BaseModel):
    """Complete timeline structure"""
    duration: float
    fps: int
    width: int
    height: int
    tracks: List[TimelineTrack]


class TimelineResponse(BaseModel):
    """Timeline response"""
    id: str
    project_id: str
    duration: float
    fps: int
    width: int
    height: int
    version: int
    data: Optional[TimelineData] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class TimelineSaveRequest(BaseModel):
    """Save timeline"""
    data: TimelineData
    description: Optional[str] = None


class TimelineVersionResponse(BaseModel):
    """Timeline version"""
    id: str
    version_number: int
    description: Optional[str] = None
    is_autosave: bool
    created_at: str

    class Config:
        from_attributes = True


class ClipEditRequest(BaseModel):
    """Edit clip"""
    track_id: str
    clip_id: str
    start: Optional[float] = None
    duration: Optional[float] = None
    offset: Optional[float] = None


class AddClipRequest(BaseModel):
    """Add clip to timeline"""
    track_id: str
    asset_id: str
    start: float
    duration: float
    offset: float


class DeleteClipRequest(BaseModel):
    """Delete clip"""
    track_id: str
    clip_id: str
