"""
Terminal User Interface (TUI) dashboard for CodeQualityLens.
Pure Python standard library - no external dependencies.
"""

import os
import sys
import shutil
from typing import Optional
from .core import ScanResult, Severity


def get_terminal_size() -> tuple:
    """Get terminal dimensions."""
    try:
        return shutil.get_terminal_size()
    except Exception:
        return (80, 24)


def colorize(text: str, color: str) -> str:
    """Apply ANSI color codes."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "reset": "\033[0m",
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def draw_box(title: str, content_lines: list, width: int = 60) -> list:
    """Draw a bordered box."""
    lines = []
    lines.append("┌" + "─" * (width - 2) + "┐")
    title_padded = f" {title} ".center(width - 2, "─")
    lines.append("├" + title_padded + "┤")
    for line in content_lines:
        truncated = line[:width - 4]
        padded = truncated + " " * (width - 2 - len(truncated))
        lines.append("│ " + padded + " │")
    lines.append("└" + "─" * (width - 2) + "┘")
    return lines


def render_dashboard(result: ScanResult, show_details: bool = True) -> str:
    """Render a beautiful TUI dashboard."""
    term_width, term_height = get_terminal_size()
    box_width = min(70, term_width - 4)

    output = []

    # Header
    output.append("")
    header = " 🔍  CodeQualityLens - AI Code Quality Detection Engine "
    output.append(colorize(header.center(box_width, "═"), "bold"))
    output.append("")

    # Score gauge
    score = result.quality_score
    if score >= 80:
        score_color = "green"
        score_emoji = "🟢"
    elif score >= 60:
        score_color = "yellow"
        score_emoji = "🟡"
    elif score >= 40:
        score_color = "magenta"
        score_emoji = "🟠"
    else:
        score_color = "red"
        score_emoji = "🔴"

    filled = int(score / 100 * (box_width - 20))
    bar = "█" * filled + "░" * (box_width - 20 - filled)
    score_line = f"  Quality Score: {colorize(f'{score:.1f}/100', score_color + ' bold')} {score_emoji}"
    bar_line = f"  [{colorize(bar, score_color)}]"

    output.append(score_line)
    output.append(bar_line)
    output.append("")

    # Summary stats
    stats = [
        f"  📁 Files Scanned:    {result.files_scanned}",
        f"  🐛 Total Findings:   {result.total_findings}",
        f"  📏 Rules Enabled:    {result.rules_enabled}",
        f"  ⏱️  Scan Duration:    {result.scan_duration_ms:.0f}ms",
    ]
    for line in stats:
        output.append(colorize(line, "white"))
    output.append("")

    # Severity breakdown
    severity_emojis = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
        "info": "⚪",
    }

    sev_lines = []
    for sev in ["critical", "high", "medium", "low", "info"]:
        count = result.findings_by_severity.get(sev, 0)
        emoji = severity_emojis.get(sev, "⚪")
        color = {"critical": "red", "high": "magenta", "medium": "yellow", "low": "green", "info": "dim"}.get(sev, "white")
        sev_lines.append(f"  {emoji} {colorize(sev.upper().ljust(10), color)} {count:>4}")

    output.extend(draw_box("Findings by Severity", sev_lines, box_width))
    output.append("")

    # Category breakdown
    cat_emojis = {
        "security": "🔒",
        "performance": "⚡",
        "reliability": "🔧",
        "maintainability": "🛠️ ",
        "style": "✏️ ",
        "ai_specific": "🤖",
    }

    cat_lines = []
    for cat, count in sorted(result.findings_by_category.items()):
        emoji = cat_emojis.get(cat, "📌")
        cat_lines.append(f"  {emoji} {cat.replace('_', ' ').title().ljust(20)} {count:>4}")

    output.extend(draw_box("Findings by Category", cat_lines, box_width))
    output.append("")

    # Top findings
    if show_details and result.total_findings > 0:
        all_findings = []
        for fr in result.file_results:
            for f in fr.findings:
                all_findings.append(f)

        all_findings.sort(key=lambda x: x.severity.score_weight(), reverse=True)
        top = all_findings[:10]

        detail_lines = []
        for finding in top:
            sev_color = {
                Severity.CRITICAL: "red",
                Severity.HIGH: "magenta",
                Severity.MEDIUM: "yellow",
                Severity.LOW: "green",
                Severity.INFO: "dim",
            }.get(finding.severity, "white")

            file_short = os.path.basename(finding.file_path)
            line = f"  {severity_emojis.get(str(finding.severity), '⚪')} {colorize(finding.severity.value[:3].upper(), sev_color)} [{finding.rule_id}] {file_short}:{finding.line_number}"
            detail_lines.append(line[:box_width - 4])
            msg = f"     {finding.message[:box_width - 8]}"
            detail_lines.append(msg)
            detail_lines.append("")

        output.extend(draw_box(f"Top Findings (showing {len(top)} of {result.total_findings})", detail_lines, box_width))
        output.append("")

    # Footer
    output.append(colorize("  💡 Run with --format html to generate a detailed HTML report".center(box_width), "dim"))
    output.append("")

    return "\n".join(output)


def render_progress(current: int, total: int, filename: str) -> str:
    """Render a progress bar for scanning."""
    term_width, _ = get_terminal_size()
    bar_width = min(40, term_width - 30)
    filled = int(current / max(total, 1) * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    pct = int(current / max(total, 1) * 100)
    return f"\r  Scanning [{colorize(bar, 'cyan')}] {pct}% ({current}/{total}) {filename[:30]}" + " " * 5
