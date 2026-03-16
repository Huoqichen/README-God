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
    no_args_is_help=True,
    help="Generate GitHub-ready README.md and docs/README.zh-CN.md from a repository.",
    rich_markup_mode="markdown",
    context_settings={"help_option_names": ["-h", "--help"]},
)
console = Console()


@app.command(short_help="Create starter config.")
def init(
    repo: Path = typer.Option(
        Path("."),
        "--repo",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Repository to initialize. Defaults to the current directory.",
    ),
) -> None:
    """Create a starter .readme-god.yml and docs directory."""
    repo = repo.resolve()
    config_path = repo / CONFIG_NAME
    if config_path.exists():
        console.print(f"[yellow]{CONFIG_NAME} already exists:[/yellow] {config_path}")
        raise typer.Exit(code=1)

    config_path.write_text(build_init_config(repo), encoding="utf-8")
    (repo / "docs").mkdir(parents=True, exist_ok=True)
    console.print(
        Panel.fit(
            "\n".join(
                [
                    f"Created: {config_path}",
                    "Next: readme-god generate --repo .",
                ]
            ),
            title="Initialized",
        )
    )


@app.command(short_help="Generate bilingual README files.")
def generate(
    repo: Path = typer.Option(
        Path("."),
        "--repo",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Repository to scan. Defaults to the current directory.",
    ),
) -> None:
    """Generate README.md and docs/README.zh-CN.md."""
    generated = generate_readmes(repo.resolve())
    console.print(
        Panel.fit(
            "\n".join(
                [
                    f"Wrote: {generated.readme_en}",
                    f"Wrote: {generated.readme_zh}",
                ]
            ),
            title="Generated",
        )
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
