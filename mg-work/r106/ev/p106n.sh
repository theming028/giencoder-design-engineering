#!/usr/bin/env bash
# r106 ④c 判据：五档位 x 预览栏 关/开，量四列相对 .r93-pane 的内间距
set -u
REPO=/e/GienCoder/giencoder-design-engineering
NODE=/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe
AB=/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js
PAGE="file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html"
JS="$REPO/mg-work/r106/ev/p106n.js"
LOG="$REPO/mg-work/r106/ev/p106n.log"

: > "$LOG"
for band in 1280 1370 1440 1920 2560; do
  for state in closed open; do
    "$NODE" "$AB" set viewport "$band" 900 >/dev/null 2>&1
    "$NODE" "$AB" open "$PAGE?v=$(date +%s%N)" >/dev/null 2>&1
    "$NODE" "$AB" wait 2600 >/dev/null 2>&1
    if [ "$state" = "open" ]; then
      "$NODE" "$AB" click '[data-r93-browse]' >/dev/null 2>&1
      "$NODE" "$AB" wait 900 >/dev/null 2>&1
    fi
    "$NODE" "$AB" eval "$(cat "$JS")" >> "$LOG" 2>&1
    echo "" >> "$LOG"
  done
done
echo "=== p106n DONE ==="
