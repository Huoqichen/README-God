from __future__ import annotations

from pathlib import Path
import subprocess

from readme_god.preview import preview_repository


def test_preview_repository_clones_generates_and_builds_html(tmp_path: Path) -> None:
    source_repo = tmp_path / "source"
    source_repo.mkdir()
    (source_repo / "pyproject.toml").write_text(
        """
[project]
name = "demo-preview"
description = "Preview demo."

[project.scripts]
demo-preview = "demo:main"
""".strip(),
        encoding="utf-8",
    )
    subprocess.run(["git", "init"], cwd=source_repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=source_repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
        cwd=source_repo,
        check=True,
        capture_output=True,
        text=True,
    )

    preview_dir = tmp_path / "preview"
    files = preview_repository(str(source_repo), preview_dir)

    assert files.repository.exists()
    assert files.readme_en.exists()
    assert files.readme_zh.exists()
    assert files.html_preview.exists()

    html = files.html_preview.read_text(encoding="utf-8")
    assert "README Preview" in html
    assert "markdown-en" in html
    assert "markdown-zh" in html
