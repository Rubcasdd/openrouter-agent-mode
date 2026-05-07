import json
import re
import requests

OPENROUTER_CHAT_URL = "https://api.openrouter.ai/v1/chat/completions"

class OpenRouterAgent:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def chat(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 500,
        }

        response = requests.post(OPENROUTER_CHAT_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        if not data.get("choices"):
            raise RuntimeError("No completion choices returned from OpenRouter.")

        message = data["choices"][0].get("message", {})
        return message.get("content", "")

    def parse_action(self, text: str):
        json_text = self._find_json_object(text)
        if not json_text:
            return None

        try:
            parsed = json.loads(json_text)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        action = parsed.get("action")
        value = parsed.get("value")
        if action and value:
            return {"action": action, "value": value}
        return None

    def _find_json_object(self, text: str):
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        return match.group(0) if match else None
