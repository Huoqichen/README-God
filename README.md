# README-God

<p align="center"><strong>Generate beautiful GitHub READMEs automatically.</strong></p>
<p align="center">One command. Professional README.</p>
<p align="center">
  <a href="https://github.com/Huoqichen/README-God/stargazers"><img src="https://img.shields.io/github/stars/Huoqichen/README-God?style=flat-square" alt="GitHub Stars"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-2563eb?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/language-Python-6b7280?style=flat-square" alt="Language">
</p>
<p align="center">
  <a href="./docs/README.zh-CN.md">简体中文</a> | English
</p>

## Features
- Scan repo metadata and infer a clean README structure.
- Generate README.md and docs/README.zh-CN.md together.
- Clone a GitHub repo and open a polished local preview page.

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Usage
```bash
readme-god preview https://github.com/user/repo
readme-god generate .
open preview/index.html
```

## CLI
| Command | Description |
| --- | --- |
| `readme-god init` | Create a starter .readme-god.yml. |
| `readme-god generate` | Generate bilingual README files for the current repository. |
| `readme-god preview <github_repo_url>` | Clone a GitHub repository, generate README files, and build a local preview page. |

## Roadmap
- Improve repo signal detection.
- Add more template customization points.

## Contributing
Issues and pull requests are welcome. Keep changes focused and tested.

## License
MIT

## Star History

<p align="center">
<a href="https://www.star-history.com/?repos=Huoqichen%2FREADME-God&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Huoqichen/README-God&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Huoqichen/README-God&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Huoqichen/README-God&type=date&legend=top-left" />
 </picture>
</a>
</p>
