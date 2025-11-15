"""
Dark War Survival Bot - Main Implementation
Based on OpenCV template matching and PyAutoGUI automation
"""

import cv2
import numpy as np
import pyautogui
from time import sleep, time
from threading import Thread
import random
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

class DarkWarBot:
    """Main bot class for Dark War Survival automation"""
    
    def __init__(self, config=None):
        """
        Initialize the bot with configuration
        
        Args:
            config (dict): Configuration dictionary with bot settings
        """
        self.is_running = False
        self.last_action_time = time()
        self.config = config or self._default_config()
        self.template_dir = Path(__file__).parent.parent / 'templates'
        self.action_count = 0
        self.error_count = 0
        
        # Anti-detection settings
        self.base_interval = self.config.get('base_interval', 60)
        self.variance = self.config.get('variance', 0.3)
        
        logging.info("Dark War Bot initialized")
    
    def _default_config(self):
        """Return default configuration"""
        return {
            'base_interval': 60,  # seconds between actions
            'variance': 0.3,  # ±30% randomization
            'template_threshold': 0.8,  # matching confidence
            'max_instances': 1,
            'enable_breaks': True,
            'break_interval': 7200,  # 2 hours
            'break_duration': 900  # 15 minutes
        }
    
    def capture_screen(self, region=None):
        """
        Capture screenshot of BlueStacks window
        
        Args:
            region (tuple): Optional (x, y, width, height) region to capture
            
        Returns:
            numpy.ndarray: Screenshot in BGR format
        """
        try:
            screenshot = pyautogui.screenshot(region=region)
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except Exception as e:
            logging.error(f"Screen capture failed: {e}")
            return None
    
    def find_template(self, screenshot, template_name, threshold=None):
        """
        Find template image in screenshot using OpenCV
        
        Args:
            screenshot (numpy.ndarray): Screenshot to search in
            template_name (str): Name of template file (e.g., 'gather_btn.png')
            threshold (float): Matching confidence threshold (0.0-1.0)
            
        Returns:
            tuple: (x, y) coordinates if found, None otherwise
        """
        if threshold is None:
            threshold = self.config['template_threshold']
        
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            logging.warning(f"Template not found: {template_path}")
            return None
        
        try:
            template = cv2.imread(str(template_path), 0)
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= threshold:
                logging.debug(f"Template '{template_name}' found with confidence {max_val:.2f}")
                return max_loc
            else:
                logging.debug(f"Template '{template_name}' not found (confidence {max_val:.2f})")
                return None
                
        except Exception as e:
            logging.error(f"Template matching error: {e}")
            return None
    
    def bezier_curve_movement(self, start, end, steps=20):
        """
        Move mouse along a Bezier curve for human-like movement
        
        Args:
            start (tuple): Starting (x, y) coordinates
            end (tuple): Ending (x, y) coordinates
            steps (int): Number of steps in the curve
        """
        control = (
            random.randint(min(start[0], end[0]), max(start[0], end[0])),
            random.randint(min(start[1], end[1]), max(start[1], end[1]))
        )
        
        for i in range(steps):
            t = i / steps
            x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
            y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
            pyautogui.moveTo(int(x), int(y))
            sleep(0.01)
    
    def human_click(self, x, y, use_bezier=True):
        """
        Perform human-like mouse click with randomization
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            use_bezier (bool): Use Bezier curve movement
        """
        # Add random offset to click position
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        target_x = x + offset_x
        target_y = y + offset_y
        
        # Get current mouse position
        current_pos = pyautogui.position()
        
        # Move to target with Bezier curve or linear movement
        if use_bezier and random.random() > 0.3:  # 70% chance to use Bezier
            self.bezier_curve_movement(current_pos, (target_x, target_y))
        else:
            duration = random.uniform(0.2, 0.5)
            pyautogui.moveTo(target_x, target_y, duration=duration)
        
        # Random pre-click delay
        sleep(random.uniform(0.1, 0.3))
        
        # Perform click
        pyautogui.click()
        logging.debug(f"Clicked at ({target_x}, {target_y})")
        
        # Post-click cooldown
        sleep(random.uniform(0.5, 1.5))
    
    def get_random_interval(self):
        """
        Calculate randomized action interval
        
        Returns:
            float: Interval in seconds with variance applied
        """
        return random.uniform(
            self.base_interval * (1 - self.variance),
            self.base_interval * (1 + self.variance)
        )
    
    def gather_resources(self):
        """
        Automated resource gathering task
        
        Returns:
            bool: True if successful, False otherwise
        """
        logging.info("Starting resource gathering...")
        screenshot = self.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find resource node on map
        resource_loc = self.find_template(screenshot, 'food_node.png')
        
        if resource_loc:
            self.human_click(*resource_loc)
            sleep(2)
            
            # Find and click "Gather" button
            gather_btn = self.find_template(screenshot, 'gather_btn.png')
            if gather_btn:
                self.human_click(*gather_btn)
                logging.info("Resource gathering initiated")
                self.action_count += 1
                return True
        
        logging.warning("Resource gathering failed - templates not found")
        return False
    
    def upgrade_building(self):
        """
        Automated building upgrade task
        
        Returns:
            bool: True if successful, False otherwise
        """
        logging.info("Checking for building upgrades...")
        screenshot = self.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find upgrade button
        upgrade_btn = self.find_template(screenshot, 'upgrade_btn.png')
        
        if upgrade_btn:
            self.human_click(*upgrade_btn)
            sleep(1)
            
            # Confirm upgrade
            confirm_btn = self.find_template(screenshot, 'confirm_btn.png')
            if confirm_btn:
                self.human_click(*confirm_btn)
                logging.info("Building upgrade initiated")
                self.action_count += 1
                return True
        
        logging.debug("No building upgrades available")
        return False
    
    def train_troops(self):
        """
        Automated troop training task
        
        Returns:
            bool: True if successful, False otherwise
        """
        logging.info("Starting troop training...")
        screenshot = self.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find barracks
        barracks = self.find_template(screenshot, 'barracks.png')
        
        if barracks:
            self.human_click(*barracks)
            sleep(2)
            
            # Find train button
            train_btn = self.find_template(screenshot, 'train_btn.png')
            if train_btn:
                self.human_click(*train_btn)
                logging.info("Troop training initiated")
                self.action_count += 1
                return True
        
        logging.debug("Troop training not available")
        return False
    
    def take_break(self):
        """Simulate human break period"""
        break_duration = random.uniform(
            self.config['break_duration'] * 0.8,
            self.config['break_duration'] * 1.2
        )
        logging.info(f"Taking break for {break_duration/60:.1f} minutes")
        sleep(break_duration)
    
    def run_loop(self):
        """Main bot execution loop"""
        self.is_running = True
        last_break_time = time()
        
        logging.info("Bot started - entering main loop")
        
        while self.is_running:
            try:
                current_time = time()
                
                # Check if break is needed
                if self.config['enable_breaks']:
                    if current_time - last_break_time >= self.config['break_interval']:
                        self.take_break()
                        last_break_time = time()
                
                # Calculate next action interval
                interval = self.get_random_interval()
                
                if current_time - self.last_action_time >= interval:
                    # Execute random task
                    tasks = [
                        self.gather_resources,
                        self.upgrade_building,
                        self.train_troops
                    ]
                    
                    # Weighted random selection (gather more often)
                    weights = [0.5, 0.3, 0.2]
                    task = random.choices(tasks, weights=weights)[0]
                    
                    try:
                        task()
                    except Exception as e:
                        logging.error(f"Task execution error: {e}")
                        self.error_count += 1
                    
                    self.last_action_time = time()
                    
                    # Log statistics every 10 actions
                    if self.action_count % 10 == 0:
                        logging.info(f"Statistics - Actions: {self.action_count}, Errors: {self.error_count}")
                
                # Sleep before next check
                sleep(1)
                
            except KeyboardInterrupt:
                logging.info("Bot stopped by user")
                self.is_running = False
                break
            except Exception as e:
                logging.error(f"Main loop error: {e}")
                self.error_count += 1
                sleep(5)
        
        logging.info("Bot stopped")
    
    def stop(self):
        """Stop the bot"""
        self.is_running = False
        logging.info("Stop signal sent")


if __name__ == "__main__":
    # Example usage
    config = {
        'base_interval': 45,
        'variance': 0.4,
        'enable_breaks': True
    }
    
    bot = DarkWarBot(config)
    bot.run_loop()
