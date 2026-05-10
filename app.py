import importlib
import os
import subprocess
import sys


def ensure_dependencies():
    """Ensure all application dependencies are installed, including overlay requirements"""
    print("Checking and installing all dependencies...")
    
    # Always install from requirements.txt to ensure all dependencies are present
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✓ All dependencies installed successfully")
    except subprocess.CalledProcessError as exc:
        print("Warning: Some dependencies may not have installed properly")
    
    # Verify critical packages
    required = ["pyautogui", "PIL", "openrouter", "playwright"]
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
        except Exception as e:
            if package == "pyautogui":
                print("Note: pyautogui may fail due to missing DISPLAY, but will work at runtime")
            else:
                print(f"Note: {package} import warning: {str(e)}")

    if missing and package != "pyautogui":
        print(f"Installing missing core packages: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        except subprocess.CalledProcessError:
            print("Warning: Some packages could not be installed")


ensure_dependencies()

# Always import OpenRouterAgent - pyautogui errors will be handled at runtime
from agent import OpenRouterAgent

DEFAULT_MODEL = "tencent/hy3-preview:free"
FALLBACK_MODELS = ["tencent/hy3-preview:free", "baidu/qianfan-ocr-fast:free"]

PROFILES = {
    "assistant": "You are a helpful assistant.",
    "coder": "You are a coding expert.",
    "agent": (
        "You are a web browsing AI assistant that helps users find products, information, and navigate websites. "
        "Your ONLY job is to browse the web, click on products/links, and provide helpful answers with links. "
        "RESPONSE PATTERN: You MUST respond with ONLY natural language and links - never show JSON to the user! "
        "When you need to use browser actions, include the JSON action in your thinking but DON'T show it to the user. "
        "After getting results from browser actions, provide a helpful answer with actual clickable links and information. "
        "AVAILABLE BROWSER ACTIONS (use internally, don't show JSON to user): "
        "- browser_search: Search the web. Value is the search query string. "
        "- browser_visit: Visit a URL and see page content with products/links. Value is {\"url\": \"https://...\", \"task\": \"description\"}. "
        "- browser_extract: Extract information from a URL. Value is {\"url\": \"https://...\", \"info\": \"what to extract\"}. "
        "- browser_analyze: Analyze a page structure, find all clickable products, buttons, links. Value is the URL string. "
        "- browser_click: Click a product or link on a page. Value is {\"url\": \"https://...\", \"selector\": \"product name or CSS selector\"}. "
        "STRATEGY FOR FINDING PRODUCTS/INFO: "
        "1. Search for what the user asks for. "
        "2. Visit relevant websites and analyze the page. "
        "3. Click on products, links, or sections to explore deeper. "
        "4. Extract specific information requested. "
        "5. Provide final answer with: "
        "   - Direct clickable links (format: [Link Text](URL)) "
        "   - Product names and descriptions "
        "   - Prices if available "
        "   - Clear, helpful explanations "
        "IMPORTANT: "
        "- ONLY use browser actions, no desktop or file operations. "
        "- ALWAYS provide clickable markdown links in your answers. "
        "- NEVER show JSON actions to the user - only show your final helpful answer with links! "
        "- When done, say 'Task completed' or provide the final answer. "
    )
}

def main():
    """Main application entry point with multi-agent support and improved screenshots"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenRouter API key: ").strip()
        if not api_key:
            print("API key required.")
            return

    print("\n" + "="*60)
    print("OPENROUTER AGENT - MULTI-AI SYSTEM")
    print("="*60 + "\n")

    # Choose mode
    print("Available modes:")
    print("  1. Multi-Agent Mode (Multiple AIs collaborate)")
    print("  2. Single Agent Mode (Traditional mode)")
    print("  3. Overlay Mode (Desktop visual interface)")
    print("  4. Web Navigation Mode (Browser automation)")
    
    mode = input("\nChoose mode (1-4) [1]: ").strip() or "1"
    
    if mode == "1":
        # Multi-Agent Mode
        run_multi_agent_mode(api_key)
    elif mode == "2":
        # Single Agent Mode
        run_single_agent_mode(api_key)
    elif mode == "3":
        # Overlay Mode
        run_overlay_mode(api_key)
    elif mode == "4":
        # Web Navigation Mode
        run_web_mode(api_key)
    else:
        print("Invalid mode. Running default multi-agent mode...")
        run_multi_agent_mode(api_key)


def run_multi_agent_mode(api_key: str):
    """Run multi-AI agent collaboration mode"""
    from multi_agent import MultiAgentSystem
    
    print("\n[Multi-Agent Mode]")
    print("Available AI models for collaboration:")
    
    multi_agent = MultiAgentSystem(api_key=api_key)
    models = multi_agent.list_available_models()
    
    for i, (role, info) in enumerate(models.items(), 1):
        print(f"  {i}. {info['name']}")
        print(f"     Model: {info['model']}")
        print(f"     {info['description']}\n")
    
    while True:
        problem = input("\nEnter problem/task (or 'exit' to quit): ").strip()
        if problem.lower() in ["exit", "quit"]:
            break
        
        if not problem:
            continue
        
        # Run multi-agent collaboration
        results = multi_agent.collaborate_on_problem(problem)
        
        print("\n" + "="*60)
        print("COLLABORATION RESULTS")
        print("="*60)
        
        for key, value in results.items():
            print(f"\n[{key.upper().replace('_', ' ')}]")
            print(value[:500] if len(str(value)) > 500 else value)
            print()
        
        print("\nScreenshots available:", end=" ")
        screenshot_manager = _get_screenshot_manager()
        print(screenshot_manager.get_screenshot_display_info()[:200])


def run_single_agent_mode(api_key: str):
    """Run traditional single agent mode with improved screenshots"""
    from screenshot_manager import ScreenshotManager
    
    print("\n[Single Agent Mode]")
    
    profile = input("Choose profile (assistant/coder/agent) [agent]: ").strip() or "agent"
    system_prompt = PROFILES.get(profile, PROFILES["agent"])
    
    screenshot_mgr = ScreenshotManager()
    history = []
    agent = OpenRouterAgent(api_key=api_key, model=DEFAULT_MODEL)

    print("Type 'exit' or 'quit' to stop.")
    print(f"Storing screenshots in: {screenshot_mgr.storage_dir}\n")
    
    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() in ["exit", "quit"]:
            break
        
        if user_text.lower() == "screenshots":
            print(screenshot_mgr.get_screenshot_display_info())
            continue

        history = [{"role": "user", "content": user_text}]
        print("Starting task...")

        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Capture screenshot
            screenshot_metadata = screenshot_mgr.capture_screenshot()
            
            image_message = None
            try:
                if os.environ.get('DISPLAY') and screenshot_metadata:
                    base64_img, img_url = screenshot_mgr.get_screenshot_for_api()
                    
                    screen_msg = f"Screenshot captured. Analyze and decide next action. Available screenshots: {len(screenshot_mgr.screenshot_history)}"
                    
                    image_message = {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": screen_msg},
                            {"type": "image_url", "image_url": {"url": img_url}}
                        ]
                    }
                else:
                    image_message = {"role": "user", "content": "Proceeding with browser automation."}
            except Exception as e:
                print(f"Screenshot processing: {str(e)}")
                image_message = {"role": "user", "content": "Using text-based interaction."}

            if not image_message:
                image_message = {"role": "user", "content": "No screen data available."}
            
            messages = [{"role": "system", "content": system_prompt}] + history + [image_message]

            try:
                assistant_text = agent.chat(messages).strip()
                print("\nAI Response:")
                
                nl_response = agent.extract_natural_language_response(assistant_text)
                if nl_response:
                    print(nl_response)
                    history.append({"role": "assistant", "content": nl_response})
                
                action_text = agent.get_action_from_response(assistant_text, system_prompt)
                
                if action_text:
                    action = agent.parse_action(action_text)
                    if action:
                        if action['action'] == 'done':
                            print("\n✓ Task completed.")
                            break
                        print(f"\nExecuting: {action['action']}")
                        result = agent.execute_action(action)
                        print(f"Result: {result}")
                        history.append({"role": "user", "content": "Executed: " + str(result)})
                    else:
                        print("No action parsed.")
                        break
                else:
                    if not nl_response:
                        break
                    else:
                        print("Task complete based on response.")
                        break
            except Exception as e:
                print(f"Error: {str(e)}")
                break
        
        # Cleanup old screenshots
        screenshot_mgr.cleanup_old_screenshots()


def run_overlay_mode(api_key: str):
    """Run with desktop overlay mode"""
    try:
        from overlay import start_overlay
        from screenshot_manager import ScreenshotManager
        
        print("\n[Overlay Mode]")
        print("Starting desktop overlay...")
        
        profile = input("Choose profile (assistant/coder/agent) [agent]: ").strip() or "agent"
        system_prompt = PROFILES.get(profile, PROFILES["agent"])
        
        screenshot_mgr = ScreenshotManager()
        start_overlay(api_key, system_prompt, screenshot_mgr)
    except Exception as e:
        print(f"Could not start overlay mode: {e}")
        print("Falling back to single agent mode...")
        run_single_agent_mode(api_key)


def run_web_mode(api_key: str):
    """Run web navigation mode optimized for browser tasks"""
    from multi_agent import MultiAgentSystem
    from screenshot_manager import ScreenshotManager
    
    print("\n[Web Navigation Mode]")
    print("Specialized for website interaction and browser automation\n")
    
    multi_agent = MultiAgentSystem(api_key=api_key)
    screenshot_mgr = ScreenshotManager()
    agent = OpenRouterAgent(api_key=api_key, model=multi_agent.AVAILABLE_MODELS["web_navigator"])
    
    print("Enter websites to visit, searches to perform, or tasks to complete.")
    print("Type 'exit' to quit.\n")
    
    while True:
        task = input("Web Task: ").strip()
        if task.lower() in ["exit", "quit"]:
            break
        
        if not task:
            continue
        
        print("\nPlanning web navigation strategy...")
        
        system_prompt = (
            "You are a web navigation expert. You specialize in:\n"
            "1. Finding information on websites quickly\n"
            "2. Navigating complex website structures\n"
            "3. Clicking buttons and filling forms\n"
            "4. Extracting and summarizing information\n"
            "5. Creating step-by-step navigation plans\n\n"
            "Always use browser_* actions to interact with websites."
        )
        
        # Get web strategy
        strategy = multi_agent.get_agent_response("web_navigator", f"Plan how to: {task}")
        print(f"\nStrategy:\n{strategy}\n")
        
        # Execute with screenshots
        history = [{"role": "user", "content": task}]
        
        for step in range(3):  # Max 3 web steps
            screenshot_mgr.capture_screenshot()
            
            messages = [{"role": "system", "content": system_prompt}] + history
            
            response = agent.chat(messages)
            print(f"\nStep {step+1} Response:")
            print(response[:300])
            
            history.append({"role": "assistant", "content": response})
            
            if "done" in response.lower() or "complete" in response.lower():
                break
        
        print("\n✓ Web navigation task complete.")
        print(f"Screenshots saved to: {screenshot_mgr.storage_dir}")


def _get_screenshot_manager():
    """Helper to get screenshot manager instance"""
    from screenshot_manager import ScreenshotManager
    return ScreenshotManager()


if __name__ == "__main__":
    main()
