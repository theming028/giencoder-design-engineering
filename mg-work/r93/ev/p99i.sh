#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 1800
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p99i.js)"
"$NODE" "$AB" wait 600
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r99v-skillbig.png"
"$NODE" "$AB" close --all >/dev/null 2>&1
