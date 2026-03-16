"""Repository scanning and config loading."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re
import subprocess
import tomllib
from typing import Any

import yaml

from readme_god.i18n import DEFAULT_CONTRIBUTING, DEFAULT_DESCRIPTION, DEFAULT_LICENSE, DEFAULT_ROADMAP


CONFIG_NAME = ".readme-god.yml"


@dataclass(slots=True)
class CommandInfo:
    name: str
    description: str


@dataclass(slots=True)
class RepositoryContext:
    title: str
    description: str
    description_zh: str
    repo_slug: str
    cli_name: str | None
    features: list[str]
    features_zh: list[str]
    installation: list[str]
    usage: list[str]
    commands: list[CommandInfo]
    commands_zh: list[CommandInfo]
    roadmap_en: list[str]
    roadmap_zh: list[str]
    contributing_en: str
    contributing_zh: str
    license_name: str
    output_repo: Path
    detected_languages: list[str] = field(default_factory=list)


def load_config(repo_path: Path) -> dict[str, Any]:
    config_path = repo_path / CONFIG_NAME
    if not config_path.exists():
        return {}
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{CONFIG_NAME} must contain a mapping at the top level.")
    return data


def scan_repository(repo_path: Path) -> RepositoryContext:
    repo_path = repo_path.resolve()
    config = load_config(repo_path)
    pyproject = _load_pyproject(repo_path)
    package_json = _load_package_json(repo_path)
    git_slug = _detect_git_slug(repo_path)

    title = _pick_title(repo_path, config, pyproject, package_json)
    description = _pick_description(config, pyproject, package_json)
    description_zh = _pick_description_zh(config, description)
    repo_slug = str(config.get("repo_slug") or git_slug or "OWNER/REPO")
    cli_name = str(config.get("cli_name") or _detect_cli_name(pyproject, package_json) or "").strip() or None
    features = _pick_features(repo_path, config, cli_name)
    features_zh = _pick_features_zh(config, features)
    installation = _pick_installation(config, pyproject, package_json)
    usage = _pick_usage(config, cli_name, pyproject)
    commands = _pick_commands(config, cli_name)
    commands_zh = _pick_commands_zh(config, commands)
    roadmap_en, roadmap_zh = _pick_roadmap(config)
    contributing_en, contributing_zh = _pick_contributing(config)
    license_name = _pick_license(repo_path, config, pyproject)
    detected_languages = _detect_languages(repo_path)

    return RepositoryContext(
        title=title,
        description=description,
        description_zh=description_zh,
        repo_slug=repo_slug,
        cli_name=cli_name,
        features=features,
        features_zh=features_zh,
        installation=installation,
        usage=usage,
        commands=commands,
        commands_zh=commands_zh,
        roadmap_en=roadmap_en,
        roadmap_zh=roadmap_zh,
        contributing_en=contributing_en,
        contributing_zh=contributing_zh,
        license_name=license_name,
        output_repo=repo_path,
        detected_languages=detected_languages,
    )


def build_init_config(repo_path: Path) -> str:
    repo_path = repo_path.resolve()
    pyproject = _load_pyproject(repo_path)
    package_json = _load_package_json(repo_path)
    title = _pick_title(repo_path, {}, pyproject, package_json)
    description = _pick_description({}, pyproject, package_json)
    cli_name = _detect_cli_name(pyproject, package_json) or "your-cli"
    repo_slug = _detect_git_slug(repo_path) or "OWNER/REPO"

    data = {
        "title": title,
        "description": description,
        "description_zh": "",
        "repo_slug": repo_slug,
        "cli_name": cli_name,
        "features": [
            "Replace this list with the 3-5 most useful project capabilities.",
        ],
        "features_zh": [],
        "installation": [
            "python -m venv .venv",
            ".venv\\Scripts\\activate",
            "pip install -e .",
        ],
        "usage": [
            f"{cli_name} --help",
        ],
        "commands": [
            {
                "name": f"{cli_name} --help",
                "description": "Show available commands and options.",
            }
        ],
        "commands_zh": [],
        "roadmap": [
            "Add your next meaningful milestone here.",
        ],
        "roadmap_zh": [],
        "contributing": "Issues and pull requests are welcome. Keep changes small and well tested.",
        "contributing_zh": "",
        "license": _pick_license(repo_path, {}, pyproject),
    }
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def _load_pyproject(repo_path: Path) -> dict[str, Any]:
    pyproject_path = repo_path / "pyproject.toml"
    if not pyproject_path.exists():
        return {}
    return tomllib.loads(pyproject_path.read_text(encoding="utf-8"))


def _load_package_json(repo_path: Path) -> dict[str, Any]:
    package_json_path = repo_path / "package.json"
    if not package_json_path.exists():
        return {}
    return json.loads(package_json_path.read_text(encoding="utf-8"))


def _pick_title(repo_path: Path, config: dict[str, Any], pyproject: dict[str, Any], package_json: dict[str, Any]) -> str:
    if config.get("title"):
        return str(config["title"]).strip()
    project = pyproject.get("project", {})
    if project.get("name"):
        return _humanize_name(str(project["name"]))
    if package_json.get("name"):
        return _humanize_name(str(package_json["name"]))
    return _humanize_name(repo_path.name)


def _pick_description(config: dict[str, Any], pyproject: dict[str, Any], package_json: dict[str, Any]) -> str:
    if config.get("description"):
        return str(config["description"]).strip()
    project = pyproject.get("project", {})
    if project.get("description"):
        return str(project["description"]).strip()
    if package_json.get("description"):
        return str(package_json["description"]).strip()
    return DEFAULT_DESCRIPTION["en"]


def _pick_description_zh(config: dict[str, Any], description: str) -> str:
    if config.get("description_zh"):
        return str(config["description_zh"]).strip()
    mapping = {
        "Generate clean bilingual GitHub README files from a repository.": "从仓库信息生成简洁、双语、适合 GitHub 的 README。",
        DEFAULT_DESCRIPTION["en"]: DEFAULT_DESCRIPTION["zh-CN"],
    }
    return mapping.get(description, description)


def _pick_features(repo_path: Path, config: dict[str, Any], cli_name: str | None) -> list[str]:
    configured = _string_list(config.get("features"))
    if configured:
        return configured

    features: list[str] = []
    languages = _detect_languages(repo_path)
    if languages:
        features.append(f"Built with {', '.join(languages[:3])}.")
    if cli_name:
        features.append(f"Provides a CLI entry point via `{cli_name}`.")
    if (repo_path / "tests").exists():
        features.append("Includes a test suite for safer iteration.")
    if (repo_path / ".github" / "workflows").exists():
        features.append("Ships with CI workflow definitions.")
    if (repo_path / "docs").exists():
        features.append("Keeps project documentation close to the codebase.")
    if not features:
        features.append("Structured for straightforward local development and review.")
    return features[:5]


def _pick_features_zh(config: dict[str, Any], features: list[str]) -> list[str]:
    configured = _string_list(config.get("features_zh"))
    if configured:
        return configured
    return [translate_feature(item) for item in features]


def _pick_installation(config: dict[str, Any], pyproject: dict[str, Any], package_json: dict[str, Any]) -> list[str]:
    configured = _string_list(config.get("installation"))
    if configured:
        return configured

    project = pyproject.get("project", {})
    if project.get("name"):
        package_name = str(project["name"])
        return [
            "python -m venv .venv",
            ".venv\\Scripts\\activate",
            f"pip install -e .  # installs {package_name}",
        ]
    if package_json.get("name"):
        return ["npm install"]
    return ["Clone the repository.", "Install the project dependencies."]


def _pick_usage(config: dict[str, Any], cli_name: str | None, pyproject: dict[str, Any]) -> list[str]:
    configured = _string_list(config.get("usage"))
    if configured:
        return configured
    if cli_name:
        return [f"{cli_name} --help"]
    project = pyproject.get("project", {})
    if project.get("name"):
        module_name = str(project["name"]).replace("-", "_")
        return [f"python -m {module_name}"]
    return ["Add a concrete usage example in .readme-god.yml."]


def _pick_commands(config: dict[str, Any], cli_name: str | None) -> list[CommandInfo]:
    raw_commands = config.get("commands")
    commands: list[CommandInfo] = []

    if isinstance(raw_commands, list):
        for item in raw_commands:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "")).strip()
            description = str(item.get("description", "")).strip()
            if name and description:
                commands.append(CommandInfo(name=name, description=description))

    if commands:
        return commands
    if cli_name:
        return [CommandInfo(name=f"{cli_name} --help", description="Show available commands and options.")]
    return [CommandInfo(name="N/A", description="No dedicated CLI entry point detected.")]


def _pick_commands_zh(config: dict[str, Any], commands: list[CommandInfo]) -> list[CommandInfo]:
    raw_commands = config.get("commands_zh")
    localized: list[CommandInfo] = []

    if isinstance(raw_commands, list):
        for item in raw_commands:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "")).strip()
            description = str(item.get("description", "")).strip()
            if name and description:
                localized.append(CommandInfo(name=name, description=description))

    if localized:
        return localized
    return [CommandInfo(name=command.name, description=translate_command_description(command.description)) for command in commands]


def _pick_roadmap(config: dict[str, Any]) -> tuple[list[str], list[str]]:
    roadmap = _string_list(config.get("roadmap"))
    if roadmap:
        zh = [translate_roadmap_item(item) for item in roadmap]
        return roadmap, zh
    return DEFAULT_ROADMAP["en"], DEFAULT_ROADMAP["zh-CN"]


def _pick_contributing(config: dict[str, Any]) -> tuple[str, str]:
    contributing = str(config.get("contributing", "")).strip()
    if contributing:
        return contributing, translate_contributing(contributing)
    return DEFAULT_CONTRIBUTING["en"], DEFAULT_CONTRIBUTING["zh-CN"]


def _pick_license(repo_path: Path, config: dict[str, Any], pyproject: dict[str, Any]) -> str:
    if config.get("license"):
        return str(config["license"]).strip()
    project = pyproject.get("project", {})
    license_field = project.get("license")
    if isinstance(license_field, dict) and license_field.get("text"):
        return str(license_field["text"]).strip()
    if (repo_path / "LICENSE").exists() or (repo_path / "LICENSE.txt").exists():
        return DEFAULT_LICENSE["en"]
    return "Proprietary"


def _detect_cli_name(pyproject: dict[str, Any], package_json: dict[str, Any]) -> str | None:
    scripts = pyproject.get("project", {}).get("scripts", {})
    if isinstance(scripts, dict) and scripts:
        return str(next(iter(scripts.keys())))
    bin_entry = package_json.get("bin")
    if isinstance(bin_entry, dict) and bin_entry:
        return str(next(iter(bin_entry.keys())))
    return None


def _detect_git_slug(repo_path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None

    if result.returncode != 0:
        return None
    return _slug_from_remote(result.stdout.strip())


def _slug_from_remote(remote: str) -> str | None:
    ssh_match = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", remote)
    if ssh_match:
        return ssh_match.group(1)
    return None


def _detect_languages(repo_path: Path) -> list[str]:
    extensions = {
        ".py": "Python",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".js": "JavaScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
    }
    seen: list[str] = []
    for path in repo_path.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".") and part not in {".github"} for part in path.parts):
            continue
        language = extensions.get(path.suffix)
        if language and language not in seen:
            seen.append(language)
    return seen


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            result.append(text)
    return result


def _humanize_name(name: str) -> str:
    chunks = re.split(r"[-_]+", name.strip())
    return " ".join(chunk.capitalize() for chunk in chunks if chunk)


def translate_roadmap_item(text: str) -> str:
    mapping = {
        "Improve framework detection for more repository types.": "增强对更多仓库类型和框架的识别能力。",
        "Add custom section hooks for project-specific templates.": "增加面向项目定制模板的扩展节能力。",
        "Refine project metadata and examples.": "补充更完整的项目元信息与示例。",
        "Expand automation, tests, or release tooling where needed.": "按需扩展自动化、测试或发布工具。",
    }
    return mapping.get(text, text)


def translate_contributing(text: str) -> str:
    mapping = {
        "Issues and pull requests are welcome. Keep changes small, tested, and documented.": "欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并补充必要的测试与文档。",
        "Issues and pull requests are welcome. Keep changes focused and include tests or docs when relevant.": "欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并在合适时补充测试或文档。",
    }
    return mapping.get(text, text)


def translate_feature(text: str) -> str:
    mapping = {
        "Scan project metadata and infer concise README sections.": "扫描项目元信息并推断简洁的 README 结构。",
        "Generate English and Simplified Chinese README files together.": "同时生成英文与简体中文 README 文件。",
        "Keep output template-driven, readable, and easy to customize.": "使用模板驱动输出，方便阅读和定制。",
        "Built with Python.": "使用 Python 构建。",
        "Includes a test suite for safer iteration.": "包含测试套件，便于安全迭代。",
        "Keeps project documentation close to the codebase.": "将文档与代码放在一起维护。",
        "Structured for straightforward local development and review.": "为直接的本地开发与评审做了清晰组织。",
    }
    if text.startswith("Provides a CLI entry point via `") and text.endswith("`."):
        cli_name = text.removeprefix("Provides a CLI entry point via `").removesuffix("`.")
        return f"提供 `{cli_name}` 命令行入口。"
    if text.startswith("Built with "):
        return text.replace("Built with ", "使用 ").replace(".", " 构建。")
    return mapping.get(text, text)


def translate_command_description(text: str) -> str:
    mapping = {
        "Show available commands and options.": "显示可用命令与选项。",
        "No dedicated CLI entry point detected.": "未检测到独立的命令行入口。",
        "Create a starter .readme-god.yml in the target repository.": "在目标仓库中创建一个起始版 .readme-god.yml 配置文件。",
        "Scan the current repository and write bilingual README files.": "扫描当前仓库并写出双语 README 文件。",
        "Scan a specific repository path.": "扫描指定仓库路径。",
    }
    return mapping.get(text, text)
