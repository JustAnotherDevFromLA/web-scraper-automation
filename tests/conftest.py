"""
Test configuration and pytest setup
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

# Register fixtures
pytest_plugins = ["tests.fixtures"]
