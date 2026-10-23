"""Pro Video Editor endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
import uuid

from app.database.session import get_db
from app.database.models.timeline import Timeline, TimelineVersion, TimelineAction
from app.database.models.project import Project
from app.database.models.user import User
from app.models.timeline import (
    TimelineResponse,
    TimelineSaveRequest,
    TimelineVersionResponse,
    AddClipRequest,
    ClipEditRequest,
    DeleteClipRequest,
)

router = APIRouter(prefix="/editor", tags=["editor"])


def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current user"""
    return db.query(User).first()


@router.post("/{project_id}/timeline/init", response_model=TimelineResponse)
async def init_timeline(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Initialize timeline for project"""

    try:
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == current_user.id,
        ).first()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dự án không tìm thấy",
            )

        # Check if timeline exists
        existing = db.query(Timeline).filter(
            Timeline.project_id == project_id,
            Timeline.is_current == True,
        ).first()

        if existing:
            return TimelineResponse(
                id=str(existing.id),
                project_id=str(existing.project_id),
                duration=existing.duration,
                fps=existing.fps,
                width=existing.width,
                height=existing.height,
                version=existing.version,
                created_at=existing.created_at.isoformat(),
                updated_at=existing.updated_at.isoformat(),
            )

        # Create new timeline
        timeline = Timeline(
            project_id=project_id,
            user_id=current_user.id,
            duration=0.0,
            fps=30,
            width=1920,
            height=1080,
            data={
                "tracks": [
                    {"id": "video-1", "type": "video", "clips": []},
                    {"id": "audio-1", "type": "audio", "clips": []},
                ],
            },
        )

        db.add(timeline)
        db.commit()
        db.refresh(timeline)

        return TimelineResponse(
            id=str(timeline.id),
            project_id=str(timeline.project_id),
            duration=timeline.duration,
            fps=timeline.fps,
            width=timeline.width,
            height=timeline.height,
            version=timeline.version,
            created_at=timeline.created_at.isoformat(),
            updated_at=timeline.updated_at.isoformat(),
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.get("/{project_id}/timeline", response_model=TimelineResponse)
async def get_timeline(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get timeline"""

    try:
        timeline = db.query(Timeline).filter(
            Timeline.project_id == project_id,
            Timeline.is_current == True,
        ).first()

        if not timeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline không tìm thấy",
            )

        return TimelineResponse(
            id=str(timeline.id),
            project_id=str(timeline.project_id),
            duration=timeline.duration,
            fps=timeline.fps,
            width=timeline.width,
            height=timeline.height,
            version=timeline.version,
            data=timeline.data,
            created_at=timeline.created_at.isoformat(),
            updated_at=timeline.updated_at.isoformat(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.post("/{project_id}/timeline/save")
async def save_timeline(
    project_id: str,
    request: TimelineSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save timeline changes"""

    try:
        timeline = db.query(Timeline).filter(
            Timeline.project_id == project_id,
            Timeline.is_current == True,
        ).first()

        if not timeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline không tìm thấy",
            )

        # Convert request data to dict if needed
        timeline_data = request.data.dict() if hasattr(request.data, 'dict') else request.data

        # Update timeline
        timeline.data = timeline_data
        timeline.duration = request.data.duration
        timeline.fps = request.data.fps
        timeline.width = request.data.width
        timeline.height = request.data.height

        db.commit()
        db.refresh(timeline)

        # Create version for autosave
        version = TimelineVersion(
            timeline_id=timeline.id,
            project_id=project_id,
            version_number=timeline.version,
            data=timeline_data,
            created_by=current_user.id,
            description=request.description,
            is_autosave=not request.description,  # If no description, it's autosave
        )
        db.add(version)
        db.commit()

        return {
            "status": "saved",
            "version": timeline.version,
            "duration": timeline.duration,
            "message": "Timeline đã lưu thành công",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.post("/{project_id}/timeline/add-clip")
async def add_clip(
    project_id: str,
    request: AddClipRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add clip to timeline"""

    try:
        timeline = db.query(Timeline).filter(
            Timeline.project_id == project_id,
            Timeline.is_current == True,
        ).first()

        if not timeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline không tìm thấy",
            )

        # Get timeline data
        timeline_data = timeline.data or {"tracks": []}

        # Find track
        track = next(
            (t for t in timeline_data.get("tracks", []) if t["id"] == request.track_id),
            None
        )

        if not track:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Track không tìm thấy",
            )

        # Add clip
        clip = {
            "id": str(uuid.uuid4()),
            "asset_id": request.asset_id,
            "start": request.start,
            "duration": request.duration,
            "offset": request.offset,
            "effects": [],
        }

        track["clips"].append(clip)

        # Update timeline
        timeline.data = timeline_data
        timeline.duration = max(timeline.duration, request.start + request.duration)

        db.commit()

        return {
            "clip_id": clip["id"],
            "status": "added",
            "message": "Clip được thêm vào timeline",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.put("/{project_id}/timeline/clip/{clip_id}")
async def edit_clip(
    project_id: str,
    clip_id: str,
    request: ClipEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Edit clip in timeline"""

    try:
        timeline = db.query(Timeline).filter(
            Timeline.project_id == project_id,
            Timeline.is_current == True,
        ).first()

        if not timeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline không tìm thấy",
            )

        timeline_data = timeline.data or {"tracks": []}

        # Find and update clip
        for track in timeline_data.get("tracks", []):
            if track["id"] == request.track_id:
                for clip in track.get("clips", []):
                    if clip["id"] == clip_id:
                        if request.start is not None:
                            clip["start"] = request.start
                        if request.duration is not None:
                            clip["duration"] = request.duration
                        if request.offset is not None:
                            clip["offset"] = request.offset

                        timeline.data = timeline_data
                        db.commit()

                        return {
                            "clip_id": clip_id,
                            "status": "updated",
                            "message": "Clip được cập nhật",
                        }

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clip không tìm thấy",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.delete("/{project_id}/timeline/clip/{clip_id}")
async def delete_clip(
    project_id: str,
    clip_id: str,
    request: DeleteClipRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete clip from timeline"""

    try:
        timeline = db.query(Timeline).filter(
            Timeline.project_id == project_id,
            Timeline.is_current == True,
        ).first()

        if not timeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline không tìm thấy",
            )

        timeline_data = timeline.data or {"tracks": []}

        # Find and delete clip
        for track in timeline_data.get("tracks", []):
            if track["id"] == request.track_id:
                track["clips"] = [c for c in track.get("clips", []) if c["id"] != clip_id]

        timeline.data = timeline_data
        db.commit()

        return {
            "clip_id": clip_id,
            "status": "deleted",
            "message": "Clip đã bị xóa",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.get("/{project_id}/timeline/versions")
async def get_timeline_versions(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get timeline version history"""

    try:
        timeline = db.query(Timeline).filter(
            Timeline.project_id == project_id,
        ).first()

        if not timeline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline không tìm thấy",
            )

        versions = db.query(TimelineVersion).filter(
            TimelineVersion.timeline_id == timeline.id,
        ).order_by(TimelineVersion.created_at.desc()).all()

        return {
            "versions": [
                {
                    "id": str(v.id),
                    "version": v.version_number,
                    "description": v.description,
                    "is_autosave": v.is_autosave,
                    "created_at": v.created_at.isoformat(),
                }
                for v in versions
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )
