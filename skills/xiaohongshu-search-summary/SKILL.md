---
name: xiaohongshu-search-summary
description: "小红书搜索与内容整理工具。搜索小红书上的笔记、整理总结用户真实反馈、产品测评、避雷/种草/攻略等内容。"
---

# xiaohongshu-search-summary

搜索小红书内容并整理成结构化总结。依赖 `xiaohongshu-mcp` Docker 容器和 `mcporter` CLI。

## 前置条件

- Docker 容器 `xiaohongshu-mcp` 运行中（端口 18060）
- 已通过 `mcporter` 注册 MCP 服务 `xiaohongshu-mcp`
- 小红书账号已登录（登录态保存在 `/root/.openclaw/workspace/xiaohongshu-mcp/data/cookies.json`）

## 调用方式

使用 `mcporter call` 命令调用 MCP 工具：

```bash
# 搜索小红书内容
mcporter call xiaohongshu-mcp.search_feeds keyword="搜索关键词"

# 搜索并筛选
mcporter call xiaohongshu-mcp.search_feeds keyword="Ice Bartender" filters='{"sort_by":"最多点赞","note_type":"不限","publish_time":"不限"}'

# 获取笔记详情（含评论和互动数据）
mcporter call xiaohongshu-mcp.get_feed_detail feed_id="笔记ID" xsec_token="token"

# 检查登录状态
mcporter call xiaohongshu-mcp.check_login_status
```

## 触发规则

当用户的问题包含以下关键词时，优先调用此 skill：

| 关键词 | 触发场景 |
|---|---|
| 小红书、小红书上、XHS | 明确指定小红书平台 |
| 种草、避雷、测评 | 常见小红书内容类型 |
| 攻略、真实体验、用户反馈 | 需要用户真实评价 |
| 好用吗、怎么样、值得买吗 | 产品/服务咨询 |
| 推荐、分享、心得 | 经验分享类查询 |

## 搜索参数

- `keyword`：搜索关键词（必填）
- `filters`：筛选选项（可选）
  - `sort_by`：排序方式（综合/最新/最多点赞/最多评论/最多收藏）
  - `note_type`：笔记类型（不限/视频/图文）
  - `publish_time`：发布时间（不限/一天内/一周内/半年内）
  - `location`：位置（不限/同城/附近）
  - `search_scope`：搜索范围（不限/已看过/未看过/已关注）

## 搜索结果整理格式

### 输出结构

```
## 搜索结果：[搜索关键词]

### 📊 总览
- 搜索结果数量：X 条
- 搜索排序方式：[综合/最新/最多点赞]

### 🏆 高频观点总结
- 观点 1：概括核心发现（来源数量）
- 观点 2：概括核心发现（来源数量）
- 观点 3：概括核心发现（来源数量）

### 📝 代表性笔记
| 标题 | 作者 | 互动数据 | 核心内容 |
|---|---|---|---|
| ... | ... | 👍X 💬X ⭐X | ... |

### 💬 用户真实反馈汇总
- 正面反馈：
  - 反馈 1
  - 反馈 2
- 负面/争议反馈：
  - 反馈 1
  - 反馈 2
- 中立建议：
  - 建议 1

### ⚠️ 争议点或注意事项
- 争议点 1
- 注意事项 1

### 💡 可执行建议
- 建议 1
- 建议 2

### 🔗 参考来源
- [标题](小红书链接)
```

## 使用示例

### 用户提问
"帮我搜索小红书上关于 Mac 菜单栏管理软件 Ice 和 Bartender 的真实使用反馈"

### 执行步骤
1. 设置搜索关键词：`Ice Bartender 对比 Mac 菜单栏`
2. 搜索结果默认取前 10-20 条
3. 如需了解更多详情，对代表性笔记调用 `get_feed_detail` 获取互动数据和评论
4. 按上述格式整理总结

## 注意事项

1. **登录状态**：每次使用前建议先检查登录状态
2. **搜索频率**：避免高频搜索，间隔至少数秒
3. **xsec_token**：获取笔记详情时需要同时提供 feed_id 和 xsec_token
4. **风控提示**：如果搜索失败或返回空，可能是触发风控或登录过期
5. **不要编造数据**：所有信息必须来自搜索结果，不要自行补充

## 错误处理

### 搜索失败
```
❌ 搜索失败：[错误信息]
可能原因：
1. 登录已过期 → 重新登录
2. 触发风控 → 降低频率或更换关键词
3. 服务连接问题 → 检查 Docker 容器状态
```

### 登录过期
```
❌ 登录已过期
修复步骤：
1. 运行 `mcporter call xiaohongshu-mcp.get_login_qrcode` 获取二维码
2. 用小红书 App 扫码
3. 运行 `mcporter call xiaohongshu-mcp.check_login_status` 确认登录成功
```

### 容器未运行
```
❌ 连接失败
修复步骤：
1. 运行 `docker compose -f <path>/docker-compose.yml up -d`
2. 确认端口 18060 可访问：`curl http://localhost:18060/mcp`
```
