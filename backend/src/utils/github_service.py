import os
import base64
from typing import Dict, List, Any, Optional, Tuple
from github import Github, GithubException, PullRequest, Repository, ContentFile
from github.PullRequest import PullRequest
from github.Repository import Repository


class GitHubService:
    def __init__(self, token: str, repo_owner: str, repo_name: str):
        """
        Initialize GitHub service with credentials.

        Args:
            token: GitHub personal access token
            repo_owner: Repository owner/organization
            repo_name: Repository name
        """
        self.client = Github(token)
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo = self.client.get_repo(f"{repo_owner}/{repo_name}")

    async def get_pull_request(self, pr_number: int) -> PullRequest:
        """
        Get a specific pull request by number.

        Args:
            pr_number: Pull request number

        Returns:
            PullRequest object
        """
        return self.repo.get_pull(pr_number)

    async def get_pr_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """
        Get all files changed in a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            List of changed files with metadata
        """
        pr = await self.get_pull_request(pr_number)
        files = []

        for file in pr.get_files():
            files.append(
                {
                    "filename": file.filename,
                    "status": file.status,  # 'added', 'modified', 'removed', 'renamed'
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch if hasattr(file, "patch") else None,
                    "raw_url": file.raw_url,
                }
            )

        return files

    async def get_file_content(self, file_path: str, ref: str = None) -> str:
        """
        Get the content of a file from the repository.

        Args:
            file_path: Path to the file
            ref: Branch, tag, or commit SHA (default: main/master branch)

        Returns:
            File content as string
        """
        try:
            content_file = self.repo.get_contents(file_path, ref=ref)
            if isinstance(content_file, list):
                # It's a directory, not a file
                raise ValueError(f"{file_path} is a directory, not a file")

            content = base64.b64decode(content_file.content).decode("utf-8")
            return content
        except GithubException as e:
            # Handle case where file doesn't exist
            if e.status == 404:
                return ""
            raise

    async def get_pr_description(self, pr_number: int) -> str:
        """
        Get the description of a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            PR description text
        """
        pr = await self.get_pull_request(pr_number)
        return pr.body or ""

    async def get_pr_commits(self, pr_number: int) -> List[Dict[str, Any]]:
        """
        Get all commits in a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            List of commits with metadata
        """
        pr = await self.get_pull_request(pr_number)
        commits = []

        for commit in pr.get_commits():
            commits.append(
                {
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat(),
                }
            )

        return commits

    async def get_pr_comments(self, pr_number: int) -> List[Dict[str, Any]]:
        """
        Get all comments in a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            List of comments with metadata
        """
        pr = await self.get_pull_request(pr_number)
        comments = []

        # Issue comments (general PR comments)
        for comment in pr.get_issue_comments():
            comments.append(
                {
                    "id": comment.id,
                    "user": comment.user.login,
                    "body": comment.body,
                    "created_at": comment.created_at.isoformat(),
                    "type": "issue_comment",
                }
            )

        # Review comments (inline code comments)
        for comment in pr.get_comments():
            comments.append(
                {
                    "id": comment.id,
                    "user": comment.user.login,
                    "body": comment.body,
                    "created_at": comment.created_at.isoformat(),
                    "path": comment.path,
                    "position": comment.position,
                    "type": "review_comment",
                }
            )

        return comments

    async def post_review_comments(
        self, pr_number: int, review_results: Dict[str, Any]
    ) -> None:
        """
        Post code review comments to a pull request.

        Args:
            pr_number: Pull request number
            review_results: Code review results with issues to comment on
        """
        pr = await self.get_pull_request(pr_number)

        # Create a new review
        review = pr.create_review(
            body="# Automated Code Review\n\nSee inline comments for details.",
            event="COMMENT",  # Can be "APPROVE", "REQUEST_CHANGES", or "COMMENT"
        )

        # Combine all issue types
        all_issues = []
        for category, issues in review_results.items():
            if isinstance(issues, list):  # Skip statistics or other non-list items
                for issue in issues:
                    if not isinstance(issue, dict):
                        continue

                    # Skip if missing required fields
                    if not all(
                        k in issue
                        for k in ["file", "line", "severity", "issue", "recommendation"]
                    ):
                        continue

                    issue["category"] = category.replace("_issues", "")
                    all_issues.append(issue)

        # Add comments to the review
        for issue in all_issues:
            # Format the comment
            comment = f"### [{issue['severity'].title()}] {issue['category'].replace('_', ' ').title()} Issue\n\n"
            comment += f"**Issue:** {issue['issue']}\n\n"
            comment += f"**Recommendation:** {issue['recommendation']}\n\n"

            if issue.get("example"):
                comment += f"**Example:**\n```\n{issue['example']}\n```\n\n"

            if issue.get("reference"):
                comment += (
                    f"**Reference:** [{issue['reference']}]({issue['reference']})"
                )

            try:
                # Add the comment to the review
                review.create_comment(
                    body=comment, path=issue["file"], position=issue["line"]
                )
            except GithubException as e:
                # Log the error and continue with other comments
                print(f"Error posting comment: {str(e)}")

        # Submit the review
        review.submit()
