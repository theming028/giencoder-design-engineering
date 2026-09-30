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
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103f.js)"
echo "[fold0 收起]"; "$NODE" "$AB" eval "window.__run(0,'f0')"; "$NODE" "$AB" wait 1200 >/dev/null 2>&1
echo "[fold0 展开]"; "$NODE" "$AB" eval "window.__run(0,'f0b','expand')"; "$NODE" "$AB" wait 1200 >/dev/null 2>&1
echo "[fold11 嵌套 收起]"; "$NODE" "$AB" eval "window.__run(11,'f11')"; "$NODE" "$AB" wait 1200 >/dev/null 2>&1
echo "[fold10 大块 收起]"; "$NODE" "$AB" eval "window.__run(10,'f10')"; "$NODE" "$AB" wait 1200 >/dev/null 2>&1
"$NODE" "$AB" eval "JSON.stringify(window.__rec)"
