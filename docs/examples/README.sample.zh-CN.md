# Sample Repo

<p align="center"><strong>用一个 CLI 把 Markdown 笔记构建成小型静态站点。</strong></p>
<p align="center">一次编写，快速预览，干净发布。</p>
<p align="center">
  <img src="https://img.shields.io/github/stars/OWNER/REPO?style=flat-square" alt="GitHub Stars">
  <img src="https://img.shields.io/badge/license-MIT-2563eb?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/language-Python-6b7280?style=flat-square" alt="Language">
</p>
<p align="center">
  简体中文 | <a href="./README.sample.md">English</a>
</p>

## 功能
- 将 Markdown 笔记转换为静态站点。
- 本地预览生成结果。
- 保持流程易于脚本化和扩展。

## 安装
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## 使用
```bash
sample-repo build ./notes
sample-repo serve
```

## 命令行
| 命令 | 说明 |
| --- | --- |
| `sample-repo build <path>` | 从笔记目录构建静态页面。 |
| `sample-repo serve` | 本地预览生成结果。 |

## 路线图
- 增加主题定制能力。
- 增加增量构建。

## 贡献
欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并在合适时补充测试或文档。

## 许可证
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
