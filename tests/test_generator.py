from pathlib import Path

from readme_god.generator import build_template_context, generate_readmes
from readme_god.scanner import CommandInfo, RepositoryContext, scan_repository


def test_scan_repository_uses_config(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "demo-app"
description = "Demo application."

[project.scripts]
demo = "demo:main"
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / ".readme-god.yml").write_text(
        """
title: Demo App
description: A clean demo.
repo_slug: acme/demo-app
cli_name: demo
features:
  - Feature A
commands:
  - name: demo run
    description: Run the demo.
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()

    context = scan_repository(tmp_path)

    assert context.title == "Demo App"
    assert context.description == "A clean demo."
    assert context.tagline == "Minimal setup. Clear project overview."
    assert context.languages == ["Python"]
    assert context.badge_label == "language"
    assert context.repo_slug == "acme/demo-app"
    assert context.features == ["Feature A"]
    assert context.commands[0].name == "demo run"


def test_generate_readmes_writes_both_languages(tmp_path: Path) -> None:
    (tmp_path / ".readme-god.yml").write_text(
        """
title: Sample Repo
description: Sample description.
tagline: Short and sharp.
repo_slug: OWNER/REPO
cli_name: sample
languages:
  - Python
features:
  - Small and direct.
installation:
  - pip install -e .
usage:
  - sample --help
commands:
  - name: sample --help
    description: Show help.
roadmap:
  - Add another command.
contributing: Welcome contributions.
license: MIT
""".strip(),
        encoding="utf-8",
    )

    generated = generate_readmes(tmp_path)

    readme_en = generated.readme_en.read_text(encoding="utf-8")
    readme_zh = generated.readme_zh.read_text(encoding="utf-8")

    assert '<a href="./docs/README.zh-CN.md">简体中文</a> | English' in readme_en
    assert '简体中文 | <a href="../README.md">English</a>' in readme_zh
    assert "https://api.star-history.com/svg?repos=OWNER/REPO&type=Date" in readme_en
    assert "https://img.shields.io/github/stars/OWNER/REPO?style=flat-square" in readme_en
    assert "https://img.shields.io/badge/language-Python-6b7280?style=flat-square" in readme_en
    assert "简体中文</a> | English" in readme_en
    assert "Sample Repo" in readme_en
    assert "Short and sharp." in readme_en
    assert "Welcome contributions." in readme_en


def test_build_template_context_serializes_commands() -> None:
    context = RepositoryContext(
        title="Demo",
        description="Short description.",
        description_zh="简短描述。",
        tagline="Short tagline.",
        tagline_zh="简短副标题。",
        languages=["Python"],
        badge_label="language",
        badge_values=["Python"],
        repo_slug="OWNER/REPO",
        cli_name="demo",
        features=["Fast"],
        features_zh=["快速。"],
        installation=["pip install -e ."],
        usage=["demo --help"],
        commands=[CommandInfo(name="demo --help", description="Show help.")],
        commands_zh=[CommandInfo(name="demo --help", description="显示帮助。")],
        roadmap_en=["Ship it."],
        roadmap_zh=["发布它。"],
        contributing_en="Contribute.",
        contributing_zh="欢迎贡献。",
        license_name="MIT",
        output_repo=Path("."),
    )

    data = build_template_context(context)

    assert data["commands"] == [{"name": "demo --help", "description": "Show help."}]


def test_scan_repository_prefers_existing_readme_content(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "repograph"
description = "CLI tool for analyzing GitHub repositories and generating architecture maps."

[project.scripts]
repomap = "repomap.cli:app"
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        """
<div align="center">
  <h1>repomap</h1>
  <p><strong>Turn any GitHub repository into an architecture diagram.</strong></p>
  <p>Analyze GitHub repositories with a Python engine, FastAPI backend, and Next.js + D3.js web UI.</p>
  <p><img src="https://img.shields.io/badge/platform-Python%20%7C%20Web-green?style=flat-square" alt="Platform" /></p>
  <p><a href="./README.md">English</a> | <a href="./docs/README.zh-CN.md">简体中文</a></p>
</div>

## Features
- Analyze GitHub repositories from both CLI and Web UI
- Export folder tree, JSON, and compact Mermaid architecture diagrams
- Render an interactive graph in the browser with D3.js

## Installation
```bash
python -m pip install -e .
cd web
npm install
```

## Usage
```bash
repomap https://github.com/user/repo
repomap https://github.com/user/repo --branch main
```

## Current Status
Still good next upgrades:

- deeper package-manager-aware monorepo resolution
- graph grouping, collapsing, and saved views

## Contributing
Contributions are welcome. Good next steps include more language-specific parsers.
""".strip(),
        encoding="utf-8",
    )
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "README.zh-CN.md").write_text(
        """
<div align="center">
  <h1>repomap</h1>
  <p><strong>将任意 GitHub 仓库转换为架构图。</strong></p>
  <p>使用 Python 分析引擎、FastAPI 后端与 Next.js + D3.js Web 界面分析 GitHub 仓库。</p>
</div>

## 特性
- 同时支持命令行和 Web 界面分析 GitHub 仓库
- 输出目录树、JSON 和精简后的 Mermaid 架构图
- 使用 D3.js 在浏览器中渲染交互式架构图

## 当前状态
- 更深入的 monorepo 解析
- 图谱分组、折叠和保存视图

## 贡献
欢迎贡献。比较值得继续扩展的方向包括更多语言专属解析器。
""".strip(),
        encoding="utf-8",
    )

    context = scan_repository(tmp_path)

    assert context.title == "repomap"
    assert context.description == "Turn any GitHub repository into an architecture diagram."
    assert context.tagline == "Analyze GitHub repositories with a Python engine, FastAPI backend, and Next.js + D3.js web UI."
    assert context.badge_label == "platform"
    assert context.badge_values == ["Python", "Web"]
    assert context.features[0] == "Analyze GitHub repositories from both CLI and Web UI"
    assert context.installation[:2] == ["python -m pip install -e .", "cd web"]
    assert context.usage[0] == "repomap https://github.com/user/repo"
