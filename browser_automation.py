"""
Advanced Browser Automation - Enhanced multi-step web task execution
Supports complex scenarios: form filling, multi-page navigation, 
button clicking, content extraction, and dynamic waits
"""

import asyncio
import json
import base64
from datetime import datetime
from typing import List, Dict, Any


class AdvancedBrowserAutomation:
    """Advanced browser automation for multi-step tasks"""
    
    def __init__(self):
        self.page = None
        self.browser = None
        self.session_history = []
    
    async def multi_step_task(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multi-step browser tasks"""
        from playwright.async_api import async_playwright
        
        results = {
            "completed": True,
            "steps_executed": 0,
            "final_content": None,
            "errors": [],
            "history": []
        }
        
        try:
            async with async_playwright() as p:
                self.browser = await p.chromium.launch(headless=True)
                self.page = await self.browser.new_page()
                
                for i, step in enumerate(steps, 1):
                    step_result = await self._execute_step(step)
                    results["steps_executed"] = i
                    results["history"].append(step_result)
                    
                    if "error" in step_result and step_result.get("critical", False):
                        results["completed"] = False
                        results["errors"].append(step_result["error"])
                        break
                
                # Capture final page state
                results["final_content"] = await self.page.content()
                
                await self.browser.close()
        except Exception as e:
            results["completed"] = False
            results["errors"].append(str(e))
        
        return results
    
    async def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step in a multi-step task"""
        action = step.get("action")
        
        result = {
            "action": action,
            "success": False,
            "result": None
        }
        
        try:
            if action == "goto":
                url = step.get("url")
                result["result"] = await self._goto(url, step.get("timeout", 10000))
            
            elif action == "click":
                selector = step.get("selector")
                result["result"] = await self._click(selector, step.get("wait_for", None))
            
            elif action == "fill":
                selector = step.get("selector")
                text = step.get("text")
                result["result"] = await self._fill(selector, text)
            
            elif action == "select":
                selector = step.get("selector")
                value = step.get("value")
                result["result"] = await self._select(selector, value)
            
            elif action == "submit_form":
                selector = step.get("selector")
                result["result"] = await self._submit_form(selector)
            
            elif action == "wait":
                ms = step.get("ms", 1000)
                await self.page.wait_for_timeout(ms)
                result["result"] = f"Waited {ms}ms"
            
            elif action == "extract":
                selector = step.get("selector")
                result["result"] = await self._extract_text(selector)
            
            elif action == "scroll":
                direction = step.get("direction", "down")
                amount = step.get("amount", 300)
                result["result"] = await self._scroll(direction, amount)
            
            elif action == "take_screenshot":
                path = step.get("path", f"/tmp/screenshot_{len(self.session_history)}.png")
                result["result"] = await self._take_screenshot(path)
            
            elif action == "evaluate":
                script = step.get("script")
                result["result"] = await self.page.evaluate(script)
            
            elif action == "navigate_by_link":
                link_text = step.get("link_text")
                result["result"] = await self._click_link_by_text(link_text)
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            result["critical"] = step.get("critical", False)
        
        self.session_history.append(result)
        return result
    
    async def _goto(self, url: str, timeout: int) -> str:
        """Navigate to a URL"""
        await self.page.goto(url, timeout=timeout)
        await self.page.wait_for_timeout(1000)
        return f"Navigated to {url}"
    
    async def _click(self, selector: str, wait_for: str = None) -> str:
        """Click an element"""
        try:
            await self.page.click(selector)
            if wait_for:
                await self.page.wait_for_selector(wait_for, timeout=10000)
            else:
                await self.page.wait_for_timeout(1000)
            return f"Clicked {selector}"
        except:
            # Try by text if selector fails
            try:
                await self.page.click(f'button:has-text("{selector}")')
                return f"Clicked button with text: {selector}"
            except:
                raise Exception(f"Could not click element: {selector}")
    
    async def _fill(self, selector: str, text: str) -> str:
        """Fill a form field"""
        await self.page.fill(selector, text)
        return f"Filled {selector} with: {text}"
    
    async def _select(self, selector: str, value: str) -> str:
        """Select from a dropdown"""
        await self.page.select_option(selector, value)
        return f"Selected {value} in {selector}"
    
    async def _submit_form(self, selector: str = None) -> str:
        """Submit a form"""
        if selector:
            await self.page.click(f'{selector}[type="submit"]')
        else:
            await self.page.click('button[type="submit"]')
        await self.page.wait_for_timeout(2000)
        return "Form submitted"
    
    async def _extract_text(self, selector: str) -> str:
        """Extract text from elements"""
        elements = await self.page.query_selector_all(selector)
        texts = []
        for el in elements:
            text = await el.inner_text()
            texts.append(text)
        return "\n".join(texts)
    
    async def _scroll(self, direction: str, amount: int) -> str:
        """Scroll the page"""
        if direction == "down":
            await self.page.keyboard.press("End") if amount > 500 else await self.page.evaluate(f"window.scrollBy(0, {amount})")
        elif direction == "up":
            await self.page.evaluate(f"window.scrollBy(0, -{amount})")
        
        return f"Scrolled {direction} by {amount}px"
    
    async def _take_screenshot(self, path: str) -> str:
        """Take a screenshot"""
        await self.page.screenshot(path=path)
        return f"Screenshot saved to {path}"
    
    async def take_and_return_screenshot(self) -> Dict[str, Any]:
        """Take a screenshot and return it as base64 for immediate use"""
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"/tmp/browser_screenshot_{timestamp}.png"
        
        # Take screenshot
        await self.page.screenshot(path=screenshot_path, full_page=True)
        
        # Read and encode as base64
        with open(screenshot_path, "rb") as image_file:
            base64_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        return {
            "success": True,
            "screenshot_path": screenshot_path,
            "base64": base64_data,
            "data_url": f"data:image/png;base64,{base64_data}",
            "timestamp": timestamp
        }
    
    async def _click_link_by_text(self, link_text: str) -> str:
        """Click a link by its text content"""
        await self.page.click(f'a:has-text("{link_text}")')
        await self.page.wait_for_timeout(2000)
        return f"Clicked link: {link_text}"
    
    async def intelligent_scrape(self, url: str, goal: str) -> Dict[str, Any]:
        """Intelligently scrape a site based on a goal"""
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(url, timeout=10000)
            
            # Get page structure
            page_structure = await page.evaluate("""
            () => {
                return {
                    title: document.title,
                    url: window.location.href,
                    headings: Array.from(document.querySelectorAll('h1, h2, h3'))
                        .slice(0, 10)
                        .map(h => h.textContent),
                    buttons: Array.from(document.querySelectorAll('button, a.btn'))
                        .slice(0, 10)
                        .map(b => ({text: b.textContent, type: b.tagName})),
                    inputs: Array.from(document.querySelectorAll('input, textarea, select'))
                        .slice(0, 10)
                        .map(i => ({name: i.name, type: i.type})),
                    text_preview: document.body.innerText.slice(0, 3000)
                };
            }
            """)
            
            await browser.close()
            
            return {
                "goal": goal,
                "page_structure": page_structure,
                "suggested_actions": _generate_actions(goal, page_structure)
            }


def _generate_actions(goal: str, page_structure: Dict) -> List[Dict]:
    """Generate suggested browser actions based on goal and page structure"""
    actions = []
    goal_lower = goal.lower()
    
    # Look for relevant buttons
    for button in page_structure.get("buttons", [])[:3]:
        text = button.get("text", "").lower()
        if any(keyword in text for keyword in ["search", "find", "submit", "create", "add"]):
            actions.append({
                "action": "click",
                "selector": f'button:has-text("{button.get("text")}")',
                "reason": f"Found relevant button: {button.get('text')}"
            })
    
    # Look for relevant form inputs
    for input_field in page_structure.get("inputs", []):
        if input_field.get("type") in ["text", "email", "search"]:
            actions.append({
                "action": "fill",
                "selector": f'input[name="{input_field.get("name")}"]',
                "text": goal,
                "reason": f"Found input field: {input_field.get('name')}"
            })
    
    return actions
