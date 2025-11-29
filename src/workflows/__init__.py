"""
Workflow orchestration and job scheduling
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from loguru import logger

from src.config import config


class JobStatus(str, Enum):
    """Job execution status"""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Individual task within a workflow"""

    name: str
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    timeout: Optional[int] = None
    skip: bool = False

    async def execute(self) -> Any:
        """Execute task and return result"""
        logger.info(f"Executing task: {self.name}")

        try:
            import asyncio

            # Run function with timeout
            timeout = self.timeout or config.workflow.job_timeout

            if asyncio.iscoroutinefunction(self.func):
                result = await asyncio.wait_for(
                    self.func(*self.args, **self.kwargs), timeout=timeout
                )
            else:
                # Run sync function in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, lambda: self.func(*self.args, **self.kwargs)
                )

            logger.info(f"Task {self.name} completed successfully")
            return result

        except asyncio.TimeoutError:
            logger.error(f"Task {self.name} timed out after {timeout}s")
            raise
        except Exception as e:
            logger.error(f"Task {self.name} failed: {str(e)}")
            raise


@dataclass
class WorkflowRun:
    """Single execution of a workflow"""

    workflow_name: str
    run_id: str
    status: JobStatus = JobStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tasks_run: int = 0
    tasks_failed: int = 0
    tasks_skipped: int = 0
    error: Optional[str] = None
    results: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> Optional[float]:
        """Get workflow duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "workflow_name": self.workflow_name,
            "run_id": self.run_id,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration": self.duration,
            "tasks_run": self.tasks_run,
            "tasks_failed": self.tasks_failed,
            "tasks_skipped": self.tasks_skipped,
            "error": self.error,
        }


class Workflow:
    """Workflow orchestration with task management and error handling"""

    def __init__(self, name: str, description: Optional[str] = None):
        """Initialize workflow"""
        self.name = name
        self.description = description
        self.tasks: List[Task] = []

        logger.info(f"Created workflow: {name}")

    def add_task(self, task: Task) -> "Workflow":
        """Add task to workflow"""
        self.tasks.append(task)
        logger.debug(f"Added task '{task.name}' to workflow '{self.name}'")
        return self

    def add_tasks(self, *tasks: Task) -> "Workflow":
        """Add multiple tasks"""
        for task in tasks:
            self.add_task(task)
        return self

    async def execute(self) -> WorkflowRun:
        """Execute all tasks in workflow sequentially"""
        import uuid

        run_id = str(uuid.uuid4())[:8]
        run = WorkflowRun(workflow_name=self.name, run_id=run_id)

        try:
            run.status = JobStatus.RUNNING
            run.started_at = datetime.now()

            logger.info(f"Starting workflow '{self.name}' (run_id: {run_id})")

            for task in self.tasks:
                if task.skip:
                    logger.info(f"Skipping task: {task.name}")
                    run.tasks_skipped += 1
                    continue

                try:
                    result = await task.execute()
                    run.results[task.name] = result
                    run.tasks_run += 1

                except Exception as e:
                    logger.error(f"Task '{task.name}' failed: {str(e)}")
                    run.tasks_failed += 1

                    # Stop on first failure (can be configurable)
                    run.error = str(e)
                    run.status = JobStatus.FAILED
                    raise

            run.status = JobStatus.SUCCESS

        except Exception as e:
            run.status = JobStatus.FAILED
            run.error = str(e)
            logger.error(f"Workflow '{self.name}' failed: {str(e)}")

        finally:
            run.completed_at = datetime.now()
            logger.info(
                f"Workflow '{self.name}' completed in {run.duration:.2f}s "
                f"(tasks: {run.tasks_run}, failed: {run.tasks_failed}, "
                f"skipped: {run.tasks_skipped})"
            )

        return run


class WorkflowScheduler:
    """Schedule workflows to run at intervals"""

    def __init__(self):
        """Initialize scheduler"""
        self.workflows: Dict[str, Workflow] = {}
        logger.info("Initialized WorkflowScheduler")

    def register(self, workflow: Workflow, interval_seconds: int) -> None:
        """Register workflow for periodic execution"""
        import schedule

        def run_workflow():
            import asyncio

            asyncio.run(workflow.execute())

        schedule.every(interval_seconds).seconds.do(run_workflow)
        self.workflows[workflow.name] = workflow

        logger.info(
            f"Registered workflow '{workflow.name}' to run every {interval_seconds}s"
        )

    def run(self) -> None:
        """Start scheduler loop"""
        import schedule

        logger.info("Starting WorkflowScheduler...")

        try:
            while True:
                schedule.run_pending()
                import time

                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("WorkflowScheduler stopped")


if __name__ == "__main__":
    import asyncio

    # Example workflow
    async def example_task():
        return "Task completed!"

    workflow = Workflow("example_workflow")
    workflow.add_task(Task(name="step1", func=example_task))
    workflow.add_task(Task(name="step2", func=example_task))

    run = asyncio.run(workflow.execute())
    print(run.to_dict())
