# FastAPI Randomizer

A modern, full-stack web application built with FastAPI that provides random number generation and list randomization features. Features a professional, interactive frontend with dark/light theme support and animated interactions.

## Features

### Backend
- **RESTful API** with full CRUD operations
- **Random Number Generation**
  - Generate random numbers up to a maximum value
  - Generate random numbers within a specified range
- **List Management**
  - Create, read, update, and delete list items
  - Shuffle lists with random ordering
  - Pick random items from lists
- **Interactive API Documentation** at `/docs`
- **Alternative API Documentation**: at `/redoc`
- **CORS-enabled** for frontend integration
- **Pydantic validation** for type-safe request/response handling

### Frontend
- **Modern, Professional UI** with gradient accents and smooth animations
- **Dark/Light Theme Toggle** with localStorage persistence
- **Formatted Number Display** - Numbers displayed with comma separators for readability
- **Quick Add Presets** - 12 pre-configured lists:
  - 👥 Names
  - 📻 Phonetic (NATO) alphabet
  - 🍎 Flavors
  - 🎨 Colors
  - 🪐 Planets
  - 🐶 Animals
  - 📅 Months
  - 📆 Weekdays
  - 🗺️ US States
  - 🌍 World Countries <!-- - 💻 Programming Languages -->
  - ♈ Zodiac Signs
  - 😄 Emojis
- **Multi-item Input** - Add multiple items at once (comma-separated)
- **Side-by-Side Views** - See original and shuffled lists simultaneously
- **Animated Interactions**
  - Spinning number reveals
  - Bouncing random item selection
  - Staggered slide-in animations for shuffled items
  - Loading spinners for async operations
- **Responsive Design** - Works on desktop and mobile devices

## Installation

### Prerequisites
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager <i>(recommended)</i>

### Setup

1. Clone the repository:
```bash
git clone git@github.com:ncarsner/fastapi-randomizer.git
```

2. Migrate to directory
```
cd fastapi-randomizer
```

3. Install dependencies:
```bash
uv sync
```

## Usage

### Running the Application

Start the development server:
```bash
uv run fastapi dev main.py
```

### API Endpoints

#### Random Numbers
- `GET /random/{max_value}` - Generate random number from 1 to max_value
- `GET /random-between?min_value={min}&max_value={max}` - Generate random number in range (min: 1-1000000, max: 1-1000000)

#### Items Management
- `POST /items` - Create a new item
- `GET /items` - Get all items
- `GET /items/shuffled` - Get shuffled list of items
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

### Example API Requests

```bash
# Get random number between 1 and 100
curl http://localhost:8000/random/100

# Get random number between 50 and 100
curl "http://localhost:8000/random-between?min_value=50&max_value=100"

# Get random number between 1 and 10,000
curl "http://localhost:8000/random-between?min_value=1&max_value=10000"

# Add an item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Apple"}'

# Get all items
curl http://localhost:8000/items

# Get shuffled items
curl http://localhost:8000/items/shuffled
```

## Project Structure

```
fastapi-randomizer/
├── main.py              # FastAPI backend application
├── pyproject.toml       # Dependencies and dev dependencies
├── pytest.ini           # Pytest configuration
├── static/
│   ├── index.html       # Frontend single-page application (SPA)
│   └── styles.css       # Styling with CSS variables
├── tests/               # Test suite (100% coverage)
│   ├── conftest.py      # Test fixtures and configuration
│   ├── test_app.py      # Application and static file tests
│   ├── test_items_endpoints.py    # Item management tests
│   ├── test_random_endpoints.py   # Random number generation tests
│   └── README.md        # Test documentation
└── README.md
```

## 💻 Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Pydantic** - Data validation using Python type hints

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework dependencies
- **CSS Custom Properties** - Dynamic theming
- **Fetch API** - Async HTTP requests

## 🧪 Testing

The project includes a comprehensive test suite with **100% code coverage**.

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=main --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_random_endpoints.py

# Generate HTML coverage report
uv run pytest --cov=main --cov-report=html
```

### Test Suite

- **50 tests** covering all endpoints and functionality
- **3 test modules**: random endpoints, items endpoints, and application tests
- **Fixtures** for test isolation and data setup
- **Integration tests** for complete workflows

See [tests/README.md](tests/README.md) for detailed test documentation.

## 🧑‍💻 Development

### Adding New Preset Lists

To add a new preset list:

1. Add the list to the `PRESET_LISTS` object in `static/index.html`:
```javascript
const PRESET_LISTS = {
    // ... existing lists
    myList: ['Item 1', 'Item 2', 'Item 3']
};
```

2. Add a button in the preset-buttons section:
```html
<button onclick="addPresetList('myList')">🎯 My List</button>
```

### Customizing Theme Colors

Edit the CSS custom properties in `static/index.html`:
```css
:root {
    --bg-primary: #f8fafc;
    --bg-secondary: #ffffff;
    /* ... other colors */
}
```

## License

This project is built following the [Real Python FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
