#!/bin/bash
# Activates the project's virtual environment and runs the test suite.
# Exits 0 if all tests pass, 1 otherwise.

# Activate the virtual environment (supports both Windows and Unix venv layouts)
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Could not find virtual environment activation script."
    exit 1
fi

# Run the test suite
pytest test_app.py

# Exit with the appropriate code based on the test result
if [ $? -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Some tests failed."
    exit 1
fi