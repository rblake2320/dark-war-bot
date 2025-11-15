"""
Error recovery and robustness features for production bot
Handles failures, retries, and automatic recovery
"""

import logging
import os
from datetime import datetime
from time import sleep
import random
from typing import Optional, Callable, Any
from functools import wraps


class ErrorRecovery:
    """Handles error recovery and retry logic"""
    
    def __init__(self, bot, screenshot_dir: str = "error_screenshots"):
        """
        Initialize error recovery system
        
        Args:
            bot: DarkWarBot instance
            screenshot_dir: Directory to save error screenshots
        """
        self.bot = bot
        self.screenshot_dir = screenshot_dir
        self.error_count = 0
        self.last_error_time = None
        self.consecutive_errors = 0
        
        # Create screenshot directory
        os.makedirs(screenshot_dir, exist_ok=True)
    
    def capture_error_screenshot(self, error_type: str) -> Optional[str]:
        """
        Capture screenshot when error occurs
        
        Args:
            error_type: Type of error that occurred
            
        Returns:
            str: Path to saved screenshot or None
        """
        try:
            screenshot = self.bot.capture_screen()
            if screenshot is not None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{error_type}_{timestamp}.png"
                filepath = os.path.join(self.screenshot_dir, filename)
                
                import cv2
                cv2.imwrite(filepath, screenshot)
                logging.info(f"Error screenshot saved: {filepath}")
                return filepath
        except Exception as e:
            logging.error(f"Failed to capture error screenshot: {e}")
        
        return None
    
    def log_error(self, error_type: str, error_message: str, capture_screenshot: bool = True):
        """
        Log error with details
        
        Args:
            error_type: Category of error
            error_message: Detailed error message
            capture_screenshot: Whether to capture screenshot
        """
        self.error_count += 1
        self.consecutive_errors += 1
        self.last_error_time = datetime.now()
        
        logging.error(f"[{error_type}] {error_message}")
        logging.error(f"Total errors: {self.error_count}, Consecutive: {self.consecutive_errors}")
        
        if capture_screenshot:
            self.capture_error_screenshot(error_type)
    
    def reset_error_counter(self):
        """Reset consecutive error counter after successful action"""
        if self.consecutive_errors > 0:
            logging.info(f"Resetting error counter (was {self.consecutive_errors})")
            self.consecutive_errors = 0
    
    def should_pause(self, threshold: int = 5) -> bool:
        """
        Check if bot should pause due to too many errors
        
        Args:
            threshold: Number of consecutive errors before pausing
            
        Returns:
            bool: True if should pause
        """
        return self.consecutive_errors >= threshold
    
    def retry_with_backoff(self, 
                          func: Callable, 
                          max_retries: int = 3,
                          initial_delay: float = 1.0,
                          backoff_factor: float = 2.0,
                          *args, **kwargs) -> Any:
        """
        Retry function with exponential backoff
        
        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            backoff_factor: Multiplier for each retry
            *args, **kwargs: Arguments to pass to function
            
        Returns:
            Result of function or None if all retries failed
        """
        delay = initial_delay
        
        for attempt in range(max_retries + 1):
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    self.reset_error_counter()
                    return result
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}")
                self.log_error("RETRY_FAILURE", str(e), capture_screenshot=(attempt == max_retries))
            
            if attempt < max_retries:
                # Add randomization to delay
                jittered_delay = delay * random.uniform(0.8, 1.2)
                logging.info(f"Retrying in {jittered_delay:.1f}s...")
                sleep(jittered_delay)
                delay *= backoff_factor
        
        logging.error(f"All {max_retries + 1} attempts failed")
        return None


def with_retry(max_retries: int = 3, initial_delay: float = 1.0):
    """
    Decorator to add retry logic to functions
    
    Args:
        max_retries: Maximum number of retries
        initial_delay: Initial delay between retries
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'error_recovery'):
                return self.error_recovery.retry_with_backoff(
                    func, max_retries, initial_delay, self, *args, **kwargs
                )
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator


class TemplateRecalibration:
    """Handles template matching calibration and adjustment"""
    
    def __init__(self, bot):
        """
        Initialize template recalibration system
        
        Args:
            bot: DarkWarBot instance
        """
        self.bot = bot
        self.template_success_rates = {}
        self.template_thresholds = {}
    
    def record_template_result(self, template_name: str, success: bool):
        """
        Record template matching result
        
        Args:
            template_name: Name of template
            success: Whether matching was successful
        """
        if template_name not in self.template_success_rates:
            self.template_success_rates[template_name] = {'success': 0, 'total': 0}
        
        self.template_success_rates[template_name]['total'] += 1
        if success:
            self.template_success_rates[template_name]['success'] += 1
    
    def get_success_rate(self, template_name: str) -> float:
        """
        Get success rate for template
        
        Args:
            template_name: Name of template
            
        Returns:
            float: Success rate (0.0 to 1.0)
        """
        if template_name not in self.template_success_rates:
            return 0.0
        
        stats = self.template_success_rates[template_name]
        if stats['total'] == 0:
            return 0.0
        
        return stats['success'] / stats['total']
    
    def adjust_threshold(self, template_name: str, current_threshold: float) -> float:
        """
        Automatically adjust threshold based on success rate
        
        Args:
            template_name: Name of template
            current_threshold: Current matching threshold
            
        Returns:
            float: Adjusted threshold
        """
        success_rate = self.get_success_rate(template_name)
        
        # If success rate is low, lower threshold
        if success_rate < 0.3 and current_threshold > 0.65:
            new_threshold = max(0.65, current_threshold - 0.05)
            logging.info(f"Lowering threshold for {template_name}: {current_threshold:.2f} -> {new_threshold:.2f}")
            return new_threshold
        
        # If success rate is high, can raise threshold for accuracy
        if success_rate > 0.9 and current_threshold < 0.9:
            new_threshold = min(0.9, current_threshold + 0.02)
            logging.info(f"Raising threshold for {template_name}: {current_threshold:.2f} -> {new_threshold:.2f}")
            return new_threshold
        
        return current_threshold


class ConnectionMonitor:
    """Monitors connection and detects game updates"""
    
    def __init__(self, bot):
        """
        Initialize connection monitor
        
        Args:
            bot: DarkWarBot instance
        """
        self.bot = bot
        self.last_successful_action = datetime.now()
        self.connection_timeout = 300  # 5 minutes
    
    def is_connected(self) -> bool:
        """
        Check if game is still connected
        
        Returns:
            bool: True if connected
        """
        # Try to capture screen
        screenshot = self.bot.capture_screen()
        if screenshot is None:
            logging.warning("Failed to capture screen - possible connection loss")
            return False
        
        # Look for connection indicators
        # (This would check for specific UI elements that indicate connection)
        return True
    
    def detect_game_update(self) -> bool:
        """
        Detect if game has been updated
        
        Returns:
            bool: True if update detected
        """
        screenshot = self.bot.capture_screen()
        if screenshot is None:
            return False
        
        # Look for update notification or changed UI
        update_indicator = self.bot.find_template(screenshot, 'update_notification.png', threshold=0.7)
        
        if update_indicator:
            logging.warning("Game update detected!")
            return True
        
        return False
    
    def handle_connection_loss(self):
        """Handle connection loss scenario"""
        logging.error("Connection lost - attempting recovery...")
        
        # Wait and retry
        for attempt in range(3):
            logging.info(f"Reconnection attempt {attempt + 1}/3...")
            sleep(10)
            
            if self.is_connected():
                logging.info("Connection restored!")
                return True
        
        logging.error("Failed to restore connection")
        return False


class CrashRecovery:
    """Handles crash recovery and state restoration"""
    
    def __init__(self, state_file: str = "bot_state.json"):
        """
        Initialize crash recovery
        
        Args:
            state_file: File to save bot state
        """
        self.state_file = state_file
    
    def save_state(self, state_data: dict):
        """
        Save current bot state
        
        Args:
            state_data: Dictionary containing bot state
        """
        try:
            import json
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
            logging.debug("Bot state saved")
        except Exception as e:
            logging.error(f"Failed to save state: {e}")
    
    def load_state(self) -> Optional[dict]:
        """
        Load saved bot state
        
        Returns:
            dict: Saved state or None
        """
        try:
            import json
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                logging.info("Bot state loaded")
                return state
        except Exception as e:
            logging.error(f"Failed to load state: {e}")
        
        return None
    
    def clear_state(self):
        """Clear saved state"""
        try:
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
                logging.info("Bot state cleared")
        except Exception as e:
            logging.error(f"Failed to clear state: {e}")


# Notification system for errors
class NotificationSystem:
    """Send notifications about bot status and errors"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize notification system
        
        Args:
            webhook_url: Discord webhook URL (optional)
        """
        self.webhook_url = webhook_url
    
    def send_notification(self, title: str, message: str, level: str = "info"):
        """
        Send notification
        
        Args:
            title: Notification title
            message: Notification message
            level: 'info', 'warning', or 'error'
        """
        if not self.webhook_url:
            return
        
        try:
            import requests
            
            color_map = {
                'info': 3447003,    # Blue
                'warning': 16776960, # Yellow
                'error': 15158332    # Red
            }
            
            payload = {
                "embeds": [{
                    "title": title,
                    "description": message,
                    "color": color_map.get(level, 3447003),
                    "timestamp": datetime.utcnow().isoformat()
                }]
            }
            
            requests.post(self.webhook_url, json=payload, timeout=5)
            logging.debug(f"Notification sent: {title}")
        except Exception as e:
            logging.error(f"Failed to send notification: {e}")
    
    def notify_error(self, error_type: str, error_message: str):
        """Send error notification"""
        self.send_notification(
            f"Bot Error: {error_type}",
            error_message,
            level="error"
        )
    
    def notify_status(self, status_message: str):
        """Send status notification"""
        self.send_notification(
            "Bot Status Update",
            status_message,
            level="info"
        )
