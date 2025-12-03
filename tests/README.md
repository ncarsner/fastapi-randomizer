# Test Suite

Comprehensive functional tests for the FastAPI Randomizer application.

## Test Coverage

The test suite provides **100% code coverage** with 50 tests covering:

### Test Files

1. **`test_random_endpoints.py`** (11 tests)
   - Random number generation (`/random/{max_value}`)
   - Random number in range (`/random-between`)
   - Boundary conditions, validation, and randomization verification

2. **`test_items_endpoints.py`** (26 tests)
   - Item creation (POST `/items`)
   - Item retrieval and shuffling (GET `/items`)
   - Item updates (PUT `/items/{item}`)
   - Item deletion (DELETE `/items/{item}`)
   - Full CRUD workflows and integration tests

3. **`test_app.py`** (13 tests)
   - Application configuration and metadata
   - API documentation endpoints (`/docs`, `/redoc`)
   - Static file serving
   - Error handling
   - CORS configuration

### Test Organization

Tests are organized using class-based grouping:
- `TestRandomNumber` - Basic random number generation tests
- `TestRandomBetween` - Range-based random generation tests
- `TestAddItem` - Item creation tests
- `TestGetItems` - Item retrieval and shuffling tests
- `TestUpdateItem` - Item update tests
- `TestDeleteItem` - Item deletion tests
- `TestItemsIntegration` - End-to-end workflow tests
- `TestAppConfiguration` - Application setup tests
- `TestAPITags` - API organization tests
- `TestErrorHandling` - Error response tests
- `TestStaticFiles` - Static file serving tests

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run with verbose output
```bash
uv run pytest -v
```

### Run specific test file
```bash
uv run pytest tests/test_random_endpoints.py
```

### Run specific test class
```bash
uv run pytest tests/test_items_endpoints.py::TestAddItem
```

### Run specific test
```bash
uv run pytest tests/test_items_endpoints.py::TestAddItem::test_add_item_success
```

### Run with coverage
```bash
uv run pytest --cov=main --cov-report=term-missing
```

### Generate HTML coverage report
```bash
uv run pytest --cov=main --cov-report=html
open htmlcov/index.html
```

## Test Fixtures

Defined in `conftest.py`:

- **`client`** - FastAPI TestClient for making API requests
- **`clear_items_db`** - Auto-use fixture that clears the database before/after each test
- **`sample_items`** - List of sample items for testing
- **`populated_db`** - Pre-populated database with sample items

## Test Features

### Isolation
- Each test runs with a clean database state (via `clear_items_db` fixture)
- Tests don't interfere with each other
- No external dependencies required

### Comprehensive Coverage
- Happy path scenarios
- Error conditions and edge cases
- Validation testing
- Integration workflows
- Boundary value testing
- Special characters and encoding

### Randomization Testing
- Multiple calls to verify true randomization
- Set-based comparisons to verify all items present
- Order preservation verification

## Adding New Tests

1. Create test file following naming convention: `test_*.py`
2. Organize tests into classes: `Test*`
3. Name test functions: `test_*`
4. Use fixtures from `conftest.py`
5. Run tests to verify they pass and maintain 100% coverage

Example:
```python
class TestNewFeature:
    """Tests for new feature."""

    def test_new_feature_basic(self, client):
        """Test basic functionality."""
        response = client.get("/new-endpoint")
        assert response.status_code == 200
```

## Dependencies

Test dependencies are defined in `pyproject.toml`:
- `pytest` - Testing framework
- `pytest-cov` - Coverage plugin
- `httpx` - HTTP client for TestClient

Install with:
```bash
uv sync --dev
```
