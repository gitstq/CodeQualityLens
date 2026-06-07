"""
Unit tests for CodeQualityLens core functionality.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from codequalitylens.core import Finding, FileResult, ScanResult, Severity, Category, RegexRule
from codequalitylens.scanner import detect_language, should_scan, scan_file, scan_directory
from codequalitylens.rules import get_all_rules


class TestCore(unittest.TestCase):
    def test_severity_score_weight(self):
        self.assertEqual(Severity.CRITICAL.score_weight(), 10)
        self.assertEqual(Severity.HIGH.score_weight(), 7)
        self.assertEqual(Severity.INFO.score_weight(), 0)

    def test_finding_creation(self):
        finding = Finding(
            rule_id="TEST-001",
            rule_name="Test Rule",
            category=Category.SECURITY,
            severity=Severity.HIGH,
            message="Test message",
            file_path="test.py",
            line_number=10,
            snippet="test code",
        )
        self.assertEqual(finding.rule_id, "TEST-001")
        self.assertEqual(finding.severity, Severity.HIGH)

    def test_scan_result_score(self):
        result = ScanResult(target_path=".")
        self.assertEqual(result.quality_score, 100.0)


class TestScanner(unittest.TestCase):
    def test_detect_language(self):
        self.assertEqual(detect_language("test.py"), "python")
        self.assertEqual(detect_language("test.js"), "javascript")
        self.assertEqual(detect_language("test.go"), "go")
        self.assertEqual(detect_language("test.java"), "java")
        self.assertEqual(detect_language("test.rs"), "rust")
        self.assertIsNone(detect_language("test.txt"))

    def test_should_scan(self):
        self.assertTrue(should_scan("/proj/src/main.py", "/proj", {"node_modules"}))
        self.assertFalse(should_scan("/proj/node_modules/x.py", "/proj", {"node_modules"}))

    def test_scan_file_with_issues(self):
        rules = get_all_rules()
        test_content = '''
api_key = "sk-1234567890abcdef1234567890abcdef"
password = "supersecret123"
'''
        test_path = "/tmp/test_scan_file.py"
        with open(test_path, "w") as f:
            f.write(test_content)

        result = scan_file(test_path, rules, "/tmp")
        self.assertGreater(len(result.findings), 0)

        # Check that SEC-001 was triggered
        sec_findings = [f for f in result.findings if f.rule_id == "SEC-001"]
        self.assertGreaterEqual(len(sec_findings), 1)

        os.remove(test_path)

    def test_scan_directory(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write('api_key = "secret1234567890abcdef"\n')
            with open(os.path.join(tmpdir, "test.js"), "w") as f:
                f.write('const password = "secret1234567890abcdef";\n')

            result = scan_directory(tmpdir)
            self.assertGreaterEqual(result.files_scanned, 2)
            self.assertGreater(result.total_findings, 0)
            self.assertLessEqual(result.quality_score, 100.0)


class TestRules(unittest.TestCase):
    def test_all_rules_have_valid_attributes(self):
        rules = get_all_rules()
        self.assertGreater(len(rules), 0)

        for rule in rules:
            self.assertTrue(rule.rule_id)
            self.assertTrue(rule.name)
            self.assertTrue(rule.description)
            self.assertIsInstance(rule.category, Category)
            self.assertIsInstance(rule.severity, Severity)
            self.assertTrue(rule.languages)

    def test_rule_id_uniqueness(self):
        rules = get_all_rules()
        ids = [r.rule_id for r in rules]
        self.assertEqual(len(ids), len(set(ids)), "Rule IDs must be unique")


class TestRegexRule(unittest.TestCase):
    def test_regex_rule_matching(self):
        rule = RegexRule(
            "TEST-001", "Test Pattern", Category.SECURITY, Severity.HIGH,
            ["python"], "Test description", r'password\s*=\s*"[^"]+"',
            "Use env vars"
        )

        content = 'password = "secret123"\nother = "ok"\n'
        lines = content.split("\n")
        findings = rule.check("test.py", content, lines)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line_number, 1)
        self.assertEqual(findings[0].rule_id, "TEST-001")


if __name__ == "__main__":
    unittest.main()
