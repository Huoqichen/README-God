from pathlib import Path

from typer.testing import CliRunner

from readme_god.cli import app


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
