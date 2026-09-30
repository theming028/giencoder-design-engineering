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
"$NODE" "$AB" wait 2600 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/e104-chat.png" >/dev/null 2>&1
echo "== E1) chat 态 =="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104e.js)"
echo "== E2) 点「轨迹」 =="
"$NODE" "$AB" click '[data-r93-tab="trace"]' >/dev/null 2>&1
"$NODE" "$AB" wait 600 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/e104-trace.png" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104e.js)"
