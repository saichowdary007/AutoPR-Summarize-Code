#!/bin/bash

# PR Summary & Code Review Assistant Setup Script

echo "Setting up PR Summary & Code Review Assistant..."

# Create .env files if they don't exist
if [ ! -f "./backend/.env" ]; then
  echo "Creating backend .env file..."
  cat > ./backend/.env << EOL
# API Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=True  # Set to False in production

# GitHub Connection
# GITHUB_TOKEN=your_github_token_here

# Application Configuration
LOG_LEVEL=INFO
CONFIG_FILE=src/config/default_config.yaml

# Security
SECRET_KEY=developmentsecretkey  # Change in production
CORS_ORIGINS=http://localhost:3000

# PR Review Configuration
PR_ASSISTANT_STRICTNESS_LEVEL=3
EOL
  echo "Backend .env file created!"
fi

if [ ! -f "./frontend/.env.local" ]; then
  echo "Creating frontend .env.local file..."
  cat > ./frontend/.env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000
EOL
  echo "Frontend .env.local file created!"
fi

# Set up backend virtual environment
echo "Setting up backend virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install root dependencies
echo "Installing root dependencies..."
npm install

echo "Setup complete!"
echo "To start the development servers, run: npm run dev" 