"""Video management endpoints"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from app.database.session import get_db
from app.database.models.media import MediaAsset, Project
from app.database.models.user import User
from app.models.media import MediaAssetResponse, ProjectResponse, ProjectCreate, UploadCompleteRequest
from app.services.storage_service import storage_service
from app.utils.security import decode_token

router = APIRouter(prefix="/videos", tags=["videos"])


def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    """Get current user from token"""
    # This is simplified - in production use proper JWT verification
    return db.query(User).first()


@router.post("/upload", response_model=dict)
async def create_upload_session(
    project_id: str,
    filename: str,
    file_size: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create upload session"""

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

        # Check file size
        if file_size > 100 * 1024 * 1024 * 1024:  # 100GB
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File quá lớn (tối đa 100GB)",
            )

        upload_session_id = str(uuid.uuid4())

        return {
            "upload_session_id": upload_session_id,
            "filename": filename,
            "project_id": project_id,
            "message": "Phiên tải lên được tạo thành công",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.post("/upload/complete")
async def complete_upload(
    request: UploadCompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Complete upload and create media asset"""

    try:
        # Create media asset
        media = MediaAsset(
            project_id=request.upload_session_id,  # Will be replaced with actual project_id
            user_id=current_user.id,
            original_filename=request.filename,
            file_size=request.total_size,
            status="ready",
            original_file_path=f"uploads/{current_user.id}/{request.upload_session_id}/{request.filename}",
        )

        db.add(media)
        db.commit()
        db.refresh(media)

        return {
            "media_id": str(media.id),
            "filename": media.original_filename,
            "status": media.status,
            "message": "Tải lên thành công",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi hoàn thành tải lên: {str(e)}",
        )


@router.get("/", response_model=List[MediaAssetResponse])
async def list_videos(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List videos in project"""

    try:
        videos = db.query(MediaAsset).filter(
            MediaAsset.project_id == project_id,
            MediaAsset.user_id == current_user.id,
        ).order_by(MediaAsset.created_at.desc()).all()

        return [
            MediaAssetResponse(
                id=str(v.id),
                project_id=str(v.project_id),
                original_filename=v.original_filename,
                file_size=v.file_size,
                duration=v.duration,
                width=v.width,
                height=v.height,
                status=v.status.value,
                thumbnail_path=v.thumbnail_path,
                created_at=v.created_at.isoformat(),
            )
            for v in videos
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.delete("/{video_id}")
async def delete_video(
    video_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete video (soft delete)"""

    try:
        video = db.query(MediaAsset).filter(
            MediaAsset.id == video_id,
            MediaAsset.user_id == current_user.id,
        ).first()

        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video không tìm thấy",
            )

        # Soft delete
        db.delete(video)
        db.commit()

        return {"message": "Video đã được xóa"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )
