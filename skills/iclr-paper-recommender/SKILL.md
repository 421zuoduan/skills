---
name: iclr-paper-recommender
description: |
  从 Zotero 论文库读取用户的研究兴趣，然后从 OpenReview 抓取 ICLR 2026 会议论文，
  进行智能匹配和个性化推荐。适用于：用户想要基于自己的 Zotero 文献库获得 ICLR 2026 论文推荐。
  触发条件：用户提到 "ICLR 2026"、"论文推荐"、"Zotero"、"学术论文推荐" 等。
---

# ICLR 2026 论文智能推荐系统

## 概述

本 skill 从用户的 Zotero 论文库提取研究兴趣，然后与 ICLR 2026 会议论文进行智能匹配，输出个性化推荐结果。

## 输入要求

### Zotero 信息（以下任选其一）
1. **私有库**：Zotero User ID + API Key
2. **公开库**：Zotero 公开 collection 链接
3. **导出链接**：Atom/RSS/Bib/JSON 导出链接

### ICLR 2026 数据
- 来源：OpenReview (https://openreview.net/group?id=ICLR.cc/2026/Conference)
- 优先保留：Accept (Oral) / Accept (Poster) / Conditional Accept

---

## 执行流程

### 步骤 1：读取 Zotero 库

按优先级尝试以下方式：
1. Zotero Web API（需要 user ID + API Key）
2. 公开 Zotero 页面/collection
3. 导出链接（Atom/RSS/Bib/JSON）
4. 若均不可用，提示用户无法读取私有库

提取字段：
- title, authors, year, venue, abstract, tags
- collections, notes, dateAdded, dateModified
- url, doi, arxiv id

### 步骤 2：建立兴趣画像

基于 Zotero 库分析：
- 核心研究主题
- 高频关键词
- 方法论偏好
- 任务类型偏好
- 最近兴趣漂移
- 与已有工作的连续性

**注意**：如果使用大模型 API 进行分析，在 SKILL.md 中说明需要用户提供 API Key。

### 步骤 3：抓取 ICLR 2026 论文

从 OpenReview 获取：
- 标题、作者、接收状态
- 摘要、关键词
- 研究主题、方法类别
- 代码/项目页链接

### 步骤 4：匹配与排序

评分维度：
- 主题相关性
- 方法相关性
- 与已有工作的连续性
- 增量价值
- 新颖性

### 步骤 5：输出结构化结果

```
A. 兴趣画像总结
B. 推荐 Top 20 论文（每篇包含推荐等级、分数、推荐理由）
C. 补充列表：
   - 和我最匹配但不一定热门
   - 热门但与我相关性一般
   - 跨领域黑马论文
D. 阅读计划
```

---

## 输出格式模板

### 每篇论文的输出格式

```
[推荐等级] S / A / B
[论文标题]
[作者]
[接收状态]
[主题标签]
[推荐分数] 0-100

[为什么推荐]
3-6 句话说明与用户兴趣的关联

[关联到我库中的已有论文]
3-8 篇最相关 Zotero 条目

[阅读建议]
精读 / 略读 / 先收藏
```

---

## 大模型集成说明

### 当前模式
使用 skill 执行者的内置大模型能力进行兴趣分析和论文匹配。

### 后续扩展
用户会提供大模型 API Key，届时可：
- 使用更强大的模型进行深度分析
- 批量处理更多论文
- 提取更精细的标签和特征

---

## 辅助脚本

### scripts/zotero_fetch.py
从 Zotero API 获取用户论文库

### scripts/iclr_scrape.py
从 OpenReview 抓取 ICLR 2026 论文

### scripts/matcher.py
基于兴趣画像进行论文匹配和排序

（如果需要，请告诉我创建这些脚本）
