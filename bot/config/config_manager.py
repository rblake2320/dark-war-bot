"""
Configuration management for Dark War Bot
Handles loading, saving, and validating bot configurations
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manage bot configuration files"""
    
    DEFAULT_CONFIG = {
        "bot_settings": {
            "base_interval": 60,
            "variance": 0.3,
            "template_threshold": 0.8,
            "enable_breaks": True,
            "break_interval": 7200,
            "break_duration": 900
        },
        "tasks": {
            "gather_resources": {
                "enabled": True,
                "weight": 0.5,
                "interval": 45
            },
            "upgrade_building": {
                "enabled": True,
                "weight": 0.3,
                "interval": 120
            },
            "train_troops": {
                "enabled": True,
                "weight": 0.2,
                "interval": 180
            },
            "research": {
                "enabled": False,
                "weight": 0.1,
                "interval": 300
            },
            "heal_troops": {
                "enabled": True,
                "weight": 0.15,
                "interval": 240
            }
        },
        "anti_detection": {
            "use_bezier_movement": True,
            "random_mistakes": True,
            "mistake_probability": 0.05,
            "vary_daily_playtime": True,
            "min_daily_hours": 18,
            "max_daily_hours": 23
        },
        "multi_instance": {
            "enabled": False,
            "max_instances": 1,
            "instance_delay": 30
        },
        "notifications": {
            "discord_webhook": "",
            "notify_on_error": True,
            "notify_on_milestone": True,
            "milestone_interval": 100
        },
        "logging": {
            "level": "INFO",
            "file": "bot.log",
            "max_size_mb": 10,
            "backup_count": 3
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default
        
        Returns:
            dict: Configuration dictionary
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logging.info(f"Configuration loaded from {self.config_path}")
                return self._merge_with_defaults(config)
            except Exception as e:
                logging.error(f"Error loading config: {e}")
                logging.info("Using default configuration")
                return self.DEFAULT_CONFIG.copy()
        else:
            logging.info("No config file found, creating default")
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_with_defaults(self, config: Dict) -> Dict:
        """
        Merge loaded config with defaults to ensure all keys exist
        
        Args:
            config (dict): Loaded configuration
            
        Returns:
            dict: Merged configuration
        """
        def deep_merge(default, custom):
            result = default.copy()
            for key, value in custom.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        
        return deep_merge(self.DEFAULT_CONFIG, config)
    
    def save_config(self, config: Dict = None):
        """
        Save configuration to file
        
        Args:
            config (dict): Configuration to save (uses current if None)
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            logging.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logging.error(f"Error saving config: {e}")
    
    def get(self, key_path: str, default=None):
        """
        Get configuration value using dot notation
        
        Args:
            key_path (str): Dot-separated path (e.g., "bot_settings.base_interval")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any, save: bool = True):
        """
        Set configuration value using dot notation
        
        Args:
            key_path (str): Dot-separated path
            value: Value to set
            save (bool): Whether to save config file immediately
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        
        if save:
            self.save_config()
    
    def validate(self) -> bool:
        """
        Validate configuration values
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Validate bot settings
            assert 0 < self.get('bot_settings.base_interval') <= 3600
            assert 0 <= self.get('bot_settings.variance') <= 1
            assert 0 <= self.get('bot_settings.template_threshold') <= 1
            
            # Validate task weights sum
            task_weights = [
                self.get(f'tasks.{task}.weight', 0)
                for task in ['gather_resources', 'upgrade_building', 'train_troops']
            ]
            total_weight = sum(task_weights)
            assert 0 < total_weight <= 1
            
            # Validate anti-detection settings
            assert 0 <= self.get('anti_detection.mistake_probability') <= 1
            
            logging.info("Configuration validation passed")
            return True
            
        except AssertionError as e:
            logging.error(f"Configuration validation failed: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
        logging.info("Configuration reset to defaults")
    
    def export_template(self, output_path: str):
        """
        Export configuration template with comments
        
        Args:
            output_path (str): Path to save template
        """
        template = {
            "_comment": "Dark War Survival Bot Configuration",
            "_instructions": {
                "bot_settings": "Core bot timing and behavior settings",
                "tasks": "Individual task configurations with weights",
                "anti_detection": "Settings to avoid detection",
                "multi_instance": "Multi-account management",
                "notifications": "Discord/alert settings",
                "logging": "Log file configuration"
            },
            **self.DEFAULT_CONFIG
        }
        
        with open(output_path, 'w') as f:
            json.dump(template, f, indent=2)
        
        logging.info(f"Configuration template exported to {output_path}")


if __name__ == "__main__":
    # Test configuration manager
    logging.basicConfig(level=logging.INFO)
    
    config_mgr = ConfigManager("test_config.json")
    
    print("Current config:")
    print(json.dumps(config_mgr.config, indent=2))
    
    print(f"\nBase interval: {config_mgr.get('bot_settings.base_interval')}")
    print(f"Gather weight: {config_mgr.get('tasks.gather_resources.weight')}")
    
    config_mgr.set('bot_settings.base_interval', 45)
    print(f"\nUpdated base interval: {config_mgr.get('bot_settings.base_interval')}")
    
    print(f"\nValidation result: {config_mgr.validate()}")
