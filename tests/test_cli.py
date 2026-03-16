from pathlib import Path

from typer.testing import CliRunner

from readme_god.cli import app
from readme_god.preview import PreviewFiles


runner = CliRunner()


def test_init_creates_config_and_docs_dir(tmp_path: Path) -> None:
    result = runner.invoke(app, ["init", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / ".readme-god.yml").exists()
    assert (tmp_path / "docs").exists()


def test_generate_creates_readme_files(tmp_path: Path) -> None:
    (tmp_path / ".readme-god.yml").write_text(
        """
title: Demo
description: Short demo.
repo_slug: OWNER/REPO
cli_name: demo
features:
  - One feature.
installation:
  - pip install -e .
usage:
  - demo --help
commands:
  - name: demo --help
    description: Show help.
roadmap:
  - Keep improving.
contributing: Contributions are welcome.
license: MIT
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["generate", "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "docs" / "README.zh-CN.md").exists()


def test_generate_accepts_positional_repo(tmp_path: Path) -> None:
    (tmp_path / ".readme-god.yml").write_text(
        """
title: Demo
description: Short demo.
repo_slug: OWNER/REPO
cli_name: demo
features:
  - One feature.
installation:
  - pip install -e .
usage:
  - demo --help
commands:
  - name: demo --help
    description: Show help.
roadmap:
  - Keep improving.
contributing: Contributions are welcome.
license: MIT
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["generate", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / "README.md").exists()


def test_preview_delegates_and_prints_paths(tmp_path: Path, monkeypatch) -> None:
    preview_dir = tmp_path / "preview"
    repo_dir = preview_dir / "repo"
    docs_dir = repo_dir / "docs"
    docs_dir.mkdir(parents=True)
    readme_en = repo_dir / "README.md"
    readme_zh = docs_dir / "README.zh-CN.md"
    html_preview = preview_dir / "index.html"
    readme_en.write_text("# Demo", encoding="utf-8")
    readme_zh.write_text("# 演示", encoding="utf-8")
    html_preview.write_text("<html></html>", encoding="utf-8")

    def fake_preview_repository(repo_url: str, out: Path) -> PreviewFiles:
        assert repo_url == "https://github.com/user/repo"
        assert out == preview_dir.resolve()
        return PreviewFiles(
            workspace=preview_dir.resolve(),
            repository=repo_dir.resolve(),
            readme_en=readme_en.resolve(),
            readme_zh=readme_zh.resolve(),
            html_preview=html_preview.resolve(),
        )

    monkeypatch.setattr("readme_god.cli.preview_repository", fake_preview_repository)

    result = runner.invoke(app, ["preview", "https://github.com/user/repo", "--out", str(preview_dir)])

    assert result.exit_code == 0
    assert "Preview Ready" in result.stdout
    assert "index.html" in result.stdout
