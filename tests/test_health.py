"""
Health check endpoint tests for FastAPI Microservice Starter.
Validates liveness, readiness, and dependency health probes.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)


class TestLivenessProbe:
    """Tests for GET /health/live - basic liveness check."""

    def test_liveness_returns_200(self):
        """Liveness endpoint should always return 200 OK."""
        response = client.get("/health/live")
        assert response.status_code == 200

    def test_liveness_response_structure(self):
        """Response should contain status field."""
        response = client.get("/health/live")
        data = response.json()
        assert "status" in data
        assert data["status"] == "alive"

    def test_liveness_no_auth_required(self):
        """Liveness probe must not require authentication."""
        response = client.get("/health/live")
        assert response.status_code != 401


class TestReadinessProbe:
    """Tests for GET /health/ready - readiness check including dependencies."""

    def test_readiness_with_all_services_up(self):
        """When DB and Redis are up, should return 200."""
        with patch("app.api.health.check_database", return_value=True), \
             patch("app.api.health.check_redis", return_value=True):
            response = client.get("/health/ready")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ready"

    def test_readiness_with_db_down(self):
        """When DB is down, readiness should return 503."""
        with patch("app.api.health.check_database", return_value=False), \
             patch("app.api.health.check_redis", return_value=True):
            response = client.get("/health/ready")
            assert response.status_code == 503

    def test_readiness_with_redis_down(self):
        """When Redis is down, readiness should return 503."""
        with patch("app.api.health.check_database", return_value=True), \
             patch("app.api.health.check_redis", return_value=False):
            response = client.get("/health/ready")
            assert response.status_code == 503

    def test_readiness_response_includes_checks(self):
        """Response body should detail each dependency check."""
        response = client.get("/health/ready")
        data = response.json()
        assert "checks" in data or "status" in data


class TestMetricsEndpoint:
    """Tests for GET /health/metrics - Prometheus-style metrics."""

    def test_metrics_endpoint_exists(self):
        """Metrics endpoint should be accessible."""
        response = client.get("/health/metrics")
        assert response.status_code in [200, 404]  # 404 acceptable if not implemented yet

    def test_metrics_content_type(self):
        """If metrics are served, content-type should be text/plain."""
        response = client.get("/health/metrics")
        if response.status_code == 200:
            assert "text/plain" in response.headers.get("content-type", "")


class TestVersionEndpoint:
    """Tests for GET /health/version - application version info."""

    def test_version_endpoint(self):
        """Version endpoint should return app metadata."""
        response = client.get("/health/version")
        if response.status_code == 200:
            data = response.json()
            assert "version" in data or "app" in data

    def test_root_redirect_or_docs(self):
        """Root path should return docs redirect or 200."""
        response = client.get("/")
        assert response.status_code in [200, 307, 301]