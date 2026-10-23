"""Analysis & AI Results ORM Models"""

import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Enum as SQLEnum, Text, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base, TimestampMixin
import enum


class AnalysisStatusEnum(str, enum.Enum):
    """Analysis processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class VideoAnalysis(Base, TimestampMixin):
    """Video analysis results (silence detection, scenes, etc)"""

    __tablename__ = "video_analyses"

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

    # Analysis results
    silence_segments = Column(JSON, nullable=True)  # Array of {start, end, duration}
    speech_segments = Column(JSON, nullable=True)
    scene_changes = Column(JSON, nullable=True)  # Scene transition points
    key_phrases = Column(JSON, nullable=True)  # Important phrases/keywords
    highlights = Column(JSON, nullable=True)  # Suggested highlight segments

    # Recommendations
    suggested_cuts = Column(JSON, nullable=True)  # Suggested segments to cut
    suggested_structure = Column(JSON, nullable=True)  # Intro, body, outro suggestions

    # Status
    status = Column(
        SQLEnum(AnalysisStatusEnum),
        default=AnalysisStatusEnum.PENDING,
        nullable=False,
        index=True,
    )
    error_message = Column(Text, nullable=True)

    # Quality metrics
    confidence_score = Column(Float, nullable=True)

    def __repr__(self):
        return f"<VideoAnalysis {self.media_asset_id}>"


class BrandTemplate(Base, TimestampMixin):
    """Brand template for styling videos"""

    __tablename__ = "brand_templates"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Brand assets
    logo_url = Column(String(500), nullable=True)
    intro_video_path = Column(String(500), nullable=True)
    outro_video_path = Column(String(500), nullable=True)

    # Brand colors & fonts
    colors = Column(JSON, nullable=True)  # {primary, secondary, accent, text, background}
    fonts = Column(JSON, nullable=True)  # {primary, secondary, sizes}

    # Templates
    call_to_action = Column(JSON, nullable=True)  # CTA template
    subtitle_template = Column(JSON, nullable=True)  # Subtitle styling

    is_active = Column(Integer, default=1, nullable=False)

    def __repr__(self):
        return f"<BrandTemplate {self.name}>"
