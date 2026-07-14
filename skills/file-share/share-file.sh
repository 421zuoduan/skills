#!/bin/bash
# File Share Script - 将文件通过公网 URL 分享
# 用法: bash share-file.sh <文件绝对路径>

set -e

FILE_PATH="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BORE_BIN="/tmp/bore"
BORE_LOG="/tmp/bore-share.log"
HTTP_LOG="/tmp/http-share.log"
TIMEOUT_SEC=600  # 10分钟

# 下载 bore（如果不存在）
install_bore() {
  if [[ ! -f "$BORE_BIN" ]]; then
    echo "[file-share] 正在下载 bore..." >&2
    curl -fsSL "https://github.com/ekzhang/bore/releases/download/v0.5.0/bore-v0.5.0-x86_64-unknown-linux-musl.tar.gz" \
      -o /tmp/bore.tar.gz
    tar -xzf /tmp/bore.tar.gz -C /tmp
    chmod +x "$BORE_BIN"
    rm -f /tmp/bore.tar.gz
    echo "[file-share] bore 安装完成" >&2
  fi
}

# 清理旧进程
cleanup() {
  echo "[file-share] 清理旧进程..." >&2
  pkill -f "python3 -m http.server.*484${STORAGE_ID:0:1}0" 2>/dev/null || true
  pkill -f "bore local.*484${STORAGE_ID:0:1}0" 2>/dev/null || true
}

# 找可用端口
find_port() {
  for i in {0..100}; do
    PORT=$((48400 + RANDOM % 100))
    if ! ss -tlnp 2>/dev/null | grep -q ":$PORT " && \
       ! nc -z localhost $PORT 2>/dev/null; then
      echo "$PORT"
      return 0
    fi
  done
  echo "48401"  # fallback
}

# 主流程
main() {
  if [[ -z "$FILE_PATH" ]]; then
    echo "用法: bash share-file.sh <文件绝对路径>" >&2
    exit 1
  fi

  if [[ ! -f "$FILE_PATH" ]]; then
    echo "[file-share] 错误：文件不存在: $FILE_PATH" >&2
    exit 1
  fi

  install_bore

  FILE_DIR="$(cd "$(dirname "$FILE_PATH")" && pwd)"
  FILENAME="$(basename "$FILE_PATH")"
  PORT=$(find_port)

  echo "[file-share] 启动 HTTP 服务 (端口 $PORT)..." >&2
  cd "$FILE_DIR"
  python3 -m http.server "$PORT" > "$HTTP_LOG" 2>&1 &
  HTTP_PID=$!
  sleep 1

  if ! kill -0 $HTTP_PID 2>/dev/null; then
    echo "[file-share] HTTP 服务启动失败" >&2
    cat "$HTTP_LOG" >&2
    exit 1
  fi

  echo "[file-share] 启动 bore 隧道..." >&2
  rm -f "$BORE_LOG"
  "$BORE_BIN" local "$PORT" --to bore.pub > "$BORE_LOG" 2>&1 &
  BORE_PID=$!

  # 等待 bore 连接成功
  REMOTE_PORT=""
  for i in {1..20}; do
    sleep 1
    if grep -q "listening at bore.pub" "$BORE_LOG" 2>/dev/null; then
      REMOTE_PORT=$(grep "listening at bore.pub" "$BORE_LOG" | grep -oP 'bore\.pub:\K\d+' | head -1)
      break
    fi
    # 检查 bore 是否还在运行
    if ! kill -0 $BORE_PID 2>/dev/null; then
      echo "[file-share] bore 连接失败" >&2
      cat "$BORE_LOG" >&2
      kill $HTTP_PID 2>/dev/null || true
      exit 1
    fi
  done

  if [[ -z "$REMOTE_PORT" ]]; then
    echo "[file-share] 无法获取 bore 公网端口" >&2
    cat "$BORE_LOG" >&2
    kill $HTTP_PID $BORE_PID 2>/dev/null || true
    exit 1
  fi

  URL="http://bore.pub:$REMOTE_PORT/$FILENAME"
  echo "[file-share] 文件: $FILENAME" >&2
  echo "[file-share] 目录: $FILE_DIR" >&2
  echo "[file-share] PID: HTTP=$HTTP_PID BORE=$BORE_PID" >&2
  echo "[file-share] 有效期: 10 分钟" >&2
  echo "" >&2

  # 输出下载链接（JSON 格式，方便程序解析）
  echo "===DOWNLOAD_URL==="
  echo "$URL"
  echo "===END==="

  # 10分钟后自动清理
  (
    sleep $TIMEOUT_SEC
    echo "[file-share] 超时清理..." >&2
    kill $HTTP_PID $BORE_PID 2>/dev/null || true
  ) &
  CLEANUP_PID=$!

  # 保持脚本运行
  wait $BORE_PID 2>/dev/null || true
  kill $CLEANUP_PID 2>/dev/null || true
  kill $HTTP_PID 2>/dev/null || true
}

main "$@"
