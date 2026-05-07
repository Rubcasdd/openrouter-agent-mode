#!/bin/bash
# Quick start script for OpenRouter Agent Mode

echo "🚀 OpenRouter Agent Mode - Setup & Run"
echo "========================================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check for API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENROUTER_API_KEY not set"
    echo "You will be prompted for it when running the app"
    echo ""
    echo "To set it permanently, add to ~/.bashrc or ~/.zshrc:"
    echo "  export OPENROUTER_API_KEY=your_key_here"
else
    echo "✓ OPENROUTER_API_KEY is set"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "🎮 To start the agent with desktop overlay:"
echo "  python app.py"
echo ""
echo "💻 Or to start the overlay directly:"
echo "  python overlay.py"
echo ""
echo "🌐 Or to use web interface:"
echo "  python app.py  # Choose 'n' for no overlay"
echo ""
