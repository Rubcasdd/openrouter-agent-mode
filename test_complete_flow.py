#!/usr/bin/env python3
"""
Quick test to verify the complete browser automation flow works:
1. Playwright is installed and accessible
2. Browser actions work
3. AI provides conversational responses
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_playwright_import():
    """Test that playwright can be imported"""
    print("Test 1: Playwright Import")
    try:
        from playwright.async_api import async_playwright
        print("  ✓ playwright.async_api imported successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Failed to import playwright: {e}")
        print("  Fix: source .venv/bin/activate && pip install playwright")
        return False

def test_playwright_browser():
    """Test that browser can launch"""
    print("\nTest 2: Browser Launch")
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def launch_browser():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto('https://example.com')
                title = await page.title()
                await browser.close()
                return title
        
        title = asyncio.run(launch_browser())
        print(f"  ✓ Browser launched successfully")
        print(f"  ✓ Page title: {title}")
        return True
    except Exception as e:
        print(f"  ✗ Browser launch failed: {e}")
        return False

def test_agent_methods():
    """Test that agent has all browser methods"""
    print("\nTest 3: Agent Browser Methods")
    try:
        from agent import OpenRouterAgent
        
        # Create agent with fake key
        agent = OpenRouterAgent(api_key='test-key-12345')
        
        # Check methods exist
        methods_to_check = [
            'browser_search',
            'browser_visit_url',
            'browser_extract_info',
            'browser_click_element',
            'browser_fill_form',
            'browser_analyze_page',
            'run_async',
            'extract_natural_language_response'
        ]
        
        all_present = True
        for method in methods_to_check:
            if hasattr(agent, method):
                print(f"  ✓ {method}() present")
            else:
                print(f"  ✗ {method}() missing")
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"  ✗ Agent test failed: {e}")
        return False

def test_response_parsing():
    """Test that response parsing works"""
    print("\nTest 4: Response Parsing")
    try:
        from agent import OpenRouterAgent
        
        agent = OpenRouterAgent(api_key='test-key-12345')
        
        # Test extract_natural_language_response
        test_response = """I will search for Python information.

{"action": "browser_search", "value": "Python"}"""
        
        nl = agent.extract_natural_language_response(test_response)
        if nl:
            print(f"  ✓ Natural language extracted: {nl[:50]}...")
        else:
            print("  ✗ No natural language extracted")
            return False
        
        # Test parse_action
        action = agent.parse_action(test_response)
        if action and action['action'] == 'browser_search':
            print(f"  ✓ Action parsed: {action}")
        else:
            print("  ✗ Action parsing failed")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Response parsing failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Browser Automation - Complete Flow Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Playwright Import", test_playwright_import()))
    results.append(("Browser Launch", test_playwright_browser()))
    results.append(("Agent Methods", test_agent_methods()))
    results.append(("Response Parsing", test_response_parsing()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Browser automation is ready!")
        print("\nNext steps:")
        print("1. Set your OPENROUTER_API_KEY")
        print("2. Run: python app.py")
        print("3. Choose 'agent' profile")
        print("4. Try: 'Search for Python tutorials'")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
