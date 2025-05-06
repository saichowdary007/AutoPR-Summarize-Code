"""
CLI-based API simulator that emulates the backend without requiring a server.
This allows testing the backend functionality even if network services are restricted.
"""

import os
import json
import logging
import argparse
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api_cli")

# Sample PR data
SAMPLE_PR_DATA = {
    "repo": "example/repo",
    "pr_number": 123,
    "title": "Add new feature X",
    "description": "This PR adds feature X to improve user experience",
    "author": "johndoe",
    "files_changed": 15,
    "additions": 250,
    "deletions": 50,
}


def get_pr_summary(pr_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a sample PR summary based on the provided PR data."""
    logger.info(f"Generating PR summary for PR #{pr_data['pr_number']}")

    return {
        "title": pr_data["title"],
        "overview": f"This PR adds a new feature to the codebase, with {pr_data['files_changed']} files changed.",
        "key_changes": [
            "Added new component X",
            "Modified existing functionality",
            "Updated documentation",
        ],
        "affected_components": ["Frontend UI", "Backend API", "Documentation"],
        "test_coverage": "Good",
        "potential_risks": "Low",
        "review_focus_areas": ["Performance impact", "Security considerations"],
    }


def get_code_review(pr_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a sample code review based on the provided PR data."""
    logger.info(f"Generating code review for PR #{pr_data['pr_number']}")

    return {
        "overall_quality": "Good",
        "issues": [
            {
                "type": "Security",
                "severity": "Medium",
                "description": "Possible SQL injection in query parameters",
                "file": "src/database/queries.py",
                "line": 42,
                "suggestion": "Use parameterized queries instead of string concatenation",
            },
            {
                "type": "Performance",
                "severity": "Low",
                "description": "Inefficient data processing in loop",
                "file": "src/utils/data_processor.py",
                "line": 105,
                "suggestion": "Consider using list comprehension or map function",
            },
        ],
        "improvements": [
            "Add more unit tests for edge cases",
            "Consider refactoring the data processing module for better reusability",
        ],
        "positive_aspects": [
            "Good documentation",
            "Clean code structure",
            "Proper error handling",
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="CLI-based API simulator for PR analysis"
    )
    parser.add_argument(
        "--action",
        type=str,
        required=True,
        choices=["pr-summary", "code-review"],
        help="Action to perform (pr-summary or code-review)",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=SAMPLE_PR_DATA["repo"],
        help="Repository name (e.g., username/repo)",
    )
    parser.add_argument(
        "--pr",
        type=int,
        default=SAMPLE_PR_DATA["pr_number"],
        help="PR number to analyze",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="console",
        choices=["console", "file"],
        help="Output method (console or file)",
    )
    parser.add_argument(
        "--file",
        type=str,
        default="output.json",
        help="Output file name when using file output",
    )

    args = parser.parse_args()

    # Prepare PR data
    pr_data = {**SAMPLE_PR_DATA, "repo": args.repo, "pr_number": args.pr}

    # Process based on action
    if args.action == "pr-summary":
        result = get_pr_summary(pr_data)
    else:  # code-review
        result = get_code_review(pr_data)

    # Output the result
    if args.output == "console":
        print(json.dumps(result, indent=2))
    else:  # file
        with open(args.file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Results written to {args.file}")


if __name__ == "__main__":
    main()
