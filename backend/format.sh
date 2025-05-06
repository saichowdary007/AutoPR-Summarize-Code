#!/bin/bash

# Install black if it's not installed
pip install black

# Format all Python files in the src directory
black src/

echo "All Python files formatted successfully!" 