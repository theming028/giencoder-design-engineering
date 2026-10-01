#!/usr/bin/env bash
# 压扁假设验证
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
ev openRv; step wait 900
ev expandAll; step wait 700
echo "--- 压扁判据"
ev squash
step screenshot "$RAW/u3-$TAG-squash.png"
echo done
