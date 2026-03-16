"""Typer-based CLI for README-God."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from readme_god.generator import generate_readmes
from readme_god.scanner import CONFIG_NAME, build_init_config


app = typer.Typer(
    add_completion=False,
    help="Generate concise bilingual README files from a repository.",
    rich_markup_mode="markdown",
)
console = Console()


@app.command()
def init(
    repo: Path = typer.Option(Path("."), "--repo", exists=True, file_okay=False, dir_okay=True, resolve_path=True),
) -> None:
    """Create a starter config for README generation."""
    repo = repo.resolve()
    config_path = repo / CONFIG_NAME
    if config_path.exists():
        console.print(f"[yellow]{CONFIG_NAME} already exists:[/yellow] {config_path}")
        raise typer.Exit(code=1)

    config_path.write_text(build_init_config(repo), encoding="utf-8")
    (repo / "docs").mkdir(parents=True, exist_ok=True)
    console.print(Panel.fit(f"Created {config_path.name}\nTarget repo: {repo}", title="README-God init"))


@app.command()
def generate(
    repo: Path = typer.Option(Path("."), "--repo", exists=True, file_okay=False, dir_okay=True, resolve_path=True),
) -> None:
    """Scan a repository and write bilingual README files."""
    generated = generate_readmes(repo.resolve())
    console.print(
        Panel.fit(
            "\n".join(
                [
                    f"English: {generated.readme_en}",
                    f"中文: {generated.readme_zh}",
                ]
            ),
            title="README-God generate",
        )
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
