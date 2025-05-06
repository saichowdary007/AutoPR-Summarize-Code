#!/bin/bash

echo "Formatting backend code with black..."
cd backend && ./format.sh && cd ..

echo "Adding changes to git..."
git add .

echo "Committing changes..."
git commit -m "Format Python code with black and update workflows"

echo "Pushing to GitHub..."
git push origin main

echo "Done! Changes have been formatted, committed, and pushed." 