"""Tests for random number generation endpoints."""


class TestRandomNumber:
    """Tests for /random/{max_value} endpoint."""

    def test_random_number_basic(self, client):
        """Test basic random number generation."""
        response = client.get("/random/100")
        assert response.status_code == 200
        data = response.json()
        assert "max" in data
        assert "random_number" in data
        assert data["max"] == 100
        assert 1 <= data["random_number"] <= 100

    def test_random_number_small_value(self, client):
        """Test random number with small max value."""
        response = client.get("/random/1")
        assert response.status_code == 200
        data = response.json()
        assert data["max"] == 1
        assert data["random_number"] == 1

    def test_random_number_large_value(self, client):
        """Test random number with large max value."""
        response = client.get("/random/10000")
        assert response.status_code == 200
        data = response.json()
        assert data["max"] == 10000
        assert 1 <= data["random_number"] <= 10000

    def test_random_number_multiple_calls(self, client):
        """Test that multiple calls can produce different results."""
        results = set()
        for _ in range(20):
            response = client.get("/random/100")
            data = response.json()
            results.add(data["random_number"])
        # Very unlikely all 20 calls return the same number
        assert len(results) > 1


class TestRandomBetween:
    """Tests for /random-between endpoint."""

    def test_random_between_basic(self, client):
        """Test basic random number generation between values."""
        response = client.get("/random-between?min_value=10&max_value=20")
        assert response.status_code == 200
        data = response.json()
        assert "min" in data
        assert "max" in data
        assert "random_number" in data
        assert data["min"] == 10
        assert data["max"] == 20
        assert 10 <= data["random_number"] <= 20

    def test_random_between_default_values(self, client):
        """Test random between with default values."""
        response = client.get("/random-between")
        assert response.status_code == 200
        data = response.json()
        assert data["min"] == 1
        assert data["max"] == 99
        assert 1 <= data["random_number"] <= 99

    def test_random_between_same_min_max(self, client):
        """Test when min and max are the same."""
        response = client.get("/random-between?min_value=50&max_value=50")
        assert response.status_code == 200
        data = response.json()
        assert data["random_number"] == 50

    def test_random_between_min_greater_than_max(self, client):
        """Test error when min is greater than max."""
        response = client.get("/random-between?min_value=100&max_value=10")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "min_value can't be greater than max_value" in data["detail"]

    def test_random_between_boundary_values(self, client):
        """Test with boundary values."""
        response = client.get("/random-between?min_value=1&max_value=1000000")
        assert response.status_code == 200
        data = response.json()
        assert 1 <= data["random_number"] <= 1000000

    def test_random_between_partial_params(self, client):
        """Test with only min_value provided."""
        response = client.get("/random-between?min_value=50")
        assert response.status_code == 200
        data = response.json()
        assert data["min"] == 50
        assert data["max"] == 99
        assert 50 <= data["random_number"] <= 99

    def test_random_between_multiple_calls(self, client):
        """Test that multiple calls can produce different results."""
        results = set()
        for _ in range(20):
            response = client.get("/random-between?min_value=1&max_value=100")
            data = response.json()
            results.add(data["random_number"])
        # Very unlikely all 20 calls return the same number
        assert len(results) > 1
