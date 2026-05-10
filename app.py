"""
OpenRouter Agent Mode - Unified Multi-AI System
All 4 AI modes run in parallel for comprehensive task solving
"""

import importlib
import os
import subprocess
import sys
import json


def ensure_dependencies():
    """Ensure all application dependencies are installed, including overlay requirements"""
    print("Checking and installing all dependencies...")
    
    # Always install from requirements.txt to ensure all dependencies are present
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✓ All dependencies installed successfully")
    except subprocess.CalledProcessError as exc:
        print("Warning: Some dependencies may not have installed properly")
    
    # Verify critical packages
    required = ["pyautogui", "PIL", "openrouter", "playwright"]
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
        except Exception as e:
            if package == "pyautogui":
                print("Note: pyautogui may fail due to missing DISPLAY, but will work at runtime")
            else:
                print(f"Note: {package} import warning: {str(e)}")

    if missing and package != "pyautogui":
        print(f"Installing missing core packages: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        except subprocess.CalledProcessError:
            print("Warning: Some packages could not be installed")


ensure_dependencies()

from agent import OpenRouterAgent
from unified_coordinator import UnifiedAgentCoordinator


def main():
    """
    Unified Main Entry Point - All 4 AI modes run in parallel
    
    Single API key prompt, then all AIs collaborate simultaneously:
    1. Multi-Agent Mode (Multiple AIs collaborate)
    2. Single Agent Mode (Traditional mode)
    3. Overlay Mode (Desktop visual interface)
    4. Web Navigation Mode (Browser automation)
    """
    
    # Single API Key Prompt
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("\n" + "="*70)
        print("🔑 OPENROUTER API KEY REQUIRED")
        print("="*70)
        print("\nGet your free API key at: https://openrouter.ai/keys")
        api_key = input("\nEnter your OpenRouter API key: ").strip()
        if not api_key:
            print("❌ API key required. Exiting.")
            return
    
    print("\n✓ API key validated\n")
    
    # Initialize unified coordinator
    coordinator = UnifiedAgentCoordinator(api_key=api_key)
    
    # Main loop - get tasks and run all 4 modes in parallel
    print("\n" + "="*70)
    print("🚀 UNIFIED AI COORDINATOR - ALL MODES ENABLED")
    print("="*70)
    print("\nAll 4 AI modes will run in parallel:")
    print("  1️⃣  Multi-Agent Collaboration (5 AI perspectives)")
    print("  2️⃣  Single Agent Mode (Traditional with screenshots)")
    print("  3️⃣  Overlay Mode (Desktop interface analysis)")
    print("  4️⃣  Web Navigation Mode (Browser automation)")
    print("\nAll AIs work together and choose the best approach.\n")
    
    while True:
        print("="*70)
        task = input("📝 Enter task/question (or 'exit' to quit): ").strip()
        
        if task.lower() in ["exit", "quit", "q"]:
            print("\n👋 Exiting unified AI coordinator.\n")
            break
        
        if not task:
            print("⚠️  Please enter a task.\n")
            continue
        
        # Run all 4 modes in parallel
        coordinator.run_all_modes(task)
        
        # Show summary
        coordinator.print_status_dashboard()
        
        # Ask if user wants details
        details = input("📊 Show detailed results? (y/n) [n]: ").strip().lower()
        if details == "y":
            summary = coordinator.get_all_results_summary()
            print("\n" + json.dumps(summary, indent=2, default=str))
        
        print()


if __name__ == "__main__":
    main()
