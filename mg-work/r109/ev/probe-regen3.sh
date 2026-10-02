#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/mg-work/r109/ev/tmp/regen2.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
run set viewport 1440 900 > "$EV/zs1.log" 2>&1
run open "$URL" > "$EV/zs2.log" 2>&1
run wait 500 > "$EV/zs3.log" 2>&1
run screenshot "#new14" "$RAW/new-regen-14.png" > "$EV/zs4.log" 2>&1
run screenshot "#new20" "$RAW/new-regen-280.png" > "$EV/zs5.log" 2>&1
ls -la "$RAW"/new-regen-*.png
