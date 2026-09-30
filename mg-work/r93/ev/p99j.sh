#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 600 300
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/mg-work/r93/ev/icontest.html?a=$(date +%s)"
"$NODE" "$AB" wait 900
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r99v-icontest.png"
"$NODE" "$AB" close --all >/dev/null 2>&1
