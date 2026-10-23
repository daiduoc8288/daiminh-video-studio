"""Timeline & Project ORM Models"""

import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base, TimestampMixin


class Timeline(Base, TimestampMixin):
    """Video timeline/project editing"""

    __tablename__ = "timelines"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Timeline dimensions
    duration = Column(Float, nullable=False, default=0.0)  # Total duration in seconds
    fps = Column(Integer, nullable=False, default=30)
    width = Column(Integer, nullable=False, default=1920)
    height = Column(Integer, nullable=False, default=1080)

    # Timeline structure (array of tracks)
    data = Column(JSON, nullable=True)  # Complete timeline structure
    # {
    #   "tracks": [
    #     {
    #       "id": "track-v1",
    #       "type": "video",
    #       "clips": [...]
    #     },
    #     {
    #       "id": "track-a1",
    #       "type": "audio",
    #       "clips": [...]
    #     }
    #   ]
    # }

    # Versioning
    version = Column(Integer, nullable=False, default=1, index=True)
    is_current = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Timeline {self.project_id} v{self.version}>"


class TimelineVersion(Base, TimestampMixin):
    """Timeline version history"""

    __tablename__ = "timeline_versions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    timeline_id = Column(UUID(as_uuid=True), ForeignKey("timelines.id"), nullable=False, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    version_number = Column(Integer, nullable=False)
    data = Column(JSON, nullable=True)  # Snapshot of timeline data

    # Metadata
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(String(500), nullable=True)
    is_autosave = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<TimelineVersion {self.timeline_id} v{self.version_number}>"


class TimelineAction(Base, TimestampMixin):
    """Timeline edit action history (for undo/redo)"""

    __tablename__ = "timeline_actions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    timeline_id = Column(UUID(as_uuid=True), ForeignKey("timelines.id"), nullable=False, index=True)

    action_type = Column(String(50), nullable=False)  # add_clip, delete_clip, move_clip, etc
    action_data = Column(JSON, nullable=False)  # State before/after

    # Stack for undo/redo
    action_order = Column(Integer, nullable=False)  # Order in undo stack
    is_undo = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<TimelineAction {self.action_type}>"
