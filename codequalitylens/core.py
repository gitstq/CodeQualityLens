"""
Core engine for CodeQualityLens - rule execution and result aggregation.
"""

import os
import re
import json
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

    def __str__(self):
        return self.value

    def score_weight(self) -> int:
        weights = {
            Severity.CRITICAL: 10,
            Severity.HIGH: 7,
            Severity.MEDIUM: 4,
            Severity.LOW: 1,
            Severity.INFO: 0,
        }
        return weights[self]


class Category(Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    RELIABILITY = "reliability"
    MAINTAINABILITY = "maintainability"
    STYLE = "style"
    AI_SPECIFIC = "ai_specific"

    def __str__(self):
        return self.value


@dataclass
class Finding:
    """Represents a single code quality finding."""
    rule_id: str
    rule_name: str
    category: Category
    severity: Severity
    message: str
    file_path: str
    line_number: int
    column_start: int = 0
    column_end: int = 0
    snippet: str = ""
    suggestion: str = ""
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": str(self.category),
            "severity": str(self.severity),
            "message": self.message,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "column_start": self.column_start,
            "column_end": self.column_end,
            "snippet": self.snippet,
            "suggestion": self.suggestion,
            "confidence": self.confidence,
        }


@dataclass
class FileResult:
    """Results for a single file."""
    file_path: str
    language: str
    findings: List[Finding] = field(default_factory=list)
    lines_of_code: int = 0
    scan_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "language": self.language,
            "findings": [f.to_dict() for f in self.findings],
            "lines_of_code": self.lines_of_code,
            "scan_time_ms": self.scan_time_ms,
        }


@dataclass
class ScanResult:
    """Aggregated results for an entire scan."""
    target_path: str
    files_scanned: int = 0
    total_findings: int = 0
    findings_by_severity: Dict[str, int] = field(default_factory=dict)
    findings_by_category: Dict[str, int] = field(default_factory=dict)
    file_results: List[FileResult] = field(default_factory=list)
    scan_duration_ms: float = 0.0
    rules_enabled: int = 0
    quality_score: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_path": self.target_path,
            "files_scanned": self.files_scanned,
            "total_findings": self.total_findings,
            "findings_by_severity": self.findings_by_severity,
            "findings_by_category": self.findings_by_category,
            "file_results": [fr.to_dict() for fr in self.file_results],
            "scan_duration_ms": self.scan_duration_ms,
            "rules_enabled": self.rules_enabled,
            "quality_score": round(self.quality_score, 2),
        }

    def calculate_score(self):
        """Calculate overall quality score (0-100)."""
        if self.total_findings == 0:
            self.quality_score = 100.0
            return

        total_weight = 0
        max_possible = self.files_scanned * 50
        for sev, count in self.findings_by_severity.items():
            try:
                sev_enum = Severity(sev)
                total_weight += count * sev_enum.score_weight()
            except ValueError:
                pass

        penalty = min(total_weight / max(max_possible, 1) * 100, 100)
        self.quality_score = max(0, 100 - penalty)


class Rule:
    """Base class for all quality rules."""

    def __init__(self, rule_id: str, name: str, category: Category,
                 severity: Severity, languages: List[str],
                 description: str, suggestion: str = ""):
        self.rule_id = rule_id
        self.name = name
        self.category = category
        self.severity = severity
        self.languages = languages
        self.description = description
        self.suggestion = suggestion

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Finding]:
        """Override this method in subclasses."""
        return []

    def supports_language(self, lang: str) -> bool:
        return lang in self.languages or "*" in self.languages


class RegexRule(Rule):
    """Rule based on regex pattern matching."""

    def __init__(self, rule_id: str, name: str, category: Category,
                 severity: Severity, languages: List[str],
                 description: str, pattern: str, suggestion: str = "",
                 confidence: float = 1.0):
        super().__init__(rule_id, name, category, severity, languages,
                         description, suggestion)
        self.pattern = re.compile(pattern, re.MULTILINE)
        self.confidence = confidence

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Finding]:
        findings = []
        for match in self.pattern.finditer(content):
            line_num = content[:match.start()].count('\n') + 1
            col_start = match.start() - content.rfind('\n', 0, match.start()) - 1
            col_end = col_start + len(match.group(0))

            snippet = lines[line_num - 1].strip() if line_num <= len(lines) else ""

            findings.append(Finding(
                rule_id=self.rule_id,
                rule_name=self.name,
                category=self.category,
                severity=self.severity,
                message=self.description,
                file_path=file_path,
                line_number=line_num,
                column_start=col_start,
                column_end=col_end,
                snippet=snippet,
                suggestion=self.suggestion,
                confidence=self.confidence,
            ))
        return findings


class ASTRule(Rule):
    """Rule based on AST-like analysis (simplified for zero-dependency)."""

    def __init__(self, rule_id: str, name: str, category: Category,
                 severity: Severity, languages: List[str],
                 description: str, check_func, suggestion: str = ""):
        super().__init__(rule_id, name, category, severity, languages,
                         description, suggestion)
        self.check_func = check_func

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Finding]:
        return self.check_func(self, file_path, content, lines)
