"""
Comprehensive task automation for all Dark War Survival features
Extends the base bot with complete game functionality
"""

import logging
from time import time, sleep
import random
from typing import Optional, Dict, List, Tuple


class TaskAutomation:
    """Complete task automation for all game features"""
    
    def __init__(self, bot):
        """
        Initialize task automation
        
        Args:
            bot: DarkWarBot instance
        """
        self.bot = bot
        self.last_task_times = {}
        self.task_cooldowns = {
            'gather_food': 300,      # 5 minutes
            'gather_wood': 300,
            'gather_stone': 300,
            'gather_iron': 300,
            'upgrade_building': 600,  # 10 minutes
            'train_troops': 400,      # 6.7 minutes
            'research': 1800,         # 30 minutes
            'heal_troops': 600,
            'collect_mail': 900,      # 15 minutes
            'claim_rewards': 1200,    # 20 minutes
            'alliance_help': 300,
            'activate_shield': 3600,  # 1 hour
            'hero_management': 1800,
            'exploration': 2400       # 40 minutes
        }
    
    def can_execute_task(self, task_name: str) -> bool:
        """
        Check if enough time has passed to execute task
        
        Args:
            task_name: Name of the task
            
        Returns:
            bool: True if task can be executed
        """
        if task_name not in self.last_task_times:
            return True
        
        elapsed = time() - self.last_task_times[task_name]
        cooldown = self.task_cooldowns.get(task_name, 300)
        
        return elapsed >= cooldown
    
    def mark_task_executed(self, task_name: str):
        """Mark task as executed with current timestamp"""
        self.last_task_times[task_name] = time()
    
    # ==================== RESOURCE GATHERING ====================
    
    def gather_resource(self, resource_type: str) -> bool:
        """
        Gather specific resource type
        
        Args:
            resource_type: 'food', 'wood', 'stone', or 'iron'
            
        Returns:
            bool: True if successful
        """
        task_name = f'gather_{resource_type}'
        
        if not self.can_execute_task(task_name):
            logging.debug(f"Task {task_name} on cooldown")
            return False
        
        logging.info(f"Gathering {resource_type}...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find resource node on map
        node_template = f'{resource_type}_node.png'
        resource_loc = self.bot.find_template(screenshot, node_template)
        
        if resource_loc:
            self.bot.human_click(*resource_loc)
            sleep(random.uniform(1.5, 2.5))
            
            # Click gather button
            gather_btn = self.bot.find_template(screenshot, 'gather_btn.png')
            if gather_btn:
                self.bot.human_click(*gather_btn)
                logging.info(f"{resource_type.capitalize()} gathering initiated")
                self.mark_task_executed(task_name)
                self.bot.action_count += 1
                return True
        
        logging.warning(f"{resource_type.capitalize()} gathering failed")
        return False
    
    def gather_all_resources(self) -> int:
        """
        Attempt to gather all resource types
        
        Returns:
            int: Number of successful gatherings
        """
        resources = ['food', 'wood', 'stone', 'iron']
        success_count = 0
        
        for resource in resources:
            if self.gather_resource(resource):
                success_count += 1
                sleep(random.uniform(2, 4))
        
        return success_count
    
    # ==================== BUILDING & UPGRADES ====================
    
    def upgrade_specific_building(self, building_type: str) -> bool:
        """
        Upgrade a specific building type
        
        Args:
            building_type: Building template name (e.g., 'farm', 'barracks')
            
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('upgrade_building'):
            return False
        
        logging.info(f"Upgrading {building_type}...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find building
        building_template = f'{building_type}.png'
        building_loc = self.bot.find_template(screenshot, building_template)
        
        if building_loc:
            self.bot.human_click(*building_loc)
            sleep(random.uniform(1.5, 2.5))
            
            # Find and click upgrade button
            upgrade_btn = self.bot.find_template(screenshot, 'upgrade_btn.png')
            if upgrade_btn:
                self.bot.human_click(*upgrade_btn)
                sleep(random.uniform(1, 2))
                
                # Confirm upgrade
                confirm_btn = self.bot.find_template(screenshot, 'confirm_btn.png')
                if confirm_btn:
                    self.bot.human_click(*confirm_btn)
                    logging.info(f"{building_type.capitalize()} upgrade initiated")
                    self.mark_task_executed('upgrade_building')
                    self.bot.action_count += 1
                    return True
        
        logging.debug(f"{building_type.capitalize()} upgrade not available")
        return False
    
    def upgrade_all_buildings(self) -> int:
        """
        Attempt to upgrade all building types
        
        Returns:
            int: Number of successful upgrades
        """
        buildings = ['farm', 'sawmill', 'quarry', 'mine', 'barracks', 
                    'hospital', 'warehouse', 'wall', 'headquarters']
        success_count = 0
        
        for building in buildings:
            if self.upgrade_specific_building(building):
                success_count += 1
                sleep(random.uniform(2, 4))
                break  # Only one upgrade at a time typically
        
        return success_count
    
    # ==================== TROOP MANAGEMENT ====================
    
    def train_specific_troops(self, troop_type: str, quantity: int = None) -> bool:
        """
        Train specific troop type
        
        Args:
            troop_type: 'infantry', 'cavalry', 'archer', etc.
            quantity: Number to train (None = max)
            
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('train_troops'):
            return False
        
        logging.info(f"Training {troop_type}...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find barracks
        barracks = self.bot.find_template(screenshot, 'barracks.png')
        
        if barracks:
            self.bot.human_click(*barracks)
            sleep(random.uniform(2, 3))
            
            # Find troop type button
            troop_btn = self.bot.find_template(screenshot, f'{troop_type}_btn.png')
            if troop_btn:
                self.bot.human_click(*troop_btn)
                sleep(random.uniform(1, 2))
                
                # Click train button (max by default)
                train_btn = self.bot.find_template(screenshot, 'train_btn.png')
                if train_btn:
                    self.bot.human_click(*train_btn)
                    logging.info(f"{troop_type.capitalize()} training initiated")
                    self.mark_task_executed('train_troops')
                    self.bot.action_count += 1
                    return True
        
        logging.debug(f"{troop_type.capitalize()} training not available")
        return False
    
    def heal_troops(self) -> bool:
        """
        Heal wounded troops
        
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('heal_troops'):
            return False
        
        logging.info("Healing troops...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find hospital
        hospital = self.bot.find_template(screenshot, 'hospital.png')
        
        if hospital:
            self.bot.human_click(*hospital)
            sleep(random.uniform(2, 3))
            
            # Find heal button
            heal_btn = self.bot.find_template(screenshot, 'heal_btn.png')
            if heal_btn:
                self.bot.human_click(*heal_btn)
                sleep(random.uniform(1, 2))
                
                # Confirm healing
                confirm_btn = self.bot.find_template(screenshot, 'confirm_btn.png')
                if confirm_btn:
                    self.bot.human_click(*confirm_btn)
                    logging.info("Troop healing initiated")
                    self.mark_task_executed('heal_troops')
                    self.bot.action_count += 1
                    return True
        
        logging.debug("Troop healing not needed or available")
        return False
    
    # ==================== RESEARCH ====================
    
    def start_research(self, research_name: str = None) -> bool:
        """
        Start research (next available or specific)
        
        Args:
            research_name: Specific research or None for next available
            
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('research'):
            return False
        
        logging.info("Starting research...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find research building
        research_building = self.bot.find_template(screenshot, 'research_lab.png')
        
        if research_building:
            self.bot.human_click(*research_building)
            sleep(random.uniform(2, 3))
            
            # Find research button
            research_btn = self.bot.find_template(screenshot, 'research_btn.png')
            if research_btn:
                self.bot.human_click(*research_btn)
                sleep(random.uniform(1, 2))
                
                # Confirm research
                confirm_btn = self.bot.find_template(screenshot, 'confirm_btn.png')
                if confirm_btn:
                    self.bot.human_click(*confirm_btn)
                    logging.info("Research initiated")
                    self.mark_task_executed('research')
                    self.bot.action_count += 1
                    return True
        
        logging.debug("Research not available")
        return False
    
    # ==================== REWARDS & ECONOMY ====================
    
    def collect_mail_rewards(self) -> bool:
        """
        Collect all mail rewards
        
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('collect_mail'):
            return False
        
        logging.info("Collecting mail rewards...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find mail icon
        mail_icon = self.bot.find_template(screenshot, 'mail_icon.png')
        
        if mail_icon:
            self.bot.human_click(*mail_icon)
            sleep(random.uniform(2, 3))
            
            # Click collect all button
            collect_all = self.bot.find_template(screenshot, 'collect_all_btn.png')
            if collect_all:
                self.bot.human_click(*collect_all)
                logging.info("Mail rewards collected")
                self.mark_task_executed('collect_mail')
                self.bot.action_count += 1
                return True
        
        logging.debug("No mail rewards to collect")
        return False
    
    def claim_daily_rewards(self) -> bool:
        """
        Claim all daily rewards
        
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('claim_rewards'):
            return False
        
        logging.info("Claiming daily rewards...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        reward_types = ['vip_reward', 'daily_reward', 'task_reward']
        claimed_any = False
        
        for reward_type in reward_types:
            reward_icon = self.bot.find_template(screenshot, f'{reward_type}_icon.png')
            if reward_icon:
                self.bot.human_click(*reward_icon)
                sleep(random.uniform(1.5, 2.5))
                
                claim_btn = self.bot.find_template(screenshot, 'claim_btn.png')
                if claim_btn:
                    self.bot.human_click(*claim_btn)
                    claimed_any = True
                    sleep(random.uniform(1, 2))
        
        if claimed_any:
            logging.info("Daily rewards claimed")
            self.mark_task_executed('claim_rewards')
            self.bot.action_count += 1
            return True
        
        logging.debug("No daily rewards available")
        return False
    
    # ==================== ALLIANCE ====================
    
    def alliance_help_all(self) -> bool:
        """
        Help all alliance members
        
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('alliance_help'):
            return False
        
        logging.info("Helping alliance members...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find alliance icon
        alliance_icon = self.bot.find_template(screenshot, 'alliance_icon.png')
        
        if alliance_icon:
            self.bot.human_click(*alliance_icon)
            sleep(random.uniform(2, 3))
            
            # Click help all button
            help_all = self.bot.find_template(screenshot, 'help_all_btn.png')
            if help_all:
                self.bot.human_click(*help_all)
                logging.info("Alliance help completed")
                self.mark_task_executed('alliance_help')
                self.bot.action_count += 1
                return True
        
        logging.debug("Alliance help not available")
        return False
    
    # ==================== PROTECTION ====================
    
    def activate_shield(self, duration: str = '8h') -> bool:
        """
        Activate peace shield
        
        Args:
            duration: Shield duration ('8h', '24h', '3d', '7d')
            
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('activate_shield'):
            return False
        
        logging.info(f"Activating {duration} shield...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find shield icon
        shield_icon = self.bot.find_template(screenshot, 'shield_icon.png')
        
        if shield_icon:
            self.bot.human_click(*shield_icon)
            sleep(random.uniform(2, 3))
            
            # Select duration
            duration_btn = self.bot.find_template(screenshot, f'shield_{duration}_btn.png')
            if duration_btn:
                self.bot.human_click(*duration_btn)
                sleep(random.uniform(1, 2))
                
                # Confirm activation
                confirm_btn = self.bot.find_template(screenshot, 'confirm_btn.png')
                if confirm_btn:
                    self.bot.human_click(*confirm_btn)
                    logging.info(f"{duration} shield activated")
                    self.mark_task_executed('activate_shield')
                    self.bot.action_count += 1
                    return True
        
        logging.debug("Shield activation not available")
        return False
    
    # ==================== HERO MANAGEMENT ====================
    
    def manage_heroes(self) -> bool:
        """
        Manage heroes (level up, upgrade skills)
        
        Returns:
            bool: True if any action performed
        """
        if not self.can_execute_task('hero_management'):
            return False
        
        logging.info("Managing heroes...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find hero icon
        hero_icon = self.bot.find_template(screenshot, 'hero_icon.png')
        
        if hero_icon:
            self.bot.human_click(*hero_icon)
            sleep(random.uniform(2, 3))
            
            # Try to level up
            levelup_btn = self.bot.find_template(screenshot, 'hero_levelup_btn.png')
            if levelup_btn:
                self.bot.human_click(*levelup_btn)
                logging.info("Hero leveled up")
                self.mark_task_executed('hero_management')
                self.bot.action_count += 1
                return True
            
            # Try to upgrade skills
            skill_upgrade = self.bot.find_template(screenshot, 'skill_upgrade_btn.png')
            if skill_upgrade:
                self.bot.human_click(*skill_upgrade)
                logging.info("Hero skill upgraded")
                self.mark_task_executed('hero_management')
                self.bot.action_count += 1
                return True
        
        logging.debug("Hero management not needed")
        return False
    
    # ==================== EXPLORATION ====================
    
    def start_exploration(self) -> bool:
        """
        Start exploration mission
        
        Returns:
            bool: True if successful
        """
        if not self.can_execute_task('exploration'):
            return False
        
        logging.info("Starting exploration...")
        screenshot = self.bot.capture_screen()
        
        if screenshot is None:
            return False
        
        # Find exploration icon
        exploration_icon = self.bot.find_template(screenshot, 'exploration_icon.png')
        
        if exploration_icon:
            self.bot.human_click(*exploration_icon)
            sleep(random.uniform(2, 3))
            
            # Click start mission
            start_btn = self.bot.find_template(screenshot, 'start_mission_btn.png')
            if start_btn:
                self.bot.human_click(*start_btn)
                logging.info("Exploration mission started")
                self.mark_task_executed('exploration')
                self.bot.action_count += 1
                return True
        
        logging.debug("Exploration not available")
        return False
