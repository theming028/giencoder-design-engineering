#!/usr/bin/env bash
# r109 第十六拍 · 真机取证：产物卡点开右栏 + 独立页签
set -u
cd /e/GienCoder/giencoder-design-engineering

AB="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
ABJS="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
RAW="mg-work/r109/raw/l16"
TS=$(date +%s)
mkdir -p "$RAW"

"$AB" "$ABJS" close --all >/dev/null 2>&1
"$AB" "$ABJS" set viewport 1440 900 > "$RAW/_vp.txt" 2>&1
"$AB" "$ABJS" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" > "$RAW/_open.txt" 2>&1
"$AB" "$ABJS" wait 2200 > /dev/null 2>&1

"$AB" "$ABJS" eval "$(cat $EV/p-l16.js)" > "$RAW/light.json" 2>&1

# 切暗色
"$AB" "$ABJS" eval "document.documentElement.setAttribute('giencoder-theme','dark');'ok'" > /dev/null 2>&1
"$AB" "$ABJS" wait 500 > /dev/null 2>&1
"$AB" "$ABJS" eval "$(cat $EV/p-l16.js)" > "$RAW/dark.json" 2>&1

# 截图（浅色态，重开一次保证干净）
"$AB" "$ABJS" eval "document.documentElement.removeAttribute('giencoder-theme');'ok'" > /dev/null 2>&1
"$AB" "$ABJS" wait 300 > /dev/null 2>&1
"$AB" "$ABJS" screenshot "$RAW/pane-artgrid.png" > /dev/null 2>&1

echo "=== DONE $RAW ==="
ls -la "$RAW"
