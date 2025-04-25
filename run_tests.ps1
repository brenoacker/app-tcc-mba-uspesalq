# Script to run tests with the correct PYTHONPATH
$env:PYTHONPATH = $PWD

# If arguments are provided, run the specific tests
if ($args.Count -gt 0) {
    python -m pytest $args -v
}
# Otherwise run all tests
else {
    python -m pytest src -v
} 