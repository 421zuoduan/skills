---
name: zotero-iclr-recommender
description: |
  基于用户的 Zotero 论文库分析研究兴趣，然后从 ICLR 2026 会议论文中筛选并推荐最相关的论文。
  适用于：用户想要根据自己的 Zotero 文献库获得 ICLR 2026 会议论文个性化推荐。
  触发条件：用户提到 "ICLR 2026"、"论文推荐"、"基于 Zotero 推荐"、"我感兴趣的论文" 等。
---

# Zotero + ICLR 2026 论文推荐系统

## 概述

本 skill 从用户的 Zotero 论文库提取研究兴趣，然后与 ICLR 2026 会议论文进行智能匹配，输出个性化推荐结果。

## 前提条件

1. **Zotero 信息**：
   - User ID
   - API Key
   
2. **搜索 API**：
   - Tavily API Key（用于搜索 ICLR 2026 论文列表）

## 执行流程

### 步骤 1：读取 Zotero 库

运行 `scripts/fetch_zotero.py` 获取用户论文库：

```bash
python scripts/fetch_zotero.py --user-id YOUR_USER_ID --api-key YOUR_API_KEY
```

输出：`data/zotero_papers.json`

### 步骤 2：建立兴趣画像

分析 Zotero 论文，提取：
- 核心研究主题
- 高频关键词
- 方法论偏好
- 任务类型偏好
- 最近兴趣漂移

### 步骤 3：搜索 ICLR 2026 论文

使用 Tavily 搜索 ICLR 2026 论文列表：

```bash
python scripts/fetch_iclr.py
```

参考数据源：
- https://papercopilot.com/paper-list/iclr-paper-list/iclr-2026-paper-list/
- https://www.paperdigest.org/2026/02/iclr-2026-papers-highlights/
- https://iclr.cc/virtual/2026/papers.html

### 步骤 4：匹配与排序

运行匹配脚本：

```bash
python scripts/match_and_rank.py
```

### 步骤 5：输出结果

输出结构化推荐结果，包含：
- 兴趣画像总结
- Top 20 推荐论文
- 每篇论文的推荐理由、关联论文、阅读建议

## 输出格式

详见 [references/output_template.md](references/output_template.md)

## 注意事项

- 如果缺少 Zotero 认证信息，提示用户提供
- 如果 Tavily API 不可用，尝试其他搜索渠道
- 优先使用大模型进行兴趣分析和论文匹配
