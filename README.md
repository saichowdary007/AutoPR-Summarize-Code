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

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/pr-summary-review-assistant.git
cd pr-summary-review-assistant

# Run the setup script
./setup.sh

# Start the development servers
./start.sh
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