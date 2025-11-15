#!/usr/bin/env python3
"""
Dark War Survival Bot - Main Entry Point
Run this script to start the bot
"""

import sys
import argparse
import logging
from pathlib import Path

# Add bot directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.dark_war_bot import DarkWarBot
from config.config_manager import ConfigManager
from utils.window_utils import WindowDetector


def setup_logging(level=logging.INFO):
    """Configure logging with color support"""
    try:
        import colorlog
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        ))
        logging.basicConfig(
            level=level,
            handlers=[
                handler,
                logging.FileHandler('bot.log')
            ]
        )
    except ImportError:
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('bot.log')
            ]
        )


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Dark War Survival Bot - Automated gameplay assistant'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--detect-window',
        action='store_true',
        help='Detect emulator window and exit'
    )
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create default configuration file and exit'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    
    logging.info("=" * 60)
    logging.info("Dark War Survival Bot v1.0")
    logging.info("=" * 60)
    
    # Handle special commands
    if args.detect_window:
        logging.info("Detecting emulator window...")
        detector = WindowDetector()
        hwnd, rect = detector.find_emulator_window()
        if hwnd:
            logging.info(f"✓ Found window: {detector.get_window_title()}")
            logging.info(f"✓ Region: {detector.get_window_region()}")
        else:
            logging.error("✗ No emulator window found")
            logging.info("Make sure BlueStacks or another emulator is running")
        return
    
    if args.create_config:
        logging.info(f"Creating configuration file: {args.config}")
        config_mgr = ConfigManager(args.config)
        config_mgr.save_config()
        logging.info("✓ Configuration file created")
        logging.info(f"Edit {args.config} to customize bot settings")
        return
    
    # Load configuration
    logging.info(f"Loading configuration from: {args.config}")
    config_mgr = ConfigManager(args.config)
    
    if not config_mgr.validate():
        logging.error("Configuration validation failed")
        logging.error("Please check your config file or create a new one with --create-config")
        return
    
    # Detect emulator window
    logging.info("Detecting emulator window...")
    detector = WindowDetector()
    hwnd, rect = detector.find_emulator_window()
    
    if not hwnd:
        logging.warning("Emulator window not detected")
        logging.warning("Bot will run without window detection")
        logging.warning("Make sure the game is visible on screen")
    else:
        logging.info(f"✓ Detected: {detector.get_window_title()}")
    
    # Initialize bot
    logging.info("Initializing bot...")
    bot_config = config_mgr.get('bot_settings')
    bot = DarkWarBot(bot_config)
    
    # Display configuration
    logging.info("Bot configuration:")
    logging.info(f"  Base interval: {bot_config['base_interval']}s")
    logging.info(f"  Variance: ±{bot_config['variance']*100}%")
    logging.info(f"  Breaks enabled: {bot_config['enable_breaks']}")
    
    # Display enabled tasks
    tasks = config_mgr.get('tasks')
    enabled_tasks = [name for name, cfg in tasks.items() if cfg.get('enabled', False)]
    logging.info(f"  Enabled tasks: {', '.join(enabled_tasks)}")
    
    # Start bot
    logging.info("=" * 60)
    logging.info("Starting bot... (Press Ctrl+C to stop)")
    logging.info("=" * 60)
    
    try:
        bot.run_loop()
    except KeyboardInterrupt:
        logging.info("\n" + "=" * 60)
        logging.info("Bot stopped by user")
        logging.info("=" * 60)
        logging.info(f"Total actions performed: {bot.action_count}")
        logging.info(f"Total errors: {bot.error_count}")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
