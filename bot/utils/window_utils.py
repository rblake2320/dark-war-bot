"""
Window detection and management utilities
Supports BlueStacks and other emulator window detection
"""

import logging
import platform

# Platform-specific imports
if platform.system() == 'Windows':
    try:
        import win32gui
        import win32con
        WINDOWS_AVAILABLE = True
    except ImportError:
        WINDOWS_AVAILABLE = False
        logging.warning("win32gui not available - window detection disabled")
else:
    WINDOWS_AVAILABLE = False


class WindowDetector:
    """Detect and manage emulator windows"""
    
    EMULATOR_TITLES = [
        "BlueStacks App Player",
        "BlueStacks",
        "MEmu",
        "NoxPlayer",
        "LDPlayer"
    ]
    
    def __init__(self):
        self.hwnd = None
        self.window_rect = None
    
    def find_emulator_window(self, title_hint=None):
        """
        Find emulator window by title
        
        Args:
            title_hint (str): Optional specific window title to search for
            
        Returns:
            tuple: (hwnd, rect) if found, (None, None) otherwise
        """
        if not WINDOWS_AVAILABLE:
            logging.error("Window detection only available on Windows")
            return None, None
        
        search_titles = [title_hint] if title_hint else self.EMULATOR_TITLES
        
        for title in search_titles:
            try:
                hwnd = win32gui.FindWindow(None, title)
                if hwnd:
                    rect = win32gui.GetWindowRect(hwnd)
                    self.hwnd = hwnd
                    self.window_rect = rect
                    logging.info(f"Found window: {title} at {rect}")
                    return hwnd, rect
            except Exception as e:
                logging.debug(f"Could not find window '{title}': {e}")
        
        logging.warning("No emulator window found")
        return None, None
    
    def get_window_region(self):
        """
        Get window region for screenshot capture
        
        Returns:
            tuple: (x, y, width, height) or None
        """
        if not self.window_rect:
            self.find_emulator_window()
        
        if self.window_rect:
            left, top, right, bottom = self.window_rect
            width = right - left
            height = bottom - top
            return (left, top, width, height)
        
        return None
    
    def bring_to_front(self):
        """Bring emulator window to foreground"""
        if not WINDOWS_AVAILABLE or not self.hwnd:
            return False
        
        try:
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.hwnd)
            logging.info("Window brought to front")
            return True
        except Exception as e:
            logging.error(f"Could not bring window to front: {e}")
            return False
    
    def is_window_visible(self):
        """Check if window is visible"""
        if not WINDOWS_AVAILABLE or not self.hwnd:
            return False
        
        try:
            return win32gui.IsWindowVisible(self.hwnd)
        except Exception as e:
            logging.error(f"Could not check window visibility: {e}")
            return False
    
    def get_window_title(self):
        """Get current window title"""
        if not WINDOWS_AVAILABLE or not self.hwnd:
            return None
        
        try:
            return win32gui.GetWindowText(self.hwnd)
        except Exception as e:
            logging.error(f"Could not get window title: {e}")
            return None


def get_bluestacks_instances():
    """
    Get all running BlueStacks instances
    
    Returns:
        list: List of (hwnd, title, rect) tuples
    """
    if not WINDOWS_AVAILABLE:
        return []
    
    instances = []
    
    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "BlueStacks" in title:
                rect = win32gui.GetWindowRect(hwnd)
                results.append((hwnd, title, rect))
    
    try:
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        return windows
    except Exception as e:
        logging.error(f"Could not enumerate windows: {e}")
        return []


if __name__ == "__main__":
    # Test window detection
    logging.basicConfig(level=logging.INFO)
    
    detector = WindowDetector()
    hwnd, rect = detector.find_emulator_window()
    
    if hwnd:
        print(f"Found emulator window: {detector.get_window_title()}")
        print(f"Window region: {detector.get_window_region()}")
        print(f"Visible: {detector.is_window_visible()}")
        
        # List all BlueStacks instances
        instances = get_bluestacks_instances()
        print(f"\nFound {len(instances)} BlueStacks instances:")
        for hwnd, title, rect in instances:
            print(f"  - {title} at {rect}")
    else:
        print("No emulator window found")
