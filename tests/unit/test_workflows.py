"""
Unit tests for workflows module
"""

import asyncio

import pytest

from src.workflows import JobStatus, Task, Workflow, WorkflowRun


@pytest.mark.unit
@pytest.mark.workflow
def test_task_creation():
    """Test task creation"""
    def dummy_func():
        return "result"

    task = Task(name="test", func=dummy_func)

    assert task.name == "test"
    assert task.func == dummy_func
    assert task.skip is False


@pytest.mark.unit
@pytest.mark.workflow
def test_workflow_creation():
    """Test workflow creation"""
    workflow = Workflow(name="test_workflow", description="Test workflow")

    assert workflow.name == "test_workflow"
    assert workflow.description == "Test workflow"
    assert len(workflow.tasks) == 0


@pytest.mark.unit
@pytest.mark.workflow
def test_workflow_add_task():
    """Test adding tasks to workflow"""
    def dummy_func():
        return "result"

    workflow = Workflow("test")
    task = Task(name="task1", func=dummy_func)
    workflow.add_task(task)

    assert len(workflow.tasks) == 1
    assert workflow.tasks[0].name == "task1"


@pytest.mark.unit
@pytest.mark.workflow
def test_workflow_add_multiple_tasks():
    """Test adding multiple tasks"""
    def dummy_func():
        return "result"

    workflow = Workflow("test")
    task1 = Task(name="task1", func=dummy_func)
    task2 = Task(name="task2", func=dummy_func)

    workflow.add_tasks(task1, task2)

    assert len(workflow.tasks) == 2


@pytest.mark.unit
@pytest.mark.workflow
@pytest.mark.asyncio
async def test_task_execution():
    """Test task execution"""
    def sync_func():
        return "completed"

    task = Task(name="test", func=sync_func)
    result = await task.execute()

    assert result == "completed"


@pytest.mark.unit
@pytest.mark.workflow
@pytest.mark.asyncio
async def test_workflow_execution():
    """Test workflow execution"""
    results = []

    def task_func(value):
        results.append(value)
        return value

    workflow = Workflow("test")
    workflow.add_task(Task(name="task1", func=task_func, args=(1,)))
    workflow.add_task(Task(name="task2", func=task_func, args=(2,)))

    run = await workflow.execute()

    assert run.status == JobStatus.SUCCESS
    assert run.tasks_run == 2
    assert results == [1, 2]


@pytest.mark.unit
@pytest.mark.workflow
def test_workflow_run_to_dict():
    """Test WorkflowRun serialization"""
    run = WorkflowRun(
        workflow_name="test",
        run_id="run-123",
        status=JobStatus.SUCCESS,
        tasks_run=2,
    )

    data = run.to_dict()

    assert data["workflow_name"] == "test"
    assert data["run_id"] == "run-123"
    assert data["status"] == "success"
    assert data["tasks_run"] == 2
