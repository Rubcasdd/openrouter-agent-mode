import os
from agent import OpenRouterAgent

DEFAULT_MODEL = "tencent/hy3-preview:free"
FALLBACK_MODELS = ["tencent/hy3-preview:free"]

PROFILES = {
    "assistant": "You are a helpful assistant.",
    "coder": "You are a coding expert.",
    "agent": (
        "You are a local PC assistant. "
        "If the user asks you to perform an action on their computer, respond ONLY with a JSON object in this format:\n"
        "{\"action\":\"open_url\",\"value\":\"https://example.com\"}\n"
        "Available actions: open_url, search, run_command, open_file, create_file\n"
        "For create_file, value is {\"path\":\"file.txt\",\"content\":\"text\"}\n"
        "Do not include any other text in your response when performing an action."
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

        history.append({"role": "user", "content": user_text})
        messages = [{"role": "system", "content": system_prompt}] + history

        try:
            assistant_text = agent.chat(messages).strip()
            print(f"AI: {assistant_text}")
            history.append({"role": "assistant", "content": assistant_text})

            action = agent.parse_action(assistant_text)
            if action:
                result = agent.execute_action(action)
                print(f"Executed: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
