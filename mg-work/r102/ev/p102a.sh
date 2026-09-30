#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"; H="${2:-900}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" "$H" >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1800 >/dev/null 2>&1
echo "===== 静态读数 ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p102a.js)"
echo
echo "===== 截图 ====="
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102a-${W}.png" >/dev/null 2>&1
echo "  saved mg-work/r102/raw/p102a-${W}.png"
