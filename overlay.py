"""
Futuristic desktop overlay for AI agent with vision capabilities.
Provides real-time screen analysis, mouse tracking, and smooth animations.
"""

import os
import subprocess
import sys
import threading
import time
import importlib
import base64
import tempfile
from io import BytesIO


def ensure_dependencies():
    required = ["pyautogui", "PIL", "openrouter"]
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)

    if missing:
        print("Installing missing dependencies: " + ", ".join(missing))
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        except subprocess.CalledProcessError as exc:
            raise RuntimeError("Failed to install required dependencies. Please run 'pip install -r requirements.txt' manually.")


ensure_dependencies()

try:
    import tkinter as tk
    from tkinter import font as tkfont
    from PIL import Image, ImageDraw, ImageTk
except ImportError:
    raise ImportError("tkinter and PIL are required. Install with: pip install pillow")


class OverlayAgent:
    """Futuristic overlay agent with vision and mouse tracking"""
    
    def __init__(self, api_key, system_prompt):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.running = True
        self.action_queue = []
        self.screen_state = "initializing"
        self.mouse_x, self.mouse_y = 0, 0
        self.analysis_text = "Initializing AI agent..."
        self.action_history = []
        
        # Import agent
        from agent import OpenRouterAgent
        self.agent = OpenRouterAgent(api_key=api_key)
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("OpenRouter Agent - Desktop Mode")
        self.root.attributes('-topmost', True)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup futuristic UI"""
        # Get screen size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Window setup - quarter of screen
        window_width = self.screen_width // 3
        window_height = self.screen_height // 4
        self.root.geometry(f"{window_width}x{window_height}+{self.screen_width - window_width - 20}+20")
        
        # Dark theme with cyan accents (futuristic)
        bg_color = "#0a0e27"
        accent_color = "#00d9ff"
        text_color = "#ffffff"
        secondary_bg = "#1a1f3a"
        
        self.root.configure(bg=bg_color)
        
        # Main frame with gradient-like appearance
        main_frame = tk.Frame(self.root, bg=bg_color, relief=tk.FLAT, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Header with title and status
        header_frame = tk.Frame(main_frame, bg=secondary_bg, height=50)
        header_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_font = tkfont.Font(family="Courier", size=10, weight="bold")
        status_font = tkfont.Font(family="Courier", size=8)
        
        title_label = tk.Label(header_frame, text="⚡ NEURAL AGENT", font=title_font, 
                              bg=secondary_bg, fg=accent_color)
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.status_label = tk.Label(header_frame, text="○ READY", font=status_font,
                                     bg=secondary_bg, fg="#00ff00")
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Analysis/Output area with scrolling
        output_frame = tk.Frame(main_frame, bg=secondary_bg)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(output_frame, bg=secondary_bg, troughcolor=bg_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output_text = tk.Text(output_frame, bg=bg_color, fg=text_color,
                                   font=tkfont.Font(family="Courier", size=7),
                                   yscrollcommand=scrollbar.set, relief=tk.FLAT, bd=0,
                                   padx=8, pady=8, wrap=tk.WORD)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)
        
        # Mouse tracker display
        tracker_frame = tk.Frame(main_frame, bg=secondary_bg, height=30)
        tracker_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        tracker_frame.pack_propagate(False)
        
        tracker_label = tk.Label(tracker_frame, text="MOUSE: ", font=status_font,
                                bg=secondary_bg, fg=accent_color)
        tracker_label.pack(side=tk.LEFT, padx=8, pady=5)
        
        self.mouse_label = tk.Label(tracker_frame, text="(0, 0)", font=status_font,
                                   bg=secondary_bg, fg=text_color)
        self.mouse_label.pack(side=tk.LEFT, padx=0, pady=5)
        
        actions_label = tk.Label(tracker_frame, text="ACTIONS: ", font=status_font,
                                bg=secondary_bg, fg=accent_color)
        actions_label.pack(side=tk.LEFT, padx=(40, 0), pady=5)
        
        self.action_count_label = tk.Label(tracker_frame, text="0", font=status_font,
                                          bg=secondary_bg, fg="#00ff00")
        self.action_count_label.pack(side=tk.LEFT, padx=0, pady=5)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.pack(fill=tk.X, padx=0, pady=(0, 5))
        
        self.start_button = tk.Button(button_frame, text="START AGENT", 
                                     command=self.start_agent,
                                     bg=accent_color, fg=bg_color, font=tkfont.Font(family="Courier", size=8, weight="bold"),
                                     relief=tk.FLAT, padx=10, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        stop_button = tk.Button(button_frame, text="STOP", 
                               command=self.stop_overlay,
                               bg="#ff0040", fg=text_color, font=tkfont.Font(family="Courier", size=8),
                               relief=tk.FLAT, padx=10, pady=5)
        stop_button.pack(side=tk.LEFT, padx=5)
        
        # Color scheme for tags
        self.output_text.tag_config("info", foreground=accent_color)
        self.output_text.tag_config("success", foreground="#00ff00")
        self.output_text.tag_config("warning", foreground="#ffaa00")
        self.output_text.tag_config("error", foreground="#ff0040")
        self.output_text.tag_config("action", foreground="#00ffff")
        
        self.log_message("System initialized", "info")
        self.log_message("Ready to analyze screen and interact", "success")
        
    def log_message(self, message, tag="info"):
        """Add timestamped message to output"""
        timestamp = time.strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] ", "info")
        self.output_text.insert(tk.END, message + "\n", tag)
        self.output_text.see(tk.END)
        self.output_text.update()
        
    def update_mouse_position(self):
        """Update mouse position display"""
        try:
            pyautogui = importlib.import_module("pyautogui")
            x, y = pyautogui.position()
            self.mouse_x = x
            self.mouse_y = y
            self.mouse_label.config(text=f"({x}, {y})")
        except:
            pass
        
    def run_agent_loop(self, user_task):
        """Main agent execution loop"""
        self.log_message(f"Task: {user_task}", "action")
        self.status_label.config(text="● ACTIVE", fg="#00ff00")
        
        history = [{"role": "user", "content": user_task}]
        step_count = 0
        max_steps = 10
        
        while self.running and step_count < max_steps:
            step_count += 1
            self.log_message(f"--- Step {step_count} ---", "info")
            
            # Update mouse position
            self.update_mouse_position()
            
            try:
                # Take screenshot
                pyautogui = importlib.import_module("pyautogui")
                screenshot = pyautogui.screenshot()
                
                # Encode to base64
                image_base64 = self.agent.encode_pil_image_to_base64(screenshot)
                mouse_pos = self.agent.get_mouse_position()
                
                screen_msg = f"Current screen. Mouse at: {mouse_pos}. Analyze and decide next action."
                
                # Prepare message with image
                image_message = {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": screen_msg},
                        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_base64}}
                    ]
                }
                
                messages = [
                    {"role": "system", "content": self.system_prompt}
                ] + history + [image_message]
                
                # Get AI response
                self.log_message("Analyzing screen...", "info")
                assistant_text = self.agent.chat(messages).strip()
                history.append({"role": "assistant", "content": assistant_text})
                
                # Parse action
                action = self.agent.parse_action(assistant_text)
                if action:
                    action_name = action.get('action', 'unknown')
                    self.log_message(f"Action: {action_name}", "action")
                    
                    if action_name == 'done':
                        self.log_message("Task completed!", "success")
                        break
                    
                    # Execute action
                    result = self.agent.execute_action(action)
                    self.log_message(f"Result: {result[:100]}", "success")
                    history.append({"role": "user", "content": f"Executed: {result}"})
                    
                    self.action_history.append(action_name)
                    self.action_count_label.config(text=str(len(self.action_history)))
                    
                    # Small delay for smooth animation
                    time.sleep(0.5)
                else:
                    self.log_message("Could not parse action", "warning")
                    break
                    
            except Exception as e:
                self.log_message(f"Error: {str(e)}", "error")
                break
        
        if step_count >= max_steps:
            self.log_message("Max steps reached", "warning")
        
        self.status_label.config(text="○ READY", fg="#00ff00")
        self.start_button.config(state=tk.NORMAL)
        
    def start_agent(self):
        """Start agent task"""
        self.start_button.config(state=tk.DISABLED)
        
        # Create a simple task input window
        task_window = tk.Toplevel(self.root)
        task_window.title("Input Task")
        task_window.geometry("400x150")
        task_window.configure(bg="#0a0e27")
        
        tk.Label(task_window, text="Enter task:", bg="#0a0e27", fg="#00d9ff",
                font=tkfont.Font(family="Courier", size=10)).pack(pady=10)
        
        task_entry = tk.Entry(task_window, font=tkfont.Font(family="Courier", size=10),
                             bg="#1a1f3a", fg="#ffffff", insertbackground="#00d9ff")
        task_entry.pack(fill=tk.X, padx=20, pady=10)
        task_entry.focus()
        
        def execute_task():
            task = task_entry.get().strip()
            if task:
                task_window.destroy()
                # Run agent in background thread
                thread = threading.Thread(target=self.run_agent_loop, args=(task,), daemon=True)
                thread.start()
            else:
                self.start_button.config(state=tk.NORMAL)
        
        tk.Button(task_window, text="Execute", command=execute_task,
                 bg="#00d9ff", fg="#0a0e27", font=tkfont.Font(family="Courier", size=10, weight="bold"),
                 relief=tk.FLAT, padx=20, pady=8).pack(pady=10)
        
        task_entry.bind('<Return>', lambda e: execute_task())
        
    def stop_overlay(self):
        """Stop overlay"""
        self.running = False
        self.log_message("Shutting down...", "warning")
        self.root.after(500, self.root.quit)
        
    def run(self):
        """Start the overlay"""
        self.root.mainloop()


def start_overlay(api_key, system_prompt):
    """Start the desktop overlay"""
    overlay = OverlayAgent(api_key, system_prompt)
    overlay.run()


if __name__ == "__main__":
    import os
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        api_key = input("Enter OpenRouter API key: ")
    
    system_prompt = (
        "You are an advanced AI desktop agent. Click on things, analyze results, and complete tasks. "
        "Respond with JSON actions only."
    )
    
    start_overlay(api_key, system_prompt)
