from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import logging

from core.pr_analyzer import analyze_pull_request
from core.code_reviewer import review_code
from utils.github_service import GitHubService

# Import middleware
from middleware.rate_limiter import RateLimiter
from middleware.auth import AuthMiddleware
from middleware.logging import LoggingMiddleware, logger

# Import routes
from routes import health

# Load environment variables
load_dotenv()

app = FastAPI(
    title="PR Summary & Code Review Assistant",
    description="API for generating PR summaries and conducting code reviews",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimiter, max_requests=100, window_seconds=60)
app.add_middleware(
    AuthMiddleware, 
    exclude_paths=["/docs", "/redoc", "/openapi.json", "/health", "/readiness", "/liveness", "/"]
)

# Include health routes
app.include_router(health.router, tags=["Health"])

# Models
class PRRequest(BaseModel):
    repo_owner: str
    repo_name: str
    pr_number: int
    github_token: str
    config: Optional[Dict[str, Any]] = None

class CodeReviewRequest(BaseModel):
    repo_owner: str
    repo_name: str
    pr_number: int
    github_token: str
    config: Optional[Dict[str, Any]] = None
    post_comments: bool = False

class SummaryResponse(BaseModel):
    title: str
    overview: str
    changes_summary: List[str]
    affected_components: List[str]
    testing: Optional[str] = None
    dependencies: Optional[List[str]] = None
    migration_notes: Optional[str] = None
    potential_risks: Optional[List[str]] = None

class CodeReviewIssue(BaseModel):
    file: str
    line: int
    severity: str
    issue: str
    recommendation: str
    example: Optional[str] = None
    reference: Optional[str] = None

class CodeReviewResponse(BaseModel):
    security_issues: List[CodeReviewIssue] = []
    performance_issues: List[CodeReviewIssue] = []
    code_quality_issues: List[CodeReviewIssue] = []
    test_coverage_issues: List[CodeReviewIssue] = []
    statistics: Dict[str, Any] = {}

@app.get("/")
async def root():
    return {"message": "PR Summary & Code Review Assistant API"}

@app.post("/api/pr-summary", response_model=SummaryResponse)
async def generate_pr_summary(request: PRRequest):
    try:
        logger.info(f"Processing PR summary request for {request.repo_owner}/{request.repo_name}#{request.pr_number}")
        
        github_service = GitHubService(
            token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name
        )
        
        summary = await analyze_pull_request(
            github_service=github_service,
            pr_number=request.pr_number,
            config=request.config
        )
        
        logger.info(f"Successfully generated PR summary for {request.repo_owner}/{request.repo_name}#{request.pr_number}")
        return summary
    except Exception as e:
        logger.error(f"Error generating PR summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/code-review", response_model=CodeReviewResponse)
async def perform_code_review(
    request: CodeReviewRequest,
    background_tasks: BackgroundTasks
):
    try:
        logger.info(f"Processing code review request for {request.repo_owner}/{request.repo_name}#{request.pr_number}")
        
        github_service = GitHubService(
            token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name
        )
        
        review_results = await review_code(
            github_service=github_service,
            pr_number=request.pr_number,
            config=request.config
        )
        
        # Optionally post comments to GitHub PR
        if request.post_comments:
            background_tasks.add_task(
                github_service.post_review_comments,
                pr_number=request.pr_number,
                review_results=review_results
            )
        
        logger.info(f"Successfully completed code review for {request.repo_owner}/{request.repo_name}#{request.pr_number}")
        return review_results
    except Exception as e:
        logger.error(f"Error performing code review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "True").lower() == "true"
    uvicorn.run("main:app", host=host, port=port, reload=reload) 