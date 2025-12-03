"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from main import app, items_db


@pytest.fixture(autouse=True)
def clear_items_db():
    """Clear the items database before each test."""
    items_db.clear()
    yield
    items_db.clear()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_items():
    """Return a list of sample items for testing."""
    return ["Apple", "Banana", "Cherry", "Date", "Elderberry"]


@pytest.fixture
def populated_db(sample_items):
    """Populate the database with sample items."""
    items_db.extend(sample_items)
    return sample_items
