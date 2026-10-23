"""User ORM Model"""

import uuid
from sqlalchemy import Column, String, Enum as SQLEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base, TimestampMixin
import enum


class RoleEnum(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    EDITOR = "editor"
    REVIEWER = "reviewer"


class User(Base, TimestampMixin):
    """User model"""

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(
        SQLEnum(RoleEnum),
        default=RoleEnum.EDITOR,
        nullable=False,
    )
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
