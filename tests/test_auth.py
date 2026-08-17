"""
Authentication endpoint tests for FastAPI Microservice Starter.
Covers JWT token generation, validation, refresh, and revocation.
"""
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from datetime import timedelta

from app.main import app
from app.core.security import create_access_token, verify_token
from app.core.config import settings


@pytest.fixture
def client():
    """Sync test client for simple endpoint tests."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def valid_token():
    """Generate a valid JWT token for testing."""
    return create_access_token(
        data={"sub": "testuser@example.com"},
        expires_delta=timedelta(minutes=30)
    )


@pytest.fixture
def expired_token():
    """Generate an expired JWT token."""
    return create_access_token(
        data={"sub": "testuser@example.com"},
        expires_delta=timedelta(seconds=-1)
    )


class TestAuthLogin:
    """Tests for the /auth/login endpoint."""

    def test_login_success(self, client):
        """Valid credentials should return access and refresh tokens."""
        response = client.post("/api/v1/auth/login", json={
            "email": "admin@example.com",
            "password": "secret123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Wrong password should return 401 Unauthorized."""
        response = client.post("/api/v1/auth/login", json={
            "email": "admin@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"

    def test_login_nonexistent_user(self, client):
        """Non-existent user should return 401."""
        response = client.post("/api/v1/auth/login", json={
            "email": "ghost@example.com",
            "password": "password"
        })
        assert response.status_code == 401

    def test_login_missing_fields(self, client):
        """Missing required fields should return 422 Unprocessable Entity."""
        response = client.post("/api/v1/auth/login", json={"email": "only@email.com"})
        assert response.status_code == 422

    def test_login_invalid_email_format(self, client):
        """Invalid email format should return 422."""
        response = client.post("/api/v1/auth/login", json={
            "email": "not-an-email",
            "password": "password"
        })
        assert response.status_code == 422


class TestTokenValidation:
    """Tests for JWT token structure and validation."""

    def test_valid_token_verified(self, valid_token):
        """Valid token should decode without errors."""
        payload = verify_token(valid_token)
        assert payload is not None
        assert payload.get("sub") == "testuser@example.com"

    def test_expired_token_raises(self, expired_token):
        """Expired token should raise an exception."""
        with pytest.raises(Exception):
            verify_token(expired_token)

    def test_tampered_token_rejected(self):
        """Tampered token signature should be rejected."""
        fake_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJoYWNrZXIifQ.invalid_sig"
        with pytest.raises(Exception):
            verify_token(fake_token)

    def test_access_token_used_as_refresh_rejected(self, valid_token, client):
        """Access token should not be accepted as a refresh token."""
        response = client.post("/api/v1/auth/refresh", json={"refresh_token": valid_token})
        assert response.status_code in [400, 401]


class TestProtectedEndpoints:
    """Tests for endpoints that require authentication."""

    def test_protected_route_no_token(self, client):
        """Request without token should return 401."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

    def test_protected_route_valid_token(self, client, valid_token):
        """Valid token in Authorization header should grant access."""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response.status_code in [200, 404]  # 404 if user not seeded

    def test_protected_route_expired_token(self, client, expired_token):
        """Expired token should be rejected with 401."""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401

    def test_protected_route_malformed_header(self, client):
        """Malformed Authorization header should return 401."""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Token badformat"}
        )
        assert response.status_code == 401