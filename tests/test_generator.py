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
