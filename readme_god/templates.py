"""Template loading helpers."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


ROOT_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
PACKAGE_TEMPLATE_DIR = Path(__file__).resolve().parent / "template_assets"


def _template_search_paths() -> list[str]:
    paths: list[str] = []
    if ROOT_TEMPLATE_DIR.exists():
        paths.append(str(ROOT_TEMPLATE_DIR))
    if PACKAGE_TEMPLATE_DIR.exists():
        paths.append(str(PACKAGE_TEMPLATE_DIR))
    return paths


@lru_cache(maxsize=1)
def get_environment() -> Environment:
    return Environment(
        loader=FileSystemLoader(_template_search_paths()),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )


def render_template(template_name: str, context: dict[str, object]) -> str:
    template = get_environment().get_template(template_name)
    return template.render(**context).strip() + "\n"
