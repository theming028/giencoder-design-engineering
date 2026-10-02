#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
run set viewport 1440 900 > "$EV/z1.log" 2>&1
run open "$URL" > "$EV/z2.log" 2>&1
run wait 3800 > "$EV/z3.log" 2>&1
run eval "$(cat "$EV/p109e.js")" > "$EV/e1.json" 2>&1
echo "---- e1（--ui-fs=18 档 + 200 压顶）----"; cat "$EV/e1.json"
run screenshot ".td-elnote" "$RAW/e-note-18px.png" > "$EV/z5.log" 2>&1
ls -la "$RAW"/e-*.png
