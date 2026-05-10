# OpenRouter Agent Mode - Complete Multi-AI System

A sophisticated AI agent framework that leverages multiple AI models from OpenRouter to collaborate on complex tasks with advanced browser automation, screenshot management, and intelligent task execution.

## 🚀 New Features

### 1. **Multi-Agent Collaboration System**
Different AI models work together, each with specialized roles:

- **Problem Solver** (NVIDIA Nemotron 3 Super) - Analyzes issues and creates plans
- **Answerer** (OpenAI GPT-OSS-120B) - Provides detailed information
- **Task Executor** (Poolside Laguna M.1) - Plans and executes multi-step workflows
- **Web Navigator** (Z.ai GLM 4.5 Air) - Specialized browser automation
- **Productivity Specialist** (MiniMax M2.5) - Handles office/productivity tasks

### 2. **Enhanced Screenshot Management**
- Automatic screenshot capture on every interaction
- Screenshots stored locally with timestamps
- Base64 encoding for API transmission
- Screenshot history tracking and cleanup
- Visual display of available screenshots

### 3. **Advanced Browser Automation**
- Multi-step task execution
- Smart element detection and clicking
- Form filling and submission
- Content extraction and analysis
- Page scrolling and navigation
- Link navigation by text content

### 4. **Four Operating Modes**

#### Mode 1: Multi-Agent Mode
```
python app.py
→ Choose option 1
```
Multiple AI models collaborate to solve problems. Each agent provides its perspective:
1. Problem analysis
2. Task planning
3. Web strategy
4. Detailed answer
5. Optimization

#### Mode 2: Single Agent Mode
```
python app.py
→ Choose option 2
```
Traditional single-agent interaction with screenshot and browser automation support.

#### Mode 3: Overlay Mode
```
python app.py
→ Choose option 3
```
Desktop overlay interface showing AI analysis in real-time with visual interface.

#### Mode 4: Web Navigation Mode
```
python app.py
→ Choose option 4
```
Specialized mode for website browsing, information extraction, and browser automation.

## 🛠️ Installation

### Quick Start
```bash
bash install_all.sh
python app.py
```

### Manual Installation
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install chromium

# Set API key
export OPENROUTER_API_KEY='your-key-here'

# Run
python app.py
```

## 📋 Requirements

- Python 3.8+
- OpenRouter API key (free tier available at https://openrouter.ai)
- Internet connection

## 💰 Cost-Free Models Available

All models used in this system have free tiers or are completely free on OpenRouter:

```
NVIDIA Nemotron 3 Super:    $0/M input & output tokens
OpenAI GPT-OSS-120B:         $0/M input & output tokens
Poolside Laguna M.1:         $0/M input & output tokens
Z.ai GLM 4.5 Air:            $0/M input & output tokens
MiniMax M2.5:                $0/M input & output tokens
```

## 📁 Project Structure

```
openrouter-agent-mode/
├── app.py                      # Main application entry point
├── agent.py                    # OpenRouter agent implementation
├── multi_agent.py              # Multi-AI collaboration system
├── screenshot_manager.py       # Screenshot capture & storage
├── browser_automation.py       # Advanced browser automation
├── overlay.py                  # Desktop overlay interface
├── requirements.txt            # Python dependencies
├── install_all.sh             # Complete installation script
└── templates/
    └── index.html             # Web UI template
```

## 🎯 Usage Examples

### Example 1: Multi-Agent Problem Solving
```
python app.py
→ Select mode 1 (Multi-Agent)
→ Enter problem: "Find the best Python web frameworks"

Expected: 
- Problem Solver analyzes what makes a "best" framework
- Task Executor plans research steps
- Web Navigator determines which sites to visit
- Answerer gathers detailed information
- Specialist suggests optimal workflow
```

### Example 2: Web Automation
```
python app.py
→ Select mode 4 (Web Navigation)
→ Enter task: "Find current AI pricing on openrouter.ai"

Expected:
- Screenshots captured automatically
- Website navigation executed
- Pricing information extracted
- Results compiled and displayed
```

### Example 3: Desktop Integration (w/ DISPLAY)
```
export DISPLAY=:0
python app.py
→ Select mode 3 (Overlay)
→ Click START AGENT
→ Enter task into input

Expected:
- Real-time screen analysis
- Desktop overlay showing AI decisions
- Automatic interaction with found elements
- Visual feedback of actions
```

## 🔧 Configuration

### API Key Setup
```bash
# Option 1: Environment variable
export OPENROUTER_API_KEY='sk-...'

# Option 2: Interactive prompt
python app.py
# System will ask for API key if not in environment
```

### Screenshot Storage
Screenshots are automatically stored in:
```
/tmp/openrouter_screenshots/
```

Customize by modifying `ScreenshotManager()` initialization:
```python
from screenshot_manager import ScreenshotManager
mgr = ScreenshotManager(storage_dir="/custom/path")
```

## 📖 API Documentation

### Multi-Agent System
```python
from multi_agent import MultiAgentSystem

ma = MultiAgentSystem(api_key="your-key")

# Get single agent response
answer = ma.get_agent_response("answerer", "What is AI?")

# Collaborate on problem
results = ma.collaborate_on_problem("Design a web scraper")

# List available models
models = ma.list_available_models()
```

### Screenshot Manager
```python
from screenshot_manager import ScreenshotManager

mgr = ScreenshotManager()

# Capture screenshot
meta = mgr.capture_screenshot("my_screenshot")

# Get for API
base64_img, img_url = mgr.get_screenshot_for_api()

# List all
all_shots = mgr.list_available_screenshots()

# Cleanup old
mgr.cleanup_old_screenshots(keep_count=20)
```

### Browser Automation
```python
from browser_automation import AdvancedBrowserAutomation
import asyncio

automation = AdvancedBrowserAutomation()

# Define multi-step task
steps = [
    {"action": "goto", "url": "https://example.com"},
    {"action": "click", "selector": "button.search"},
    {"action": "fill", "selector": "input[name='q']", "text": "python"},
    {"action": "submit_form", "selector": "form"},
    {"action": "extract", "selector": ".result"}
]

# Execute
results = asyncio.run(automation.multi_step_task(steps))
```

## 🐛 Troubleshooting

### "No DISPLAY" Error
This is normal for headless environments. The system automatically falls back to browser automation.

### Screenshot Not Working
- Check if `DISPLAY` environment variable is set: `echo $DISPLAY`
- Install X11 if running in container: `apt install x11-apps`

### API Key Not Working
- Verify key format: should start with `sk-`
- Check OpenRouter account and billing
- Ensure free tier usage limits aren't exceeded

### Pygame/Display Issues
Install Xvfb for virtual display:
```bash
apt install xvfb
xvfb-run -a python app.py
```

## ✨ Features Summary

| Feature | Mode 1 | Mode 2 | Mode 3 | Mode 4 |
|---------|--------|--------|--------|--------|
| Multi-Agent | ✅ | ❌ | ❌ | ❌ |
| Screenshots | ✅ | ✅ | ✅ | ✅ |
| Browser Auto | ✅ | ✅ | ✅ | ✅ |
| Desktop Overlay | ❌ | ❌ | ✅ | ❌ |
| Web Specialist | ✅ | ✅ | ✅ | ✅ |

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Mobile browser support
- [ ] PDF processing
- [ ] Email automation
- [ ] Custom model support
- [ ] Performance optimization
- [ ] Database integration

## 📞 Support

For issues with:
- **OpenRouter API**: Visit https://openrouter.ai/docs
- **Playwright**: Visit https://playwright.dev
- **This project**: Check GitHub Issues

## 🎓 Learning Resources

- OpenRouter Documentation: https://openrouter.ai/docs
- AI Model Capabilities: https://openrouter.ai/models
- Playwright Guide: https://playwright.dev/python/docs/intro
- Python Async: https://docs.python.org/3/library/asyncio.html

---

**Version:** 2.0.0  
**Last Updated:** 2026-05-10  
**Status:** ✅ Production Ready
