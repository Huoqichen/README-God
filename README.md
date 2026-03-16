[English](./README.md) | [简体中文](./docs/README.zh-CN.md)

# README-God

Generate clean bilingual GitHub README files from a repository.

## Features
- Scan project metadata and infer concise README sections.
- Generate English and Simplified Chinese README files together.
- Keep output template-driven, readable, and easy to customize.

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Usage
```bash
readme-god init
readme-god generate --repo .
```

## CLI
- `readme-god init`: Create a starter .readme-god.yml in the target repository.
- `readme-god generate`: Scan the current repository and write bilingual README files.
- `readme-god generate --repo .`: Scan a specific repository path.

## Roadmap
- Improve framework detection for more repository types.
- Add custom section hooks for project-specific templates.

## Contributing
Issues and pull requests are welcome. Keep changes small, tested, and documented.

## License
MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Huoqichen/README-God&type=Date)](https://star-history.com/#Huoqichen/README-God&Date)
