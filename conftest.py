import pytest

# This will automatically mark all tests with pytest.mark.asyncio
pytest.importorskip("pytest_asyncio")
pytest_plugins = ["pytest_asyncio"] 