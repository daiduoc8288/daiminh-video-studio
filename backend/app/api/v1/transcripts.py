"""Transcription endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app.database.session import get_db
from app.database.models.transcript import Transcript, TranscriptStatusEnum
from app.database.models.media import MediaAsset
from app.database.models.user import User
from app.models.transcript import TranscriptResponse, TranscriptUpdateRequest
from app.services.transcription_service import transcription_service

router = APIRouter(prefix="/transcripts", tags=["transcripts"])


def get_current_user(db: Session = Depends(get_db)) -> User:
    """Get current user"""
    return db.query(User).first()


@router.post("/{media_id}/generate")
async def generate_transcript(
    media_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate transcript from video"""

    try:
        media = db.query(MediaAsset).filter(MediaAsset.id == media_id).first()

        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video không tìm thấy",
            )

        # Check if transcript already exists
        existing = db.query(Transcript).filter(
            Transcript.media_asset_id == media_id
        ).first()

        if existing:
            if existing.status == TranscriptStatusEnum.COMPLETED:
                return {
                    "transcript_id": str(existing.id),
                    "status": "completed",
                    "message": "Transcript đã tồn tại",
                }

        # Create transcript record
        transcript = Transcript(
            media_asset_id=media_id,
            status=TranscriptStatusEnum.PROCESSING,
            provider="whisper",
        )

        db.add(transcript)
        db.commit()
        db.refresh(transcript)

        # Queue transcription job (would use Celery/RQ in production)
        # For now, just return pending status
        return {
            "transcript_id": str(transcript.id),
            "status": "processing",
            "message": "Đang tạo transcript...",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.get("/{transcript_id}", response_model=TranscriptResponse)
async def get_transcript(
    transcript_id: str,
    db: Session = Depends(get_db),
):
    """Get transcript"""

    try:
        transcript = db.query(Transcript).filter(
            Transcript.id == transcript_id
        ).first()

        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transcript không tìm thấy",
            )

        # Parse segments if stored as JSON
        segments = None
        if transcript.segments:
            import json
            if isinstance(transcript.segments, str):
                segments = json.loads(transcript.segments)
            else:
                segments = transcript.segments

        return TranscriptResponse(
            id=str(transcript.id),
            media_asset_id=str(transcript.media_asset_id),
            content=transcript.content,
            segments=segments,
            language=transcript.language,
            duration=transcript.duration,
            status=transcript.status.value,
            created_at=transcript.created_at.isoformat(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.put("/{transcript_id}")
async def update_transcript(
    transcript_id: str,
    request: TranscriptUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update transcript"""

    try:
        transcript = db.query(Transcript).filter(
            Transcript.id == transcript_id
        ).first()

        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transcript không tìm thấy",
            )

        if request.content:
            transcript.content = request.content

        if request.segments:
            import json
            transcript.segments = json.dumps(request.segments)

        db.commit()
        db.refresh(transcript)

        return {
            "transcript_id": str(transcript.id),
            "status": "updated",
            "message": "Transcript đã cập nhật",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


@router.post("/{transcript_id}/export")
async def export_transcript(
    transcript_id: str,
    format: str = "srt",
    db: Session = Depends(get_db),
):
    """Export transcript to SRT or other format"""

    try:
        transcript = db.query(Transcript).filter(
            Transcript.id == transcript_id
        ).first()

        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transcript không tìm thấy",
            )

        if format == "srt":
            # Generate SRT format
            srt_content = _generate_srt(transcript)
            return {
                "format": "srt",
                "content": srt_content,
                "filename": f"transcript_{transcript_id}.srt",
            }

        return {
            "message": "Format không hỗ trợ",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi: {str(e)}",
        )


def _generate_srt(transcript: Transcript) -> str:
    """Generate SRT format from transcript"""

    srt_lines = []
    index = 1

    if not transcript.segments:
        return ""

    segments = transcript.segments
    if isinstance(segments, str):
        import json
        segments = json.loads(segments)

    for seg in segments:
        start_time = _seconds_to_srt_time(seg.get("start_time", 0))
        end_time = _seconds_to_srt_time(seg.get("end_time", 0))
        text = seg.get("text", "")

        srt_lines.append(str(index))
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
        srt_lines.append("")

        index += 1

    return "\n".join(srt_lines)


def _seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
