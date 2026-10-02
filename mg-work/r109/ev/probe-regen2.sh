#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
run set viewport 1440 900 > "$EV/zq1.log" 2>&1
run open "$URL" > "$EV/zq2.log" 2>&1
run wait 3800 > "$EV/zq3.log" 2>&1
run eval "$(cat "$EV/p-regen.js")" > "$EV/q1.json" 2>&1
echo "==== q1 ===="; cat "$EV/q1.json"
run screenshot "#regenzoom" "$RAW/real-regen-zoom.png" > "$EV/zq4.log" 2>&1
ls -la "$RAW"/real-regen-zoom.png
