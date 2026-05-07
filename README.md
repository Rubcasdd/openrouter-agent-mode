# openrouter-agent-mode

A simple local agent web app that uses OpenRouter to process instructions and perform local actions such as opening websites or running a search.

## Features

- Enter your OpenRouter API key in a local browser session
- Send instructions to an agent powered by OpenRouter
- Automatically open URLs and search results in your default browser
- Keep a simple conversation history during the session

## Getting started

1. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open your browser to `http://127.0.0.1:5000`
5. Enter your OpenRouter API key and start sending tasks.

## Usage examples

- `Open https://openrouter.ai`
- `Search for nearby coffee shops`
- `Open the GitHub homepage`

## Notes

- This app stores your API key only in the current browser session.
- The agent is local and designed for simple web actions.
