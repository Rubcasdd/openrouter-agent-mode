# Quick Reference - OpenRouter Agent Mode v2.0

## 🎯 Start Application

```bash
# Automatic setup
bash install_all.sh
python app.py

# Or manual
export OPENROUTER_API_KEY='your-key'
python app.py
```

---

## 📱 Four Operation Modes

| Mode | Command | Best For |
|------|---------|----------|
| **Multi-Agent** | Choose `1` | Complex problems needing multiple AI perspectives |
| **Single Agent** | Choose `2` | Traditional interaction with screenshots |
| **Overlay** | Choose `3` | Desktop UI with real-time AI analysis |
| **Web Nav** | Choose `4` | Automated website navigation & scraping |

---

## 🧠 AI Model Roles

```python
# Problem Solver (NVIDIA Nemotron 3 Super)
→ Breaks down issues, creates analysis plans

# Answerer (OpenAI GPT-OSS-120B)
→ Provides detailed information and explanations

# Task Executor (Poolside Laguna M.1)
→ Plans and executes multi-step workflows

# Web Navigator (Z.ai GLM 4.5 Air)
→ Specializes in website interaction

# Productivity Specialist (MiniMax M2.5)
→ Handles office and productivity tasks
```

---

## 📸 Screenshot Features

```python
from screenshot_manager import ScreenshotManager

mgr = ScreenshotManager()

# Capture
meta = mgr.capture_screenshot("name")

# Get for API
base64, url = mgr.get_screenshot_for_api()

# List all
all_shots = mgr.list_available_screenshots()

# Display info
print(mgr.get_screenshot_display_info())

# Cleanup
mgr.cleanup_old_screenshots(keep_count=20)
```

Default storage: `/tmp/openrouter_screenshots/`

---

## 🌐 Browser Automation

```python
from browser_automation import AdvancedBrowserAutomation
import asyncio

auto = AdvancedBrowserAutomation()

steps = [
    # Navigate
    {"action": "goto", "url": "https://..."},
    
    # Interact
    {"action": "click", "selector": "button"},
    {"action": "fill", "selector": "input", "text": "query"},
    {"action": "submit_form", "selector": "form"},
    
    # Extract
    {"action": "extract", "selector": ".result"},
    {"action": "screenshot", "path": "/tmp/shot.png"},
    
    # Navigate by text
    {"action": "navigate_by_link", "link_text": "Next Page"},
    
    # Scroll
    {"action": "scroll", "direction": "down", "amount": 300},
    
    # Wait
    {"action": "wait", "ms": 2000},
]

result = asyncio.run(auto.multi_step_task(steps))
```

---

## 🤖 Multi-Agent System

```python
from multi_agent import MultiAgentSystem

ma = MultiAgentSystem(api_key="key")

# Get single agent response
answer = ma.get_agent_response("answerer", "Question?")

# Full collaboration
results = ma.collaborate_on_problem("Problem description")
# Returns:
# - problem_analysis
# - task_plan
# - web_strategy
# - detailed_answer
# - optimization

# List models
models = ma.list_available_models()

# Best model for task
model = ma.get_best_model_for_task("web")
```

---

## 🔧 Integration Examples

### Example 1: Web Research
```bash
python app.py
→ Mode 1: Multi-Agent
→ "Find latest AI model benchmarks"
```
Result: 5 AI perspectives on where to look and what to find

### Example 2: Website Automation
```bash
python app.py
→ Mode 4: Web Navigation
→ "Scrape pricing from openrouter.ai"
```
Result: Automatic navigation and data extraction

### Example 3: Desktop Control
```bash
export DISPLAY=:0
python app.py
→ Mode 3: Overlay
→ "Open calculator and compute 2+2"
```
Result: Real-time screen overlay with AI control

### Example 4: Simple Task
```bash
python app.py
→ Mode 2: Single Agent
→ "Search for Python tutorials"
```
Result: Browser automation with screenshot capture

---

## 📋 File Structure

```
openrouter-agent-mode/
├── app.py                    # 4 modes, enhanced startup
├── agent.py                  # OpenRouter client
├── multi_agent.py            # 5-agent collaboration system
├── screenshot_manager.py     # Screenshot capture & history
├── browser_automation.py     # Advanced browser tasks
├── overlay.py                # Desktop UI interface
├── requirements.txt          # All dependencies
├── install_all.sh           # One-click setup
├── MULTI_AGENT_GUIDE.md     # Full documentation
└── IMPLEMENTATION_COMPLETE_v2.md  # Change log
```

---

## ⚙️ Environment Variables

```bash
# Required
export OPENROUTER_API_KEY='sk-...'

# Optional - for overlay mode
export DISPLAY=:0

# Optional - custom screenshot dir
export SCREENSHOT_DIR='/my/path'
```

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module" | Run `bash install_all.sh` |
| "No DISPLAY" | Screenshot mode disabled, browser mode active |
| API errors | Check key: `echo $OPENROUTER_API_KEY` |
| Slow startup | First run installs browsers, subsequent runs faster |
| Memory usage | Run `cleanup_old_screenshots()` |

---

## 💡 Tips & Tricks

### Faster Startup
```bash
# Skip installation check
pip install -q -r requirements.txt
python app.py
```

### Custom Storage
```python
mgr = ScreenshotManager("/my/storage")  # Custom path
```

### Headless Mode
```python
# Playwright already runs headless
# Add DISPLAY for overlay:
export DISPLAY=:0
```

### Batch Tasks
```bash
# Use Mode 1 for multiple problems
# Loop through tasks programmatically
```

### Monitor Actions
```python
# Check history after task
mgr.list_available_screenshots()
automation.session_history
```

---

## 📊 Performance Notes

- **Screenshots**: Auto-cleanup keeps <20 by default
- **Browser**: Headless Chrome optimized for speed
- **API**: Free-tier rates typically 100+ req/min
- **Memory**: ~300MB baseline, grows with screenshots

---

## 🎓 Learning Path

1. Start with Mode 2 (Single Agent) - understand basics
2. Move to Mode 4 (Web Nav) - learn browser automation
3. Advance to Mode 1 (Multi-Agent) - see collaboration
4. Use Mode 3 (Overlay) - advanced desktop control

---

## 🔗 Useful Links

- API Keys: https://openrouter.ai/keys
- Models: https://openrouter.ai/models
- Docs: https://openrouter.ai/docs
- Playwright: https://playwright.dev

---

## 💰 Cost Planning

All free tier - $0 cost for testing:
```
100 demo requests = $0
1000 research queries = $0
10,000 automation steps = $0
```

---

## ✅ Checklist

- [ ] Installed dependencies: `bash install_all.sh`
- [ ] Set API key: `export OPENROUTER_API_KEY=...`
- [ ] Tested startup: `python app.py`
- [ ] Tried Mode 1 (Multi-Agent)
- [ ] Tried Mode 4 (Web Navigation)
- [ ] Checked screenshots: `/tmp/openrouter_screenshots/`
- [ ] Reviewed MULTI_AGENT_GUIDE.md

---

## 🚀 Next Steps

1. **Set up:** Run `bash install_all.sh`
2. **Configure:** Export OPENROUTER_API_KEY
3. **Explore:** Try each mode with different tasks
4. **Integrate:** Use the classes in your own code
5. **Extend:** Add custom AI models and actions

---

## 📞 Quick Support

```bash
# Check Python
python3 --version

# Verify pip
pip list | grep openrouter

# Test import
python3 -c "from multi_agent import MultiAgentSystem; print('✓')"

# View API key
echo ${OPENROUTER_API_KEY}

# List screenshots
ls /tmp/openrouter_screenshots/
```

---

**v2.0.0** | Ready to Use | All Features Implemented
