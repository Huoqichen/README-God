"""Repository scanning and config loading."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re
import subprocess
import tomllib
from urllib.parse import unquote
from typing import Any

import yaml

from readme_god.i18n import DEFAULT_CONTRIBUTING, DEFAULT_DESCRIPTION, DEFAULT_LANGUAGES, DEFAULT_LICENSE, DEFAULT_ROADMAP, DEFAULT_TAGLINE


CONFIG_NAME = ".readme-god.yml"


@dataclass(slots=True)
class CommandInfo:
    name: str
    description: str


@dataclass(slots=True)
class ReadmeInsights:
    title: str | None = None
    description: str | None = None
    tagline: str | None = None
    features: list[str] = field(default_factory=list)
    installation: list[str] = field(default_factory=list)
    usage: list[str] = field(default_factory=list)
    commands: list[CommandInfo] = field(default_factory=list)
    roadmap: list[str] = field(default_factory=list)
    contributing: str | None = None
    badge_label: str | None = None
    badge_values: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RepositoryContext:
    title: str
    description: str
    description_zh: str
    tagline: str
    tagline_zh: str
    languages: list[str]
    badge_label: str
    badge_values: list[str]
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
    readme_en = _load_readme_insights(repo_path / "README.md")
    readme_zh = _load_readme_insights(repo_path / "docs" / "README.zh-CN.md")

    title = _pick_title(repo_path, config, pyproject, package_json, readme_en)
    description = _pick_description(config, pyproject, package_json, readme_en)
    description_zh = _pick_description_zh(config, description, readme_zh)
    tagline = _pick_tagline(config, readme_en)
    tagline_zh = _pick_tagline_zh(config, tagline, readme_zh)
    detected_languages = _detect_languages(repo_path)
    languages = _pick_languages(config, detected_languages, readme_en)
    badge_label, badge_values = _pick_badge(config, languages, readme_en)
    repo_slug = str(config.get("repo_slug") or git_slug or "OWNER/REPO")
    cli_name = str(config.get("cli_name") or _detect_cli_name(pyproject, package_json) or "").strip() or None
    features = _pick_features(repo_path, config, cli_name, readme_en, languages)
    features_zh = _pick_features_zh(config, features, readme_zh)
    installation = _pick_installation(config, pyproject, package_json, readme_en)
    usage = _pick_usage(config, cli_name, pyproject, readme_en)
    commands = _pick_commands(config, cli_name, readme_en, usage)
    commands_zh = _pick_commands_zh(config, commands, readme_zh)
    roadmap_en, roadmap_zh = _pick_roadmap(config, readme_en, readme_zh)
    contributing_en, contributing_zh = _pick_contributing(config, readme_en, readme_zh)
    license_name = _pick_license(repo_path, config, pyproject)

    return RepositoryContext(
        title=title,
        description=description,
        description_zh=description_zh,
        tagline=tagline,
        tagline_zh=tagline_zh,
        languages=languages,
        badge_label=badge_label,
        badge_values=badge_values,
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
    readme = _load_readme_insights(repo_path / "README.md")
    title = _pick_title(repo_path, {}, pyproject, package_json, readme)
    description = _pick_description({}, pyproject, package_json, readme)
    cli_name = _detect_cli_name(pyproject, package_json) or "your-cli"
    repo_slug = _detect_git_slug(repo_path) or "OWNER/REPO"

    data = {
        "title": title,
        "description": description,
        "description_zh": "",
        "tagline": "",
        "tagline_zh": "",
        "languages": [],
        "badge_label": "",
        "badge_values": [],
        "repo_slug": repo_slug,
        "cli_name": cli_name,
        "features": [
            "Replace this list with 3-5 concrete project capabilities.",
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
                "description": "Show commands and options.",
            }
        ],
        "commands_zh": [],
        "roadmap": [
            "Add your next meaningful milestone.",
        ],
        "roadmap_zh": [],
        "contributing": "Issues and pull requests are welcome. Keep changes focused and tested.",
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


def _pick_title(repo_path: Path, config: dict[str, Any], pyproject: dict[str, Any], package_json: dict[str, Any], readme: ReadmeInsights) -> str:
    if config.get("title"):
        return str(config["title"]).strip()
    if readme.title:
        return readme.title
    project = pyproject.get("project", {})
    if project.get("name"):
        return _humanize_name(str(project["name"]))
    if package_json.get("name"):
        return _humanize_name(str(package_json["name"]))
    return _humanize_name(repo_path.name)


def _pick_description(config: dict[str, Any], pyproject: dict[str, Any], package_json: dict[str, Any], readme: ReadmeInsights) -> str:
    if config.get("description"):
        return str(config["description"]).strip()
    if readme.description:
        return readme.description
    project = pyproject.get("project", {})
    if project.get("description"):
        return str(project["description"]).strip()
    if package_json.get("description"):
        return str(package_json["description"]).strip()
    return DEFAULT_DESCRIPTION["en"]


def _pick_description_zh(config: dict[str, Any], description: str, readme: ReadmeInsights) -> str:
    if config.get("description_zh"):
        return str(config["description_zh"]).strip()
    if readme.description:
        return readme.description
    mapping = {
        "Generate clean bilingual GitHub README files from a repository.": "从仓库信息生成简洁、双语、适合 GitHub 的 README。",
        "Generate GitHub-ready bilingual READMEs from any repository.": "从任意仓库生成适合 GitHub 的双语 README。",
        "Generate beautiful GitHub READMEs automatically.": "自动生成漂亮的 GitHub README。",
        DEFAULT_DESCRIPTION["en"]: DEFAULT_DESCRIPTION["zh-CN"],
    }
    return mapping.get(description, description)


def _pick_tagline(config: dict[str, Any], readme: ReadmeInsights) -> str:
    if config.get("tagline"):
        return str(config["tagline"]).strip()
    if readme.tagline:
        return readme.tagline
    return DEFAULT_TAGLINE["en"]


def _pick_tagline_zh(config: dict[str, Any], tagline: str, readme: ReadmeInsights) -> str:
    if config.get("tagline_zh"):
        return str(config["tagline_zh"]).strip()
    if readme.tagline:
        return readme.tagline
    mapping = {
        "One command. Professional README.": "一条命令，专业 README。",
        DEFAULT_TAGLINE["en"]: DEFAULT_TAGLINE["zh-CN"],
    }
    return mapping.get(tagline, tagline)


def _pick_languages(config: dict[str, Any], detected_languages: list[str], readme: ReadmeInsights) -> list[str]:
    configured = _string_list(config.get("languages"))
    if configured:
        return configured
    if readme.badge_values:
        return readme.badge_values
    if detected_languages:
        return detected_languages[:3]
    return DEFAULT_LANGUAGES


def _pick_badge(config: dict[str, Any], languages: list[str], readme: ReadmeInsights) -> tuple[str, list[str]]:
    if readme.badge_label and readme.badge_values:
        return readme.badge_label, readme.badge_values
    return "language", languages


def _pick_features(
    repo_path: Path,
    config: dict[str, Any],
    cli_name: str | None,
    readme: ReadmeInsights,
    languages: list[str],
) -> list[str]:
    configured = _string_list(config.get("features"))
    if configured:
        return configured
    if readme.features:
        return readme.features[:6]

    features: list[str] = []
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


def _pick_features_zh(config: dict[str, Any], features: list[str], readme: ReadmeInsights) -> list[str]:
    configured = _string_list(config.get("features_zh"))
    if configured:
        return configured
    if readme.features:
        return readme.features[:6]
    return [translate_feature(item) for item in features]


def _pick_installation(config: dict[str, Any], pyproject: dict[str, Any], package_json: dict[str, Any], readme: ReadmeInsights) -> list[str]:
    configured = _string_list(config.get("installation"))
    if configured:
        return configured
    if readme.installation:
        return readme.installation

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


def _pick_usage(config: dict[str, Any], cli_name: str | None, pyproject: dict[str, Any], readme: ReadmeInsights) -> list[str]:
    configured = _string_list(config.get("usage"))
    if configured:
        return configured
    if readme.usage:
        return readme.usage
    if cli_name:
        return [f"{cli_name} --help"]
    project = pyproject.get("project", {})
    if project.get("name"):
        module_name = str(project["name"]).replace("-", "_")
        return [f"python -m {module_name}"]
    return ["Add a concrete usage example in .readme-god.yml."]


def _pick_commands(config: dict[str, Any], cli_name: str | None, readme: ReadmeInsights, usage: list[str]) -> list[CommandInfo]:
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
    if readme.commands:
        return readme.commands[:3]
    inferred = _infer_commands_from_usage(usage, cli_name)
    if inferred:
        return inferred
    if cli_name:
        return [CommandInfo(name=f"{cli_name} --help", description="Show available commands and options.")]
    return [CommandInfo(name="N/A", description="No dedicated CLI entry point detected.")]


def _pick_commands_zh(config: dict[str, Any], commands: list[CommandInfo], readme: ReadmeInsights) -> list[CommandInfo]:
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
    if readme.commands:
        return [CommandInfo(name=command.name, description=translate_command_description(command.description)) for command in readme.commands[:3]]
    return [CommandInfo(name=command.name, description=translate_command_description(command.description)) for command in commands]


def _pick_roadmap(config: dict[str, Any], readme: ReadmeInsights, readme_zh: ReadmeInsights) -> tuple[list[str], list[str]]:
    roadmap = _string_list(config.get("roadmap"))
    if roadmap:
        zh = [translate_roadmap_item(item) for item in roadmap]
        return roadmap, zh
    if readme.roadmap:
        zh = readme_zh.roadmap[: len(readme.roadmap)] if readme_zh.roadmap else [translate_roadmap_item(item) for item in readme.roadmap]
        return readme.roadmap, zh
    return DEFAULT_ROADMAP["en"], DEFAULT_ROADMAP["zh-CN"]


def _pick_contributing(config: dict[str, Any], readme: ReadmeInsights, readme_zh: ReadmeInsights) -> tuple[str, str]:
    contributing = str(config.get("contributing", "")).strip()
    if contributing:
        return contributing, translate_contributing(contributing)
    if readme.contributing:
        zh = readme_zh.contributing or translate_contributing(readme.contributing)
        return readme.contributing, zh
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
    if not seen:
        if (repo_path / "pyproject.toml").exists():
            seen.append("Python")
        elif (repo_path / "package.json").exists():
            seen.append("JavaScript")
    return seen


def _load_readme_insights(path: Path) -> ReadmeInsights:
    if not path.exists():
        return ReadmeInsights()

    content = path.read_text(encoding="utf-8")
    sections = _split_markdown_sections(content)
    title = _extract_title(content)
    hero_description, hero_tagline = _extract_hero(content)
    badge_label, badge_values = _extract_badge(content)

    installation_body = sections.get("installation") or sections.get("安装") or ""
    usage_body = sections.get("usage") or sections.get("用法") or sections.get("使用") or sections.get("demo") or sections.get("演示") or ""
    features_body = sections.get("features") or sections.get("特性") or sections.get("功能") or ""
    roadmap_body = sections.get("roadmap") or sections.get("current status") or sections.get("当前状态") or ""
    contributing_body = sections.get("contributing") or sections.get("贡献") or ""

    usage_lines = _extract_usage_lines(usage_body, limit=4)
    feature_lines = _extract_bullets(features_body, limit=5)

    return ReadmeInsights(
        title=title,
        description=hero_description,
        tagline=hero_tagline,
        features=feature_lines,
        installation=_extract_shell_code_lines(installation_body, limit=6),
        usage=usage_lines,
        commands=_infer_commands_from_usage(usage_lines, None),
        roadmap=_extract_roadmap_items(roadmap_body),
        contributing=_extract_first_paragraph(contributing_body),
        badge_label=badge_label,
        badge_values=badge_values,
    )


def _split_markdown_sections(content: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", content))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        name = match.group(1).strip().lower()
        sections[name] = content[start:end].strip()
    return sections


def _extract_title(content: str) -> str | None:
    h1_match = re.search(r"<h1>(.*?)</h1>", content, flags=re.IGNORECASE | re.DOTALL)
    if h1_match:
        return _strip_html(h1_match.group(1)).strip()
    markdown_match = re.search(r"(?m)^#\s+(.+?)\s*$", content)
    if markdown_match:
        return markdown_match.group(1).strip()
    return None


def _extract_hero(content: str) -> tuple[str | None, str | None]:
    paragraphs = re.findall(r"<p>(.*?)</p>", content, flags=re.IGNORECASE | re.DOTALL)
    description: str | None = None
    tagline: str | None = None
    for raw in paragraphs:
        if "<img" in raw.lower():
            continue
        text = _strip_html(raw).strip()
        if not text:
            continue
        if description is None:
            description = text
            continue
        tagline = text
        break

    if description:
        return description, tagline

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    prose_lines = [line for line in lines if not line.startswith("#") and not line.startswith("-") and "<img" not in line and "<a " not in line]
    if prose_lines:
        description = _strip_html(prose_lines[0])
        tagline = _strip_html(prose_lines[1]) if len(prose_lines) > 1 else None
    return description, tagline


def _extract_badge(content: str) -> tuple[str | None, list[str]]:
    match = re.search(r"badge/(platform|language)-([^\"?]+)", content, flags=re.IGNORECASE)
    if not match:
        return None, []
    label = match.group(1).lower()
    raw_value = match.group(2).split("?", maxsplit=1)[0]
    value = unquote(raw_value.rsplit("-", maxsplit=1)[0])
    parts = [part.strip() for part in value.split("|") if part.strip()]
    return label, parts


def _extract_bullets(content: str, limit: int) -> list[str]:
    bullets = [match.group(1).strip() for match in re.finditer(r"(?m)^\s*-\s+(.*)$", content)]
    bullets = [item for item in bullets if item and not item.endswith(":") and not item.endswith("：")]
    return bullets[:limit]


def _extract_code_lines(content: str, limit: int) -> list[str]:
    lines: list[str] = []
    for block in re.findall(r"```(?:\w+)?\n(.*?)```", content, flags=re.DOTALL):
        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line or line in lines:
                continue
            lines.append(line)
            if len(lines) >= limit:
                return lines
    return lines


def _extract_shell_code_lines(content: str, limit: int) -> list[str]:
    lines: list[str] = []
    for language, block in _extract_code_blocks(content):
        if language not in {"bash", "sh", "shell", ""}:
            continue
        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line or line in lines:
                continue
            lines.append(line)
            if len(lines) >= limit:
                return lines
    return lines or _extract_code_lines(content, limit)


def _extract_usage_lines(content: str, limit: int) -> list[str]:
    for language, block in _extract_code_blocks(content):
        if language and language not in {"bash", "sh", "shell"}:
            continue
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines:
            return lines[:limit]
    return _extract_code_lines(content, limit)


def _extract_code_blocks(content: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for match in re.finditer(r"```(\w+)?\n(.*?)```", content, flags=re.DOTALL):
        language = (match.group(1) or "").strip().lower()
        blocks.append((language, match.group(2)))
    return blocks


def _extract_roadmap_items(content: str) -> list[str]:
    preferred = re.search(r"Still good next upgrades:\s*(.*)", content, flags=re.IGNORECASE | re.DOTALL)
    if preferred:
        return _extract_bullets(preferred.group(1), limit=4)
    preferred_zh = re.search(r"仍然值得继续增强：\s*(.*)", content, flags=re.DOTALL)
    if preferred_zh:
        return _extract_bullets(preferred_zh.group(1), limit=4)
    return _extract_bullets(content, limit=4)


def _extract_first_paragraph(content: str) -> str | None:
    if not content.strip():
        return None
    stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    for paragraph in re.split(r"\n\s*\n", stripped):
        text = _strip_html(paragraph).strip()
        if text and not text.startswith("-"):
            normalized = " ".join(text.split())
            normalized = normalized.removesuffix(":").removesuffix("：")
            normalized = re.sub(r"\binclude[s]?$", "", normalized).strip()
            normalized = re.sub(r"包括$", "", normalized).strip()
            return normalized
    return None


def _infer_commands_from_usage(usage: list[str], cli_name: str | None) -> list[CommandInfo]:
    commands: list[CommandInfo] = []
    for line in usage[:3]:
        if line.endswith(":") or line.isupper():
            continue
        description = "Run the project."
        if "--help" in line:
            description = "Show available commands and options."
        elif "--branch" in line:
            description = "Analyze a specific branch."
        elif "--json-out" in line or "--mermaid-out" in line:
            description = "Export analysis artifacts."
        elif "https://github.com/" in line:
            description = "Analyze a GitHub repository."
        elif cli_name and line.startswith(cli_name):
            description = "Run the main CLI flow."
        commands.append(CommandInfo(name=line, description=description))
    return commands


def _strip_html(text: str) -> str:
    cleaned = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    return " ".join(cleaned.split())


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
        "Improve repo signal detection.": "改进仓库特征识别能力。",
        "Add more template customization points.": "增加更多模板定制点。",
    }
    return mapping.get(text, text)


def translate_contributing(text: str) -> str:
    mapping = {
        "Issues and pull requests are welcome. Keep changes small, tested, and documented.": "欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并补充必要的测试与文档。",
        "Issues and pull requests are welcome. Keep changes focused and include tests or docs when relevant.": "欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并在合适时补充测试或文档。",
        "Issues and pull requests are welcome. Keep changes focused and tested.": "欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并补充测试。",
    }
    return mapping.get(text, text)


def translate_feature(text: str) -> str:
    mapping = {
        "Scan project metadata and infer concise README sections.": "扫描项目元信息并推断简洁的 README 结构。",
        "Generate English and Simplified Chinese README files together.": "同时生成英文与简体中文 README 文件。",
        "Keep output template-driven, readable, and easy to customize.": "使用模板驱动输出，方便阅读和定制。",
        "Scan repo metadata and infer a clean README structure.": "扫描仓库元信息并推断清晰的 README 结构。",
        "Generate README.md and docs/README.zh-CN.md together.": "同时生成 README.md 和 docs/README.zh-CN.md。",
        "Keep output concise, template-driven, and easy to refine.": "输出简洁、模板化，便于继续调整。",
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
        "Show commands and options.": "显示命令与选项。",
        "No dedicated CLI entry point detected.": "未检测到独立的命令行入口。",
        "Create a starter .readme-god.yml in the target repository.": "在目标仓库中创建一个起始版 .readme-god.yml 配置文件。",
        "Scan the current repository and write bilingual README files.": "扫描当前仓库并写出双语 README 文件。",
        "Scan a specific repository path.": "扫描指定仓库路径。",
        "Create a starter .readme-god.yml.": "创建起始版 .readme-god.yml。",
        "Generate bilingual README files for the current repository.": "为当前仓库生成双语 README。",
        "Generate bilingual README files for a specific repository path.": "为指定仓库路径生成双语 README。",
        "Analyze a GitHub repository.": "分析一个 GitHub 仓库。",
    }
    return mapping.get(text, text)
