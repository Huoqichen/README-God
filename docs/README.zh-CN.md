# README-God

<p align="center"><strong>自动生成漂亮的 GitHub README。</strong></p>
<p align="center">一条命令，专业 README。</p>
<p align="center">
  <a href="https://github.com/Huoqichen/README-God/stargazers"><img src="https://img.shields.io/github/stars/Huoqichen/README-God?style=flat-square" alt="GitHub Stars"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/license-MIT-2563eb?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/language-Python-6b7280?style=flat-square" alt="Language">
</p>
<p align="center">
  简体中文 | <a href="../README.md">English</a>
</p>

## 功能
- 扫描仓库元信息并推断清晰的 README 结构。
- 同时生成 README.md 和 docs/README.zh-CN.md。
- 输出简洁、模板化，便于继续调整。

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
| 命令 | 说明 |
| --- | --- |
| `readme-god init` | 创建起始版 .readme-god.yml。 |
| `readme-god generate` | 为当前仓库生成双语 README。 |
| `readme-god generate --repo .` | 为指定仓库路径生成双语 README。 |

## 路线图
- 改进仓库特征识别能力。
- 增加更多模板定制点。

## 贡献
欢迎提交 Issue 和 Pull Request。请保持改动聚焦，并补充测试。

## 许可证
MIT

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=Huoqichen/README-God&type=Date)
