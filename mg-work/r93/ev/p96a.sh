#!/usr/bin/env bash
# r96 侦查：会话详情页 5 条需求的现状读数
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 1500
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p96a.js)"
"$NODE" "$AB" screenshot "" mg-work/r93/raw/r96-before-full.png
