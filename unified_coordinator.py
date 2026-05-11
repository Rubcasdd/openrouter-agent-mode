"""
Unified AI Agent Coordinator - Runs all 4 modes in parallel
All AIs collaborate simultaneously to solve problems and choose the best approach
"""

import threading
import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime
import queue


class UnifiedAgentCoordinator:
    """Coordinates all 4 AI modes running in parallel"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.task_queue = queue.Queue()
        self.results = {
            "multi_agent": None,
            "single_agent": None,
            "overlay": None,
            "web_nav": None,
        }
        self.agents = {}
        self.running = True
        self.final_recommendation = None
        self.start_time = datetime.now()
        
        # Import all agent types
        from multi_agent import MultiAgentSystem
        from agent import OpenRouterAgent
        from screenshot_manager import ScreenshotManager
        
        self.MultiAgentSystem = MultiAgentSystem
        self.OpenRouterAgent = OpenRouterAgent
        self.ScreenshotManager = ScreenshotManager
        
        print("\n" + "="*70)
        print("🤖 UNIFIED AI AGENT COORDINATOR - ALL MODES RUNNING PARALLEL")
        print("="*70)
        print("\nInitializing all AI systems...")
        
        # Initialize all agents
        self.agents["multi_agent"] = MultiAgentSystem(api_key=api_key)
        self.agents["single_agent"] = OpenRouterAgent(api_key=api_key)
        self.agents["web_nav"] = MultiAgentSystem(api_key=api_key)
        self.agents["screenshot_mgr"] = ScreenshotManager()
        
        print("✓ All AI systems initialized and ready\n")
    
    def run_all_modes(self, user_task: str):
        """Run all 4 modes in parallel and get unified recommendation"""
        print(f"\n📋 Task: {user_task}\n")
        print("="*70)
        print("Starting all 4 AI modes in parallel...\n")
        
        # Create threads for each mode
        threads = [
            threading.Thread(target=self._run_multi_agent_mode, args=(user_task,), name="MultiAgent"),
            threading.Thread(target=self._run_single_agent_mode, args=(user_task,), name="SingleAgent"),
            threading.Thread(target=self._run_overlay_mode, args=(user_task,), name="Overlay"),
            threading.Thread(target=self._run_web_nav_mode, args=(user_task,), name="WebNav"),
        ]
        
        # Start all threads
        for thread in threads:
            thread.daemon = True
            thread.start()
        
        # Wait for all to complete with timeout
        for thread in threads:
            thread.join(timeout=30)
        
        # Analyze and combine results
        self._analyze_and_recommend()
    
    def _run_multi_agent_mode(self, task: str):
        """Mode 1: Multi-Agent Collaboration"""
        try:
            print("[1/4] 🧠 Multi-Agent Mode: Collaborating...")
            result = self.agents["multi_agent"].collaborate_on_problem(task)
            self.results["multi_agent"] = {
                "status": "success",
                "data": result,
                "weight": 0.3  # 30% weight in final decision
            }
            print("      ✓ Multi-Agent analysis complete")
        except Exception as e:
            print(f"      ✗ Error: {str(e)}")
            self.results["multi_agent"] = {"status": "error", "error": str(e), "weight": 0}
    
    def _run_single_agent_mode(self, task: str):
        """Mode 2: Single Agent with Screenshots"""
        try:
            print("[2/4] 📸 Single Agent Mode: Taking screenshots and analyzing...")
            
            # Capture screenshot
            self.agents["screenshot_mgr"].capture_screenshot("single_agent_start")
            base64_img, img_url = self.agents["screenshot_mgr"].get_screenshot_for_api()
            
            # Get response
            messages = [
                {"role": "system", "content": "You are a helpful assistant with visual understanding. Analyze the task and provide actionable steps."},
                {"role": "user", "content": f"Task: {task}"}
            ]
            
            response = self.agents["single_agent"].chat(messages)
            
            self.results["single_agent"] = {
                "status": "success",
                "data": {
                    "response": response,
                    "screenshots_taken": len(self.agents["screenshot_mgr"].screenshot_history)
                },
                "weight": 0.25  # 25% weight
            }
            print("      ✓ Single Agent analysis complete")
        except Exception as e:
            print(f"      ✗ Error: {str(e)}")
            self.results["single_agent"] = {"status": "error", "error": str(e), "weight": 0}
    
    def _run_overlay_mode(self, task: str):
        """Mode 3: Overlay Mode Analysis"""
        try:
            print("[3/4] 🖥️  Overlay Mode: Analyzing desktop context...")
            
            import os
            if os.environ.get('DISPLAY'):
                # Get desktop info
                desktop_info = "Desktop environment available with visual capabilities"
            else:
                desktop_info = "Headless environment - browser automation mode"
            
            # Get overlay-specific analysis
            system_prompt = "You are a desktop automation expert. Provide strategies for visual interface interaction."
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Task for desktop: {task}\n{desktop_info}"}
            ]
            
            response = self.agents["single_agent"].chat(messages)
            
            self.results["overlay"] = {
                "status": "success",
                "data": {
                    "response": response,
                    "overlay_capable": bool(os.environ.get('DISPLAY'))
                },
                "weight": 0.2  # 20% weight
            }
            print("      ✓ Overlay Mode analysis complete")
        except Exception as e:
            print(f"      ✗ Error: {str(e)}")
            self.results["overlay"] = {"status": "error", "error": str(e), "weight": 0}
    
    def _run_web_nav_mode(self, task: str):
        """Mode 4: Web Navigation Mode - Executes browser automation"""
        try:
            print("[4/4] 🌐 Web Navigation Mode: Executing browser automation...")
            
            # Import browser automation
            from browser_automation import AdvancedBrowserAutomation
            import asyncio
            
            # Create browser automation instance
            browser = AdvancedBrowserAutomation()
            
            # Plan the task using web navigator AI
            strategy = self.agents["multi_agent"].get_agent_response(
                "web_navigator",
                f"You are a web navigation expert. Given this task: '{task}', provide a JSON array of browser automation steps to accomplish it. Each step should have: action (goto, click, fill, extract, etc.), selector (if needed), text/value (if needed), and optional description. Focus on finding information and providing actionable results."
            )
            
            # Try to parse strategy as JSON steps
            import json
            try:
                # Extract JSON from strategy if it's wrapped in text
                if '[' in strategy and ']' in strategy:
                    json_start = strategy.find('[')
                    json_end = strategy.rfind(']') + 1
                    json_str = strategy[json_start:json_end]
                    steps = json.loads(json_str)
                else:
                    # Fallback: create basic steps
                    steps = [
                        {"action": "goto", "url": "https://www.google.com", "description": "Navigate to Google"},
                        {"action": "fill", "selector": 'input[name="q"]', "text": task, "description": "Search for the task"},
                        {"action": "click", "selector": 'input[name="btnK"]', "description": "Click search button"},
                        {"action": "wait", "ms": 2000, "description": "Wait for results"},
                        {"action": "extract", "selector": 'h3', "description": "Extract search result titles"}
                    ]
            except:
                # Default steps if parsing fails
                steps = [
                    {"action": "goto", "url": "https://www.google.com", "description": "Navigate to Google"},
                    {"action": "fill", "selector": 'input[name="q"]', "text": task, "description": "Search for the task"},
                    {"action": "click", "selector": 'input[name="btnK"]', "description": "Click search button"},
                    {"action": "wait", "ms": 2000, "description": "Wait for results"},
                    {"action": "extract", "selector": 'h3', "description": "Extract search result titles"}
                ]
            
            # Execute browser automation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(browser.multi_step_task(steps))
            loop.close()
            
            # Format results for user interaction
            if result.get("completed") and result.get("history"):
                # Extract useful information from results
                extracted_content = []
                for step_result in result["history"]:
                    if step_result.get("result") and isinstance(step_result["result"], str):
                        extracted_content.append(step_result["result"])
                
                # Get screenshot from result
                screenshot_available = result.get("screenshot", {}).get("success", False)
                screenshot_data = result.get("screenshot", {}).get("data_url") if screenshot_available else None
                
                # Create actionable response with screenshot and publishing info
                actionable_response = f"""🔍 **Web Navigation Results for: {task}**

**Steps Executed:** {result['steps_executed']}
**Status:** {'✅ Completed' if result['completed'] else '❌ Failed'}
**Screenshot:** {'📸 Captured' if screenshot_available else '❌ Failed'}

**Findings:**
{chr(10).join(['• ' + item for item in extracted_content[:5]])}

**Suggested Actions:**
1. Open browser to review results
2. Click on relevant links from search results
3. Extract specific information from found pages
4. Navigate to specific websites mentioned
5. {'View captured screenshot' if screenshot_available else 'Screenshot not available'}
6. **Publish results** - Share findings with others

**To interact:** You can ask me to:
- Open specific URLs
- Click on buttons/links by text
- Fill forms on websites
- Extract information from pages
- Take screenshots of interesting content
- Publish/share these results"""
                
                self.results["web_nav"] = {
                    "status": "success",
                    "data": {
                        "response": actionable_response,
                        "raw_result": result,
                        "screenshot_available": screenshot_available,
                        "screenshot_data": screenshot_data,
                        "actionable": True,
                        "suggested_next_steps": [
                            "Open browser to review results",
                            "Click on relevant links", 
                            "Extract specific information",
                            "Navigate to specific websites",
                            "View captured screenshot" if screenshot_available else "Screenshot capture failed",
                            "Publish/share these results"
                        ]
                    },
                    "weight": 0.25  # 25% weight
                }
                print("      ✓ Web Navigation execution complete with screenshot")
            else:
                raise Exception("Browser automation failed to produce results")
                
        except Exception as e:
            print(f"      ✗ Error: {str(e)}")
            # Fallback to planning mode if execution fails
            strategy = self.agents["multi_agent"].get_agent_response(
                "web_navigator",
                f"You are a web navigation expert. Plan how to accomplish this task using browser automation: {task}"
            )
            
            self.results["web_nav"] = {
                "status": "success",
                "data": {
                    "strategy": strategy,
                    "automation_ready": True,
                    "fallback": True
                },
                "weight": 0.25  # 25% weight
            }
            print("      ✓ Web Navigation planning complete (fallback)")
    
    def _analyze_and_recommend(self):
        """Analyze all results and provide unified recommendation"""
        print("\n" + "="*70)
        print("📊 ANALYZING ALL RESULTS AND CREATING UNIFIED RECOMMENDATION")
        print("="*70 + "\n")
        
        # Collect all successful results
        successful_results = {k: v for k, v in self.results.items() if v and v.get("status") == "success"}
        
        if not successful_results:
            print("❌ All modes failed - unable to provide recommendation")
            return
        
        # Build unified analysis prompt
        analysis_prompt = self._build_analysis_prompt()
        
        # Get final recommendation from main AI
        try:
            messages = [
                {"role": "system", "content": "You are a master AI coordinator. Analyze inputs from 4 different AI systems and provide a unified, optimal solution."},
                {"role": "user", "content": analysis_prompt}
            ]
            
            final_response = self.agents["single_agent"].chat(messages)
            self.final_recommendation = final_response
            
            print("\n" + "="*70)
            print("✅ UNIFIED RECOMMENDATION FROM ALL AI SYSTEMS")
            print("="*70 + "\n")
            print(final_response)
            print("\n" + "="*70)
            
        except Exception as e:
            print(f"❌ Error generating final recommendation: {str(e)}")
    
    def _build_analysis_prompt(self) -> str:
        """Build comprehensive analysis prompt from all results"""
        prompt = "Analyze these results from 4 AI systems and provide a unified optimal solution:\n\n"
        
        # Multi-Agent results
        if self.results["multi_agent"] and self.results["multi_agent"].get("status") == "success":
            prompt += "=== MULTI-AGENT COLLABORATION ===\n"
            data = self.results["multi_agent"]["data"]
            for key, value in data.items():
                prompt += f"• {key}: {str(value)[:200]}...\n"
            prompt += "\n"
        
        # Single Agent results
        if self.results["single_agent"] and self.results["single_agent"].get("status") == "success":
            prompt += "=== SINGLE AGENT ANALYSIS ===\n"
            prompt += f"Response: {self.results['single_agent']['data'].get('response')[:300]}...\n\n"
        
        # Overlay results
        if self.results["overlay"] and self.results["overlay"].get("status") == "success":
            prompt += "=== OVERLAY/DESKTOP ANALYSIS ===\n"
            prompt += f"Strategy: {self.results['overlay']['data'].get('response')[:300]}...\n\n"
        
        # Web Nav results
        if self.results["web_nav"] and self.results["web_nav"].get("status") == "success":
            prompt += "=== WEB NAVIGATION STRATEGY ===\n"
            prompt += f"Plan: {self.results['web_nav']['data'].get('strategy')[:300]}...\n\n"
        
        prompt += "\nProvide a UNIFIED recommendation that combines the best insights from all 4 AI systems."
        prompt += "\nChoose and explain which approach is best for this task."
        
        return prompt
    
    def print_status_dashboard(self):
        """Print real-time status of all modes"""
        print("\n" + "="*70)
        print("📈 REAL-TIME STATUS DASHBOARD")
        print("="*70)
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        for mode, result in self.results.items():
            if result:
                status = "✅ " if result.get("status") == "success" else "❌ "
                print(f"{status} {mode.upper()}: {result.get('status')}")
            else:
                print(f"⏳ {mode.upper()}: Running...")
        
        print(f"\nElapsed time: {elapsed:.2f}s")
        print("="*70 + "\n")
    
    def get_all_results_summary(self) -> Dict[str, Any]:
        """Get summary of all results"""
        return {
            "timestamp": datetime.now().isoformat(),
            "multi_agent": self.results.get("multi_agent"),
            "single_agent": self.results.get("single_agent"),
            "overlay": self.results.get("overlay"),
            "web_nav": self.results.get("web_nav"),
            "final_recommendation": self.final_recommendation,
            "elapsed_seconds": (datetime.now() - self.start_time).total_seconds()
        }
