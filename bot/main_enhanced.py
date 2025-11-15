"""
Enhanced main entry point for Dark War Survival Bot
Integrates all modules for production-ready autonomous operation
"""

import argparse
import logging
import sys
from time import sleep, time
import random

from core.dark_war_bot import DarkWarBot
from core.task_automation import TaskAutomation
from core.error_recovery import ErrorRecovery, TemplateRecalibration, ConnectionMonitor, CrashRecovery, NotificationSystem
from core.task_scheduler import TaskScheduler
from config.config_manager import ConfigManager


def setup_logging(verbose: bool = False):
    """
    Setup logging configuration
    
    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main bot execution"""
    parser = argparse.ArgumentParser(description='Dark War Survival Bot - Enhanced Version')
    parser.add_argument('--config', type=str, default='config.json',
                       help='Path to configuration file')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--detect-window', action='store_true',
                       help='Detect BlueStacks window and exit')
    parser.add_argument('--test-templates', action='store_true',
                       help='Test template matching and exit')
    parser.add_argument('--max-cycles', type=int, default=None,
                       help='Maximum number of task cycles (None = infinite)')
    parser.add_argument('--cycle-delay', type=int, default=60,
                       help='Delay between cycles in seconds')
    parser.add_argument('--webhook-url', type=str, default=None,
                       help='Discord webhook URL for notifications')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    logging.info("=" * 60)
    logging.info("Dark War Survival Bot - Enhanced Version")
    logging.info("=" * 60)
    
    # Load configuration
    config_manager = ConfigManager(args.config)
    config = config_manager.load_config()
    
    # Initialize bot
    bot = DarkWarBot(config)
    
    # Window detection mode
    if args.detect_window:
        logging.info("Window detection mode")
        if bot.find_bluestacks_window():
            logging.info("✓ BlueStacks window found and focused")
            logging.info(f"Window position: {bot.window_rect}")
            return 0
        else:
            logging.error("✗ BlueStacks window not found")
            return 1
    
    # Initialize all modules
    task_automation = TaskAutomation(bot)
    error_recovery = ErrorRecovery(bot)
    template_recalibration = TemplateRecalibration(bot)
    connection_monitor = ConnectionMonitor(bot)
    crash_recovery = CrashRecovery()
    notification_system = NotificationSystem(args.webhook_url)
    task_scheduler = TaskScheduler(task_automation)
    
    # Link error recovery to bot
    bot.error_recovery = error_recovery
    
    # Register all default tasks
    task_scheduler.register_default_tasks()
    
    # Template testing mode
    if args.test_templates:
        logging.info("Template testing mode")
        test_templates(bot, template_recalibration)
        return 0
    
    # Load saved state if exists
    saved_state = crash_recovery.load_state()
    if saved_state:
        logging.info("Resuming from saved state")
        # Restore state (task history, etc.)
    
    # Send startup notification
    notification_system.notify_status("Bot started successfully")
    
    # Main bot loop
    try:
        cycle_count = 0
        start_time = time()
        
        while True:
            cycle_count += 1
            logging.info(f"\n{'='*60}")
            logging.info(f"CYCLE {cycle_count} - Runtime: {(time() - start_time)/3600:.1f}h")
            logging.info(f"{'='*60}\n")
            
            # Check connection
            if not connection_monitor.is_connected():
                logging.error("Connection lost!")
                notification_system.notify_error("CONNECTION_LOSS", "Bot lost connection to game")
                
                if connection_monitor.handle_connection_loss():
                    notification_system.notify_status("Connection restored")
                else:
                    logging.error("Failed to restore connection - stopping bot")
                    break
            
            # Check for game updates
            if connection_monitor.detect_game_update():
                logging.warning("Game update detected - stopping bot")
                notification_system.notify_error("GAME_UPDATE", "Game update detected - bot stopped")
                break
            
            # Check if too many errors
            if error_recovery.should_pause(threshold=5):
                logging.error("Too many consecutive errors - pausing for 5 minutes")
                notification_system.notify_error("ERROR_THRESHOLD", 
                                                f"Too many errors ({error_recovery.consecutive_errors})")
                sleep(300)
                error_recovery.consecutive_errors = 0
            
            # Execute task cycle
            try:
                tasks_executed = task_scheduler.execute_cycle(max_tasks=5)
                
                if tasks_executed == 0:
                    logging.info("No tasks available - waiting...")
                    sleep(args.cycle_delay)
                else:
                    error_recovery.reset_error_counter()
                
            except Exception as e:
                logging.error(f"Error during task cycle: {e}")
                error_recovery.log_error("TASK_CYCLE_ERROR", str(e))
                sleep(30)
            
            # Periodic maintenance
            if cycle_count % 10 == 0:
                logging.info("\n--- Periodic Maintenance ---")
                task_scheduler.print_statistics()
                task_scheduler.optimize_priorities()
                
                # Save state
                state_data = {
                    'cycle_count': cycle_count,
                    'runtime': time() - start_time,
                    'task_stats': task_scheduler.get_task_statistics()
                }
                crash_recovery.save_state(state_data)
            
            # Send status update every hour
            if cycle_count % 60 == 0:
                runtime_hours = (time() - start_time) / 3600
                notification_system.notify_status(
                    f"Bot running for {runtime_hours:.1f}h - "
                    f"{bot.action_count} actions completed"
                )
            
            # Check max cycles
            if args.max_cycles and cycle_count >= args.max_cycles:
                logging.info(f"Reached maximum cycles ({args.max_cycles})")
                break
            
            # Delay between cycles
            if tasks_executed > 0:
                delay = random.uniform(args.cycle_delay * 0.8, args.cycle_delay * 1.2)
                logging.info(f"Waiting {delay:.1f}s before next cycle...")
                sleep(delay)
        
    except KeyboardInterrupt:
        logging.info("\nBot stopped by user")
        notification_system.notify_status("Bot stopped by user")
    
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        error_recovery.log_error("FATAL_ERROR", str(e))
        notification_system.notify_error("FATAL_ERROR", str(e))
    
    finally:
        # Final statistics
        logging.info("\n" + "=" * 60)
        logging.info("FINAL STATISTICS")
        logging.info("=" * 60)
        
        runtime = time() - start_time
        logging.info(f"Total runtime: {runtime/3600:.2f} hours")
        logging.info(f"Total cycles: {cycle_count}")
        logging.info(f"Total actions: {bot.action_count}")
        logging.info(f"Total errors: {error_recovery.error_count}")
        
        task_scheduler.print_statistics()
        
        # Clean up
        crash_recovery.clear_state()
        notification_system.notify_status(
            f"Bot stopped - Runtime: {runtime/3600:.1f}h, Actions: {bot.action_count}"
        )
    
    return 0


def test_templates(bot: DarkWarBot, recalibration: TemplateRecalibration):
    """
    Test all templates and report results
    
    Args:
        bot: DarkWarBot instance
        recalibration: TemplateRecalibration instance
    """
    import os
    
    logging.info("Testing all templates...")
    
    screenshot = bot.capture_screen()
    if screenshot is None:
        logging.error("Failed to capture screenshot")
        return
    
    template_dir = 'templates'
    templates = [f for f in os.listdir(template_dir) if f.endswith('.png')]
    
    results = []
    
    for template_name in templates:
        location = bot.find_template(screenshot, template_name, threshold=0.7)
        
        if location:
            logging.info(f"✓ {template_name:30} - Found at {location}")
            recalibration.record_template_result(template_name, True)
            results.append((template_name, True, location))
        else:
            logging.warning(f"✗ {template_name:30} - Not found")
            recalibration.record_template_result(template_name, False)
            results.append((template_name, False, None))
    
    # Summary
    found = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    logging.info(f"\n{'='*60}")
    logging.info(f"Template Test Results: {found}/{total} found ({found/total*100:.1f}%)")
    logging.info(f"{'='*60}")


if __name__ == '__main__':
    sys.exit(main())
