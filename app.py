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

DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
FALLBACK_MODELS = ["nvidia/nemotron-3-super-120b-a12b:free"]

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
    print(f"Using AI Model: {DEFAULT_MODEL}")
    print("AI will use browser automation for web tasks and screenshots...\n")
    
    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() in ["exit", "quit"]:
            break

        history = [{"role": "user", "content": user_text}]
        print("\n🌐 Starting web browsing with screenshots...")
        
        # Try unified coordinator with browser automation
        try:
            from unified_coordinator import UnifiedAgentCoordinator
            coordinator = UnifiedAgentCoordinator(api_key=api_key)
            coordinator.run_all_modes(user_text)
            print("\n✅ Task completed\n")
            continue
        except Exception as e:
            print(f"Browser mode failed: {e}. Falling back to standard chat...")
        
        print("Starting multi-step analysis...")

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
                    print("No DISPLAY - skipping screenshot. Using browser automation for web tasks.")
                    image_message = {"role": "user", "content": "No display available for screenshot. Use browser actions for web tasks."}
            except Exception as e:
                print("Screenshot error: " + str(e))
                image_message = {"role": "user", "content": "Screenshot failed."}

            if not image_message:
                image_message = {"role": "user", "content": "No screen data available."}
            
            messages = [{"role": "system", "content": system_prompt}] + history + [image_message]

            try:
                # Step 1: Get conversational response from AI
                assistant_text = agent.chat(messages).strip()
                print("\nAI Response:")
                
                # Step 2: Extract and display the natural language part
                nl_response = agent.extract_natural_language_response(assistant_text)
                if nl_response:
                    print(nl_response)
                    history.append({"role": "assistant", "content": nl_response})
                
                # Step 3: Extract action
                action_text = agent.get_action_from_response(assistant_text, system_prompt)
                
                if action_text:
                    action = agent.parse_action(action_text)
                    if action:
                        if action['action'] == 'done':
                            print("\nTask completed.")
                            break
                        print(f"\nExecuting: {action['action']}")
                        result = agent.execute_action(action)
                        print(f"Result: {result}")
                        history.append({"role": "user", "content": "Executed: " + str(result)})
                        
                        # Step 4: Get final conversational answer from AI
                        final_prompt = f"The action has been executed. Result: {result}\n\nNow provide a final conversational answer to the user based on this result."
                        final_messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": final_prompt}]
                        final_response = agent.chat(final_messages).strip()
                        
                        # Extract only the natural language part
                        final_nl = agent.extract_natural_language_response(final_response)
                        if final_nl:
                            print(f"\nFinal Answer:\n{final_nl}")
                            history.append({"role": "assistant", "content": final_nl})
                        else:
                            # If no NL part, use the whole response
                            print(f"\nFinal Answer:\n{final_response}")
                            history.append({"role": "assistant", "content": final_response})
                    else:
                        print("No action parsed from response.")
                        break
                else:
                    print("Could not extract action from AI response.")
                    # If no action but there was NL response, continue
                    if not nl_response:
                        break
            except Exception as e:
                print("Error: " + str(e))
                break

if __name__ == "__main__":
    main()
