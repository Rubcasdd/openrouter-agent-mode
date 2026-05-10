# Browser-Use Integration Guide

## Overview

Your AI agent now has full Chrome browser automation capabilities via `browser-use` and `playwright`. The agent can search the web, visit URLs, and extract information **without needing a display**.

## New Browser Actions

### 1. browser_search
Search the web using Chrome and get results.

```json
{
  "action": "browser_search",
  "value": "Python programming best practices"
}
```

**Response Flow:**
- AI says: "I will search for Python programming best practices and provide you with the top results."
- Browser searches the web
- AI returns: "Here are the best practices for Python..."

### 2. browser_visit
Visit a URL and perform a task on the page.

```json
{
  "action": "browser_visit",
  "value": {
    "url": "https://example.com",
    "task": "Find and summarize the pricing information"
  }
}
```

### 3. browser_extract
Extract specific information from a URL.

```json
{
  "action": "browser_extract",
  "value": {
    "url": "https://weather.com",
    "info": "Current temperature and weather forecast"
  }
}
```

## Response Pattern

The AI now follows this pattern:

1. **Conversational Response**: First, the AI tells you what it will do
   - Example: "I will search for that information and get back to you."

2. **Browser Action**: Then executes a JSON action
   - Example: `{"action": "browser_search", "value": "your query"}`

3. **Final Answer**: After the browser completes, AI provides the result
   - Example: "Based on my search, I found..."

## Usage Examples

### Example 1: Search the Web
```
User: "Find information about the latest Python features"

AI Response:
I will search for information about the latest Python features and provide you with current information.

```json
{
  "action": "browser_search",
  "value": "latest Python features 2024"
}
```

Result:
The latest Python features include...
```

### Example 2: Extract Data from a Website
```
User: "Get the current BTC price"

AI Response:
I will visit a financial website and get you the current Bitcoin price.

```json
{
  "action": "browser_extract",
  "value": {
    "url": "https://coinmarketcap.com",
    "info": "current Bitcoin price"
  }
}
```

Result:
The current Bitcoin price is...
```

## Installation Verification

The following packages have been installed:
- `browser-use`: Chrome automation framework
- `playwright`: Browser control library
- Chromium browser binaries

Verify installation:
```bash
python -c "import browser_use; print('browser-use installed')"
python -c "import playwright; print('playwright installed')"
```

## Environment Variables

No additional environment variables are needed for browser automation. The agent uses Chrome in headless mode by default.

## Key Benefits

✅ **No Display Required**: Browser actions work without DISPLAY environment variable
✅ **Full Chrome Control**: Complete browser automation capabilities
✅ **Conversational AI**: Natural language responses followed by action
✅ **Real-time Web Access**: Search, visit, and extract from any website
✅ **Background Execution**: Browser runs in the background, no UI popup

## Troubleshooting

### Issue: "browser_use module not found"
**Solution**: Reinstall packages
```bash
pip install browser-use playwright
playwright install chromium
```

### Issue: "playwright chrome launch failed"
**Solution**: Install system dependencies
```bash
sudo apt-get install -y libx11-xcb1 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxfixes3 libgtk-3-0t64 libatk1.0-0t64 libcairo-gobject2 libgdk-pixbuf-2.0-0 libasound2t64
```

## AI System Prompt

The agent's system prompt now includes instructions for:
- Using browser actions for web tasks
- Providing conversational responses before taking actions
- Returning natural language answers after browser operations
- Choosing appropriate actions (browser vs desktop)
