"""Video analysis endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app.database.session import get_db
from app.database.models.media import MediaAsset
from app.database.models.transcript import Transcript
from app.database.models.analysis import VideoAnalysis, AnalysisStatusEnum
from app.database.models.user import User
from app.services.transcription_service import transcription_service
from app.models.transcript import SilenceSegment

router = APIRouter(prefix="/analysis", tags=["analysis"])


def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current user"""
    return db.query(User).first()


@router.post("/{media_id}/analyze")
async def analyze_video(
    media_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Analyze video for silence, highlights, etc"""

    try:
        media = db.query(MediaAsset).filter(MediaAsset.id == media_id).first()

        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video không tìm thấy",
            )

        # Check if analysis already exists
        existing = db.query(VideoAnalysis).filter(
            VideoAnalysis.media_asset_id == media_id
        ).first()

        if existing and existing.status == AnalysisStatusEnum.COMPLETED:
            return {
                "analysis_id": str(existing.id),
                "status": "completed",
                "message": "Phân tích video đã tồn tại",
            }

        # Get or create transcript first
        transcript = db.query(Transcript).filter(
            Transcript.media_asset_id == media_id
        ).first()

        if not transcript or not transcript.segments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cần có transcript trước khi phân tích. Hãy tạo transcript trước.",
            )

        # Create or update analysis
        if existing:
            analysis = existing
        else:
            analysis = VideoAnalysis(
                media_asset_id=media_id,
                status=AnalysisStatusEnum.PROCESSING,
            )
            db.add(analysis)
            db.commit()

        # Perform analysis
        _perform_analysis(analysis, transcript, db)

        return {
            "analysis_id": str(analysis.id),
            "status": "completed",
            "message": "Phân tích video hoàn thành",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.get("/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    """Get analysis results"""

    try:
        analysis = db.query(VideoAnalysis).filter(
            VideoAnalysis.id == analysis_id
        ).first()

        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phân tích không tìm thấy",
            )

        return {
            "analysis_id": str(analysis.id),
            "media_id": str(analysis.media_asset_id),
            "status": analysis.status.value,
            "silence_segments": analysis.silence_segments,
            "highlights": analysis.highlights,
            "suggested_cuts": analysis.suggested_cuts,
            "suggested_structure": analysis.suggested_structure,
            "confidence_score": analysis.confidence_score,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


def _perform_analysis(analysis: VideoAnalysis, transcript: Transcript, db: Session) -> None:
    """Perform actual analysis"""

    try:
        import json

        # Parse segments
        segments = transcript.segments
        if isinstance(segments, str):
            segments = json.loads(segments)

        # Detect silence
        silence_segments = transcription_service.detect_silence(
            segments,
            min_silence_duration=2.0,
        )

        # Find highlights (longer speaking segments)
        highlights = []
        for seg in segments:
            duration = seg.get("end_time", 0) - seg.get("start_time", 0)
            if duration > 3.0:  # More than 3 seconds
                highlights.append({
                    "start_time": seg.get("start_time"),
                    "end_time": seg.get("end_time"),
                    "text": seg.get("text", "")[:100],
                })

        # Suggest cuts (silence segments)
        suggested_cuts = silence_segments

        # Suggested structure
        suggested_structure = {
            "intro_duration": 3.0,
            "main_content_start": 3.0,
            "outro_duration": 3.0,
            "total_video_duration": transcript.duration or 0,
        }

        # Update analysis
        analysis.silence_segments = silence_segments
        analysis.highlights = highlights
        analysis.suggested_cuts = suggested_cuts
        analysis.suggested_structure = suggested_structure
        analysis.confidence_score = 0.95
        analysis.status = AnalysisStatusEnum.COMPLETED

        db.commit()

    except Exception as e:
        analysis.status = AnalysisStatusEnum.ERROR
        analysis.error_message = str(e)
        db.commit()
