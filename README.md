# README-God

English | [简体中文](./docs/README.zh-CN.md)

<p align="center"><strong>Generate beautiful GitHub READMEs automatically.</strong></p>
<p align="center">One command. Professional README.</p>
<p align="center">
  <a href="https://github.com/Huoqichen/README-God/stargazers"><img src="https://img.shields.io/github/stars/Huoqichen/README-God?style=flat-square" alt="GitHub Stars"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-2563eb?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-6b7280?style=flat-square" alt="Platform">
</p>
<p align="center">
  <a href="./docs/README.zh-CN.md">简体中文</a> | 繁體中文 | Español | Deutsch | Français | 日本語
</p>

## Features
- Scan repo metadata and infer a clean README structure.
- Generate README.md and docs/README.zh-CN.md together.
- Keep output concise, template-driven, and easy to refine.

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
| Command | Description |
| --- | --- |
| `readme-god init` | Create a starter .readme-god.yml. |
| `readme-god generate` | Generate bilingual README files for the current repository. |
| `readme-god generate --repo .` | Generate bilingual README files for a specific repository path. |

## Roadmap
- Improve repo signal detection.
- Add more template customization points.

## Contributing
Issues and pull requests are welcome. Keep changes focused and tested.

## License
MIT

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=Huoqichen/README-God&type=Date)
