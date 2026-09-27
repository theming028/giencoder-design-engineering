#!/usr/bin/env bash
# 推送 main（本机到 GitHub 偶发 408/502/443 隧道故障）—— 固定配方 + 多轮重试
# 判据：输出里出现 "main -> main" 才算成功；不要用管道 + break 误判。
set -u
cd /e/GienCoder/giencoder-design-engineering
DEST="${1:-mg-work/r35/push.log}"
: > "$DEST"
for i in $(seq 1 20); do
  echo "===== attempt $i =====" >> "$DEST"
  OUT="$(git -c http.version=HTTP/1.1 push origin main 2>&1)"
  echo "$OUT" >> "$DEST"
  if printf '%s' "$OUT" | grep -q 'main -> main'; then
    echo "PUSH_OK attempt=$i" >> "$DEST"
    echo "PUSH_OK"
    exit 0
  fi
  case "$OUT" in
    *"up-to-date"*) echo "PUSH_OK (already up-to-date) attempt=$i" >> "$DEST"; echo "PUSH_OK"; exit 0 ;;
  esac
  sleep 6
done
echo "PUSH_FAIL" >> "$DEST"
echo "PUSH_FAIL"
