#!/usr/bin/env bash
# r96 取证：气泡 240 上限内滚（用足量内容触发）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 1500
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p96c.js)"
# 截图：速率行 + 气泡
"$NODE" "$AB" screenshot ".r93-rateline" mg-work/r93/raw/r96-rate.png
"$NODE" "$AB" screenshot ".r93-bub" mg-work/r93/raw/r96-bub.png
