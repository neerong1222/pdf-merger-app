#!/bin/bash

# Setup script for PDF Merger App
# This script sets up the development environment on macOS/Linux

set -e

echo "🔧 PDF Merger App - Setup Script"
echo "=================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create directories
echo "📁 Creating required directories..."
mkdir -p uploads logs temp
echo "✓ Directories created"

# Setup environment
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from template..."
    cp .env.example .env
    echo "✓ .env created - please update SECRET_KEY and other settings"
else
    echo "✓ .env already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your settings (especially SECRET_KEY)"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"
echo "4. Visit: http://localhost:5000"
echo ""
