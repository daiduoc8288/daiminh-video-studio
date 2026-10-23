"""Authentication service"""

from sqlalchemy.orm import Session
from app.database.models.user import User
from app.models.user import UserCreate, LoginRequest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from datetime import datetime


class AuthService:
    """Authentication business logic"""

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        db_user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            password_hash=hash_password(user_create.password),
            role=user_create.role,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, login_request: LoginRequest) -> User | None:
        """Authenticate user by email and password"""
        user = db.query(User).filter(User.email == login_request.email).first()

        if not user:
            return None

        if not verify_password(login_request.password, user.password_hash):
            return None

        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User | None:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def generate_tokens(user_id: str) -> dict:
        """Generate access and refresh tokens"""
        return {
            "access_token": create_access_token({"sub": str(user_id)}),
            "refresh_token": create_refresh_token({"sub": str(user_id)}),
        }
