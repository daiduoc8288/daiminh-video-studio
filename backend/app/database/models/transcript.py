"""Transcript ORM Model"""

import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum as SQLEnum, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base, TimestampMixin
import enum


class TranscriptStatusEnum(str, enum.Enum):
    """Transcript processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class Transcript(Base, TimestampMixin):
    """Transcript model - stores transcribed text with timestamps"""

    __tablename__ = "transcripts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    media_asset_id = Column(
        UUID(as_uuid=True),
        ForeignKey("media_assets.id"),
        nullable=False,
        index=True,
    )

    # Content
    content = Column(Text, nullable=True)  # Full transcript
    segments = Column(JSON, nullable=True)  # Array of {start_time, end_time, text}

    # Metadata
    language = Column(String(10), default="vi", nullable=False)
    duration = Column(Float, nullable=True)
    word_count = Column(Integer, nullable=True)

    status = Column(
        SQLEnum(TranscriptStatusEnum),
        default=TranscriptStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    error_message = Column(Text, nullable=True)

    # Processing details
    provider = Column(String(50), nullable=True)  # whisper, google, azure, etc
    confidence = Column(Float, nullable=True)  # Average confidence score

    def __repr__(self):
        return f"<Transcript {self.media_asset_id}>"
