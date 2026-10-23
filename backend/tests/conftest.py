"""Pytest configuration and fixtures"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from app.main import create_app
from fastapi.testclient import TestClient


# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client"""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app = create_app()

    from app.database.session import get_db

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture
def demo_user_data():
    """Demo user data for testing"""
    return {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
    }
