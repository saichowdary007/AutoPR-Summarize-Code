#!/bin/bash

# PR Summary & Code Review Assistant Start Script

# Check if the setup has been run
if [ ! -f "./backend/.env" ] || [ ! -f "./frontend/.env.local" ]; then
  echo "Please run ./setup.sh first to set up the environment."
  exit 1
fi

# Start the services using the npm script
npm run dev 