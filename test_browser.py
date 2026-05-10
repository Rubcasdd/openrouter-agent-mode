#!/usr/bin/env python3
"""
Quick test to verify browser-use functionality
Run this to ensure your browser automation is working correctly
"""

import asyncio
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_browser_search():
    """Test browser search functionality"""
    print("Testing browser_search...")
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Simple search test
            await page.goto("https://www.google.com/search?q=python")
            await page.wait_for_timeout(1000)
            
            results = await page.evaluate("""
            () => {
                const items = document.querySelectorAll('h3');
                return Array.from(items).slice(0, 3).map(h => h.textContent).filter(t => t);
            }
            """)
            
            await browser.close()
            
            if results:
                print(f"✓ Browser search works! Found {len(results)} results")
                return True
            else:
                print("✗ Browser search returned no results")
                return False
    except Exception as e:
        print(f"✗ Browser search failed: {e}")
        return False

async def test_agent_methods():
    """Test the extended agent methods"""
    print("\nTesting Agent methods...")
    try:
        from agent import OpenRouterAgent
        
        # We can't fully test without an API key, but we can verify methods exist
        fake_key = "test-key-12345"
        agent = OpenRouterAgent(api_key=fake_key)
        
        # Check if methods exist
        assert hasattr(agent, 'browser_search'), "browser_search method missing"
        assert hasattr(agent, 'browser_visit_url'), "browser_visit_url method missing"
        assert hasattr(agent, 'browser_extract_info'), "browser_extract_info method missing"
        assert hasattr(agent, 'run_async'), "run_async method missing"
        assert hasattr(agent, 'extract_natural_language_response'), "extract_natural_language_response method missing"
        
        print("✓ All agent methods exist!")
        return True
    except Exception as e:
        print(f"✗ Agent methods test failed: {e}")
        return False

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        import browser_use
        print("  ✓ browser_use imported")
        
        import playwright
        print("  ✓ playwright imported")
        
        from openrouter import OpenRouter
        print("  ✓ openrouter imported")
        
        from agent import OpenRouterAgent
        print("  ✓ agent.OpenRouterAgent imported")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def main():
    print("=" * 50)
    print("Browser-Use Integration Test Suite")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n✗ Basic imports failed. Install dependencies:")
        print("  pip install browser-use playwright openrouter")
        return False
    
    # Test agent methods
    if not test_agent_methods():
        return False
    
    # Test browser search (requires async)
    print("\nTesting browser automation...")
    print("(This will take a moment as it launches Chrome)")
    try:
        result = asyncio.run(test_browser_search())
        if not result:
            return False
    except Exception as e:
        print(f"✗ Async test failed: {e}")
        print("  (This might be expected in some environments)")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! Your browser automation is ready.")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Set your OPENROUTER_API_KEY environment variable")
    print("2. Run: python app.py")
    print("3. Choose 'agent' profile")
    print("4. Try: 'Search for Python best practices'")
    print("\nSee BROWSER_USAGE.md for more examples.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
