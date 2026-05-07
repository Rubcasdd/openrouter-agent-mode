import json
import re
import subprocess
import os
from openrouter import OpenRouter

class OpenRouterAgent:
    def __init__(self, api_key: str, model: str = "tencent/hy3-preview:free"):
        self.client = OpenRouter(api_key=api_key)
        self.model = model

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content

    def parse_action(self, text: str):
        # First, try to find JSON in code blocks
        import re
        code_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if code_block_match:
            json_text = code_block_match.group(1)
        else:
            # Fallback to plain JSON
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            json_text = json_match.group(0) if json_match else None

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

    def execute_action(self, action_dict):
        action = action_dict["action"]
        value = action_dict["value"]

        if action == "open_url":
            import webbrowser
            webbrowser.open(value, new=2)
            return f"Opened URL: {value}"
        elif action == "search":
            import webbrowser
            from urllib.parse import quote
            search_url = f"https://www.google.com/search?q={quote(value)}"
            webbrowser.open(search_url, new=2)
            return f"Opened search for: {value}"
        elif action == "run_command":
            try:
                result = subprocess.run(value, shell=True, capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                return f"Command output: {output.strip()}"
            except subprocess.TimeoutExpired:
                return "Command timed out"
            except Exception as e:
                return f"Command failed: {str(e)}"
        elif action == "open_file":
            try:
                os.startfile(value)  # Windows
                return f"Opened file: {value}"
            except AttributeError:
                try:
                    subprocess.run(["xdg-open", value])  # Linux
                    return f"Opened file: {value}"
                except:
                    try:
                        subprocess.run(["open", value])  # macOS
                        return f"Opened file: {value}"
                    except:
                        return f"Could not open file: {value}"
        elif action == "create_file":
            try:
                with open(value["path"], "w") as f:
                    f.write(value["content"])
                return f"Created file: {value['path']}"
            except Exception as e:
                return f"Failed to create file: {str(e)}"
        else:
            return f"Unknown action: {action}"
