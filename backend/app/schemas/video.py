from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None

class VideoCreate(VideoBase):
    pass

class VideoResponse(VideoBase):
    id: int
    user_id: int
    file_url: str
    duration: Optional[float]
    status: str
    transcript: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
