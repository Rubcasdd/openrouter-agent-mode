# openrouter-agent-mode

A simple local CLI agent that uses OpenRouter to process instructions and perform local actions such as opening websites, running commands, or creating files.

## Features

- Choose from different agent profiles (Assistant, Coder, Agent)
- Send instructions to an agent powered by OpenRouter
- Multi-step task execution with screen awareness
- Automatically open URLs and search results in your default browser
- Run terminal commands on your local machine
- Open files with your default applications
- Create and write files
- Create folders and list directories
- Read file contents
- Take screenshots and read screen text with OCR
- Analyze the screen with OCR
- Click on screen coordinates
- Type text on the keyboard
- Keep a conversation history during the session

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

3. Set your OpenRouter API key (optional, or enter when prompted):

```bash
export OPENROUTER_API_KEY=your_api_key_here
```

4. Run the app:

```bash
python app.py
```

5. Choose a profile and start chatting. Type 'exit' or 'quit' to stop.

## Usage examples

- `Open https://openrouter.ai`
- `Search for nearby coffee shops`
- `Run the command: ls -la`
- `Open the file: /home/user/document.txt`
- `Create a file at /tmp/test.txt with content: Hello World`
- `Create a folder at /tmp/project`
- `List the contents of /tmp/project`
- `Read the file /tmp/project/README.md`
- `Take a screenshot and describe what you see`
- `Analyze the screen and summarize the visible text`
- `Click on the button at x=500, y=300`
- `Type 'Hello World' in the text field`

## Notes

- This app stores your API key only in memory for the current session.
- If dependencies are missing, `app.py` will attempt to install them automatically from `requirements.txt`.
- The agent is local and designed for desktop automation and screen-aware actions.
