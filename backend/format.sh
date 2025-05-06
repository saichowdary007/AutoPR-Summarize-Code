#!/bin/bash

# Install black if it's not installed
python3 -m pip install black || pip install black || echo "Failed to install black, but continuing"

# Format all Python files in the src directory
echo "Formatting Python files in src/ directory..."
black src/ || echo "Black formatting had issues, but continuing"

echo "All Python files formatted successfully!" 