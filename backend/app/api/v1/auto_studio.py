"""Auto Studio endpoints - AI automatic video generation"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from app.database.session import get_db
from app.database.models.media import MediaAsset
from app.database.models.transcript import Transcript
from app.database.models.analysis import VideoAnalysis
from app.database.models.user import User
from app.services.auto_studio_service import auto_studio_service

router = APIRouter(prefix="/auto-studio", tags=["auto-studio"])


def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current user"""
    return db.query(User).first()


@router.post("/{media_id}/generate")
async def generate_auto_draft(
    media_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate AI auto-draft for video"""

    try:
        # Get media asset
        media = db.query(MediaAsset).filter(MediaAsset.id == media_id).first()

        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video không tìm thấy",
            )

        # Get transcript
        transcript = db.query(Transcript).filter(
            Transcript.media_asset_id == media_id
        ).first()

        if not transcript or not transcript.segments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cần có transcript trước khi tạo auto draft",
            )

        # Get analysis
        analysis = db.query(VideoAnalysis).filter(
            VideoAnalysis.media_asset_id == media_id
        ).first()

        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cần phân tích video trước khi tạo auto draft",
            )

        # Parse segments
        segments = transcript.segments
        if isinstance(segments, str):
            segments = json.loads(segments)

        # Parse silence segments
        silence_segments = analysis.silence_segments or []
        if isinstance(silence_segments, str):
            silence_segments = json.loads(silence_segments)

        # Parse highlights
        highlights = analysis.highlights or []
        if isinstance(highlights, str):
            highlights = json.loads(highlights)

        # Analyze content
        content_analysis = auto_studio_service.analyze_content(
            segments,
            transcript.content or ""
        )

        # Suggest structure
        structure = auto_studio_service.suggest_structure(
            transcript.duration or 0,
            highlights,
            silence_segments,
        )

        # Generate auto cuts
        auto_cuts = auto_studio_service.generate_auto_cuts(
            segments,
            silence_segments,
        )

        # Generate draft timeline
        draft_timeline = auto_studio_service.generate_draft_timeline(
            media_id,
            segments,
            highlights,
            structure,
            silence_segments,
        )

        return {
            "status": "generated",
            "media_id": media_id,
            "analysis": content_analysis,
            "structure": structure,
            "auto_cuts": auto_cuts,
            "draft_timeline": draft_timeline,
            "message": "Bản nháp tự động được tạo thành công",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.post("/{media_id}/apply-draft")
async def apply_auto_draft(
    media_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Apply auto-generated draft to timeline"""

    try:
        # This would integrate with the timeline editor
        return {
            "status": "applied",
            "media_id": media_id,
            "message": "Bản nháp được áp dụng vào timeline",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )
