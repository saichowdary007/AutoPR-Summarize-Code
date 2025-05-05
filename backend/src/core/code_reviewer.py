import re
import os
from typing import Dict, List, Any, Optional, Tuple
import yaml

async def review_code(
    github_service, 
    pr_number: int, 
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Conduct a comprehensive code review on a pull request.
    
    Args:
        github_service: GitHub service instance
        pr_number: Pull request number
        config: Optional configuration parameters
        
    Returns:
        Dictionary containing code review results
    """
    if config is None:
        config = {}
    
    # Get default configuration and merge with provided config
    default_config = _get_default_config()
    for key, value in config.items():
        default_config[key] = value
    config = default_config
    
    # Get PR files and details
    pr_files = await github_service.get_pr_files(pr_number)
    
    # Initialize results structure
    results = {
        "security_issues": [],
        "performance_issues": [],
        "code_quality_issues": [],
        "test_coverage_issues": [],
        "statistics": {
            "files_analyzed": len(pr_files),
            "lines_added": sum(f["additions"] for f in pr_files),
            "lines_removed": sum(f["deletions"] for f in pr_files),
            "issue_counts": {
                "security": 0,
                "performance": 0,
                "code_quality": 0,
                "test_coverage": 0
            },
            "severity_counts": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            }
        }
    }
    
    # Review each file
    for file_info in pr_files:
        filename = file_info["filename"]
        
        # Skip files we can't analyze meaningfully
        if _should_skip_file(filename, config):
            continue
        
        # Get file content (from the PR's head branch)
        file_content = ""
        if file_info["status"] != "removed":
            # Get the PR to get the head ref
            pr = await github_service.get_pull_request(pr_number)
            file_content = await github_service.get_file_content(filename, ref=pr.head.ref)
        
        if not file_content:
            continue
        
        # Determine language and file type
        language, file_type = _detect_language(filename)
        
        # Analyze for different types of issues
        
        # Security analysis
        security_issues = _analyze_security(filename, file_content, language, file_type, config)
        results["security_issues"].extend(security_issues)
        results["statistics"]["issue_counts"]["security"] += len(security_issues)
        
        # Performance analysis
        performance_issues = _analyze_performance(filename, file_content, language, file_type, config)
        results["performance_issues"].extend(performance_issues)
        results["statistics"]["issue_counts"]["performance"] += len(performance_issues)
        
        # Code quality analysis
        code_quality_issues = _analyze_code_quality(filename, file_content, language, file_type, config)
        results["code_quality_issues"].extend(code_quality_issues)
        results["statistics"]["issue_counts"]["code_quality"] += len(code_quality_issues)
        
        # Test coverage analysis
        test_coverage_issues = _analyze_test_coverage(filename, file_content, language, file_type, config)
        results["test_coverage_issues"].extend(test_coverage_issues)
        results["statistics"]["issue_counts"]["test_coverage"] += len(test_coverage_issues)
        
    # Update severity counts
    for category in ["security_issues", "performance_issues", "code_quality_issues", "test_coverage_issues"]:
        for issue in results[category]:
            severity = issue.get("severity", "medium").lower()
            results["statistics"]["severity_counts"][severity] += 1
    
    return results

def _get_default_config() -> Dict[str, Any]:
    """Get default configuration for code review."""
    return {
        "strictness_level": 3,  # 1-5 scale, where 5 is strictest
        "focus_areas": ["security", "performance", "code_quality"],
        "verbosity": "normal",  # "minimal", "normal", "detailed"
        "issue_thresholds": {
            "critical": "block",
            "high": "block",
            "medium": "warn",
            "low": "report"
        },
        "language_rules": {},
        "custom_rules": []
    }

def _should_skip_file(filename: str, config: Dict[str, Any]) -> bool:
    """Determine if a file should be skipped in analysis."""
    # Skip binary files, generated files, and other non-reviewable files
    skip_patterns = [
        r"\.(png|jpg|jpeg|gif|svg|ico|ttf|woff|woff2|eot|pdf|zip|tar|gz|rar)$",
        r"^dist/",
        r"^build/",
        r"^node_modules/",
        r"^vendor/",
        r"^\.git/",
        r"package-lock\.json$",
        r"yarn\.lock$",
        r"^__pycache__/",
        r"\.min\.(js|css)$"
    ]
    
    # Add custom skip patterns from config if any
    if "skip_patterns" in config:
        skip_patterns.extend(config["skip_patterns"])
    
    for pattern in skip_patterns:
        if re.search(pattern, filename):
            return True
    
    return False

def _detect_language(filename: str) -> Tuple[str, str]:
    """Detect the programming language and file type from filename."""
    extensions = {
        ".js": ("javascript", "source"),
        ".jsx": ("javascript", "react"),
        ".ts": ("typescript", "source"),
        ".tsx": ("typescript", "react"),
        ".py": ("python", "source"),
        ".go": ("go", "source"),
        ".java": ("java", "source"),
        ".kt": ("kotlin", "source"),
        ".rb": ("ruby", "source"),
        ".php": ("php", "source"),
        ".c": ("c", "source"),
        ".cpp": ("cpp", "source"),
        ".h": ("c", "header"),
        ".hpp": ("cpp", "header"),
        ".cs": ("csharp", "source"),
        ".html": ("html", "markup"),
        ".xml": ("xml", "markup"),
        ".json": ("json", "data"),
        ".yaml": ("yaml", "data"),
        ".yml": ("yaml", "data"),
        ".md": ("markdown", "documentation"),
        ".css": ("css", "style"),
        ".scss": ("scss", "style"),
        ".less": ("less", "style"),
        ".sh": ("shell", "script"),
        ".bat": ("batch", "script"),
        ".ps1": ("powershell", "script"),
        ".sql": ("sql", "database"),
        ".dockerfile": ("dockerfile", "config"),
        "Dockerfile": ("dockerfile", "config"),
        ".gitignore": ("gitignore", "config"),
        ".env": ("env", "config"),
        ".toml": ("toml", "config"),
        ".ini": ("ini", "config")
    }
    
    # Check the exact filename first
    if filename in extensions:
        return extensions[filename]
    
    # Check by extension
    _, ext = os.path.splitext(filename)
    if ext in extensions:
        return extensions[ext]
    
    # If we can't determine, return generic values
    return ("unknown", "unknown")

def _analyze_security(filename: str, content: str, language: str, file_type: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze code for security issues."""
    issues = []
    strictness = config.get("strictness_level", 3)
    
    # Only include checks appropriate for the strictness level
    
    # Always check these critical security patterns regardless of strictness
    security_patterns = {
        # SQL injection
        r"(?i)(execute|exec|run).*\b(sql|query)\b.*(\+|\|\||concat|template)": {
            "severity": "critical",
            "issue": "Potential SQL injection vulnerability",
            "recommendation": "Use parameterized queries or prepared statements",
            "example": "db.execute('SELECT * FROM users WHERE id = ?', [userId])",
            "reference": "https://owasp.org/www-community/attacks/SQL_Injection"
        },
        # XSS vulnerabilities
        r"(?i)innerHTML|outerHTML|document\.write": {
            "severity": "high",
            "issue": "Potential XSS vulnerability with direct DOM manipulation",
            "recommendation": "Use safer alternatives like textContent or createElement and sanitize user input",
            "example": "element.textContent = userProvidedString;",
            "reference": "https://owasp.org/www-community/attacks/xss/"
        },
        # Hardcoded secrets
        r"(?i)(password|secret|token|key|credential|auth)[_\s]*=\s*['\"]((?!\${)[^'\"]+)['\"]\s*;?": {
            "severity": "critical",
            "issue": "Hardcoded secret or credential in source code",
            "recommendation": "Move sensitive values to environment variables or a secure configuration store",
            "example": "const apiKey = process.env.API_KEY;",
            "reference": "https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password"
        }
    }
    
    # Additional checks for medium strictness and above
    if strictness >= 3:
        medium_security_patterns = {
            # Path traversal
            r"(?i)\.\.\/|\.\.\\|\bpath\.join\(.*\.\.|fs\.read.*\.\.|open\(.*\.\.": {
                "severity": "high",
                "issue": "Potential path traversal vulnerability",
                "recommendation": "Validate and sanitize file paths, use path normalization",
                "example": "const safePath = path.normalize(userInput).replace(/^(\.\.[\/\\])+/, '');",
                "reference": "https://owasp.org/www-community/attacks/Path_Traversal"
            },
            # Insecure random values
            r"(?i)\bMath\.random\(\)|\brand\(|\brandom\.\b(?!secure)": {
                "severity": "medium",
                "issue": "Use of non-cryptographically secure random number generator",
                "recommendation": "Use cryptographically secure random generators for security-sensitive operations",
                "example": "const crypto = require('crypto'); const secureValue = crypto.randomBytes(16);",
                "reference": "https://owasp.org/www-community/vulnerabilities/Insecure_Randomness"
            }
        }
        security_patterns.update(medium_security_patterns)
    
    # Additional checks for high strictness
    if strictness >= 4:
        high_security_patterns = {
            # Regex DoS (ReDoS)
            r"(?i)(\.\*|\.\+|\d+,\s*([^,]|\n)*).*\*": {
                "severity": "medium",
                "issue": "Regular expression pattern susceptible to ReDoS attacks",
                "recommendation": "Avoid nested quantifiers and use atomic groups or possessive quantifiers",
                "example": "Use /^(a+)+$/.test(input) -> /^(?>(a+))+$/.test(input) or impose input length limits",
                "reference": "https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS"
            },
            # CORS misconfigurations
            r"(?i)Access-Control-Allow-Origin:\s*\*": {
                "severity": "medium",
                "issue": "Overly permissive CORS policy",
                "recommendation": "Restrict CORS to specific trusted domains rather than using a wildcard",
                "example": "Access-Control-Allow-Origin: https://trusted-domain.com",
                "reference": "https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny"
            }
        }
        security_patterns.update(high_security_patterns)
    
    # Language-specific security checks
    if language == "javascript" or language == "typescript":
        js_security_patterns = {
            # JavaScript eval
            r"(?i)\beval\s*\(": {
                "severity": "high",
                "issue": "Use of eval() can lead to code injection vulnerabilities",
                "recommendation": "Avoid using eval(); use safer alternatives",
                "example": "Instead of eval(jsonString), use JSON.parse(jsonString)",
                "reference": "https://owasp.org/www-community/attacks/Code_Injection"
            },
            # Prototype pollution
            r"(?i)Object\.assign\(\{?\}?,\s*[^,]+\)": {
                "severity": "medium",
                "issue": "Potential prototype pollution vulnerability",
                "recommendation": "Use safe object cloning or Object.create(null)",
                "example": "const obj = Object.create(null); Object.assign(obj, userInput);",
                "reference": "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/prototype-pollution.html"
            }
        }
        security_patterns.update(js_security_patterns)
    elif language == "python":
        py_security_patterns = {
            # Python code execution
            r"(?i)\beval\s*\(|\bexec\s*\(|\bcompile\s*\(": {
                "severity": "high",
                "issue": "Use of eval(), exec(), or compile() can lead to code execution vulnerabilities",
                "recommendation": "Avoid executing dynamic code; use safer alternatives",
                "example": "Instead of eval(expression), use ast.literal_eval() for safe evaluation of literals",
                "reference": "https://owasp.org/www-community/attacks/Code_Injection"
            },
            # Pickle deserialization
            r"(?i)pickle\.loads?\(|marshal\.loads?\(": {
                "severity": "high", 
                "issue": "Insecure deserialization with pickle/marshal",
                "recommendation": "Use safer serialization formats like JSON",
                "example": "import json; data = json.loads(user_input)",
                "reference": "https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data"
            }
        }
        security_patterns.update(py_security_patterns)
    
    # Check for all security patterns
    for pattern, issue_info in security_patterns.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            line_number = content[:match.start()].count('\n') + 1
            issues.append({
                "file": filename,
                "line": line_number,
                "severity": issue_info["severity"],
                "issue": issue_info["issue"],
                "recommendation": issue_info["recommendation"],
                "example": issue_info.get("example"),
                "reference": issue_info.get("reference")
            })
    
    return issues

def _analyze_performance(filename: str, content: str, language: str, file_type: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze code for performance issues."""
    issues = []
    strictness = config.get("strictness_level", 3)
    
    # Common performance patterns across languages
    performance_patterns = {
        # Nested loops
        r"for\s+\w+\s+in\s+.*:\s*[^\n]*\n\s+for\s+\w+\s+in": {
            "severity": "medium",
            "issue": "Nested loops may lead to O(n²) time complexity",
            "recommendation": "Consider restructuring the algorithm to avoid nested iterations",
            "example": "Use a more efficient data structure or algorithm to reduce time complexity"
        }
    }
    
    # Language-specific performance checks
    if language == "javascript" or language == "typescript":
        js_performance_patterns = {
            # Inefficient DOM queries
            r"(?i)document\.getElements?By": {
                "severity": "low",
                "issue": "Repeated DOM queries may cause performance issues",
                "recommendation": "Cache DOM elements in variables if used multiple times",
                "example": "const elements = document.getElementsByClassName('item'); // Cache once and reuse"
            },
            # Array in loop modification
            r"for\s*\([^)]+\)\s*\{\s*[^}]*\.(push|splice|unshift)": {
                "severity": "medium",
                "issue": "Modifying arrays inside loops can be inefficient",
                "recommendation": "Consider using map, filter, or reduce for array transformations",
                "example": "const newArray = originalArray.map(item => transformItem(item));"
            }
        }
        performance_patterns.update(js_performance_patterns)
    elif language == "python":
        py_performance_patterns = {
            # List comprehension vs append in loop
            r"for\s+\w+\s+in\s+[^:]+:\s*[^\n]*\n\s+\w+\.append": {
                "severity": "low",
                "issue": "Using list.append() in a loop instead of a list comprehension",
                "recommendation": "Use list comprehension for building lists when possible",
                "example": "new_list = [transform(item) for item in original_list]"
            },
            # Inefficient string concatenation
            r"\+= \"": {
                "severity": "low",
                "issue": "Inefficient string concatenation in a loop",
                "recommendation": "Use ''.join() or string formatting for building strings",
                "example": "result = ''.join(parts) instead of repeated += operations"
            }
        }
        performance_patterns.update(py_performance_patterns)
    
    # Check for all performance patterns
    for pattern, issue_info in performance_patterns.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            line_number = content[:match.start()].count('\n') + 1
            issues.append({
                "file": filename,
                "line": line_number,
                "severity": issue_info["severity"],
                "issue": issue_info["issue"],
                "recommendation": issue_info["recommendation"],
                "example": issue_info.get("example"),
                "reference": issue_info.get("reference")
            })
    
    return issues

def _analyze_code_quality(filename: str, content: str, language: str, file_type: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze code for quality issues."""
    issues = []
    strictness = config.get("strictness_level", 3)
    
    # Common code quality patterns across languages
    quality_patterns = {
        # Long functions
        r"(def|function)\s+\w+[^{]*\{[^}]{500,}\}": {
            "severity": "medium",
            "issue": "Function is too long (over 500 characters)",
            "recommendation": "Break down large functions into smaller, focused functions"
        },
        # Magic numbers
        r"[^A-Za-z0-9_\"']\d{4,}[^A-Za-z0-9_]": {
            "severity": "low",
            "issue": "Magic number detected",
            "recommendation": "Replace magic numbers with named constants for better readability"
        },
        # TODO comments
        r"(?i)//\s*TODO|#\s*TODO": {
            "severity": "low",
            "issue": "TODO comment found",
            "recommendation": "Address TODO comments before finalizing the PR"
        }
    }
    
    # Language-specific quality checks
    if language == "javascript" or language == "typescript":
        js_quality_patterns = {
            # Console statements
            r"console\.(log|debug|info|warn|error)\(": {
                "severity": "low",
                "issue": "Console statement in production code",
                "recommendation": "Remove or wrap console statements in development-only conditionals"
            },
            # Callback hell (nested callbacks)
            r"}\)[^)]*\(\s*function\s*\([^)]*\)\s*\{": {
                "severity": "medium",
                "issue": "Nested callbacks (callback hell) detected",
                "recommendation": "Refactor to use Promises, async/await, or named functions"
            }
        }
        quality_patterns.update(js_quality_patterns)
    elif language == "python":
        py_quality_patterns = {
            # Print statements
            r"print\s*\(": {
                "severity": "low",
                "issue": "Print statement in production code",
                "recommendation": "Use proper logging instead of print statements"
            },
            # Except without specific exceptions
            r"except:": {
                "severity": "medium",
                "issue": "Bare except clause",
                "recommendation": "Specify the exceptions to catch instead of using a bare except"
            }
        }
        quality_patterns.update(py_quality_patterns)
    
    # Check for all quality patterns
    for pattern, issue_info in quality_patterns.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            line_number = content[:match.start()].count('\n') + 1
            issues.append({
                "file": filename,
                "line": line_number,
                "severity": issue_info["severity"],
                "issue": issue_info["issue"],
                "recommendation": issue_info["recommendation"],
                "example": issue_info.get("example"),
                "reference": issue_info.get("reference")
            })
    
    return issues

def _analyze_test_coverage(filename: str, content: str, language: str, file_type: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze code for test coverage issues."""
    issues = []
    
    # Only analyze source files, not test files themselves
    if "test" in filename.lower() or "spec" in filename.lower():
        return issues
    
    # Check for testable patterns without corresponding test files
    testable_patterns = {
        "javascript": {
            r"export\s+(default\s+)?((class|function|const|let|var)\s+)?(\w+)": {
                "severity": "medium",
                "issue": "Exported module lacks corresponding test file",
                "recommendation": "Create a test file for this module"
            }
        },
        "python": {
            r"def\s+(\w+)\s*\([^)]*\):\s*(?!\"\"\"|\'\'\')": {
                "severity": "medium",
                "issue": "Function lacks docstring and possibly tests",
                "recommendation": "Add docstring and ensure function is tested"
            },
            r"class\s+(\w+)[^:]*:": {
                "severity": "medium",
                "issue": "Class might need dedicated tests",
                "recommendation": "Ensure this class has test coverage"
            }
        }
    }
    
    # Get patterns for the current language
    language_patterns = testable_patterns.get(language, {})
    
    for pattern, issue_info in language_patterns.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            # Attempt to extract the identifier name
            identifier = None
            if match.groups() and len(match.groups()) >= 1:
                for group in match.groups():
                    if group and isinstance(group, str) and not any(kw in group for kw in ["class", "function", "const", "let", "var", "default"]):
                        identifier = group
                        break
            
            line_number = content[:match.start()].count('\n') + 1
            
            # Customize the message if we found an identifier
            issue = issue_info["issue"]
            recommendation = issue_info["recommendation"]
            if identifier:
                issue = f"{identifier}: {issue}"
                recommendation = f"{recommendation} for {identifier}"
            
            issues.append({
                "file": filename,
                "line": line_number,
                "severity": issue_info["severity"],
                "issue": issue,
                "recommendation": recommendation,
                "example": issue_info.get("example"),
                "reference": issue_info.get("reference")
            })
    
    return issues 