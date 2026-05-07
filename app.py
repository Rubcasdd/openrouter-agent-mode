import importlib
import os
import subprocess
import sys


def ensure_dependencies():
    # Always check all dependencies, but handle pyautogui gracefully
    required = ["pyautogui", "PIL", "openrouter"]
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
        except Exception as e:
            # pyautogui might fail due to missing DISPLAY - that's ok for now
            if package == "pyautogui":
                print("Warning: pyautogui import failed (may need DISPLAY): " + str(e))
            else:
                missing.append(package)

    if missing:
        print("Installing missing dependencies: " + ", ".join(missing))
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        except subprocess.CalledProcessError as exc:
            print("Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.")
            raise SystemExit(exc)


ensure_dependencies()

# Always import OpenRouterAgent - pyautogui errors will be handled at runtime
from agent import OpenRouterAgent

DEFAULT_MODEL = "baidu/qianfan-ocr-fast:free"
FALLBACK_MODELS = ["baidu/qianfan-ocr-fast:free", "tencent/hy3-preview:free"]

PROFILES = {
    "assistant": "You are a helpful assistant.",
    "coder": "You are a coding expert.",
    "agent": (
        "You are an advanced AI desktop agent with full desktop control and vision capabilities. "
        "Your role is to click on as many things as possible, analyze data at every step, and then reach conclusions or complete tasks. "
        "You can inspect the screen using vision (images), search the web, click UI elements, create files, run terminal commands, and execute Python code. "
        "Available actions: open_url, search, run_command, open_file, create_file, create_folder, read_file, list_dir, "
        "take_screenshot, click, double_click, right_click, move_mouse, scroll, type_text, execute_python. "
        "For click/double_click/right_click/move_mouse, value is {\"x\":100, \"y\":200}. "
        "For move_mouse, add 'duration': 0.5 for smooth animation. "
        "For scroll, value is {\"direction\":\"down\",\"amount\":3}. "
        "For create_file, value is {\"path\":\"file.txt\",\"content\":\"text\"}. "
        "For type_text, value is the text to type. "
        "For list_dir, value is the folder path. "
        "For read_file, value is the file path. "
        "For create_folder, value is the folder path. "
        "For run_command, value is any shell command. "
        "For execute_python, value is any Python code to run. "
        "STRATEGY: Take screenshots frequently to analyze the screen. Click on interactive elements you find. "
        "Analyze results after each action. Explore the interface thoroughly before concluding. "
        "Respond ONLY with a JSON object for the next action, or {\"action\":\"done\"} when finished. "
        "Do not include any other text."
    )
}

def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenRouter API key: ").strip()
        if not api_key:
            print("API key required.")
            return

    profile = input("Choose profile (assistant/coder/agent) [agent]: ").strip() or "agent"
    system_prompt = PROFILES.get(profile, PROFILES["agent"])
    
    # Ask if user wants desktop overlay mode
    use_overlay = input("Use desktop overlay mode? (y/n) [y]: ").strip().lower() != "n"
    
    if use_overlay:
        # Import and start overlay
        try:
            from overlay import start_overlay
            print("Starting desktop overlay mode...")
            start_overlay(api_key, system_prompt)
            return
        except Exception as e:
            print(f"Could not start overlay mode: {e}. Falling back to CLI mode.")

    history = []
    agent = OpenRouterAgent(api_key=api_key, model=DEFAULT_MODEL)

    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() in ["exit", "quit"]:
            break

        history = [{"role": "user", "content": user_text}]
        print("Starting multi-step task...")

        while True:
            # Take screenshot and send as image to AI (only if DISPLAY available)
            image_message = None
            try:
                if os.environ.get('DISPLAY'):
                    import importlib
                    pyautogui = importlib.import_module("pyautogui")
                    screenshot = pyautogui.screenshot()
                    
                    # Encode to base64
                    image_base64 = agent.encode_pil_image_to_base64(screenshot)
                    mouse_pos = agent.get_mouse_position()
                    
                    screen_msg = "Current screen image analyzed. Mouse at: " + str(mouse_pos) + ". Analyze the screen and decide what to do next."
                    
                    # Prepare message with image for OpenRouter vision API
                    image_message = {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": screen_msg},
                            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + image_base64}}
                        ]
                    }
                else:
                    print("No DISPLAY - skipping screenshot")
                    image_message = {"role": "user", "content": "No display available for screenshot."}
            except Exception as e:
                print("Screenshot error: " + str(e))
                image_message = {"role": "user", "content": "Screenshot failed."}

            if not image_message:
                image_message = {"role": "user", "content": "No screen data available."}
            
            messages = [{"role": "system", "content": system_prompt}] + history + [image_message]

            try:
                assistant_text = agent.chat(messages).strip()
                print("AI: " + assistant_text)
                history.append({"role": "assistant", "content": assistant_text})

                action = agent.parse_action(assistant_text)
                if action:
                    if action['action'] == 'done':
                        print("Task completed.")
                        break
                    result = agent.execute_action(action)
                    print("Executed: " + str(result))
                    history.append({"role": "user", "content": "Executed: " + str(result)})
                else:
                    print("No action parsed.")
                    break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    main()
