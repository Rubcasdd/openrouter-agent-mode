#!/bin/bash

# OpenRouter Agent Mode - Comprehensive Startup Script
# Ensures all dependencies are properly installed and configured

set -e

echo "================================================"
echo "OpenRouter Agent Mode - Initialization"
echo "================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✓ Python $(python3 --version 2>&1) found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and setuptools
echo "📥 Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install requirements
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt > /dev/null 2>&1

# Install playwright browsers
echo "🎬 Installing Playwright browsers..."
python3 -m playwright install chromium > /dev/null 2>&1

# Check API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENROUTER_API_KEY not set"
    echo "📌 Set it with: export OPENROUTER_API_KEY='your_api_key'"
    echo ""
fi

echo ""
echo "================================================"
echo "✅ Initialization Complete!"
echo "================================================"
echo ""
echo "Available modes:"
echo "  1. Multi-Agent Mode (Multiple AIs collaborate)"
echo "  2. Single Agent Mode (Traditional mode)"
echo "  3. Overlay Mode (Desktop visual interface)"
echo "  4. Web Navigation Mode (Browser automation)"
echo ""
echo "To start, run:"
echo "  python app.py"
echo ""
echo "Available AI Models:"
echo "  • NVIDIA Nemotron 3 Super (Problem Solver)"
echo "  • OpenAI GPT-OSS-120B (Answerer)"
echo "  • Poolside Laguna M.1 (Task Executor)"
echo "  • Z.ai GLM 4.5 Air (Web Navigator)"
echo "  • MiniMax M2.5 (Productivity Specialist)"
echo ""
