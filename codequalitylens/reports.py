"""
Report generators for CodeQualityLens - JSON, HTML, SARIF, Markdown.
"""

import json
import html
import datetime
from typing import Dict, Any
from .core import ScanResult


def generate_json_report(result: ScanResult) -> str:
    """Generate JSON format report."""
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False)


def generate_sarif_report(result: ScanResult, tool_name: str = "CodeQualityLens") -> str:
    """Generate SARIF (Static Analysis Results Interchange Format) report."""
    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": tool_name,
                    "version": "1.0.0",
                    "informationUri": "https://github.com/gitstq/CodeQualityLens",
                    "rules": [],
                }
            },
            "results": [],
        }]
    }

    rule_ids = set()
    for fr in result.file_results:
        for finding in fr.findings:
            if finding.rule_id not in rule_ids:
                rule_ids.add(finding.rule_id)
                sarif["runs"][0]["tool"]["driver"]["rules"].append({
                    "id": finding.rule_id,
                    "name": finding.rule_name,
                    "shortDescription": {"text": finding.message},
                    "defaultConfiguration": {
                        "level": "warning" if finding.severity.value in ["medium", "low", "info"] else "error"
                    },
                })

            sarif["runs"][0]["results"].append({
                "ruleId": finding.rule_id,
                "message": {"text": finding.message},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": finding.file_path},
                        "region": {
                            "startLine": finding.line_number,
                            "startColumn": finding.column_start,
                            "endColumn": finding.column_end,
                            "snippet": {"text": finding.snippet},
                        }
                    }
                }],
                "properties": {
                    "category": str(finding.category),
                    "severity": str(finding.severity),
                    "suggestion": finding.suggestion,
                }
            })

    return json.dumps(sarif, indent=2, ensure_ascii=False)


def generate_html_report(result: ScanResult) -> str:
    """Generate HTML format report with styling."""
    severity_colors = {
        "critical": "#dc2626",
        "high": "#ea580c",
        "medium": "#ca8a04",
        "low": "#16a34a",
        "info": "#6b7280",
    }

    category_icons = {
        "security": "&#128274;",
        "performance": "&#9889;",
        "reliability": "&#128736;",
        "maintainability": "&#128295;",
        "style": "&#9997;",
        "ai_specific": "&#129302;",
    }

    rows = []
    for fr in result.file_results:
        for finding in fr.findings:
            color = severity_colors.get(str(finding.severity), "#6b7280")
            icon = category_icons.get(str(finding.category), "&#8226;")
            rows.append(f"""
            <tr>
                <td><span style="color:{color};font-weight:bold;">{finding.severity.value.upper()}</span></td>
                <td>{icon} {finding.category.value}</td>
                <td><code>{html.escape(finding.rule_id)}</code></td>
                <td>{html.escape(finding.message)}</td>
                <td><code>{html.escape(finding.file_path)}:{finding.line_number}</code></td>
                <td><pre style="margin:0;">{html.escape(finding.snippet[:80])}</pre></td>
                <td>{html.escape(finding.suggestion)}</td>
            </tr>
            """)

    summary_cards = ""
    for sev, count in sorted(result.findings_by_severity.items(),
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}.get(x[0], 5)):
        color = severity_colors.get(sev, "#6b7280")
        summary_cards += f"""
        <div style="background:{color};color:white;padding:15px 25px;border-radius:8px;text-align:center;">
            <div style="font-size:28px;font-weight:bold;">{count}</div>
            <div style="font-size:12px;text-transform:uppercase;">{sev}</div>
        </div>
        """

    score_color = "#16a34a" if result.quality_score >= 80 else "#ca8a04" if result.quality_score >= 60 else "#dc2626"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodeQualityLens Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1f2937; margin-bottom: 5px; }}
        .subtitle {{ color: #6b7280; margin-bottom: 25px; }}
        .score-card {{ background: {score_color}; color: white; padding: 20px 40px; border-radius: 12px; display: inline-block; margin-bottom: 25px; }}
        .score-value {{ font-size: 48px; font-weight: bold; }}
        .score-label {{ font-size: 14px; opacity: 0.9; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin-bottom: 25px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #f3f4f6; padding: 12px; text-align: left; font-weight: 600; color: #374151; border-bottom: 2px solid #e5e7eb; }}
        td {{ padding: 12px; border-bottom: 1px solid #e5e7eb; vertical-align: top; }}
        tr:hover {{ background: #f9fafb; }}
        code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
        pre {{ background: #f3f4f6; padding: 8px; border-radius: 4px; font-size: 12px; overflow-x: auto; }}
        .meta {{ color: #6b7280; font-size: 14px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>&#128269; CodeQualityLens Report</h1>
        <p class="subtitle">AI-Generated Code Quality Detection Engine</p>
        <p class="meta">Target: <code>{result.target_path}</code> | Scanned: {result.files_scanned} files | Duration: {result.scan_duration_ms:.0f}ms | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="score-card">
            <div class="score-value">{result.quality_score:.1f}</div>
            <div class="score-label">QUALITY SCORE</div>
        </div>

        <h3>Findings by Severity</h3>
        <div class="summary-grid">
            {summary_cards}
        </div>

        <h3>Detailed Findings ({result.total_findings})</h3>
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Category</th>
                    <th>Rule</th>
                    <th>Message</th>
                    <th>Location</th>
                    <th>Snippet</th>
                    <th>Suggestion</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows) if rows else '<tr><td colspan="7" style="text-align:center;color:#6b7280;">No issues found! Great job!</td></tr>'}
            </tbody>
        </table>
    </div>
</body>
</html>"""


def generate_markdown_report(result: ScanResult) -> str:
    """Generate Markdown format report."""
    lines = [
        "# CodeQualityLens Report",
        "",
        f"**Target:** `{result.target_path}`",
        f"**Files Scanned:** {result.files_scanned}",
        f"**Total Findings:** {result.total_findings}",
        f"**Quality Score:** {result.quality_score:.1f}/100",
        f"**Scan Duration:** {result.scan_duration_ms:.0f}ms",
        f"**Rules Enabled:** {result.rules_enabled}",
        "",
        "## Findings by Severity",
        "",
    ]

    for sev, count in sorted(result.findings_by_severity.items(),
                              key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}.get(x[0], 5)):
        emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "info": "⚪"}.get(sev, "⚪")
        lines.append(f"- {emoji} **{sev.upper()}**: {count}")

    lines.extend(["", "## Findings by Category", ""])
    for cat, count in sorted(result.findings_by_category.items()):
        lines.append(f"- **{cat}**: {count}")

    lines.extend(["", "## Detailed Findings", ""])

    if not result.total_findings:
        lines.append("✅ No issues found! Your code looks great.")
    else:
        for fr in result.file_results:
            if fr.findings:
                lines.append(f"### {fr.file_path} ({fr.language})")
                for finding in fr.findings:
                    lines.append(f"- **{finding.severity.value.upper()}** | `{finding.rule_id}` | Line {finding.line_number}")
                    lines.append(f"  - {finding.message}")
                    if finding.suggestion:
                        lines.append(f"  - 💡 {finding.suggestion}")
                    lines.append("")

    return "\n".join(lines)
