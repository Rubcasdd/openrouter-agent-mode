# openrouter-agent-mode

**Advanced AI Desktop Agent with Vision Capabilities** 🤖✨

An intelligent desktop automation system that uses OpenRouter's vision API to analyze screens, interact with websites, and control your computer through natural language commands.

## ⚡ Features

### Vision & Screen Analysis
- **Direct AI Vision**: Send full screen images directly to AI for advanced analysis (no OCR needed)
- **Smart Screenshot Capture**: Automatic screen monitoring with base64 encoding
- **Mouse Position Tracking**: Real-time cursor position feedback for precise interactions
- **Visual Reasoning**: AI analyzes visual elements and decides what to click

### Desktop Interaction
- **Multi-click Strategy**: Click on multiple UI elements, analyze results, and adapt
- **Advanced Mouse Control**: 
  - Click, double-click, right-click at specific coordinates
  - Smooth mouse movement with animation
  - Scroll up/down with configurable amounts
- **Keyboard Control**: Type text on keyboard
- **Terminal Integration**: Run shell commands
- **Python Execution**: Execute Python code for complex tasks

### Two Interface Modes

#### 1. **Desktop Overlay Mode** (NEW - Recommended)
- Futuristic terminal-style overlay UI
- Real-time neural analysis display
- Smooth cyan/neon animations
- Automatic startup with `app.py`
- Mouse tracking overlay
- Action history counter
- Perfect for watching AI work in real-time

#### 2. **CLI Mode**
- Terminal-based interface
- Step-by-step execution logging
- Fallback when overlay unavailable

### Profiles
- **Assistant**: General helpful assistant
- **Coder**: Programming expert
- **Agent**: Advanced desktop control (RECOMMENDED)

### Additional Capabilities
- Open URLs and search the web
- Create and manage files/folders
- Read file contents
- List directories
- Analyze data at every step
- Multi-step task completion with conversation history

## 📋 Installation

### Prerequisites
- Python 3.8+
- X11 or compatible display server (for overlay)
- OpenRouter API key

### Setup

1. Clone and setup:
```bash
git clone <repo>
cd openrouter-agent-mode
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set API key:
```bash
export OPENROUTER_API_KEY=your_key_here
```

## 🚀 Usage

### Desktop Overlay Mode (Default)
```bash
python app.py
# Choose overlay mode when prompted
# Enter your task in the GUI
# Watch the AI analyze and interact with your desktop
```

**Overlay Features:**
- ⚡ Real-time analysis display
- 🖱️ Mouse position tracker
- 📊 Action counter
- ✨ Smooth cyan/neon animations
- 🔧 Start/Stop controls

### CLI Mode
```bash
python app.py
# Choose "n" when asked about overlay mode
# Type your task
# Watch execution in terminal
```

### Direct Python Overlay
```bash
python overlay.py
# Starts overlay directly
# Input task in dialog
```

## 📝 Example Tasks

1. **Web Browsing**
   - "Open YouTube and search for AI tutorials"
   - "Browse GitHub and find Python projects trending today"

2. **Data Analysis**
   - "Open a spreadsheet and analyze quarterly sales data"
   - "Find and click on all charts, screenshot each one"

3. **Desktop Automation**
   - "Create a folder, write a file, and open it"
   - "Search for files and organize them by type"

4. **Complex Analysis**
   - "Take screenshots of different websites, compare them"
   - "Analyze the current desktop, click on everything interactive, report findings"

## 🎮 Action Types

### Screen Analysis
```json
{"action": "take_screenshot"}
```

### Clicking & Interaction
```json
{"action": "click", "value": {"x": 100, "y": 200}}
{"action": "double_click", "value": {"x": 100, "y": 200}}
{"action": "right_click", "value": {"x": 100, "y": 200}}
{"action": "move_mouse", "value": {"x": 100, "y": 200, "duration": 0.5}}
{"action": "scroll", "value": {"direction": "down", "amount": 5}}
{"action": "type_text", "value": "Hello World"}
```

### Web & Navigation
```json
{"action": "open_url", "value": "https://example.com"}
{"action": "search", "value": "query"}
```

### File Operations
```json
{"action": "create_file", "value": {"path": "file.txt", "content": "text"}}
{"action": "read_file", "value": "/path/file.txt"}
{"action": "list_dir", "value": "/path"}
{"action": "create_folder", "value": "/path/folder"}
```

### System Control
```json
{"action": "run_command", "value": "ls -la"}
{"action": "execute_python", "value": "print('hello')"}
```

## 🎨 Futuristic UI Features

The overlay mode features:
- **Neon Cyan Theme**: #00d9ff primary color with glow effects
- **Smooth Animations**: All elements animate with ease transitions
- **Real-time Feedback**: Live text, mouse position, action counter
- **Glassmorphism**: Blur effects on card backgrounds
- **Shimmer Effects**: Dynamic light effects across UI elements
- **Status Indicators**: Pulsing green indicator for active state
- **Monospace Font**: Courier font for authentic terminal feel

### Web Interface
The Flask web version includes:
- Dark gradient background with animated pulses
- Glitch text effect on title
- Smooth card animations with borders
- Neon text shadows and glows
- Custom scrollbars matching theme
- Responsive grid layout

## 🔧 Architecture

### agent.py
- Core AI agent using OpenRouter API
- Vision encoding (PIL images to base64)
- Mouse position tracking
- Action parsing and execution
- Action history tracking

### app.py
- Flask web interface (optional)
- CLI mode with screen vision
- Profile selection
- Message history management

### overlay.py
- Tkinter-based desktop overlay
- Futuristic UI with animations
- Real-time task execution
- Threading for smooth performance
- Mouse tracking
- Action counter

## 🎯 AI Strategy

The agent is prompted to:
1. ✅ Click on as many interactive elements as possible
2. ✅ Analyze data after each step
3. ✅ Explore the interface thoroughly
4. ✅ Scroll and interact with all visible elements
5. ✅ Come to conclusions or complete tasks
6. ✅ Report findings in detail

## 🆘 Troubleshooting

### Overlay won't start
- Check if Tkinter is installed: `python -m tkinter`
- Check X11 connection if on WSL/remote
- Fallback to CLI mode

### Mouse clicks not working
- Check pyautogui permissions
- Try running with `xinput` available
- Verify mouse coordinates with overlay tracker

### Vision not working
- Ensure base64 encoding is working
- Check API supports image inputs
- Test with simpler models first

## 📦 Dependencies

- `openrouter` - AI API client
- `pyautogui` - Mouse/keyboard control
- `pillow` - Image processing  
- `requests` - HTTP client
- `python-dotenv` - Environment variables

## 📄 License

MIT License - See LICENSE file

---

**Built with ⚡ for advanced desktop automation**

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
- `Execute Python code: print('Hello from Python!')`

## Notes

- This app stores your API key only in memory for the current session.
- If dependencies are missing, `app.py` will attempt to install them automatically from `requirements.txt` before startup.
- If you run `overlay.py` directly, it also checks and installs missing packages automatically.
- The agent is local and designed for desktop automation and screen-aware actions.
