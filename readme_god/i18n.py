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
    "en": "Generate a GitHub-ready README from a repository.",
    "zh-CN": "从仓库生成适合 GitHub 的 README。",
}

DEFAULT_ROADMAP = {
    "en": [
        "Improve repo signal detection.",
        "Add more template customization points.",
    ],
    "zh-CN": [
        "改进仓库特征识别能力。",
        "增加更多模板定制点。",
    ],
}

DEFAULT_CONTRIBUTING = {
    "en": "Issues and pull requests are welcome. Keep changes focused and tested.",
    "zh-CN": "欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并补充测试。",
}

DEFAULT_LICENSE = {
    "en": "MIT",
    "zh-CN": "MIT",
}
