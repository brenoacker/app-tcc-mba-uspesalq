# Testing Guide

This guide explains how to run tests and contribute to test coverage for the MBA USP-ESALQ TCC Project.

## Testing Framework

This project uses:
- **pytest**: For running test suites
- **pytest-cov**: For measuring test coverage
- **unittest.mock**: For mocking dependencies in unit tests

## Test Types

The project employs various types of tests:

### 1. Unit Tests

Unit tests validate individual components in isolation.

- Located in files named `test_*.py` next to the implementation files
- Focus on testing a single class or function
- Dependencies are mocked or stubbed

### 2. Integration Tests

Integration tests validate that components work together properly.

- Located in the `tests/` directory
- Test interactions between multiple components
- May involve database interactions

### 3. Performance Tests

Performance tests measure and validate the system's performance characteristics.

- Reports are generated in `report_perf_test.ods`
- Used to identify performance bottlenecks

## Running Tests

### Using the PowerShell Script

The project includes a PowerShell script `run_tests.ps1` that sets up the correct PYTHONPATH and runs the tests.

#### Run all tests:

```powershell
.\run_tests.ps1
```

#### Run a specific test file:

```powershell
.\run_tests.ps1 src/domain/cart/test_cart_entity.py
```

#### Run tests with specific markers:

```powershell
.\run_tests.ps1 -m "unit"
```

### Manual Test Running

You can also run tests manually by setting the PYTHONPATH first:

```bash
# Linux/macOS
export PYTHONPATH=$PWD
python -m pytest src/domain/cart/test_cart_entity.py -v

# Windows PowerShell
$env:PYTHONPATH = $PWD
python -m pytest src/domain/cart/test_cart_entity.py -v
```

## Test Configuration

The test configuration is defined in `pytest.ini` and `conftest.py`.

### pytest.ini

```ini
[pytest]
testpaths = src
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: mark a test as a unit test
    integration: mark a test as an integration test
    slow: mark a test as slow
```

### conftest.py

This file contains fixtures that can be used across multiple tests. Common fixtures include:

- Database connections
- Test data setup and cleanup
- Authentication tokens

## Writing Tests

### Unit Test Example

Here's an example of a unit test for the Cart entity:

```python
def test_cart_create_with_valid_data():
    cart = Cart(user_id="123", items=[])
    assert cart.user_id == "123"
    assert cart.items == []
    assert cart.id is not None
```

### Testing Patterns

#### Arrange-Act-Assert (AAA)

Tests follow the AAA pattern:
1. **Arrange**: Set up the test environment
2. **Act**: Execute the code being tested
3. **Assert**: Verify the results

#### Given-When-Then (GWT)

Alternatively, tests can follow the GWT pattern:
1. **Given**: The initial context
2. **When**: An action occurs
3. **Then**: Verify the outcome

## Test Fixtures

Test fixtures are defined in the `tests/fixtures/` directory or in `conftest.py` files. These provide reusable test data and setup/cleanup procedures.

## Mocking

Dependencies are mocked using the `unittest.mock` library:

```python
from unittest.mock import Mock, patch

@patch('src.domain.user.user_repository_interface.UserRepository')
def test_get_user_use_case(mock_repo):
    # Configure the mock
    mock_repo.get_by_id.return_value = User(id="123", name="Test User")
    
    # Use the mock in the test
    use_case = GetUserUseCase(repository=mock_repo)
    result = use_case.execute(id="123")
    
    # Verify interactions with the mock
    mock_repo.get_by_id.assert_called_once_with("123")
    assert result.name == "Test User"
```

## Test Coverage

To run tests with coverage reporting:

```bash
python -m pytest --cov=src --cov-report=html src/
```

This generates an HTML coverage report in the `htmlcov/` directory.

## Continuous Integration

Tests are run automatically as part of the CI/CD pipeline:

- Tests run on every pull request
- A minimum coverage threshold is enforced
- Performance regression tests are run for major changes

## Tips for Effective Testing

1. **Test Business Rules**: Ensure all domain business rules are covered by tests
2. **Keep Tests Fast**: Slow tests discourage frequent running
3. **Independence**: Tests should be independent and not rely on each other
4. **Test Edge Cases**: Include tests for boundary conditions and error cases
5. **Clean Test Code**: Keep test code clean and readable like production code