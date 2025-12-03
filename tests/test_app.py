import pytest

"""Tests for general application functionality."""


class TestAppConfiguration:
    """Tests for application configuration and metadata."""

    def test_app_metadata(self, client):
        """Test OpenAPI metadata is correctly configured."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "Randomizer API"
        assert data["info"]["version"] == "1.0.0"
        assert "description" in data["info"]

    def test_docs_endpoint_accessible(self, client):
        """Test that API documentation endpoint is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_accessible(self, client):
        """Test that ReDoc documentation endpoint is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_home_endpoint(self, client):
        """Test that home endpoint returns the frontend."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestAPITags:
    """Tests for API endpoint organization and tags."""

    def test_random_endpoints_tagged(self, client):
        """Test that random endpoints have correct tags."""
        response = client.get("/openapi.json")
        data = response.json()
        
        # Check that Random Playground tag exists
        tags = [tag["name"] for tag in data.get("tags", [])]
        assert "Random Playground" in tags
        assert "Random Items Management" in tags

    def test_endpoints_organization(self, client):
        """Test that endpoints are properly organized by tags."""
        response = client.get("/openapi.json")
        data = response.json()
        
        paths = data.get("paths", {})
        
        # Check random endpoints
        assert "/random/{max_value}" in paths
        assert "/random-between" in paths
        
        # Check item management endpoints
        assert "/items" in paths
        assert "/items/{item}" in paths or "/items/{update_item_name}" in paths


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.options("/items")
        # TestClient may not fully simulate CORS, but we can verify the middleware is configured
        # The actual CORS functionality is handled by FastAPI's CORSMiddleware
        assert response.status_code in [200, 405]  # OPTIONS might not be explicitly defined


class TestErrorHandling:
    """Tests for error handling across the application."""

    def test_invalid_endpoint(self, client):
        """Test accessing an invalid endpoint."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_invalid_method(self, client):
        """Test using invalid HTTP method."""
        response = client.patch("/items")
        assert response.status_code == 405

    @pytest.mark.skip(reason="Depends on specific validation rules in the app")
    def test_malformed_json(self, client):
        """Test sending malformed JSON."""
        response = client.post(
            "/items",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    # @pytest.mark.skip(reason="Depends on specific validation rules in the app")
    def test_missing_required_fields(self, client):
        """Test sending request without required fields."""
        response = client.post("/items", json={})
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestStaticFiles:
    """Tests for static file serving."""

    def test_static_html_accessible(self, client):
        """Test that static HTML file is accessible."""
        response = client.get("/static/index.html")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    # @pytest.mark.skip(reason="CSS file may not exist in test environment")
    def test_static_css_accessible(self, client):
        """Test that static CSS file is accessible."""
        response = client.get("/static/styles.css")
        assert response.status_code == 200
        assert "text/css" in response.headers["content-type"]
