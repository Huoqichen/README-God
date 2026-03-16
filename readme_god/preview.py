"""GitHub repository preview workflow."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
from urllib.parse import urlparse

from readme_god.generator import GeneratedFiles, generate_readmes
from readme_god.templates import render_template


@dataclass(slots=True)
class PreviewFiles:
    workspace: Path
    repository: Path
    readme_en: Path
    readme_zh: Path
    html_preview: Path


def preview_repository(repo_url: str, output_dir: Path) -> PreviewFiles:
    output_dir = output_dir.resolve()
    repository_dir = output_dir / "repo"
    html_preview = output_dir / "index.html"

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    _clone_repository(repo_url, repository_dir)
    generated = generate_readmes(repository_dir)
    _write_preview_page(repo_url, generated, html_preview)

    return PreviewFiles(
        workspace=output_dir,
        repository=repository_dir,
        readme_en=generated.readme_en,
        readme_zh=generated.readme_zh,
        html_preview=html_preview,
    )


def _clone_repository(repo_url: str, destination: Path) -> None:
    result = subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(destination)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git clone failed."
        raise RuntimeError(message)


def _write_preview_page(repo_url: str, generated: GeneratedFiles, destination: Path) -> None:
    repo_label = _repo_label_from_url(repo_url)
    english_markdown = generated.readme_en.read_text(encoding="utf-8")
    chinese_markdown = generated.readme_zh.read_text(encoding="utf-8")

    html = render_template(
        "preview.html.j2",
        {
            "repo_url": repo_url,
            "repo_label": repo_label,
            "readme_en_path": str(generated.readme_en),
            "readme_zh_path": str(generated.readme_zh),
            "readme_en_json": json.dumps(english_markdown),
            "readme_zh_json": json.dumps(chinese_markdown),
        },
    )
    destination.write_text(html, encoding="utf-8")


def _repo_label_from_url(repo_url: str) -> str:
    parsed = urlparse(repo_url)
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return path or repo_url
