#!/usr/bin/env bash
# r109 第一拍 · 探针 A：发现右栏/浏览器模块的进入方式
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"
RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }

run set viewport 1440 900 > "$EV/z1.log" 2>&1
run open "$URL" > "$EV/z2.log" 2>&1
run wait 3800 > "$EV/z3.log" 2>&1
run eval "$(cat "$EV/p109z.js")" > "$EV/z4.json" 2>&1
echo "---- z4 ----"
cat "$EV/z4.json"
