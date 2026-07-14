---
name: latex2md
description: Convert LaTeX to Markdown using Pandoc
---

# LaTeX to Markdown Converter

使用 Pandoc 将 LaTeX 文件转换为 Markdown。

## 安装依赖

```bash
yum install pandoc  # CentOS/RHEL
# 或
apt install pandoc   # Debian/Ubuntu
```

## 使用方法

```bash
# 基本转换
pandoc input.tex -o output.md

# 保留数学公式为 LaTeX 格式
pandoc input.tex -o output.md --standalone

# 转换为 Markdown + 数学公式 (使用 mathjax)
pandoc input.tex -o output.md -t markdown+tex_math_dollars
```

## 示例

```bash
# 转换单个文件
pandoc paper.tex -o paper.md

# 批量转换 (在 zsh/bash 4+)
for f in *.tex; do pandoc "$f" -o "${f%.tex}.md"; done
```

## 输出选项

- `-o output.md` - 指定输出文件
- `--wrap=none` - 不自动换行
- `--standalone` - 保留完整文档结构
- `-t markdown+tex_math_dollars` - Markdown 保留 LaTeX 数学公式

## 注意事项

- Pandoc 会尝试保留文档结构，但复杂 LaTeX 可能需要手动调整
- 数学公式默认转为 Unicode 或 LaTeX 语法
- 图片需要确保路径正确
