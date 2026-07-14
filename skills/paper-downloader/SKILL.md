---
name: paper-downloader
description: >
  批量下载学术论文并规范重命名。当用户提供论文标题列表、论文截图、或要求下载/搜索学术论文时触发。
  支持从 Semantic Scholar、OpenReview、PMLR、arXiv 多源级联下载，自动识别会议/期刊，pypdf 内容校验。
  触发词：下载论文、找论文、paper download、批量下载、论文列表。
---

# Paper Downloader

## 流程

1. **获取论文标题** — 用户直接给标题列表，或发图片用 OCR 提取
2. **写入标题文件** — 每行一个标题，保存到 `titles.txt`
3. **运行脚本** — 直接 exec，不要手动搜索

```bash
python3 {SKILL_DIR}/scripts/paper_downloader.py -f titles.txt -o downloaded_papers
```

4. **检查结果** — 脚本会输出成功/失败报告
5. **打包交付** — `zip -j papers.zip downloaded_papers/*.pdf`

## 关键规则

- **不要手动搜索论文** — 脚本已包含 SS/OpenReview/PMLR/arXiv 全部搜索逻辑
- **不要手动下载** — 脚本自动级联下载 + pypdf 首页校验
- **不要手动重命名** — 脚本自动 `[会议 年份] 标题.pdf` 或 `[arXiv_ID] 标题.pdf`
- **失败的论文** — 报告给用户，让用户确认标题是否正确

## 从图片提取标题

```bash
tesseract image.png stdout | grep -i "title\|paper"
```

或直接 OCR 全文后人工提取论文标题。

## 脚本能力

| 搜索源 | 用途 |
|--------|------|
| Semantic Scholar REST API | 精准/模糊搜索，获取 venue + year |
| OpenReview API v2 | 搜索会议论文 PDF |
| DBLP → PMLR | 搜索 PMLR proceedings PDF |
| arXiv API | 兜底搜索 + 下载 |

## 注意

- SS API 有限速（429），脚本已内置重试
- 大批量（>15篇）建议分批运行，避免限速
- 依赖：`pip install arxiv pypdf requests`
