#!/bin/bash

echo "Rebuilding frontend..."

# Remove build cache
rm -rf .next

# Remove node_modules
rm -rf node_modules

# Reinstall dependencies
npm install

# Rebuild the application
npm run build

# Start development server
npm run dev 