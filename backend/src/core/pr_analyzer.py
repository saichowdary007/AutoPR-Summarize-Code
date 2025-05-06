import re
from typing import Dict, List, Any, Optional
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter

# Ensure necessary NLTK data is downloaded
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


async def analyze_pull_request(
    github_service, pr_number: int, config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze a pull request and generate a comprehensive summary.

    Args:
        github_service: GitHub service instance
        pr_number: Pull request number
        config: Optional configuration parameters

    Returns:
        Dictionary containing PR summary details
    """
    if config is None:
        config = {}

    # Get PR details
    pr = await github_service.get_pull_request(pr_number)
    pr_description = await github_service.get_pr_description(pr_number)
    pr_files = await github_service.get_pr_files(pr_number)
    pr_commits = await github_service.get_pr_commits(pr_number)

    # Extract PR type/purpose
    pr_type = _determine_pr_type(pr.title, pr_description, pr_commits)

    # Generate basic summary
    title = f"PR Summary: {pr.title}"
    overview = _generate_overview(pr, pr_description, pr_type)

    # Analyze changes
    changes_summary = _extract_key_changes(pr_description, pr_commits, pr_files)
    affected_components = _identify_affected_components(pr_files)

    # Analyze testing
    testing = _extract_testing_info(pr_description, pr_files)

    # Analyze dependencies
    dependencies = _extract_dependency_changes(pr_files)

    # Extract migration notes
    migration_notes = _extract_migration_notes(pr_description)

    # Identify potential risks
    potential_risks = _identify_potential_risks(pr_files, pr_description)

    # Construct summary response
    summary = {
        "title": title,
        "overview": overview,
        "changes_summary": changes_summary,
        "affected_components": affected_components,
    }

    # Add optional fields if they have content
    if testing:
        summary["testing"] = testing

    if dependencies:
        summary["dependencies"] = dependencies

    if migration_notes:
        summary["migration_notes"] = migration_notes

    if potential_risks:
        summary["potential_risks"] = potential_risks

    return summary


def _determine_pr_type(
    title: str, description: str, commits: List[Dict[str, Any]]
) -> str:
    """Determine the type/purpose of the PR (feature, bugfix, refactoring, etc.)."""
    # Check for explicit type in title
    title_lower = title.lower()
    if any(kw in title_lower for kw in ["fix", "bug", "issue", "problem"]):
        return "bug fix"
    elif any(kw in title_lower for kw in ["feat", "feature", "add", "implement"]):
        return "feature addition"
    elif any(
        kw in title_lower for kw in ["refactor", "clean", "simplify", "restructure"]
    ):
        return "refactoring"
    elif any(kw in title_lower for kw in ["docs", "documentation"]):
        return "documentation"
    elif any(kw in title_lower for kw in ["test", "testing"]):
        return "testing improvements"
    elif any(kw in title_lower for kw in ["perf", "performance"]):
        return "performance improvement"

    # Check commit messages
    commit_types = []
    for commit in commits:
        message = commit["message"].lower()
        if any(kw in message for kw in ["fix", "bug", "issue", "problem"]):
            commit_types.append("bug fix")
        elif any(kw in message for kw in ["feat", "feature", "add", "implement"]):
            commit_types.append("feature addition")
        elif any(kw in message for kw in ["refactor", "clean"]):
            commit_types.append("refactoring")

    # Return most common commit type if any
    if commit_types:
        counter = Counter(commit_types)
        return counter.most_common(1)[0][0]

    # Default
    return "code changes"


def _generate_overview(pr, description: str, pr_type: str) -> str:
    """Generate a concise overview of the PR."""
    if description:
        # Try to extract the first paragraph that's not a heading
        paragraphs = [p.strip() for p in description.split("\n\n")]
        for paragraph in paragraphs:
            if paragraph and not paragraph.startswith("#") and len(paragraph) > 10:
                # Limit to two sentences for brevity
                sentences = sent_tokenize(paragraph)
                if sentences:
                    return " ".join(sentences[:2])

    # Fallback to a generated overview
    return f"This PR implements {pr_type} for {pr.title}."


def _extract_key_changes(
    description: str, commits: List[Dict[str, Any]], files: List[Dict[str, Any]]
) -> List[str]:
    """Extract key changes from PR description, commits, and file changes."""
    changes = []

    # Try to extract from PR description first
    if description:
        list_pattern = r"[-*] (.+)"
        matches = re.findall(list_pattern, description)
        if matches:
            # Limit to the top 5 most relevant changes
            return [match for match in matches[:5]]

    # Extract from commit messages
    commit_changes = set()
    for commit in commits:
        message = commit["message"].split("\n")[0]  # Just the first line
        if 10 < len(message) < 100 and not message.startswith("Merge"):
            commit_changes.add(message)

    if commit_changes:
        changes.extend(list(commit_changes)[:5])

    # If we still don't have changes, infer from files
    if not changes:
        file_patterns = {
            r"^tests?/": "Added or updated tests",
            r"^docs?/": "Updated documentation",
            r"^src/": "Modified source code",
            r"package.json|requirements.txt|go.mod": "Updated dependencies",
            r"\.github/|\.circleci/|\.travis|Jenkinsfile": "CI configuration changes",
            r"Dockerfile|docker-compose": "Docker configuration changes",
        }

        found_patterns = set()
        for file in files:
            filename = file["filename"]
            for pattern, description in file_patterns.items():
                if re.search(pattern, filename) and description not in found_patterns:
                    found_patterns.add(description)
                    changes.append(description)

    # Ensure we have at least one change
    if not changes:
        total_additions = sum(file["additions"] for file in files)
        total_deletions = sum(file["deletions"] for file in files)

        if total_additions > total_deletions:
            changes.append(
                f"Added {total_additions} lines of code across {len(files)} files"
            )
        elif total_deletions > total_additions:
            changes.append(
                f"Removed {total_deletions} lines of code across {len(files)} files"
            )
        else:
            changes.append(
                f"Modified {len(files)} files with balanced additions and deletions"
            )

    return changes


def _identify_affected_components(files: List[Dict[str, Any]]) -> List[str]:
    """Identify affected components or modules from file changes."""
    components = set()

    for file in files:
        filepath = file["filename"]
        parts = filepath.split("/")

        # Handle different project structures
        if len(parts) >= 2:
            # For typical structures like src/components/Button.js
            if parts[0] in ["src", "app", "lib", "pkg", "internal"]:
                if len(parts) >= 3:
                    component = f"{parts[0]}/{parts[1]}/{parts[2]}"
                    components.add(component)
                else:
                    component = f"{parts[0]}/{parts[1]}"
                    components.add(component)
            # For typical test files
            elif parts[0] in ["test", "tests", "spec", "specs"]:
                if len(parts) >= 3:
                    component = f"{parts[0]}/{parts[1]}"
                    components.add(component)
            # For documentation
            elif parts[0] in ["docs", "documentation"]:
                if len(parts) >= 2:
                    component = f"{parts[0]}/{parts[1]}"
                    components.add(component)
            # For config files
            elif parts[0] in [".github", "config", "configs"]:
                component = parts[0]
                components.add(component)
            # Default to first two directory levels
            elif len(parts) >= 2:
                component = f"{parts[0]}/{parts[1]}"
                components.add(component)
            else:
                components.add(parts[0])

    return sorted(list(components))


def _extract_testing_info(
    description: str, files: List[Dict[str, Any]]
) -> Optional[str]:
    """Extract testing information from PR description and file changes."""
    test_files = [
        f
        for f in files
        if "test" in f["filename"].lower() or "spec" in f["filename"].lower()
    ]

    # Extract testing section from description
    test_section = None
    if description:
        # Look for a test section in the description
        test_patterns = [
            r"(?i)#+\s*tests?.*?\n(.*?)(?:\n#+\s*|$)",
            r"(?i)tests?:?\s*(.*?)(?:\n\n|$)",
        ]

        for pattern in test_patterns:
            matches = re.search(pattern, description, re.DOTALL)
            if matches:
                test_section = matches.group(1).strip()
                break

    if test_section:
        return test_section

    # Generate testing info based on file changes
    if test_files:
        test_additions = sum(f["additions"] for f in test_files)
        coverage_impact = "improved" if test_additions > 0 else "maintained"

        return f"Added or modified {len(test_files)} test files with {test_additions} lines of test code. Test coverage has been {coverage_impact}."

    return None


def _extract_dependency_changes(files: List[Dict[str, Any]]) -> Optional[List[str]]:
    """Extract dependency changes from relevant files."""
    dependency_files = [
        "package.json",
        "yarn.lock",
        "package-lock.json",
        "requirements.txt",
        "Pipfile",
        "Pipfile.lock",
        "go.mod",
        "go.sum",
        "Gemfile",
        "Gemfile.lock",
        "build.gradle",
        "pom.xml",
        "build.sbt",
    ]

    dep_changes = []
    for file in files:
        if any(dep_file in file["filename"] for dep_file in dependency_files):
            if file["patch"]:
                # Extract added dependencies from the patch
                added_lines = [
                    line[1:]
                    for line in file["patch"].split("\n")
                    if line.startswith("+") and not line.startswith("+++")
                ]

                # Look for dependency patterns in different formats
                for line in added_lines:
                    # npm/yarn pattern
                    npm_match = re.search(r'"([^"]+)":\s*"([^"]+)"', line)
                    if npm_match:
                        dep_changes.append(
                            f"Added: {npm_match.group(1)}@{npm_match.group(2)}"
                        )
                        continue

                    # requirements.txt pattern
                    req_match = re.search(r"([a-zA-Z0-9_-]+)[=~<>]+([0-9.]+)", line)
                    if req_match:
                        dep_changes.append(
                            f"Added: {req_match.group(1)}=={req_match.group(2)}"
                        )
                        continue

                    # go.mod pattern
                    go_match = re.search(r"([a-zA-Z0-9_\-./]+)\s+v([0-9.]+)", line)
                    if go_match:
                        dep_changes.append(
                            f"Added: {go_match.group(1)}@v{go_match.group(2)}"
                        )
                        continue

            # If we couldn't extract specific dependencies, just note the file was changed
            if not dep_changes:
                dep_changes.append(f"Modified dependencies in {file['filename']}")

    return dep_changes if dep_changes else None


def _extract_migration_notes(description: str) -> Optional[str]:
    """Extract migration or breaking change notes from PR description."""
    if not description:
        return None

    migration_patterns = [
        r"(?i)#+\s*migration.*?\n(.*?)(?:\n#+\s*|$)",
        r"(?i)#+\s*breaking changes.*?\n(.*?)(?:\n#+\s*|$)",
        r"(?i)migration( notes)?:?\s*(.*?)(?:\n\n|$)",
        r"(?i)breaking changes:?\s*(.*?)(?:\n\n|$)",
    ]

    for pattern in migration_patterns:
        matches = re.search(pattern, description, re.DOTALL)
        if matches:
            content = matches.group(1).strip()
            if content:
                return content

    return None


def _identify_potential_risks(
    files: List[Dict[str, Any]], description: str
) -> List[str]:
    """Identify potential risk areas that might need special attention during review."""
    risks = []

    # Check for risky file patterns
    risk_patterns = {
        r"(?i)auth|password|secret|token|credential": "Security-sensitive code related to authentication or credentials",
        r"(?i)payment|billing|price|money|checkout": "Payment or billing related functionality",
        r"(?i)user.+data|data.+user": "Code handling user data",
        r"(?i)database|migration|schema": "Database schema or migration changes",
        r"migrations?/": "Database migrations",
        r"config/[^/]+\.(prod|production)\.": "Production configuration changes",
        r"(?i)performance|benchmark": "Performance-critical code",
        r"(?i)concurrent|parallel|locks?|mutex": "Concurrency or parallelism related code",
        r"(?i)perm[is]+ion|access.?control": "Permission or access control logic",
    }

    for file in files:
        filepath = file["filename"]
        for pattern, risk in risk_patterns.items():
            if re.search(pattern, filepath):
                risks.append(risk)
                break

    # Check for risk-related content in PR description
    if description:
        risk_section_patterns = [
            r"(?i)#+\s*risks?.*?\n(.*?)(?:\n#+\s*|$)",
            r"(?i)risks?:?\s*(.*?)(?:\n\n|$)",
        ]

        for pattern in risk_section_patterns:
            matches = re.search(pattern, description, re.DOTALL)
            if matches:
                risk_content = matches.group(1).strip()
                if risk_content:
                    # Extract bullet points
                    bullet_points = re.findall(r"[-*]\s*(.*?)(?:\n|$)", risk_content)
                    if bullet_points:
                        risks.extend(bullet_points)
                    else:
                        # Just use the whole section if no bullet points
                        risks.append(risk_content.split("\n")[0])

    # Remove duplicates while preserving order
    unique_risks = []
    for risk in risks:
        if risk not in unique_risks:
            unique_risks.append(risk)

    return unique_risks
