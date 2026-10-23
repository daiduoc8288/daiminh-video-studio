"""Media Asset ORM Model"""

import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin
import enum


class MediaStatusEnum(str, enum.Enum):
    """Media upload status"""
    UPLOADING = "uploading"
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"


class MediaAsset(Base, TimestampMixin):
    """Media asset model (video files)"""

    __tablename__ = "media_assets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # File info
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)  # Bytes

    # Video metadata
    duration = Column(Float, nullable=True)  # Seconds
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    fps = Column(Float, nullable=True)
    codec = Column(String(50), nullable=True)

    # Storage paths
    original_file_path = Column(String(500), nullable=False)
    proxy_file_path = Column(String(500), nullable=True)
    thumbnail_path = Column(String(500), nullable=True)

    # Status
    status = Column(
        SQLEnum(MediaStatusEnum),
        default=MediaStatusEnum.UPLOADING,
        nullable=False,
        index=True,
    )
    error_message = Column(Text, nullable=True)

    # Additional metadata
    metadata = Column(JSON, nullable=True)
    upload_session_id = Column(String(100), nullable=True)  # For resume

    def __repr__(self):
        return f"<MediaAsset {self.original_filename}>"


class Project(Base, TimestampMixin):
    """Project model"""

    __tablename__ = "projects"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(
        String(50),
        default="draft",
        nullable=False,
    )

    # Relationships
    media_assets = relationship("MediaAsset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.title}>"
