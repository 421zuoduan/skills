---
name: file-share
description: 将服务器上的文件通过公网 URL 分享给用户。用户想从服务器下载文件时触发此技能。启动本地 HTTP 服务 + bore 隧道生成公网下载链接。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3", "curl"] },
      "install": [
        { "id": "bore", "kind": "binary", "name": "bore", "url": "https://github.com/ekzhang/bore/releases/download/v0.5.0/bore-v0.5.0-x86_64-unknown-linux-musl.tar.gz" }
      ]
    }
  }
---

# File Share - 文件分享技能

将服务器上的文件通过公网 HTTP URL 分享出去。

## 工作流程

1. 接收文件路径（绝对路径）
2. 在本地启动 HTTP 服务（随机可用端口）
3. 通过 bore.pub 创建公网隧道
4. 返回公网下载链接给用户
5. 静默保持隧道存活（10 分钟超时）

## 使用方式

用户说"下载文件"、"分享文件"、"给我文件链接"等时触发。

### 输入

- 文件路径（绝对路径，如 `/path/to/file.pptx`）

### 输出

- 公网可访问的下载链接（格式：`http://bore.pub:<port>/<filename>`）
- 告知用户链接有效期（10 分钟）

## 脚本

`share-file.sh` - 一键分享文件

```bash
bash /path/to/skills/file-share/share-file.sh <文件绝对路径>
```

返回：公网 URL

## 实现细节

- HTTP 服务：Python `http.server`，服务于文件所在目录
- 隧道工具：bore（连接 bore.pub）
- 端口范围：48400-48500（随机选择可用端口）
- 超时清理：10 分钟后自动杀死进程

## 依赖

- bore 二进制：`/tmp/bore`（由脚本自动下载，如缺失）
- Python3：http.server 模块
- curl：检测 bore.pub 连通性
