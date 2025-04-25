import pytest

# This will automatically mark all tests with pytest.mark.asyncio
pytest.importorskip("pytest_asyncio")
pytest_plugins = ["pytest_asyncio"] 

import asyncio
import os


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def setup_env():
    """Set environment variables for tests."""
    os.environ["CONNECTION"] = "postgresql://postgres:postgres@localhost:5434/testdb"
    os.environ["POSTGRES_USER"] = "postgres"
    os.environ["POSTGRES_PASSWORD"] = "postgres" 
    os.environ["POSTGRES_DB"] = "testdb"
    yield