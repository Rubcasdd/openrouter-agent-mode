import importlib
import os
import subprocess
import sys


def ensure_dependencies():
    required = ["pyautogui", "pytesseract", "PIL", "openrouter"]
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        except subprocess.CalledProcessError as exc:
            print("Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.")
            raise SystemExit(exc)


ensure_dependencies()

from agent import OpenRouterAgent

DEFAULT_MODEL = "tencent/hy3-preview:free"
FALLBACK_MODELS = ["tencent/hy3-preview:free"]

PROFILES = {
    "assistant": "You are a helpful assistant.",
    "coder": "You are a coding expert.",
    "agent": (
        "You are a multi-step local PC assistant. "
        "You can see the screen by taking screenshots and reading text with OCR. "
        "Perform actions step by step to complete tasks. "
        "Available actions: open_url, search, run_command, open_file, create_file, take_screenshot, click (with x,y), type_text. "
        "For click, value is {\"x\":100, \"y\":200}. "
        "For type_text, value is the text to type. "
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
            # Take screenshot and add OCR to messages
            try:
                import importlib
                pyautogui = importlib.import_module("pyautogui")
                pytesseract = importlib.import_module("pytesseract")
                screenshot = pyautogui.screenshot()
                text = pytesseract.image_to_string(screenshot)[:1000]  # Limit
                screen_msg = f"Current screen text: {text}"
            except Exception:
                screen_msg = "Screenshot failed."

            messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": screen_msg}]

            try:
                assistant_text = agent.chat(messages).strip()
                print(f"AI: {assistant_text}")
                history.append({"role": "assistant", "content": assistant_text})

                action = agent.parse_action(assistant_text)
                if action:
                    if action['action'] == 'done':
                        print("Task completed.")
                        break
                    result = agent.execute_action(action)
                    print(f"Executed: {result}")
                    history.append({"role": "user", "content": f"Executed: {result}"})
                else:
                    print("No action parsed.")
                    break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    main()
