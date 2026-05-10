#!/bin/bash
# Quick Start Guide - Browser Agent Setup

echo "🚀 Chrome Browser Integration for OpenRouter Agent"
echo "=================================================="
echo ""

# Check if running in the project directory
if [ ! -f "agent.py" ]; then
    echo "❌ Error: Not in openrouter-agent-mode directory"
    exit 1
fi

echo "✅ Step 1: Verify Installation"
python -c "
import browser_use
import playwright.sync_api
from openrouter import OpenRouter
from agent import OpenRouterAgent
print('✓ All packages imported successfully')
print('✓ browser-use ready')
print('✓ playwright ready')
print('✓ agent ready')
" || {
    echo "❌ Missing packages. Installing..."
    pip install browser-use playwright
    playwright install chromium
}

echo ""
echo "✅ Step 2: Configuration"
echo "Set your OpenRouter API key:"
echo "  export OPENROUTER_API_KEY='your-key-here'"
echo ""

echo "✅ Step 3: Start the Agent"
echo "Run: python app.py"
echo ""

echo "✅ Step 4: Try Browser Actions"
echo "Try these examples:"
echo "  - 'Search for Python programming tips'"
echo "  - 'Find information about AI'"
echo "  - 'Check if example.com is online'"
echo ""

echo "📚 Documentation:"
echo "  - IMPLEMENTATION_COMPLETE.md - Full technical details"
echo "  - BROWSER_USAGE.md - Usage examples"
echo "  - test_browser.py - Run tests"
echo ""

echo "=================================================="
echo "Ready to go! Your browser-enabled AI awaits! 🎉"
