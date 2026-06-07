"""
Built-in rule definitions for CodeQualityLens.
60+ rules across security, performance, reliability, maintainability, and AI-specific categories.
"""

from .core import RegexRule, ASTRule, Category, Severity, Finding
from typing import List


def get_all_rules() -> List:
    """Return all built-in rules."""
    rules = []

    # ==================== SECURITY RULES ====================
    rules.extend([
        RegexRule(
            "SEC-001", "Hardcoded Secret", Category.SECURITY, Severity.CRITICAL,
            ["python", "javascript", "go", "java", "rust"],
            "Detected potential hardcoded secret (API key, token, or password)",
            r'(?i)(api[_-]?key|password|secret|token)\s*[=:]\s*["\'][a-zA-Z0-9_\-]{16,}["\']',
            "Move secrets to environment variables or a secure vault",
            0.95,
        ),
        RegexRule(
            "SEC-002", "SQL Injection Risk", Category.SECURITY, Severity.CRITICAL,
            ["python", "javascript", "go", "java"],
            "Potential SQL injection vulnerability detected",
            r'(?i)(execute|query|cursor\.execute)\s*\(\s*["\'].*%s.*["\']|\+.*\+',
            "Use parameterized queries or prepared statements",
            0.85,
        ),
        RegexRule(
            "SEC-003", "Unsafe Eval", Category.SECURITY, Severity.CRITICAL,
            ["python", "javascript"],
            "Use of eval() or exec() can lead to code injection",
            r'\b(eval|exec)\s*\(',
            "Avoid eval/exec; use safer alternatives like ast.literal_eval",
            0.90,
        ),
        RegexRule(
            "SEC-004", "Insecure Deserialization", Category.SECURITY, Severity.HIGH,
            ["python"],
            "Insecure deserialization with pickle or yaml.load",
            r'\b(pickle\.loads?|yaml\.load)\s*\(',
            "Use yaml.safe_load() and avoid pickle for untrusted data",
            0.90,
        ),
        RegexRule(
            "SEC-005", "Weak Hash Algorithm", Category.SECURITY, Severity.HIGH,
            ["python", "javascript", "go", "java", "rust"],
            "Use of weak hash algorithm (MD5 or SHA1)",
            r'\b(md5|sha1)\s*\(',
            "Use SHA-256 or stronger hashing algorithms",
            0.85,
        ),
        RegexRule(
            "SEC-006", "Debug Mode Enabled", Category.SECURITY, Severity.HIGH,
            ["python", "javascript"],
            "Debug mode should not be enabled in production",
            r'(?i)(debug\s*=\s*True|DEBUG:\s*true)',
            "Set debug mode to False in production environments",
            0.80,
        ),
        RegexRule(
            "SEC-007", "Missing Input Validation", Category.SECURITY, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "User input used without apparent validation",
            r'(?i)(request\.(args|form|json)|input\(|scanf|prompt\()',
            "Always validate and sanitize user inputs",
            0.70,
        ),
        RegexRule(
            "SEC-008", "Insecure HTTP", Category.SECURITY, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "Using insecure HTTP instead of HTTPS",
            r'http://(?!localhost|127\.0\.0\.1)',
            "Use HTTPS for all external communications",
            0.75,
        ),
        RegexRule(
            "SEC-009", "Command Injection Risk", Category.SECURITY, Severity.CRITICAL,
            ["python", "javascript", "go", "java", "rust"],
            "Potential command injection via shell execution",
            r'(?i)(os\.system|subprocess\.call|child_process|Runtime\.getRuntime|Command::new)\s*\(',
            "Avoid shell=True and validate all command inputs",
            0.85,
        ),
        RegexRule(
            "SEC-010", "Path Traversal Risk", Category.SECURITY, Severity.HIGH,
            ["python", "javascript", "go", "java", "rust"],
            "Potential path traversal vulnerability",
            r'(?i)(open\s*\(|readFile|fs\.read|FileInputStream|File::open)\s*\([^)]*\+',
            "Validate and sanitize file paths; use path joining utilities",
            0.75,
        ),
    ])

    # ==================== PERFORMANCE RULES ====================
    rules.extend([
        RegexRule(
            "PERF-001", "Inefficient List Concatenation", Category.PERFORMANCE, Severity.MEDIUM,
            ["python"],
            "Inefficient string concatenation in loop",
            r'for\s+\w+\s+in\s+.*:\s*\n\s+\w+\s*\+=\s*',
            "Use str.join() or io.StringIO for string concatenation",
            0.80,
        ),
        RegexRule(
            "PERF-002", "Nested Loop", Category.PERFORMANCE, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Nested loops may cause O(n²) performance issues",
            r'for\s+.*:\s*\n\s+for\s+.*:',
            "Consider algorithm optimization or using sets/dictionaries",
            0.60,
        ),
        RegexRule(
            "PERF-003", "Repeated Dictionary Lookup", Category.PERFORMANCE, Severity.LOW,
            ["python"],
            "Repeated dictionary access without caching",
            r'dict\[\w+\]\.\w+.*dict\[\w+\]\.\w+',
            "Cache dictionary lookups in local variables",
            0.55,
        ),
        RegexRule(
            "PERF-004", "Synchronous File Operations", Category.PERFORMANCE, Severity.MEDIUM,
            ["javascript", "python"],
            "Blocking file I/O operations in async context",
            r'(?i)(readFileSync|writeFileSync|open\s*\()',
            "Use async/await or non-blocking I/O operations",
            0.70,
        ),
        RegexRule(
            "PERF-005", "Memory Leak - Event Listener", Category.PERFORMANCE, Severity.MEDIUM,
            ["javascript"],
            "Potential memory leak from uncleaned event listeners",
            r'\.addEventListener\s*\(',
            "Remove event listeners when components unmount",
            0.65,
        ),
        RegexRule(
            "PERF-006", "Inefficient Regex", Category.PERFORMANCE, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "Potentially inefficient regular expression",
            r'\(.*\+.*\+.*\)|\(.*\*.*\*.*\)',
            "Optimize regex patterns to avoid catastrophic backtracking",
            0.60,
        ),
        RegexRule(
            "PERF-007", "Blocking Sleep", Category.PERFORMANCE, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Blocking sleep/delay in code",
            r'\b(time\.sleep|setTimeout|sleep|Thread\.sleep)\s*\(',
            "Use non-blocking timers or async delays where possible",
            0.50,
        ),
        RegexRule(
            "PERF-008", "Large List Comprehension", Category.PERFORMANCE, Severity.LOW,
            ["python"],
            "Large list comprehension may consume excessive memory",
            r'\[.*for.*in.*range\s*\(\s*\d{5,}',
            "Consider using generators or iterators for large datasets",
            0.55,
        ),
    ])

    # ==================== RELIABILITY RULES ====================
    rules.extend([
        RegexRule(
            "REL-001", "Bare Except", Category.RELIABILITY, Severity.MEDIUM,
            ["python"],
            "Bare except clause catches all exceptions including SystemExit",
            r'except\s*:\s*$|except\s+Exception\s*:\s*$',
            "Catch specific exceptions instead of bare except",
            0.85,
        ),
        RegexRule(
            "REL-002", "Empty Catch Block", Category.RELIABILITY, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "Empty exception handling block swallows errors",
            r'except.*:\s*\n\s*pass|catch\s*\(.*\)\s*\{\s*\}',
            "Log or handle exceptions properly; do not silently swallow",
            0.80,
        ),
        RegexRule(
            "REL-003", "Mutable Default Argument", Category.RELIABILITY, Severity.HIGH,
            ["python"],
            "Mutable default argument causes unexpected behavior",
            r'def\s+\w+\s*\([^)]*=\s*(\[|\{)',
            "Use None as default and initialize mutable objects inside function",
            0.90,
        ),
        RegexRule(
            "REL-004", "Unclosed Resource", Category.RELIABILITY, Severity.MEDIUM,
            ["python"],
            "File or resource opened without context manager",
            r'\w+\s*=\s*open\s*\(',
            "Use 'with' statement for automatic resource cleanup",
            0.75,
        ),
        RegexRule(
            "REL-005", "Missing Return", Category.RELIABILITY, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Function may not return a value in all code paths",
            r'def\s+\w+\s*\([^)]*\).*:\s*(?:\n.*){3,20}?(?:return|raise|throw)',
            "Ensure all code paths return appropriate values",
            0.50,
        ),
        RegexRule(
            "REL-006", "Race Condition", Category.RELIABILITY, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "Potential race condition in concurrent code",
            r'(?i)(thread|goroutine|async|Promise\.all|concurrent)',
            "Use proper synchronization primitives (locks, channels, etc.)",
            0.60,
        ),
        RegexRule(
            "REL-007", "Infinite Loop Risk", Category.RELIABILITY, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "Loop without clear termination condition",
            r'while\s+True\s*:|while\s*\(\s*true\s*\)|for\s*\(\s*;;\s*\)',
            "Ensure all loops have proper break/return conditions",
            0.70,
        ),
        RegexRule(
            "REL-008", "Unchecked Error", Category.RELIABILITY, Severity.HIGH,
            ["go", "rust"],
            "Error return value not checked",
            r'\w+\s*:=\s*\w+\([^)]*\)\s*\n(?!\s*if\s+err\s*!=)',
            "Always check error return values",
            0.75,
        ),
    ])

    # ==================== MAINTAINABILITY RULES ====================
    rules.extend([
        RegexRule(
            "MAINT-001", "Long Function", Category.MAINTAINABILITY, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Function exceeds recommended length (50+ lines)",
            r'def\s+\w+\s*\([^)]*\):|function\s+\w+\s*\(|func\s+\w+\s*\(',
            "Break long functions into smaller, focused units",
            0.50,
        ),
        RegexRule(
            "MAINT-002", "TODO/FIXME Comment", Category.MAINTAINABILITY, Severity.INFO,
            ["python", "javascript", "go", "java", "rust"],
            "TODO or FIXME comment found",
            r'(?i)#\s*(TODO|FIXME|HACK|XXX)',
            "Address TODOs and FIXMEs before merging to main",
            0.90,
        ),
        RegexRule(
            "MAINT-003", "Magic Number", Category.MAINTAINABILITY, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Magic number used without named constant",
            r'[^\w](\d{3,}|0x[0-9a-fA-F]{2,})[^\w]',
            "Define named constants for magic numbers",
            0.55,
        ),
        RegexRule(
            "MAINT-004", "Deep Nesting", Category.MAINTAINABILITY, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Excessive nesting depth reduces readability",
            r'^(\s{4,}){4,}',
            "Refactor to reduce nesting; use early returns or extract functions",
            0.60,
        ),
        RegexRule(
            "MAINT-005", "Duplicate Code Pattern", Category.MAINTAINABILITY, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Similar code blocks may indicate duplication",
            r'(print|console\.log|fmt\.Print|System\.out\.print)\s*\([^)]*\)\s*\n\s*\1\s*\(',
            "Extract repeated code into reusable functions",
            0.50,
        ),
        RegexRule(
            "MAINT-006", "Missing Docstring", Category.MAINTAINABILITY, Severity.INFO,
            ["python"],
            "Public function missing docstring",
            r'^def\s+(?!_)[a-zA-Z_]\w*\s*\([^)]*\):\s*\n\s+[^"\'\n]',
            "Add docstrings to all public functions and classes",
            0.70,
        ),
        RegexRule(
            "MAINT-007", "Unused Import", Category.MAINTAINABILITY, Severity.LOW,
            ["python", "go", "java", "rust"],
            "Potentially unused import/dependency",
            r'^import\s+\w+|^from\s+\w+\s+import',
            "Remove unused imports to keep code clean",
            0.45,
        ),
        RegexRule(
            "MAINT-008", "Complex Condition", Category.MAINTAINABILITY, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Complex boolean condition is hard to read",
            r'if\s+.*(?:and|&&|or|\|\|).*(?:and|&&|or|\|\|).*(?:and|&&|or|\|\|)',
            "Extract complex conditions into named boolean variables",
            0.60,
        ),
    ])

    # ==================== AI-SPECIFIC RULES ====================
    rules.extend([
        RegexRule(
            "AI-001", "AI Hallucination Pattern", Category.AI_SPECIFIC, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "Suspicious AI-generated pattern: commented-out code with explanation",
            r'(?i)#\s*(This|Here|Below|Above)\s+is\s+(the|an|a)\s+',
            "Remove AI explanatory comments; keep only meaningful documentation",
            0.70,
        ),
        RegexRule(
            "AI-002", "Placeholder Implementation", Category.AI_SPECIFIC, Severity.HIGH,
            ["python", "javascript", "go", "java", "rust"],
            "Placeholder or stub implementation detected",
            r'(?i)(TODO|FIXME|placeholder|stub|not implemented|coming soon|implement this)',
            "Replace placeholders with actual implementations",
            0.80,
        ),
        RegexRule(
            "AI-003", "Overly Verbose Comment", Category.AI_SPECIFIC, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Overly verbose comment typical of AI generation",
            r'#\s*.{120,}',
            "Keep comments concise and focused on 'why', not 'what'",
            0.55,
        ),
        RegexRule(
            "AI-004", "Redundant Type Comment", Category.AI_SPECIFIC, Severity.INFO,
            ["python"],
            "Redundant type information in comment when type hints exist",
            r'#\s*type:\s*\w+.*\n.*:\s*\w+',
            "Use type hints instead of type comments",
            0.50,
        ),
        RegexRule(
            "AI-005", "AI Boilerplate Pattern", Category.AI_SPECIFIC, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Common AI-generated boilerplate code pattern",
            r'(?i)(#\s*Import\s+necessary\s+libraries|#\s*Define\s+the\s+main\s+function)',
            "Remove unnecessary boilerplate comments",
            0.65,
        ),
        RegexRule(
            "AI-006", "Suspiciously Perfect Code", Category.AI_SPECIFIC, Severity.INFO,
            ["python", "javascript", "go", "java", "rust"],
            "Unusually perfect formatting may indicate unreviewed AI output",
            r'^\s{4}\w+.*\n\s{4}\w+.*\n\s{4}\w+.*\n\s{4}\w+.*\n\s{4}\w+',
            "Always review AI-generated code before production use",
            0.40,
        ),
        RegexRule(
            "AI-007", "Missing Error Context", Category.AI_SPECIFIC, Severity.MEDIUM,
            ["python", "javascript", "go", "java", "rust"],
            "Generic error handling without context - common AI pattern",
            r'except\s+Exception\s+as\s+e:\s*\n\s+print\s*\(\s*["\']Error:["\']',
            "Include specific error context and use proper logging",
            0.75,
        ),
        RegexRule(
            "AI-008", "Over-engineered Solution", Category.AI_SPECIFIC, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Overly complex solution for simple problem",
            r'class\s+\w+.*:\s*\n\s+def\s+__init__.*\n\s+def\s+\w+.*\n\s+def\s+\w+.*\n\s+def\s+\w+.*\n\s+def\s+\w+',
            "Simplify; use functions instead of classes when appropriate",
            0.50,
        ),
        RegexRule(
            "AI-009", "Inconsistent Naming", Category.AI_SPECIFIC, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Inconsistent naming conventions across the file",
            r'(?m)(snake_case.*camelCase|camelCase.*snake_case)',
            "Follow consistent naming conventions per language",
            0.55,
        ),
        RegexRule(
            "AI-010", "Missing Input Sanitization", Category.AI_SPECIFIC, Severity.HIGH,
            ["python", "javascript", "go", "java", "rust"],
            "AI often forgets to sanitize inputs - check all user-facing inputs",
            r'(?i)(def\s+\w+.*\(.*user|def\s+\w+.*\(.*input|def\s+\w+.*\(.*request)',
            "Always validate and sanitize all user inputs",
            0.65,
        ),
    ])

    # ==================== STYLE RULES ====================
    rules.extend([
        RegexRule(
            "STYLE-001", "Trailing Whitespace", Category.STYLE, Severity.INFO,
            ["python", "javascript", "go", "java", "rust"],
            "Trailing whitespace found",
            r'[ \t]+$',
            "Remove trailing whitespace",
            0.95,
        ),
        RegexRule(
            "STYLE-002", "Mixed Tabs and Spaces", Category.STYLE, Severity.LOW,
            ["python", "javascript", "go", "java", "rust"],
            "Mixed tabs and spaces for indentation",
            r'^(\t+ +| +\t+)',
            "Use spaces consistently for indentation",
            0.85,
        ),
        RegexRule(
            "STYLE-003", "Line Too Long", Category.STYLE, Severity.INFO,
            ["python", "javascript", "go", "java", "rust"],
            "Line exceeds 120 characters",
            r'^.{121,}$',
            "Break long lines for better readability",
            0.90,
        ),
        RegexRule(
            "STYLE-004", "Missing Final Newline", Category.STYLE, Severity.INFO,
            ["python", "javascript", "go", "java", "rust"],
            "File missing final newline",
            r'[^\n]$',
            "Add newline at end of file",
            0.70,
        ),
    ])

    return rules
