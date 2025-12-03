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
- **Quick Add Presets** - 11 pre-configured lists:
  - 👥 Students
  - 📻 Phonetic (NATO alphabet)
  - 🍎 Fruits
  - 🎨 Colors
  - 🪐 Planets
  - 🐶 Animals
  - 📅 Months
  - 📆 Weekdays
  - 🗺️ US States
  - 💻 Programming Languages
  - ♈ Zodiac Signs
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
- `GET /random/{max_value}` - Generate random number from 0 to max_value
- `GET /random-between?min={min}&max={max}` - Generate random number in range

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
curl "http://localhost:8000/random-between?min=50&max=100"

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
fast_api_demo/
├── main.py              # FastAPI backend application
├── static/
│   └── index.html       # Frontend single-page application
├── pyproject.toml       # Project dependencies and metadata
└── README.md
```

## Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Pydantic** - Data validation using Python type hints

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework dependencies
- **CSS Custom Properties** - Dynamic theming
- **Fetch API** - Async HTTP requests

## Development

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
