#!/bin/bash

# Agent Utility API - Quick Start Script
# This script sets up and runs the API locally

set -e

echo "🚀 Agent Utility API - Quick Start"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Check if .env exists, if not create from example
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from .env.example..."
    cp .env.example .env
    echo "📝 Edit .env file to configure your settings"
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo ""
echo "✨ Setup complete!"
echo ""
echo "🌐 Starting server on http://localhost:${PORT:-8000}"
echo "📚 API docs available at http://localhost:${PORT:-8000}/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python main.py
