"""
Test fixtures and mock data
"""

from unittest.mock import Mock, patch

import pytest

from src.config import AppConfig
from src.database import Base, SessionLocal, engine
from src.workflows import Task, Workflow


@pytest.fixture(scope="session")
def test_config():
    """Create test configuration"""
    config = AppConfig()
    config.debug = True
    config.environment = "testing"
    return config


@pytest.fixture(scope="function")
def test_db():
    """Create test database"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    # Drop tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_response():
    """Mock HTTP response"""
    mock = Mock()
    mock.status_code = 200
    mock.text = "<html><body>Test</body></html>"
    mock.content = b"<html><body>Test</body></html>"
    mock.headers = {"Content-Type": "text/html"}
    return mock


@pytest.fixture
def mock_session():
    """Mock requests session"""
    with patch("requests.Session") as mock:
        yield mock


@pytest.fixture
def sample_workflow():
    """Create sample workflow for testing"""
    def task_func():
        return "test_result"

    workflow = Workflow("test_workflow")
    workflow.add_task(Task(name="test_task", func=task_func))
    return workflow


@pytest.fixture
def sample_data():
    """Sample scraped data"""
    return {
        "url": "https://example.com",
        "title": "Example Domain",
        "content": "This domain is for use in examples...",
    }
