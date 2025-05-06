#!/bin/bash

# PR Summary & Code Review Assistant Enhanced Setup Script

echo "Setting up PR Summary & Code Review Assistant..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker to continue."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose to continue."
    exit 1
fi

# Create necessary directories
mkdir -p .github/workflows
mkdir -p backend/src/middleware
mkdir -p backend/src/routes

# Create GitHub Actions workflow files if they don't exist
if [ ! -f ".github/workflows/ci.yml" ]; then
  echo "GitHub Actions CI workflow already exists."
fi

if [ ! -f ".github/workflows/cd.yml" ]; then
  echo "GitHub Actions CD workflow already exists."
fi

# Create or update .env files
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

# Initialize middleware files
touch backend/src/middleware/__init__.py
touch backend/src/routes/__init__.py

# Create start script for Docker Compose
cat > docker-start.sh << 'EOL'
#!/bin/bash

# PR Summary & Code Review Assistant Docker Start Script

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker to continue."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose to continue."
    exit 1
fi

# Start the application using Docker Compose
docker-compose up -d

echo "Application started in the background"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
EOL
chmod +x docker-start.sh

# Set up traditional environment as well
echo "Setting up backend virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Setup complete!"
echo "You can now start the application using:"
echo "1. Traditional setup: ./start.sh"
echo "2. Docker setup: ./docker-start.sh"
echo ""
echo "For deployment, run: docker-compose build" 