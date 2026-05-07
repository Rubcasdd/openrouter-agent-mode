import importlib
import json
import re
import subprocess
import os
import sys
import tempfile
import base64
from io import BytesIO
from openrouter import OpenRouter

class OpenRouterAgent:
    def __init__(self, api_key: str, model: str = "tencent/hy3-preview:free"):
        self.client = OpenRouter(api_key=api_key)
        self.model = model
        self.action_history = []

    def chat(self, messages):
        print("Calling chat.send")
        response = self.client.chat.send(
            model=self.model,
            messages=messages,
            stream=False,
        )
        print("Response received")
        content = self._extract_content(response.choices[0].message.content)
        return content
    
    def encode_image_to_base64(self, image_path):
        """Convert image file to base64 for API"""
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print("Error encoding image: " + str(e))
            return None
    
    def encode_pil_image_to_base64(self, pil_image):
        """Convert PIL image to base64"""
        try:
            buffer = BytesIO()
            pil_image.save(buffer, format="PNG")
            buffer.seek(0)
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        except Exception as e:
            print("Error encoding PIL image: " + str(e))
            return None

    def _extract_content(self, content):
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if hasattr(item, "text"):
                    parts.append(item.text)
                elif isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
            return "\n".join(parts)
        return str(content)
    
    def get_mouse_position(self):
        """Get current mouse position"""
        try:
            pyautogui = importlib.import_module("pyautogui")
            x, y = pyautogui.position()
            return {"x": x, "y": y}
        except Exception as e:
            return {"x": 0, "y": 0, "error": str(e)}

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
        if action:
            return {"action": action, "value": value}
        return None

    def execute_action(self, action_dict):
        action = action_dict["action"]
        value = action_dict.get("value")

        def import_pyautogui():
            try:
                return importlib.import_module("pyautogui")
            except Exception as exc:
                raise RuntimeError("pyautogui is required for screen actions: " + str(exc))

        def import_pytesseract():
            try:
                return importlib.import_module("pytesseract")
            except Exception as exc:
                raise RuntimeError("pytesseract is required for OCR: " + str(exc))

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
                folder = os.path.dirname(value["path"])
                if folder:
                    os.makedirs(folder, exist_ok=True)
                with open(value["path"], "w", encoding="utf-8") as f:
                    f.write(value["content"])
                return f"Created file: {value['path']}"
            except Exception as e:
                return f"Failed to create file: {str(e)}"
        elif action == "create_folder":
            try:
                os.makedirs(value, exist_ok=True)
                return f"Created folder: {value}"
            except Exception as e:
                return f"Failed to create folder: {str(e)}"
        elif action == "read_file":
            try:
                with open(value, "r", encoding="utf-8") as f:
                    content = f.read(2000)
                return f"Read file {value}: {content}"
            except Exception as e:
                return f"Failed to read file: {str(e)}"
        elif action == "list_dir":
            try:
                entries = os.listdir(value)
                return f"Directory contents of {value}: {entries}"
            except Exception as e:
                return f"Failed to list directory: {str(e)}"
        elif action == "analyze_screen":
            try:
                pyautogui = importlib.import_module("pyautogui")
                screenshot = pyautogui.screenshot()
                image_base64 = self.encode_pil_image_to_base64(screenshot)
                if image_base64:
                    mouse_pos = self.get_mouse_position()
                    result = f"Screen analyzed. Image sent to AI for vision analysis. Current mouse position: {mouse_pos}"
                    self.action_history.append({"action": "analyze_screen", "result": result})
                    return result
                else:
                    return "Failed to encode screenshot"
            except Exception as e:
                return f"Failed to analyze screen: {str(e)}"
        elif action == "take_screenshot":
            try:
                pyautogui = importlib.import_module("pyautogui")
                screenshot = pyautogui.screenshot()
                temp_dir = tempfile.gettempdir()
                os.makedirs(temp_dir, exist_ok=True)
                screenshot_path = os.path.join(temp_dir, "screenshot.png")
                screenshot.save(screenshot_path)
                
                image_base64 = self.encode_pil_image_to_base64(screenshot)
                mouse_pos = self.get_mouse_position()
                
                result = f"Screenshot taken: {screenshot_path}. Mouse at: {mouse_pos}. Image encoded for AI vision."
                self.action_history.append({"action": "take_screenshot", "path": screenshot_path, "mouse": mouse_pos})
                return result
            except Exception as e:
                return f"Failed to take screenshot: {str(e)}"
        elif action == "click":
            try:
                pyautogui = import_pyautogui()
                x, y = value["x"], value["y"]
                pyautogui.click(x, y)
                result = f"Clicked at ({x}, {y})"
                self.action_history.append({"action": "click", "x": x, "y": y})
                return result
            except Exception as e:
                return f"Failed to click: {str(e)}"
        elif action == "move_mouse":
            try:
                pyautogui = import_pyautogui()
                x, y = value["x"], value["y"]
                duration = value.get("duration", 0.5)
                pyautogui.moveTo(x, y, duration=duration)
                result = f"Moved mouse to ({x}, {y})"
                self.action_history.append({"action": "move_mouse", "x": x, "y": y})
                return result
            except Exception as e:
                return f"Failed to move mouse: {str(e)}"
        elif action == "scroll":
            try:
                pyautogui = import_pyautogui()
                direction = value.get("direction", "down")  # "up" or "down"
                amount = value.get("amount", 3)
                if direction.lower() == "up":
                    pyautogui.scroll(amount)
                else:
                    pyautogui.scroll(-amount)
                result = f"Scrolled {direction} by {amount}"
                self.action_history.append({"action": "scroll", "direction": direction, "amount": amount})
                return result
            except Exception as e:
                return f"Failed to scroll: {str(e)}"
        elif action == "double_click":
            try:
                pyautogui = import_pyautogui()
                x, y = value["x"], value["y"]
                pyautogui.doubleClick(x, y)
                result = f"Double clicked at ({x}, {y})"
                self.action_history.append({"action": "double_click", "x": x, "y": y})
                return result
            except Exception as e:
                return f"Failed to double click: {str(e)}"
        elif action == "right_click":
            try:
                pyautogui = import_pyautogui()
                x, y = value["x"], value["y"]
                pyautogui.rightClick(x, y)
                result = f"Right clicked at ({x}, {y})"
                self.action_history.append({"action": "right_click", "x": x, "y": y})
                return result
            except Exception as e:
                return f"Failed to right click: {str(e)}"
        elif action == "type_text":
            try:
                pyautogui = import_pyautogui()
                pyautogui.typewrite(value)
                return f"Typed: {value}"
            except Exception as e:
                return f"Failed to type: {str(e)}"
        elif action == "execute_python":
            try:
                result = subprocess.run([sys.executable, "-c", value], capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                return f"Python executed: {output.strip()}"
            except subprocess.TimeoutExpired:
                return "Python execution timed out"
            except Exception as e:
                return f"Python execution failed: {str(e)}"
        elif action == "done":
            return "Task finished."
        else:
            return f"Unknown action: {action}"
