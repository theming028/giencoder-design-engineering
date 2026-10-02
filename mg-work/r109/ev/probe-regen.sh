#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/mg-work/r109/ev/tmp/regen.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
run set viewport 1440 900 > "$EV/zr1.log" 2>&1
run open "$URL" > "$EV/zr2.log" 2>&1
run wait 600 > "$EV/zr3.log" 2>&1
run screenshot "#a" "$RAW/cur-regen-14.png" > "$EV/zr4.log" 2>&1
run screenshot "#b" "$RAW/cur-regen-280.png" > "$EV/zr5.log" 2>&1
ls -la "$RAW"/cur-regen-*.png
