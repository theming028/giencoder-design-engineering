#!/usr/bin/env bash
# r108 第十九拍 · ② 对照实验（现状写法 vs 两步写法）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/r108v3.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"
step set viewport 1440 900
step wait 3800
echo "=== 对照实验 ==="
ev exp
step wait 2200
ev expRead
ev expReset
echo "done"
