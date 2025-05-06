# PR Summary & Code Review Assistant

A powerful tool for generating comprehensive PR summaries and conducting code reviews automatically.

## Overview

This application helps developers and reviewers by:

1. **Generating PR Summaries** - Analyze PR content, changes, and context to create structured summaries
2. **Conducting Code Reviews** - Scan code for security, performance, quality, and test coverage issues
3. **Providing Actionable Feedback** - Offer specific recommendations for improvements

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: Next.js
- **GitHub Integration**: PyGithub

## Features

### PR Summary Generation

- Automatic title & overview extraction
- Key changes summary
- Affected components listing
- Testing information
- Dependency changes detection
- Migration notes identification
- Potential risk highlighting

### Code Review Capabilities

- **Security Analysis**
  - SQL injection detection
  - XSS vulnerability scanning
  - Hardcoded secrets detection
  - Path traversal vulnerabilities
  - Insecure randomness
  - Language-specific security issues

- **Performance Analysis**
  - Time complexity warnings (nested loops)
  - Memory usage concerns
  - Inefficient patterns detection
  - Language-specific performance issues

- **Code Quality Assessment**
  - Long functions detection
  - Magic numbers identification
  - TODO comment tracking
  - Code style evaluation
  - Language-specific quality checks

- **Test Coverage Evaluation**
  - Missing test detection
  - Testable code identification
  - Test quality assessment

## Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- GitHub access token (for API integration)
- Docker & Docker Compose (for containerized deployment)

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/pr-summary-review-assistant.git
cd pr-summary-review-assistant

# Run the enhanced setup script
./enhanced_setup.sh

# Start the development servers
# Traditional method:
./start.sh

# Or using Docker:
./docker-start.sh
```

### Manual Setup

#### Backend Setup

```bash
# Set up Python environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the API server
cd src
python run.py
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Run development server
npm run dev
```

## CI/CD Pipeline

This project includes a complete CI/CD pipeline using GitHub Actions:

- **Continuous Integration**: Automated testing, linting, and code quality checks
- **Continuous Deployment**: Automated Docker image building and deployment

### Pipeline Workflows

- `ci.yml`: Runs on every pull request to ensure code quality
- `cd.yml`: Runs on merges to the main branch to deploy changes

## Docker Deployment

The application can be run using Docker:

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## API Security

The backend API includes several security features:

- **Rate Limiting**: Prevents abuse by limiting requests per client
- **JWT Authentication**: Secures API endpoints requiring authentication
- **CORS Protection**: Controls which domains can access the API
- **Request Logging**: Tracks all API requests for auditing

## Monitoring

The application includes health check endpoints for monitoring:

- `/health`: Returns detailed service metrics
- `/readiness`: Kubernetes readiness probe endpoint
- `/liveness`: Kubernetes liveness probe endpoint

## Usage

### API Endpoints

- `POST /api/pr-summary` - Generate PR summary
- `POST /api/code-review` - Perform code review

### Configuration

The application can be configured through:

1. YAML configuration file (`backend/src/config/default_config.yaml`)
2. Environment variables (prefixed with `PR_ASSISTANT_`)
3. Runtime API parameters

See the [Configuration Guide](docs/configuration.md) for detailed options.

## License

MIT 