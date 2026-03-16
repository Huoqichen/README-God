[English](./README.sample.md) | [简体中文](./README.sample.zh-CN.md)

# Sample Repo

A tiny CLI app for turning Markdown notes into static pages.

## Features
- Built with Python.
- Provides a CLI entry point via `sample-repo`.
- Includes a test suite for safer iteration.

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Usage
```bash
sample-repo build ./notes
```

## CLI
- `sample-repo build <path>`: Build static pages from a notes directory.
- `sample-repo serve`: Preview the generated site locally.

## Roadmap
- Add theme customization.
- Add incremental builds.

## Contributing
Issues and pull requests are welcome. Keep changes focused and include tests or docs when relevant.

## License
MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=OWNER/REPO&type=Date)](https://star-history.com/#OWNER/REPO&Date)

