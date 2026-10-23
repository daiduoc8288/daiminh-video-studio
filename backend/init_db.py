"""
Initialize database with migrations and seed data
Run: python init_db.py
"""

import sys
import os
from sqlalchemy import text
from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.database.models import User
from app.utils.security import hash_password
from app.database.models.user import RoleEnum

def init_database():
    """Create all tables"""
    print("Creating database tables...")

    try:
        # Create enum type
        with engine.connect() as conn:
            conn.execute(text("CREATE TYPE roleenum AS ENUM ('admin', 'editor', 'reviewer')"))
            conn.commit()
    except Exception as e:
        print(f"Enum type might already exist: {e}")

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def seed_demo_users():
    """Add demo users"""
    db = SessionLocal()

    try:
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == "test@example.com").first()

        if demo_user:
            print("✓ Demo users already exist")
            return

        # Create demo users
        demo_users = [
            User(
                email="admin@example.com",
                full_name="Admin User",
                password_hash=hash_password("admin123"),
                role=RoleEnum.ADMIN,
            ),
            User(
                email="test@example.com",
                full_name="Test Editor",
                password_hash=hash_password("password123"),
                role=RoleEnum.EDITOR,
            ),
            User(
                email="reviewer@example.com",
                full_name="Test Reviewer",
                password_hash=hash_password("password123"),
                role=RoleEnum.REVIEWER,
            ),
        ]

        db.add_all(demo_users)
        db.commit()

        print("✓ Demo users created:")
        print("  - test@example.com / password123 (EDITOR)")
        print("  - admin@example.com / admin123 (ADMIN)")
        print("  - reviewer@example.com / password123 (REVIEWER)")

    except Exception as e:
        db.rollback()
        print(f"Error seeding users: {e}")
    finally:
        db.close()


def main():
    """Initialize database"""
    print("\n=== DaiMinh Video Studio - Database Initialization ===\n")

    try:
        init_database()
        seed_demo_users()
        print("\n✓ Database initialization complete!")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
