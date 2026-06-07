"""
File scanner and rule execution engine for CodeQualityLens.
"""

import os
import time
from typing import List, Optional
from .core import ScanResult, FileResult, Finding, Rule, Severity, Category
from .rules import get_all_rules


LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "javascript",
    ".tsx": "javascript",
    ".go": "go",
    ".java": "java",
    ".rs": "rust",
}

DEFAULT_EXCLUDES = {
    "node_modules", "venv", ".venv", "__pycache__", ".git",
    ".github", ".vscode", "dist", "build", "target", "vendor",
    ".idea", ".tox", ".pytest_cache", ".mypy_cache", "site-packages",
}


def detect_language(file_path: str) -> Optional[str]:
    """Detect programming language from file extension."""
    _, ext = os.path.splitext(file_path.lower())
    return LANGUAGE_MAP.get(ext)


def should_scan(file_path: str, root: str, excludes: set) -> bool:
    """Check if a file should be scanned."""
    rel_path = os.path.relpath(file_path, root)
    parts = rel_path.split(os.sep)

    for part in parts:
        if part in excludes:
            return False

    lang = detect_language(file_path)
    return lang is not None


def scan_file(file_path: str, rules: List[Rule], root: str) -> FileResult:
    """Scan a single file against all applicable rules."""
    start_time = time.time()
    lang = detect_language(file_path)

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except (IOError, OSError) as e:
        return FileResult(file_path=file_path, language=lang or "unknown",
                          lines_of_code=0, scan_time_ms=0)

    lines = content.split("\n")
    loc = len([l for l in lines if l.strip()])

    findings = []
    for rule in rules:
        if rule.supports_language(lang):
            try:
                rule_findings = rule.check(file_path, content, lines)
                findings.extend(rule_findings)
            except Exception:
                continue

    elapsed = (time.time() - start_time) * 1000

    return FileResult(
        file_path=file_path,
        language=lang or "unknown",
        findings=findings,
        lines_of_code=loc,
        scan_time_ms=elapsed,
    )


def scan_directory(
    target_path: str,
    rules: Optional[List[Rule]] = None,
    excludes: Optional[set] = None,
    max_file_size: int = 1024 * 1024,  # 1MB
) -> ScanResult:
    """Scan a directory recursively."""
    start_time = time.time()
    rules = rules or get_all_rules()
    excludes = excludes or DEFAULT_EXCLUDES

    result = ScanResult(target_path=target_path, rules_enabled=len(rules))

    if os.path.isfile(target_path):
        if should_scan(target_path, os.path.dirname(target_path) or ".", excludes):
            file_result = scan_file(target_path, rules, os.path.dirname(target_path) or ".")
            result.file_results.append(file_result)
    else:
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in excludes]

            for filename in files:
                file_path = os.path.join(root, filename)

                if not should_scan(file_path, target_path, excludes):
                    continue

                try:
                    if os.path.getsize(file_path) > max_file_size:
                        continue
                except OSError:
                    continue

                file_result = scan_file(file_path, rules, target_path)
                result.file_results.append(file_result)

    # Aggregate results
    result.files_scanned = len(result.file_results)
    result.total_findings = sum(len(fr.findings) for fr in result.file_results)

    severity_counts = {}
    category_counts = {}
    for fr in result.file_results:
        for finding in fr.findings:
            sev = str(finding.severity)
            cat = str(finding.category)
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            category_counts[cat] = category_counts.get(cat, 0) + 1

    result.findings_by_severity = severity_counts
    result.findings_by_category = category_counts
    result.scan_duration_ms = (time.time() - start_time) * 1000
    result.calculate_score()

    return result
