# FastAPI-Scrapper

A FastAPI-based web scraping application.

## Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

#### Quick Setup (Linux/macOS)

1. Clone the repository:
```bash
git clone https://github.com/mathisbukowski/FastAPI-Scrapper.git
cd FastAPI-Scrapper
```

2. Run the setup script:
```bash
./setup.sh
```

#### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/mathisbukowski/FastAPI-Scrapper.git
cd FastAPI-Scrapper
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at:
- Main application: http://localhost:8000
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Development

To deactivate the virtual environment when you're done:
```bash
deactivate
```