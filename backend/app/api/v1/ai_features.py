"""Advanced AI features endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.database.models.media import MediaAsset
from app.database.models.transcript import Transcript
from app.database.models.user import User
from app.services.ai_image_service import ai_image_service
from app.services.voice_service import voice_service

router = APIRouter(prefix="/ai-features", tags=["ai-features"])


def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current user"""
    return db.query(User).first()


@router.post("/{media_id}/generate-images")
async def generate_images(
    media_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate AI images for video"""

    try:
        transcript = db.query(Transcript).filter(
            Transcript.media_asset_id == media_id
        ).first()

        if not transcript or not transcript.segments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cần transcript để tạo hình ảnh",
            )

        # Get segments
        import json
        segments = transcript.segments
        if isinstance(segments, str):
            segments = json.loads(segments)

        # Suggest images
        suggestions = ai_image_service.suggest_images_for_transcript(segments)

        return {
            "media_id": media_id,
            "suggestions": suggestions,
            "total": len(suggestions),
            "message": "Đề xuất hình ảnh được tạo",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.post("/{media_id}/generate-narration")
async def generate_narration(
    media_id: str,
    voice: str = "vi-VN-Female-1",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate AI narration from transcript"""

    try:
        transcript = db.query(Transcript).filter(
            Transcript.media_asset_id == media_id
        ).first()

        if not transcript or not transcript.segments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cần transcript để tạo thuyết minh",
            )

        # Get segments
        import json
        segments = transcript.segments
        if isinstance(segments, str):
            segments = json.loads(segments)

        # Generate narration
        narration = await voice_service.generate_narration(segments, voice)

        return {
            "media_id": media_id,
            "narration": narration,
            "voice": voice,
            "message": "Thuyết minh được tạo thành công",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.post("/enhance-audio")
async def enhance_audio(
    audio_url: str,
    enhancements: List[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enhance audio"""

    try:
        if enhancements is None:
            enhancements = ["denoise", "normalize"]

        enhanced = await voice_service.enhance_audio(audio_url, enhancements)

        return {
            "original_url": audio_url,
            "enhanced_url": enhanced['enhanced_url'],
            "enhancements": enhancements,
            "message": "Âm thanh được nâng cao thành công",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )
