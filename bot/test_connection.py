"""
Simple test script to verify BlueStacks connection
Run this to confirm the bot can see and control your BlueStacks
"""

import sys
import os

print("=" * 60)
print("BlueStacks Connection Test")
print("=" * 60)
print()

# Test 1: Check Python version
print("Test 1: Python Version")
print(f"  Python: {sys.version}")
if sys.version_info >= (3, 11):
    print("  ✓ Python 3.11+ detected")
else:
    print("  ✗ Python 3.11+ required")
    print("  Please install Python 3.11 from python.org")
    sys.exit(1)
print()

# Test 2: Check dependencies
print("Test 2: Dependencies")
required_modules = {
    'cv2': 'opencv-python',
    'numpy': 'numpy',
    'PIL': 'pillow',
    'pyautogui': 'pyautogui'
}

missing = []
for module, package in required_modules.items():
    try:
        __import__(module)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} - MISSING")
        missing.append(package)

if missing:
    print()
    print("  Missing dependencies. Install with:")
    print(f"  pip install {' '.join(missing)}")
    sys.exit(1)
print()

# Test 3: Check Windows platform
print("Test 3: Platform Check")
import platform
if platform.system() == 'Windows':
    print(f"  ✓ Windows {platform.release()}")
else:
    print(f"  ✗ This bot requires Windows (detected: {platform.system()})")
    sys.exit(1)
print()

# Test 4: Check win32gui
print("Test 4: Window Detection")
try:
    import win32gui
    print("  ✓ win32gui available")
except ImportError:
    print("  ✗ win32gui not available")
    print("  Install with: pip install pywin32")
    sys.exit(1)
print()

# Test 5: Find BlueStacks window
print("Test 5: BlueStacks Detection")
print("  Searching for BlueStacks window...")

def find_bluestacks():
    """Find BlueStacks window"""
    titles_to_try = [
        "BlueStacks App Player",
        "BlueStacks",
        "BlueStacks 5",
        "BlueStacks 4"
    ]
    
    for title in titles_to_try:
        try:
            hwnd = win32gui.FindWindow(None, title)
            if hwnd:
                rect = win32gui.GetWindowRect(hwnd)
                return hwnd, title, rect
        except:
            pass
    
    return None, None, None

hwnd, title, rect = find_bluestacks()

if hwnd:
    print(f"  ✓ Found: {title}")
    print(f"  Window Handle: {hwnd}")
    print(f"  Position: {rect}")
    print(f"  Size: {rect[2]-rect[0]}x{rect[3]-rect[1]}")
    
    # Check if visible
    is_visible = win32gui.IsWindowVisible(hwnd)
    print(f"  Visible: {'Yes' if is_visible else 'No'}")
else:
    print("  ✗ BlueStacks window not found")
    print()
    print("  Make sure:")
    print("  1. BlueStacks is running")
    print("  2. BlueStacks window is open (not minimized)")
    print("  3. You can see the BlueStacks window on your screen")
    sys.exit(1)
print()

# Test 6: Screenshot capability
print("Test 6: Screenshot Test")
try:
    from PIL import ImageGrab
    
    # Take screenshot of BlueStacks window
    screenshot = ImageGrab.grab(bbox=rect)
    width, height = screenshot.size
    
    print(f"  ✓ Screenshot captured: {width}x{height}")
    
    # Save test screenshot
    screenshot_path = "test_screenshot.png"
    screenshot.save(screenshot_path)
    print(f"  ✓ Saved to: {screenshot_path}")
    print(f"  → Open this file to see what the bot sees!")
    
except Exception as e:
    print(f"  ✗ Screenshot failed: {e}")
    sys.exit(1)
print()

# Test 7: Mouse control
print("Test 7: Mouse Control")
try:
    import pyautogui
    
    # Get current mouse position
    x, y = pyautogui.position()
    print(f"  ✓ Current mouse position: ({x}, {y})")
    print(f"  ✓ Mouse control available")
    
    # Calculate BlueStacks center
    center_x = (rect[0] + rect[2]) // 2
    center_y = (rect[1] + rect[3]) // 2
    print(f"  BlueStacks center: ({center_x}, {center_y})")
    
except Exception as e:
    print(f"  ✗ Mouse control failed: {e}")
    sys.exit(1)
print()

# Test 8: Template matching
print("Test 8: Template Matching")
try:
    import cv2
    import numpy as np
    
    # Convert screenshot to OpenCV format
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    print(f"  ✓ OpenCV conversion successful")
    print(f"  ✓ Template matching ready")
    
except Exception as e:
    print(f"  ✗ Template matching failed: {e}")
    sys.exit(1)
print()

# Final summary
print("=" * 60)
print("CONNECTION TEST COMPLETE")
print("=" * 60)
print()
print("✓ All tests passed!")
print()
print("Your BlueStacks is ready for bot control!")
print()
print("Next steps:")
print("  1. Open Dark War Survival in BlueStacks")
print("  2. Run: python main_enhanced.py --test-templates")
print("  3. Run: python main_enhanced.py --max-cycles 3 --verbose")
print()
print("The bot will:")
print("  - Focus your BlueStacks window")
print("  - Take screenshots of the game")
print("  - Find UI elements (buttons, resources)")
print("  - Move your mouse automatically")
print("  - Click and play the game")
print()
print("Check 'test_screenshot.png' to see what the bot sees!")
print("=" * 60)
