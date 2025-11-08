#!/bin/bash

# Setup script for FastAPI Scrapper
# This script creates and sets up a virtual environment with all dependencies

echo "🚀 Setting up FastAPI Scrapper..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the FastAPI server, run:"
echo "  python src/main.py"
echo "  or"
echo "  uvicorn src/main:app --reload"
echo ""
echo "The API will be available at:"
echo "  - http://localhost:8000"
echo "  - Interactive docs: http://localhost:8000/docs"
echo ""
