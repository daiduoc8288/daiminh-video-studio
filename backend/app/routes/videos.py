from fastapi import APIRouter, File, UploadFile, HTTPException
from app.schemas.video import VideoResponse, VideoCreate, VideoUpdate
from typing import List

router = APIRouter()

# Temporary video storage
videos_db = {}

@router.post("/upload", response_model=VideoResponse)
async def upload_video(file: UploadFile = File(...), title: str = "Untitled"):
    """Upload video file"""
    if not file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Invalid video format")
    
    video_id = len(videos_db) + 1
    videos_db[video_id] = {
        "id": video_id,
        "user_id": 1,
        "title": title,
        "description": None,
        "file_url": f"/videos/files/{file.filename}",
        "duration": None,
        "status": "processing",
        "transcript": None
    }
    
    return videos_db[video_id]

@router.get("/", response_model=List[VideoResponse])
async def list_videos():
    """Get all user videos"""
    return list(videos_db.values())

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int):
    """Get video details"""
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos_db[video_id]

@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(video_id: int, update: VideoUpdate):
    """Update video metadata"""
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video = videos_db[video_id]
    if update.title:
        video["title"] = update.title
    if update.description:
        video["description"] = update.description
    if update.status:
        video["status"] = update.status
    
    return video

@router.delete("/{video_id}")
async def delete_video(video_id: int):
    """Delete video"""
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    del videos_db[video_id]
    return {"message": "Video deleted"}
