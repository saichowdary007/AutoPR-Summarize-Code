#!/bin/bash

# Set up venv if not exists
if [ ! -d "temp_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv temp_venv
fi

# Activate venv
source temp_venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install pylint black isort autopep8

# Format with black
echo "Formatting code with black..."
black src/

# Sort imports with isort
echo "Sorting imports with isort..."
isort src/

# Run autopep8 for additional fixes
echo "Running autopep8 for additional fixes..."
autopep8 --in-place --recursive --aggressive --aggressive src/

# Run pylint to see remaining issues
echo "Running pylint to check for remaining issues..."
pylint --rcfile=.pylintrc src/ || echo "Linting issues found but all automatic fixes have been applied."

echo "All automatic fixes have been applied!" 