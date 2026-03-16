[English](../README.md) | [简体中文](./README.zh-CN.md)

# README-God

从仓库信息生成简洁、双语、适合 GitHub 的 README。

## 功能
- 扫描项目元信息并推断简洁的 README 结构。
- 同时生成英文与简体中文 README 文件。
- 使用模板驱动输出，方便阅读和定制。

## 安装
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## 使用
```bash
readme-god init
readme-god generate --repo .
```

## 命令行
- `readme-god init`: 在目标仓库中创建一个起始版 .readme-god.yml 配置文件。
- `readme-god generate`: 扫描当前仓库并写出双语 README 文件。
- `readme-god generate --repo .`: 扫描指定仓库路径。

## 路线图
- 增强对更多仓库类型和框架的识别能力。
- 增加面向项目定制模板的扩展节能力。

## 贡献
欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并补充必要的测试与文档。

## 许可证
MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Huoqichen/README-God&type=Date)](https://star-history.com/#Huoqichen/README-God&Date)
