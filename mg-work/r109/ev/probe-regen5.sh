#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/mg-work/r109/ev/tmp/regen3.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
run set viewport 1440 900 > "$EV/zu1.log" 2>&1
run open "$URL" > "$EV/zu2.log" 2>&1
run wait 500 > "$EV/zu3.log" 2>&1
run screenshot "#v14" "$RAW/v1-regen-14.png" > "$EV/zu4.log" 2>&1
run screenshot "#v252" "$RAW/v1-regen-252.png" > "$EV/zu5.log" 2>&1
ls -la "$RAW"/v1-regen-*.png
