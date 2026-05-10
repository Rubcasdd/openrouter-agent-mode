import importlib
import json
import re
import subprocess
import os
import sys
import tempfile
import base64
import asyncio
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

    def extract_natural_language_response(self, text: str):
        """Extract the natural language part of the response (before the JSON)"""
        # Find where JSON starts
        json_match = re.search(r'```(?:json)?\s*\{', text)
        if json_match:
            # Everything before the code block is NL response
            nl_part = text[:json_match.start()].strip()
            return nl_part if nl_part else None
        
        # If no code block, check for plain JSON
        json_match = re.search(r'\{\s*"action"', text)
        if json_match:
            nl_part = text[:json_match.start()].strip()
            return nl_part if nl_part else None
        
        return None

    def execute_action(self, action_dict):
        action = action_dict["action"]
        value = action_dict.get("value")

        if action == "browser_search":
            try:
                result = self.run_async(self.browser_search(value))
                return f"Search results: {result}"
            except Exception as e:
                return f"Browser search error: {str(e)}"
        elif action == "browser_visit":
            try:
                url = value.get("url") if isinstance(value, dict) else value
                task = value.get("task", "Browse the page") if isinstance(value, dict) else "Browse the page"
                result = self.run_async(self.browser_visit_url(url, task))
                return f"Browser visit result: {result}"
            except Exception as e:
                return f"Browser visit error: {str(e)}"
        elif action == "browser_extract":
            try:
                url = value.get("url") if isinstance(value, dict) else ""
                info = value.get("info") if isinstance(value, dict) else value
                result = self.run_async(self.browser_extract_info(url, info))
                return f"Extracted information: {result}"
            except Exception as e:
                return f"Browser extraction error: {str(e)}"
        elif action == "browser_click":
            try:
                url = value.get("url") if isinstance(value, dict) else ""
                selector = value.get("selector") if isinstance(value, dict) else str(value)
                result = self.run_async(self.browser_click_element(url, selector))
                return result
            except Exception as e:
                return f"Browser click error: {str(e)}"
        elif action == "browser_fill_form":
            try:
                url = value.get("url") if isinstance(value, dict) else ""
                form_data = value.get("data") if isinstance(value, dict) else str(value)
                result = self.run_async(self.browser_fill_form(url, form_data))
                return result
            except Exception as e:
                return f"Browser form error: {str(e)}"
        elif action == "browser_analyze":
            try:
                url = value if isinstance(value, str) else value.get("url", "")
                result = self.run_async(self.browser_analyze_page(url))
                return result
            except Exception as e:
                return f"Page analysis error: {str(e)}"
        elif action == "done":
            return "Task finished."
        else:
            return f"Unknown action: {action}"

    async def browser_search(self, query: str):
        """Search the web using Playwright and Chrome"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Google search
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                await page.goto(search_url, timeout=10000)
                await page.wait_for_timeout(2000)  # Wait for results to load
                
                # Extract search results
                results = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('h3');
                    return Array.from(items).slice(0, 5).map(h => h.textContent).filter(t => t);
                }
                """)
                
                await browser.close()
                return f"Search results for '{query}':\n" + "\n".join(results[:5])
        except Exception as e:
            return f"Browser search failed: {str(e)}"

    async def browser_visit_url(self, url: str, task_description: str = "Get page content"):
        """Visit a URL and extract full content including clickable elements using Playwright"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                await page.wait_for_timeout(2000)
                
                # Get page structure and elements
                page_data = await page.evaluate("""
                () => {
                    const getElements = (selector, limit = 10) => {
                        return Array.from(document.querySelectorAll(selector))
                            .slice(0, limit)
                            .map((el, idx) => ({
                                id: idx,
                                text: el.textContent?.slice(0, 100) || '',
                                tag: el.tagName
                            }));
                    };
                    
                    return {
                        title: document.title,
                        url: window.location.href,
                        buttons: getElements('button, [role="button"]'),
                        links: getElements('a[href]', 5),
                        forms: getElements('form', 3),
                        headings: getElements('h1, h2, h3', 5),
                        bodyText: document.body.innerText.slice(0, 2000)
                    };
                }
                """)
                
                await browser.close()
                
                # Format response with interactive elements
                result = f"""Page: {page_data['title']}
URL: {page_data['url']}

=== BUTTONS ===
"""
                for btn in page_data['buttons']:
                    result += f"[{btn['id']}] {btn['text']}\n"
                
                result += """
=== LINKS ===
"""
                for link in page_data['links']:
                    result += f"[{link['id']}] {link['text']}\n"
                
                result += f"""
=== HEADINGS ===
"""
                for heading in page_data['headings']:
                    result += f"- {heading['text']}\n"
                
                result += f"""
=== PAGE CONTENT ===
{page_data['bodyText']}

Use 'browser_click' action to click buttons/links by their ID number."""
                
                return result
        except Exception as e:
            return f"Browser visit failed: {str(e)}"

    async def browser_extract_info(self, url: str, info_to_extract: str):
        """Visit a URL and extract specific information, with page analysis"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                await page.wait_for_timeout(2000)
                
                # Extract structured page info
                page_info = await page.evaluate("""
                () => ({
                    title: document.title,
                    description: document.querySelector('meta[name="description"]')?.content || '',
                    allText: document.body.innerText,
                    headings: Array.from(document.querySelectorAll('h1, h2, h3, h4'))
                        .map(h => h.textContent)
                        .slice(0, 10),
                    images: Array.from(document.querySelectorAll('img'))
                        .slice(0, 5)
                        .map(img => ({alt: img.alt, src: img.src})),
                    links: Array.from(document.querySelectorAll('a'))
                        .slice(0, 10)
                        .map(a => ({text: a.textContent, href: a.href}))
                })
                """)
                
                await browser.close()
                
                # Format extracted info
                result = f"""
=== PAGE INFORMATION ===
Title: {page_info['title']}
Description: {page_info['description']}

=== HEADINGS ===
"""
                for heading in page_info['headings']:
                    result += f"- {heading}\n"
                
                result += f"""
=== AVAILABLE LINKS ===
"""
                for i, link in enumerate(page_info['links']):
                    result += f"[{i}] {link['text']} -> {link['href']}\n"
                
                result += f"""
=== CONTENT RELEVANT TO: {info_to_extract} ===
{page_info['allText'][:1500]}
"""
                return result
        except Exception as e:
            return f"Browser extraction failed: {str(e)}"

    async def browser_click_element(self, url: str, element_selector: str):
        """Click a button or element on a page"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                await page.wait_for_timeout(1000)
                
                # Try to click the element
                try:
                    await page.click(element_selector)
                    await page.wait_for_timeout(2000)
                except:
                    return f"Could not find or click element: {element_selector}"
                
                # Get updated page content after click
                content = await page.evaluate("() => document.body.innerText")
                
                await browser.close()
                return f"Clicked element. Page content after click:\n{content[:1500]}"
        except Exception as e:
            return f"Browser click failed: {str(e)}"

    async def browser_fill_form(self, url: str, form_data: str):
        """Fill and submit a form on a page"""
        try:
            from playwright.async_api import async_playwright
            import json
            
            # Parse form data (should be JSON like {"field_name": "value"})
            try:
                data = json.loads(form_data)
            except:
                data = {}
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                await page.wait_for_timeout(1000)
                
                # Fill form fields
                for field_name, value in data.items():
                    try:
                        await page.fill(f'input[name="{field_name}"]', value)
                    except:
                        try:
                            await page.fill(f'[name="{field_name}"]', value)
                        except:
                            pass
                
                # Submit form
                try:
                    await page.click('button[type="submit"]')
                except:
                    await page.click('input[type="submit"]')
                
                await page.wait_for_timeout(2000)
                content = await page.evaluate("() => document.body.innerText")
                
                await browser.close()
                return f"Form submitted. Result page:\n{content[:1500]}"
        except Exception as e:
            return f"Browser form submission failed: {str(e)}"

    async def browser_analyze_page(self, url: str):
        """Get detailed analysis of a page - elements, structure, interactive components"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                await page.wait_for_timeout(2000)
                
                # Comprehensive page analysis
                analysis = await page.evaluate("""
                () => {
                    const analyzeElements = () => {
                        return {
                            buttons: Array.from(document.querySelectorAll('button, [role="button"]'))
                                .slice(0, 15)
                                .map((el, idx) => ({
                                    id: idx,
                                    text: el.textContent?.slice(0, 50) || '(empty)',
                                    ariaLabel: el.getAttribute('aria-label'),
                                    class: el.className
                                })),
                            clickableLinks: Array.from(document.querySelectorAll('a[href]'))
                                .slice(0, 10)
                                .map((el, idx) => ({
                                    id: idx,
                                    text: el.textContent?.slice(0, 50) || '(empty)',
                                    href: el.href
                                })),
                            forms: Array.from(document.querySelectorAll('form'))
                                .slice(0, 5)
                                .map((form, idx) => ({
                                    id: idx,
                                    inputs: Array.from(form.querySelectorAll('input, textarea, select'))
                                        .map(inp => ({
                                            name: inp.name,
                                            type: inp.type,
                                            label: inp.previousElementSibling?.textContent || ''
                                        }))
                                })),
                            pageStructure: {
                                title: document.title,
                                url: window.location.href,
                                headers: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => h.textContent).slice(0, 5),
                                hasSearch: !!document.querySelector('input[type="search"], input[placeholder*="search" i]'),
                                hasLogin: !!document.querySelector('input[type="password"]')
                            },
                            totalElements: document.querySelectorAll('*').length,
                            allText: document.body.innerText.slice(0, 2000)
                        };
                    };
                    return analyzeElements();
                }
                """)
                
                await browser.close()
                
                # Format comprehensive analysis
                result = f"""
=== PAGE ANALYSIS ===
Title: {analysis['pageStructure']['title']}
URL: {analysis['pageStructure']['url']}
Total Elements: {analysis['totalElements']}

=== CLICKABLE BUTTONS ===
"""
                for btn in analysis['buttons'][:10]:
                    result += f"[BTN {btn['id']}] {btn['text']}\n"
                
                result += f"""
=== LINKS ===
"""
                for link in analysis['clickableLinks'][:10]:
                    result += f"[LINK {link['id']}] {link['text']} -> {link['href']}\n"
                
                result += f"""
=== FORMS & INPUT FIELDS ===
"""
                for form in analysis['forms']:
                    result += f"Form {form['id']}:\n"
                    for inp in form['inputs']:
                        result += f"  - {inp['name']} ({inp['type']}): {inp['label']}\n"
                
                result += f"""
=== PAGE FEATURES ===
Has Search: {analysis['pageStructure']['hasSearch']}
Has Login: {analysis['pageStructure']['hasLogin']}

=== CONTENT ===
{analysis['allText']}

=== HOW TO INTERACT ===
Use actions:
- 'browser_click' to click buttons/links by their ID
- 'browser_fill_form' to fill and submit forms
- 'browser_visit' to navigate to a link
"""
                return result
        except Exception as e:
            return f"Page analysis failed: {str(e)}"

    def run_async(self, coro):
        """Helper to run async functions"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

    def get_action_from_response(self, ai_response, system_prompt):
        """Make separate API call to extract action from AI response"""
        print("Extracting action from AI response")
        
        action_prompt = str(system_prompt) + "\n\nBased on the following response, respond with ONLY a JSON action object (or {\"action\":\"done\"} if task is complete):\n\n" + str(ai_response)
        
        messages = [{"role": "user", "content": action_prompt}]
        
        try:
            response = self.client.chat.send(
                model=self.model,
                messages=messages,
                stream=False,
            )
            action_text = self._extract_content(response.choices[0].message.content)
            print("Action extracted: " + str(action_text))
            return action_text
        except Exception as e:
            print("Error extracting action: " + str(e))
            return None
