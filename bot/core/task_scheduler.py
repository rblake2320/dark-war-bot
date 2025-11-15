"""
Intelligent task scheduler with priority-based execution
Manages task queue, dependencies, and optimal timing
"""

import logging
from time import time
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import random


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1    # Must do immediately (errors, shields expiring)
    HIGH = 2        # Important tasks (resource gathering, upgrades)
    MEDIUM = 3      # Regular tasks (training, research)
    LOW = 4         # Optional tasks (exploration, cosmetic)


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Represents a bot task"""
    name: str
    priority: TaskPriority
    action: Callable
    cooldown: int = 300  # seconds
    dependencies: List[str] = field(default_factory=list)
    resource_requirements: Dict[str, int] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    last_executed: float = 0
    success_count: int = 0
    failure_count: int = 0
    
    def can_execute(self, current_time: float, resources: Dict[str, int] = None) -> bool:
        """
        Check if task can be executed
        
        Args:
            current_time: Current timestamp
            resources: Available resources
            
        Returns:
            bool: True if task can execute
        """
        # Check cooldown
        if current_time - self.last_executed < self.cooldown:
            return False
        
        # Check resource requirements
        if resources and self.resource_requirements:
            for resource, amount in self.resource_requirements.items():
                if resources.get(resource, 0) < amount:
                    return False
        
        return True
    
    def execute(self) -> bool:
        """
        Execute the task
        
        Returns:
            bool: True if successful
        """
        try:
            self.status = TaskStatus.RUNNING
            result = self.action()
            
            if result:
                self.status = TaskStatus.COMPLETED
                self.success_count += 1
                self.last_executed = time()
                logging.info(f"Task '{self.name}' completed successfully")
                return True
            else:
                self.status = TaskStatus.FAILED
                self.failure_count += 1
                logging.warning(f"Task '{self.name}' failed")
                return False
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.failure_count += 1
            logging.error(f"Task '{self.name}' error: {e}")
            return False
        finally:
            if self.status != TaskStatus.COMPLETED:
                self.status = TaskStatus.PENDING
    
    def get_success_rate(self) -> float:
        """Get task success rate"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return self.success_count / total


class TaskScheduler:
    """Intelligent task scheduler"""
    
    def __init__(self, task_automation):
        """
        Initialize task scheduler
        
        Args:
            task_automation: TaskAutomation instance
        """
        self.task_automation = task_automation
        self.bot = task_automation.bot
        self.tasks: List[Task] = []
        self.task_history: List[Dict] = []
        self.resources = {
            'food': 0,
            'wood': 0,
            'stone': 0,
            'iron': 0
        }
    
    def register_task(self, task: Task):
        """
        Register a new task
        
        Args:
            task: Task to register
        """
        self.tasks.append(task)
        logging.info(f"Registered task: {task.name} (Priority: {task.priority.name})")
    
    def register_default_tasks(self):
        """Register all default game tasks"""
        
        # Resource gathering - HIGH priority
        for resource in ['food', 'wood', 'stone', 'iron']:
            self.register_task(Task(
                name=f"gather_{resource}",
                priority=TaskPriority.HIGH,
                action=lambda r=resource: self.task_automation.gather_resource(r),
                cooldown=300
            ))
        
        # Building upgrades - HIGH priority
        self.register_task(Task(
            name="upgrade_buildings",
            priority=TaskPriority.HIGH,
            action=self.task_automation.upgrade_all_buildings,
            cooldown=600,
            resource_requirements={'food': 1000, 'wood': 1000}
        ))
        
        # Troop training - MEDIUM priority
        self.register_task(Task(
            name="train_troops",
            priority=TaskPriority.MEDIUM,
            action=lambda: self.task_automation.train_specific_troops('infantry'),
            cooldown=400,
            resource_requirements={'food': 500}
        ))
        
        # Heal troops - CRITICAL when needed
        self.register_task(Task(
            name="heal_troops",
            priority=TaskPriority.CRITICAL,
            action=self.task_automation.heal_troops,
            cooldown=600
        ))
        
        # Research - MEDIUM priority
        self.register_task(Task(
            name="research",
            priority=TaskPriority.MEDIUM,
            action=self.task_automation.start_research,
            cooldown=1800
        ))
        
        # Collect rewards - HIGH priority
        self.register_task(Task(
            name="collect_mail",
            priority=TaskPriority.HIGH,
            action=self.task_automation.collect_mail_rewards,
            cooldown=900
        ))
        
        self.register_task(Task(
            name="claim_rewards",
            priority=TaskPriority.HIGH,
            action=self.task_automation.claim_daily_rewards,
            cooldown=1200
        ))
        
        # Alliance help - MEDIUM priority
        self.register_task(Task(
            name="alliance_help",
            priority=TaskPriority.MEDIUM,
            action=self.task_automation.alliance_help_all,
            cooldown=300
        ))
        
        # Hero management - MEDIUM priority
        self.register_task(Task(
            name="hero_management",
            priority=TaskPriority.MEDIUM,
            action=self.task_automation.manage_heroes,
            cooldown=1800
        ))
        
        # Exploration - LOW priority
        self.register_task(Task(
            name="exploration",
            priority=TaskPriority.LOW,
            action=self.task_automation.start_exploration,
            cooldown=2400
        ))
        
        # Shield activation - CRITICAL (conditional)
        self.register_task(Task(
            name="activate_shield",
            priority=TaskPriority.CRITICAL,
            action=lambda: self.task_automation.activate_shield('8h'),
            cooldown=3600
        ))
        
        logging.info(f"Registered {len(self.tasks)} default tasks")
    
    def get_executable_tasks(self) -> List[Task]:
        """
        Get list of tasks that can be executed now
        
        Returns:
            List[Task]: Executable tasks sorted by priority
        """
        current_time = time()
        executable = []
        
        for task in self.tasks:
            if task.can_execute(current_time, self.resources):
                # Check dependencies
                dependencies_met = True
                for dep_name in task.dependencies:
                    dep_task = next((t for t in self.tasks if t.name == dep_name), None)
                    if dep_task and dep_task.status != TaskStatus.COMPLETED:
                        dependencies_met = False
                        break
                
                if dependencies_met:
                    executable.append(task)
        
        # Sort by priority (lower number = higher priority)
        executable.sort(key=lambda t: (t.priority.value, random.random()))
        
        return executable
    
    def execute_next_task(self) -> Optional[Task]:
        """
        Execute the next highest priority task
        
        Returns:
            Task: Executed task or None
        """
        executable_tasks = self.get_executable_tasks()
        
        if not executable_tasks:
            logging.debug("No executable tasks available")
            return None
        
        task = executable_tasks[0]
        logging.info(f"Executing task: {task.name} (Priority: {task.priority.name})")
        
        success = task.execute()
        
        # Record in history
        self.task_history.append({
            'task': task.name,
            'timestamp': time(),
            'success': success,
            'priority': task.priority.name
        })
        
        return task
    
    def execute_cycle(self, max_tasks: int = 5) -> int:
        """
        Execute a cycle of tasks
        
        Args:
            max_tasks: Maximum tasks to execute in one cycle
            
        Returns:
            int: Number of tasks executed
        """
        executed_count = 0
        
        for _ in range(max_tasks):
            task = self.execute_next_task()
            if task:
                executed_count += 1
                # Add delay between tasks
                import time as time_module
                time_module.sleep(random.uniform(3, 7))
            else:
                break
        
        logging.info(f"Cycle complete: {executed_count} tasks executed")
        return executed_count
    
    def get_task_statistics(self) -> Dict:
        """
        Get task execution statistics
        
        Returns:
            Dict: Statistics for all tasks
        """
        stats = {}
        
        for task in self.tasks:
            stats[task.name] = {
                'success_count': task.success_count,
                'failure_count': task.failure_count,
                'success_rate': task.get_success_rate(),
                'last_executed': task.last_executed,
                'status': task.status.value
            }
        
        return stats
    
    def print_statistics(self):
        """Print task statistics to log"""
        stats = self.get_task_statistics()
        
        logging.info("=" * 60)
        logging.info("TASK STATISTICS")
        logging.info("=" * 60)
        
        for task_name, task_stats in stats.items():
            success_rate = task_stats['success_rate'] * 100
            logging.info(f"{task_name:20} | Success: {task_stats['success_count']:3} | "
                        f"Failed: {task_stats['failure_count']:3} | Rate: {success_rate:5.1f}%")
        
        logging.info("=" * 60)
    
    def optimize_priorities(self):
        """Automatically adjust task priorities based on success rates"""
        for task in self.tasks:
            success_rate = task.get_success_rate()
            
            # If task consistently fails, lower priority
            if task.failure_count > 5 and success_rate < 0.3:
                if task.priority != TaskPriority.LOW:
                    old_priority = task.priority
                    task.priority = TaskPriority(min(task.priority.value + 1, 4))
                    logging.info(f"Lowered priority for {task.name}: "
                               f"{old_priority.name} -> {task.priority.name}")
            
            # If task consistently succeeds, can raise priority
            elif task.success_count > 10 and success_rate > 0.9:
                if task.priority != TaskPriority.CRITICAL:
                    old_priority = task.priority
                    task.priority = TaskPriority(max(task.priority.value - 1, 2))
                    logging.info(f"Raised priority for {task.name}: "
                               f"{old_priority.name} -> {task.priority.name}")
    
    def update_resources(self, resources: Dict[str, int]):
        """
        Update available resources
        
        Args:
            resources: Dictionary of resource amounts
        """
        self.resources.update(resources)
        logging.debug(f"Resources updated: {self.resources}")
    
    def clear_completed_tasks(self):
        """Reset completed task statuses"""
        for task in self.tasks:
            if task.status == TaskStatus.COMPLETED:
                task.status = TaskStatus.PENDING
