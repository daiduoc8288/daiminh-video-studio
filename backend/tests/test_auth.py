"""Authentication endpoint tests"""

import pytest
from app.models.user import UserCreate
from app.services.auth_service import AuthService


class TestAuthService:
    """Test authentication service"""

    def test_create_user(self, db, demo_user_data):
        """Test user creation"""
        user_create = UserCreate(**demo_user_data)
        user = AuthService.create_user(db, user_create)

        assert user.email == demo_user_data["email"]
        assert user.full_name == demo_user_data["full_name"]
        assert user.password_hash != demo_user_data["password"]
        assert user.id is not None

    def test_authenticate_user_success(self, db, demo_user_data):
        """Test successful user authentication"""
        # Create user
        user_create = UserCreate(**demo_user_data)
        AuthService.create_user(db, user_create)

        # Authenticate
        from app.models.user import LoginRequest

        login_request = LoginRequest(
            email=demo_user_data["email"],
            password=demo_user_data["password"],
        )
        user = AuthService.authenticate_user(db, login_request)

        assert user is not None
        assert user.email == demo_user_data["email"]

    def test_authenticate_user_wrong_password(self, db, demo_user_data):
        """Test authentication with wrong password"""
        # Create user
        user_create = UserCreate(**demo_user_data)
        AuthService.create_user(db, user_create)

        # Authenticate with wrong password
        from app.models.user import LoginRequest

        login_request = LoginRequest(
            email=demo_user_data["email"],
            password="wrong_password",
        )
        user = AuthService.authenticate_user(db, login_request)

        assert user is None

    def test_authenticate_user_not_found(self, db):
        """Test authentication with non-existent user"""
        from app.models.user import LoginRequest

        login_request = LoginRequest(
            email="nonexistent@example.com",
            password="password123",
        )
        user = AuthService.authenticate_user(db, login_request)

        assert user is None

    def test_generate_tokens(self):
        """Test token generation"""
        user_id = "test-user-id"
        tokens = AuthService.generate_tokens(user_id)

        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert isinstance(tokens["access_token"], str)
        assert isinstance(tokens["refresh_token"], str)


class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_login_success(self, client, db, demo_user_data):
        """Test successful login"""
        # Create user
        user_create = UserCreate(**demo_user_data)
        AuthService.create_user(db, user_create)

        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": demo_user_data["email"],
                "password": demo_user_data["password"],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data
        assert data["user"]["email"] == demo_user_data["email"]
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, db, demo_user_data):
        """Test login with wrong password"""
        # Create user
        user_create = UserCreate(**demo_user_data)
        AuthService.create_user(db, user_create)

        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": demo_user_data["email"],
                "password": "wrong_password",
            },
        )

        assert response.status_code == 401
        assert "detail" in response.json()

    def test_login_user_not_found(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 401

    def test_logout(self, client):
        """Test logout endpoint"""
        response = client.post("/api/v1/auth/logout")

        assert response.status_code == 200
        assert response.json()["message"] == "Đã đăng xuất thành công"
