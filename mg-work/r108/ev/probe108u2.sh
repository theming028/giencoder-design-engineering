#!/usr/bin/env bash
# 追加：内容超出时的滚动归属（视图高可调，默认 900）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"; RAW="$ROOT/mg-work/r108/raw"
TAG="${1:-before}"; VH="${2:-900}"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108u2.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"; step set viewport 1440 "$VH"; step wait 3800
echo "--- 走菜单开审查"
ev openRv; step wait 900
ev rvNow
echo "--- 全部 diff 展开"
ev expandAll; step wait 700
ev rvNow
echo "--- 真滚轮打给容器"
ev wheel; step wait 500
ev rvNow
step screenshot "$RAW/u2-$TAG-expand.png"
echo "done"
