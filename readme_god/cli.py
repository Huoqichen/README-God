"""Typer-based CLI for README-God."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from readme_god.generator import generate_readmes
from readme_god.preview import preview_repository
from readme_god.scanner import CONFIG_NAME, build_init_config


app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Generate GitHub-ready README.md and docs/README.zh-CN.md from a repository.",
    rich_markup_mode="markdown",
    context_settings={"help_option_names": ["-h", "--help"]},
)
console = Console()


def _resolve_repo_argument(repo: Path | None, repo_option: Path | None) -> Path:
    if repo is not None and repo_option is not None and repo.resolve() != repo_option.resolve():
        console.print("[red]REPO and --repo must point to the same directory.[/red]")
        raise typer.Exit(code=1)
    return (repo_option or repo or Path(".")).resolve()


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
    repo: Path | None = typer.Argument(
        None,
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        metavar="[REPO]",
    ),
    repo_option: Path | None = typer.Option(
        None,
        "--repo",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Repository to scan. Same as the positional REPO argument.",
    ),
) -> None:
    """Generate README.md and docs/README.zh-CN.md."""
    repo_path = _resolve_repo_argument(repo, repo_option)
    generated = generate_readmes(repo_path)
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


@app.command(short_help="Clone a repo and build a local preview.")
def preview(
    github_repo_url: str = typer.Argument(..., help="GitHub repository URL to preview."),
    out: Path = typer.Option(
        Path("preview"),
        "--out",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Output directory for the cloned repo and preview page.",
    ),
) -> None:
    """Clone a GitHub repository, generate README files, and build a local preview."""
    try:
        preview_files = preview_repository(github_repo_url, out)
    except RuntimeError as exc:
        console.print(f"[red]Preview failed:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(
        Panel.fit(
            "\n".join(
                [
                    f"Cloned: {preview_files.repository}",
                    f"Wrote: {preview_files.readme_en}",
                    f"Wrote: {preview_files.readme_zh}",
                    f"Open:  {preview_files.html_preview}",
                ]
            ),
            title="Preview Ready",
        )
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
