"""
Command-line interface for CodeQualityLens.
"""

import argparse
import os
import sys
import json
from typing import Optional

from .core import ScanResult
from .scanner import scan_directory, get_all_rules, DEFAULT_EXCLUDES
from .reports import generate_json_report, generate_html_report, generate_sarif_report, generate_markdown_report
from .tui import render_dashboard, render_progress


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="codequalitylens",
        description="🔍 CodeQualityLens - Lightweight AI-Generated Code Quality Detection Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codequalitylens .                           # Scan current directory
  codequalitylens src/ --format html          # Generate HTML report
  codequalitylens app.py --severity medium    # Show medium+ severity only
  codequalitylens . --output report.json      # Save JSON report to file
  codequalitylens . --exclude tests,vendor    # Exclude directories

For more info: https://github.com/gitstq/CodeQualityLens
        """,
    )

    parser.add_argument("target", nargs="?", default=".", help="Path to scan (file or directory)")
    parser.add_argument("--format", "-f", choices=["json", "html", "sarif", "markdown", "tui"],
                        default="tui", help="Output format (default: tui)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--severity", "-s", choices=["critical", "high", "medium", "low", "info"],
                        default="info", help="Minimum severity to report")
    parser.add_argument("--exclude", "-e", help="Comma-separated list of directories to exclude")
    parser.add_argument("--category", "-c", help="Filter by category (security,performance,reliability,maintainability,style,ai_specific)")
    parser.add_argument("--rules", "-r", action="store_true", help="List all enabled rules")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress output")

    return parser


def filter_results(result: ScanResult, min_severity: str, category: Optional[str] = None) -> ScanResult:
    """Filter findings by severity and category."""
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    min_level = severity_order.get(min_severity, 4)

    filtered_files = []
    for fr in result.file_results:
        filtered_findings = []
        for finding in fr.findings:
            finding_level = severity_order.get(str(finding.severity), 4)
            if finding_level <= min_level:
                if category is None or str(finding.category) == category:
                    filtered_findings.append(finding)
        if filtered_findings:
            new_fr = __import__('dataclasses').replace(fr, findings=filtered_findings)
            filtered_files.append(new_fr)

    new_result = ScanResult(
        target_path=result.target_path,
        files_scanned=result.files_scanned,
        total_findings=sum(len(fr.findings) for fr in filtered_files),
        findings_by_severity={},  # Recalculated below
        findings_by_category={},
        file_results=filtered_files,
        scan_duration_ms=result.scan_duration_ms,
        rules_enabled=result.rules_enabled,
        quality_score=result.quality_score,
    )

    for fr in filtered_files:
        for finding in fr.findings:
            sev = str(finding.severity)
            cat = str(finding.category)
            new_result.findings_by_severity[sev] = new_result.findings_by_severity.get(sev, 0) + 1
            new_result.findings_by_category[cat] = new_result.findings_by_category.get(cat, 0) + 1

    new_result.calculate_score()
    return new_result


def list_rules():
    """Print all available rules."""
    from .rules import get_all_rules
    rules = get_all_rules()

    print("\n" + "═" * 70)
    print("  📋 CodeQualityLens - Built-in Rules ({} total)".format(len(rules)))
    print("═" * 70 + "\n")

    categories = {}
    for rule in rules:
        cat = str(rule.category)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(rule)

    cat_emojis = {
        "security": "🔒", "performance": "⚡", "reliability": "🔧",
        "maintainability": "🛠️", "style": "✏️", "ai_specific": "🤖",
    }

    for cat, cat_rules in sorted(categories.items()):
        emoji = cat_emojis.get(cat, "📌")
        print(f"\n{emoji} {cat.upper().replace('_', ' ')} ({len(cat_rules)} rules)")
        print("─" * 50)
        for rule in cat_rules:
            sev_color = {"critical": "91", "high": "95", "medium": "93", "low": "92", "info": "90"}
            color = sev_color.get(str(rule.severity), "97")
            langs = ", ".join(rule.languages) if "*" not in rule.languages else "all"
            print(f"  \033[{color}m[{rule.rule_id}]\033[0m {rule.name}")
            print(f"       Severity: {rule.severity.value} | Languages: {langs}")
            print(f"       {rule.description}")
    print("")


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"CodeQualityLens v{__version__}")
        sys.exit(0)

    if args.rules:
        list_rules()
        sys.exit(0)

    target = os.path.abspath(args.target)
    if not os.path.exists(target):
        print(f"Error: Path not found: {target}", file=sys.stderr)
        sys.exit(1)

    excludes = DEFAULT_EXCLUDES.copy()
    if args.exclude:
        excludes.update(args.exclude.split(","))

    # Scan
    if not args.no_progress and args.format == "tui":
        print(f"\n  🔍 Scanning: {target}\n")

    result = scan_directory(target, excludes=excludes)
    filtered = filter_results(result, args.severity, args.category)

    # Generate output
    if args.format == "json":
        output = generate_json_report(filtered)
    elif args.format == "html":
        output = generate_html_report(filtered)
    elif args.format == "sarif":
        output = generate_sarif_report(filtered)
    elif args.format == "markdown":
        output = generate_markdown_report(filtered)
    else:
        output = render_dashboard(filtered, show_details=True)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n  ✅ Report saved to: {os.path.abspath(args.output)}\n")
    else:
        print(output)

    # Exit with non-zero if critical/high findings
    critical_high = filtered.findings_by_severity.get("critical", 0) + filtered.findings_by_severity.get("high", 0)
    sys.exit(1 if critical_high > 0 else 0)


if __name__ == "__main__":
    main()
