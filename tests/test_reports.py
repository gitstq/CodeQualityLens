"""
Unit tests for report generators.
"""

import unittest
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from codequalitylens.core import ScanResult, FileResult, Finding, Severity, Category
from codequalitylens.reports import generate_json_report, generate_html_report, generate_sarif_report, generate_markdown_report


class TestReports(unittest.TestCase):
    def setUp(self):
        self.result = ScanResult(
            target_path="/test",
            files_scanned=2,
            total_findings=3,
            findings_by_severity={"high": 2, "medium": 1},
            findings_by_category={"security": 2, "performance": 1},
            rules_enabled=10,
            quality_score=75.5,
        )

        finding1 = Finding(
            rule_id="SEC-001", rule_name="Hardcoded Secret",
            category=Category.SECURITY, severity=Severity.HIGH,
            message="Secret found", file_path="test.py", line_number=5,
            snippet='api_key = "xxx"', suggestion="Use env vars",
        )
        finding2 = Finding(
            rule_id="PERF-001", rule_name="Inefficient Loop",
            category=Category.PERFORMANCE, severity=Severity.MEDIUM,
            message="Slow loop", file_path="test.py", line_number=10,
            snippet="for i in range(1000000):", suggestion="Use generator",
        )

        self.result.file_results = [
            FileResult(file_path="test.py", language="python", findings=[finding1, finding2], lines_of_code=20),
        ]

    def test_json_report(self):
        report = generate_json_report(self.result)
        data = json.loads(report)
        self.assertEqual(data["target_path"], "/test")
        self.assertEqual(data["total_findings"], 3)
        self.assertIn("file_results", data)

    def test_html_report(self):
        report = generate_html_report(self.result)
        self.assertIn("<!DOCTYPE html>", report)
        self.assertIn("CodeQualityLens", report)
        self.assertIn("SEC-001", report)
        self.assertIn("test.py", report)

    def test_sarif_report(self):
        report = generate_sarif_report(self.result)
        data = json.loads(report)
        self.assertEqual(data["version"], "2.1.0")
        self.assertIn("runs", data)
        self.assertTrue(len(data["runs"][0]["results"]) > 0)

    def test_markdown_report(self):
        report = generate_markdown_report(self.result)
        self.assertIn("# CodeQualityLens Report", report)
        self.assertIn("SEC-001", report)
        self.assertIn("75.5", report)


if __name__ == "__main__":
    unittest.main()
