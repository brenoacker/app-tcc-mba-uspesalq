# MBA USP-ESALQ TCC Project

## Running Tests

To run the tests correctly, you need to make sure Python can find the modules in the project. We've provided a PowerShell script to help with this.

### Using the PowerShell Script

Run all tests:
```powershell
.\run_tests.ps1
```

Run a specific test file:
```powershell
.\run_tests.ps1 src/domain/cart/test_cart_entity.py
```

### Manual Method

If you prefer to run tests manually, set the PYTHONPATH environment variable first:

```powershell
$env:PYTHONPATH = $PWD
python -m pytest src/domain/cart/test_cart_entity.py -v
```

## Project Structure

- `src/`: Main source code
  - `domain/`: Domain entities and business rules
  - `usecases/`: Application use cases
  - `infrastructure/`: External interfaces like databases and APIs 