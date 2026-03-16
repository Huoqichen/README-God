"""README generation pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from readme_god.scanner import RepositoryContext, scan_repository
from readme_god.templates import render_template


@dataclass(slots=True)
class GeneratedFiles:
    readme_en: Path
    readme_zh: Path


def build_template_context(context: RepositoryContext) -> dict[str, object]:
    return {
        "title": context.title,
        "description": context.description,
        "description_zh": context.description_zh,
        "tagline": context.tagline,
        "tagline_zh": context.tagline_zh,
        "repo_slug": context.repo_slug,
        "cli_name": context.cli_name,
        "features": context.features,
        "features_zh": context.features_zh,
        "installation": context.installation,
        "usage": context.usage,
        "commands": [asdict(command) for command in context.commands],
        "commands_zh": [asdict(command) for command in context.commands_zh],
        "roadmap_en": context.roadmap_en,
        "roadmap_zh": context.roadmap_zh,
        "contributing_en": context.contributing_en,
        "contributing_zh": context.contributing_zh,
        "license_name": context.license_name,
    }


def render_readmes(context: RepositoryContext) -> tuple[str, str]:
    template_context = build_template_context(context)
    readme_en = render_template("README.en.j2", template_context)
    readme_zh = render_template("README.zh-CN.j2", template_context)
    return readme_en, readme_zh


def generate_readmes(repo_path: Path) -> GeneratedFiles:
    repo_path = repo_path.resolve()
    context = scan_repository(repo_path)
    readme_en, readme_zh = render_readmes(context)

    readme_path = repo_path / "README.md"
    zh_dir = repo_path / "docs"
    zh_path = zh_dir / "README.zh-CN.md"

    zh_dir.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(readme_en, encoding="utf-8")
    zh_path.write_text(readme_zh, encoding="utf-8")

    return GeneratedFiles(readme_en=readme_path, readme_zh=zh_path)
