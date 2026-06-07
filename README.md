<div align="center">

# 🔍 CodeQualityLens

**轻量级 AI 生成代码质量检测引擎**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-orange)](requirements.txt)
[![Rules](https://img.shields.io/badge/Rules-48%2B-purple)](codequalitylens/rules.py)

[English](#english) | [简体中文](#simplified-chinese) | [繁體中文](#traditional-chinese)

</div>

---

<a name="english"></a>
## English

### Introduction

**CodeQualityLens** is a lightweight, zero-dependency CLI tool designed to detect quality issues in AI-generated code. As AI coding assistants (Claude Code, Copilot, Cursor, etc.) become increasingly prevalent, the quality and security of AI-generated code has become a critical concern. CodeQualityLens addresses this pain point by providing instant static analysis without requiring any external AI APIs or heavy dependencies.

**Key Differentiators:**
- Zero dependencies — runs on pure Python standard library
- AI-specific rules — detects patterns unique to AI-generated code (placeholders, boilerplate, hallucinations)
- 5-language support — Python, JavaScript, Go, Java, Rust
- Beautiful TUI dashboard — real-time visual feedback in your terminal
- Multi-format reports — JSON, HTML, SARIF, Markdown

### Quick Start

**Requirements:** Python 3.8+

```bash
git clone https://github.com/gitstq/CodeQualityLens.git
cd CodeQualityLens
python -m codequalitylens .
```

### Features

| Feature | Description |
|---------|-------------|
| Security Rules (10) | Detect hardcoded secrets, SQL injection, unsafe eval, weak hashes |
| Performance Rules (8) | Identify inefficient loops, blocking I/O, memory leaks |
| Reliability Rules (8) | Catch bare excepts, mutable defaults, unclosed resources |
| Maintainability Rules (8) | Flag long functions, TODOs, magic numbers, deep nesting |
| AI-Specific Rules (10) | Detect placeholders, boilerplate, verbose comments |
| Style Rules (4) | Check trailing whitespace, mixed tabs/spaces, line length |
| Quality Score | 0-100 score based on weighted severity analysis |
| TUI Dashboard | Beautiful terminal UI with color-coded severity breakdown |
| Report Formats | JSON, HTML, SARIF 2.1.0, Markdown |

### Usage

```bash
python -m codequalitylens .                           # Scan current directory
python -m codequalitylens app.py                      # Scan specific file
python -m codequalitylens src/ --format html          # Generate HTML report
python -m codequalitylens . --severity high           # Show high+ severity only
python -m codequalitylens . --category security       # Filter by category
python -m codequalitylens --rules                     # List all rules
```

### License

MIT License

---

<a name="simplified-chinese"></a>
## 简体中文

### 项目介绍

**CodeQualityLens** 是一款轻量级、零依赖的 CLI 工具，专门用于检测 AI 生成代码中的质量问题。随着 AI 编程助手（Claude Code、Copilot、Cursor 等）越来越普及，AI 生成代码的质量与安全性已成为开发者关注的焦点。CodeQualityLens 通过提供即时静态分析来解决这一痛点，无需任何外部 AI API 或繁重依赖。

**核心差异化亮点：**
- 零依赖 — 纯 Python 标准库运行
- AI 专属规则 — 检测 AI 生成代码特有的模式（占位符、样板代码、幻觉注释）
- 5 语言支持 — Python、JavaScript、Go、Java、Rust
- 精美 TUI 仪表盘 — 终端内实时可视化反馈
- 多格式报告 — JSON、HTML、SARIF、Markdown

### 快速开始

**环境要求：** Python 3.8+

```bash
git clone https://github.com/gitstq/CodeQualityLens.git
cd CodeQualityLens
python -m codequalitylens .
```

### 核心特性

| 特性 | 说明 |
|------|------|
| 安全规则 (10条) | 检测硬编码密钥、SQL 注入、不安全 eval、弱哈希 |
| 性能规则 (8条) | 识别低效循环、阻塞 I/O、内存泄漏 |
| 可靠性规则 (8条) | 捕获裸 except、可变默认参数、未关闭资源 |
| 可维护性规则 (8条) | 标记过长函数、TODO、魔法数字、深层嵌套 |
| AI 专属规则 (10条) | 检测占位符、样板代码、冗长注释 |
| 风格规则 (4条) | 检查尾部空格、混用制表符/空格、行长度 |
| 质量评分 | 基于加权严重度分析的 0-100 分评分 |
| TUI 仪表盘 | 带颜色编码严重度分解的精美终端界面 |
| 报告格式 | JSON、HTML、SARIF 2.1.0、Markdown |

### 使用方法

```bash
python -m codequalitylens .                           # 扫描当前目录
python -m codequalitylens app.py                      # 扫描指定文件
python -m codequalitylens src/ --format html          # 生成 HTML 报告
python -m codequalitylens . --severity high           # 仅显示 high 及以上
python -m codequalitylens . --category security       # 按类别过滤
python -m codequalitylens --rules                     # 列出所有规则
```

### 开源协议

MIT 协议

---

<a name="traditional-chinese"></a>
## 繁體中文

### 專案介紹

**CodeQualityLens** 是一款輕量級、零依賴的 CLI 工具，專門用於檢測 AI 生成程式碼中的品質問題。隨著 AI 編程助手（Claude Code、Copilot、Cursor 等）越來越普及，AI 生成程式碼的品質與安全性已成為開發者關注的焦點。CodeQualityLens 透過提供即時靜態分析來解決這一痛點，無需任何外部 AI API 或繁重依賴。

**核心差異化亮點：**
- 零依賴 — 純 Python 標準庫運行
- AI 專屬規則 — 檢測 AI 生成程式碼特有的模式（佔位符、樣板程式碼、幻覺註解）
- 5 語言支援 — Python、JavaScript、Go、Java、Rust
- 精美 TUI 儀表板 — 終端機內即時視覺化回饋
- 多格式報告 — JSON、HTML、SARIF、Markdown

### 快速開始

**環境要求：** Python 3.8+

```bash
git clone https://github.com/gitstq/CodeQualityLens.git
cd CodeQualityLens
python -m codequalitylens .
```

### 核心特性

| 特性 | 說明 |
|------|------|
| 安全規則 (10條) | 檢測硬編碼金鑰、SQL 注入、不安全 eval、弱雜湊 |
| 效能規則 (8條) | 識別低效迴圈、阻塞 I/O、記憶體洩漏 |
| 可靠性規則 (8條) | 捕獲裸 except、可變預設參數、未關閉資源 |
| 可維護性規則 (8條) | 標記過長函式、TODO、魔法數字、深層巢狀 |
| AI 專屬規則 (10條) | 檢測佔位符、樣板程式碼、冗長註解 |
| 風格規則 (4條) | 檢查尾部空格、混用定位字元/空格、行長度 |
| 品質評分 | 基於加權嚴重度分析的 0-100 分評分 |
| TUI 儀表板 | 帶顏色編碼嚴重度分解的精美終端介面 |
| 報告格式 | JSON、HTML、SARIF 2.1.0、Markdown |

### 使用方法

```bash
python -m codequalitylens .                           # 掃描目前目錄
python -m codequalitylens app.py                      # 掃描指定檔案
python -m codequalitylens src/ --format html          # 產生 HTML 報告
python -m codequalitylens . --severity high           # 僅顯示 high 及以上
python -m codequalitylens . --category security       # 按類別篩選
python -m codequalitylens --rules                     # 列出所有規則
```

### 開源協議

MIT 協議
