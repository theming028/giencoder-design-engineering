#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/mg-work/r109/ev/tmp/regen5.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
run set viewport 1440 900 > "$EV/zw1.log" 2>&1
run open "$URL" > "$EV/zw2.log" 2>&1
run wait 500 > "$EV/zw3.log" 2>&1
run screenshot "#f252" "$RAW/fix-regen-252.png" > "$EV/zw4.log" 2>&1
run screenshot "#f14" "$RAW/fix-regen-14.png" > "$EV/zw5.log" 2>&1
ls -la "$RAW"/fix-regen-*.png
