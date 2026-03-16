# Sample Repo

English | [简体中文](./README.sample.zh-CN.md)

<p align="center"><strong>Turn Markdown notes into a small static site from one CLI.</strong></p>
<p align="center">Write once. Preview fast. Ship clean docs.</p>

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

![Star History Chart](https://api.star-history.com/svg?repos=OWNER/REPO&type=Date)
