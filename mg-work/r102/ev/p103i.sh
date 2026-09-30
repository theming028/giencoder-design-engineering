#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 2560 1400 >/dev/null 2>&1
TS=$(date +%s)
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1
echo "===== I1) 2560 浅色 ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103i.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/i103-2560.png" >/dev/null 2>&1
echo
echo "===== I2) 1440 暗色档 ====="
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){document.documentElement.setAttribute('giencoder-theme','dark');return 'dark';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 600 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103i.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/i103-dark-1440.png" >/dev/null 2>&1
echo "  shot i103-dark-1440.png"
