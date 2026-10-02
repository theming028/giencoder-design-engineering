#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
run set viewport 1440 900 > "$EV/zt1.log" 2>&1
run open "$URL" > "$EV/zt2.log" 2>&1
run wait 3800 > "$EV/zt3.log" 2>&1
run eval "$(cat "$EV/p-regen4.js")" > "$EV/t1.json" 2>&1
echo "==== t1 ===="; cat "$EV/t1.json"
run screenshot "#umzoom" "$RAW/real-umeta-zoom.png" > "$EV/zt4.log" 2>&1
ls -la "$RAW"/real-umeta-zoom.png
