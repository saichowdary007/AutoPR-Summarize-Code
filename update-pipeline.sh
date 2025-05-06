#!/bin/bash

# Fix all Python issues with our script
echo "Fixing Python issues..."
cd backend && ./pylint-fix.sh && cd ..

# Add changes to git
echo "Adding changes to git..."
git add backend/src/
git add backend/.pylintrc
git add backend/.gitignore
git add backend/setup.py
git add .github/workflows/ci.yml

# Commit changes
echo "Committing changes..."
git commit -m "Fix pylint and other code quality issues"

# Push changes
echo "Pushing changes..."
git push origin main

echo "Done! All fixes have been committed and pushed." 