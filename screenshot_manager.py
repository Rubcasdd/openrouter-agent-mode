"""
Enhanced Screenshot and Display Management
Handles screenshot capture, storage, and display with fallback mechanisms
"""

import os
import base64
import tempfile
from datetime import datetime
from pathlib import Path


class ScreenshotManager:
    """Manages screenshots - capture, storage, and retrieval"""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(tempfile.gettempdir(), "openrouter_screenshots")
        
        self.storage_dir = storage_dir
        Path(storage_dir).mkdir(parents=True, exist_ok=True)
        self.screenshot_history = []
    
    def capture_screenshot(self, name: str = None) -> dict:
        """Capture a screenshot and store it"""
        try:
            import pyautogui
            
            if name is None:
                name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Capture screenshot
            screenshot = pyautogui.screenshot()
            
            # Save to disk
            file_path = os.path.join(self.storage_dir, f"{name}.png")
            screenshot.save(file_path)
            
            # Encode to base64 for API
            base64_data = self.encode_image_to_base64(file_path)
            
            # Store metadata
            metadata = {
                "name": name,
                "path": file_path,
                "timestamp": datetime.now().isoformat(),
                "base64": base64_data,
                "size": os.path.getsize(file_path),
            }
            
            self.screenshot_history.append(metadata)
            print(f"✓ Screenshot captured: {file_path}")
            
            return metadata
        except Exception as e:
            print(f"Error capturing screenshot: {str(e)}")
            return None
    
    def get_latest_screenshot(self) -> dict:
        """Get the most recent screenshot"""
        if self.screenshot_history:
            return self.screenshot_history[-1]
        return None
    
    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 for API"""
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image: {str(e)}")
            return None
    
    def encode_pil_image_to_base64(self, pil_image) -> str:
        """Convert PIL image to base64"""
        try:
            from io import BytesIO
            buffer = BytesIO()
            pil_image.save(buffer, format="PNG")
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding PIL image: {str(e)}")
            return None
    
    def get_screenshot_for_api(self) -> tuple:
        """Get screenshot data for API (base64 and URL format)"""
        latest = self.get_latest_screenshot()
        if latest and latest.get("base64"):
            return (latest.get("base64"), f"data:image/png;base64,{latest.get('base64')}")
        return (None, None)
    
    def list_available_screenshots(self) -> list:
        """List all available screenshots"""
        return sorted(self.screenshot_history, key=lambda x: x["timestamp"], reverse=True)
    
    def get_screenshot_display_info(self) -> str:
        """Get formatted info about available screenshots"""
        if not self.screenshot_history:
            return "No screenshots available yet"
        
        info = f"Available Screenshots ({len(self.screenshot_history)} total):\n"
        for i, screenshot in enumerate(self.list_available_screenshots()[:10], 1):
            info += f"  [{i}] {screenshot['name']} - {screenshot['size']} bytes - {screenshot['timestamp']}\n"
        
        return info
    
    def cleanup_old_screenshots(self, keep_count: int = 20):
        """Remove old screenshots, keeping only recent ones"""
        if len(self.screenshot_history) > keep_count:
            old_screenshots = sorted(self.screenshot_history, key=lambda x: x["timestamp"])[:-keep_count]
            for old_screenshot in old_screenshots:
                try:
                    if os.path.exists(old_screenshot["path"]):
                        os.remove(old_screenshot["path"])
                        self.screenshot_history.remove(old_screenshot)
                except Exception as e:
                    print(f"Error removing old screenshot: {str(e)}")
