"""Language labels and lightweight localized text."""

from __future__ import annotations

SECTION_TITLES = {
    "en": {
        "features": "Features",
        "installation": "Installation",
        "usage": "Usage",
        "cli": "CLI",
        "roadmap": "Roadmap",
        "contributing": "Contributing",
        "license": "License",
        "star_history": "Star History",
    },
    "zh-CN": {
        "features": "功能",
        "installation": "安装",
        "usage": "使用",
        "cli": "命令行",
        "roadmap": "路线图",
        "contributing": "贡献",
        "license": "许可证",
        "star_history": "Star History",
    },
}

DEFAULT_DESCRIPTION = {
    "en": "A concise README generated from repository signals.",
    "zh-CN": "根据仓库信息生成的简洁 README。",
}

DEFAULT_ROADMAP = {
    "en": [
        "Refine project metadata and examples.",
        "Expand automation, tests, or release tooling where needed.",
    ],
    "zh-CN": [
        "补充更完整的项目元信息与示例。",
        "按需扩展自动化、测试或发布流程。",
    ],
}

DEFAULT_CONTRIBUTING = {
    "en": "Issues and pull requests are welcome. Keep changes focused and include tests or docs when relevant.",
    "zh-CN": "欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并在合适时补充测试或文档。",
}

DEFAULT_LICENSE = {
    "en": "MIT",
    "zh-CN": "MIT",
}

