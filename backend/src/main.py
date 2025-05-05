from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

from core.pr_analyzer import analyze_pull_request
from core.code_reviewer import review_code
from utils.github_service import GitHubService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="PR Summary & Code Review Assistant",
    description="API for generating PR summaries and conducting code reviews",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/code-review", response_model=CodeReviewResponse)
async def perform_code_review(
    request: CodeReviewRequest,
    background_tasks: BackgroundTasks
):
    try:
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
        
        return review_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 