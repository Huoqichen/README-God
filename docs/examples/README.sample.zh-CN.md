[English](./README.sample.md) | [简体中文](./README.sample.zh-CN.md)

# Sample Repo

一个用于将 Markdown 笔记转换为静态页面的轻量 CLI 工具。

## 功能
- 使用 Python 构建。
- 提供 `sample-repo` 命令行入口。
- 包含测试套件，便于安全迭代。

## 安装
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## 使用
```bash
sample-repo build ./notes
```

## 命令行
- `sample-repo build <path>`: 从笔记目录构建静态页面。
- `sample-repo serve`: 本地预览生成结果。

## 路线图
- 增加主题定制能力。
- 增加增量构建。

## 贡献
欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并在合适时补充测试或文档。

## 许可证
MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=OWNER/REPO&type=Date)](https://star-history.com/#OWNER/REPO&Date)
