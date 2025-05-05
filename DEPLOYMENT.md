# Deployment Guide

This document provides instructions for deploying the PR Summary & Code Review Assistant in various environments.

## Prerequisites

- Python 3.8+
- Node.js 14+
- Docker (optional)
- GitHub account with a personal access token

## Environment Setup

### Environment Variables

The application requires certain environment variables to be set:

#### Backend (Python FastAPI)

Create a `.env` file in the backend directory:

```bash
# API Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=False  # Set to False in production

# GitHub Connection
GITHUB_TOKEN=your_github_token_here

# Application Configuration
LOG_LEVEL=INFO
CONFIG_FILE=src/config/default_config.yaml

# Security
SECRET_KEY=your_secret_key_here  # Generate a strong random key
CORS_ORIGINS=https://your-frontend-domain.com

# PR Review Configuration
PR_ASSISTANT_STRICTNESS_LEVEL=3
```

#### Frontend (Next.js)

Create a `.env.production` file in the frontend directory:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-api-url.com
```

## Deployment Options

### Option 1: Traditional Deployment

#### Backend Deployment

1. Set up a virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run with a production WSGI server:

```bash
cd src
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

3. Configure Nginx or Apache as a reverse proxy (recommended for production).

#### Frontend Deployment

1. Build the Next.js application:

```bash
cd frontend
npm install
npm run build
```

2. Start the production server:

```bash
npm run start
```

3. Alternatively, use a static export if your hosting doesn't support Node.js:

```bash
# Add "export": "next export" to package.json scripts
npm run build
npm run export
# Deploy the 'out' directory to your static hosting
```

### Option 2: Docker Deployment

#### Using Docker Compose

Create a `docker-compose.yml` file in the project root:

```yaml
version: '3'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend/src:/app/src

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    env_file:
      - ./frontend/.env.production
    depends_on:
      - backend
```

Create a Dockerfile for the backend in the `backend` directory:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/run.py"]
```

Create a Dockerfile for the frontend in the `frontend` directory:

```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

CMD ["npm", "run", "start"]
```

Start the services:

```bash
docker-compose up -d
```

### Option 3: Cloud Platform Deployment

#### AWS Deployment

1. Backend: Deploy as an AWS Lambda function with API Gateway, or use Elastic Beanstalk
2. Frontend: Deploy to S3 with CloudFront for distribution

#### Heroku Deployment

1. Add a Procfile to the backend directory:

```
web: cd src && uvicorn main:app --host=0.0.0.0 --port=$PORT
```

2. Deploy both services:

```bash
# Deploy backend
cd backend
heroku create pr-assistant-api
git init
heroku git:remote -a pr-assistant-api
git add .
git commit -m "Initial backend deployment"
git push heroku master

# Deploy frontend
cd frontend
heroku create pr-assistant-frontend
git init
heroku git:remote -a pr-assistant-frontend
git add .
git commit -m "Initial frontend deployment"
git push heroku master
```

## Security Considerations

1. **GitHub Token:** Use a token with minimal permissions (repo access only)
2. **API Security:** Set up rate limiting and authentication for the API
3. **CORS:** Restrict CORS to only your frontend domain in production
4. **Environment Variables:** Never commit sensitive values to the repository

## Monitoring & Maintenance

- Set up logging with CloudWatch, LogDNA, or similar services
- Configure monitoring alerts for application health
- Implement a CI/CD pipeline for automated testing and deployment 