#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1500 >/dev/null 2>&1
for TOP in 3325 3300; do
  "$NODE" "$AB" eval "var s=document.querySelector('.r93-conv-host .r93-scroll');s.scrollTop=$TOP;String(s.scrollTop)" >/dev/null 2>&1
  "$NODE" "$AB" wait 300 >/dev/null 2>&1
  "$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fade2-$TOP.png" >/dev/null 2>&1
  echo "   top=$TOP 已拍"
done
