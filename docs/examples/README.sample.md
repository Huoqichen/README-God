# Sample Repo

<p align="center"><strong>Turn Markdown notes into a small static site from one CLI.</strong></p>
<p align="center">Write once. Preview fast. Ship clean docs.</p>
<p align="center">
  <img src="https://img.shields.io/github/stars/OWNER/REPO?style=flat-square" alt="GitHub Stars">
  <img src="https://img.shields.io/badge/license-MIT-2563eb?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/language-Python-6b7280?style=flat-square" alt="Language">
</p>
<p align="center">
  <a href="./README.sample.zh-CN.md">简体中文</a> | English
</p>

## Features
- Convert Markdown notes into a static site.
- Preview the generated site locally.
- Keep the workflow scriptable and easy to extend.

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Usage
```bash
sample-repo build ./notes
sample-repo serve
```

## CLI
| Command | Description |
| --- | --- |
| `sample-repo build <path>` | Build static pages from a notes directory. |
| `sample-repo serve` | Preview the generated site locally. |

## Roadmap
- Add theme customization.
- Add incremental builds.

## Contributing
Issues and pull requests are welcome. Keep changes focused and include tests or docs when relevant.

## License
MIT

## Star History

<p align="center">
<a href="https://www.star-history.com/?repos=OWNER%2FREPO&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=OWNER/REPO&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=OWNER/REPO&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=OWNER/REPO&type=date&legend=top-left" />
 </picture>
</a>
</p>
