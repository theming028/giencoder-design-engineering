#!/usr/bin/env bash
# r109 第一拍 · 探针 C：④稿2（输入态）+ Ctrl 联动 + 稿3（锚点）
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

run eval "$(cat "$EV/p109b.js")" > "$EV/b1.json" 2>&1
echo "---- b1（稿2 输入态读数）----"; cat "$EV/b1.json"
run screenshot ".td-elnote" "$RAW/b-note-typing.png" > "$EV/z5.log" 2>&1
run screenshot ".td-brw" "$RAW/b-brw-typing.png" > "$EV/z6.log" 2>&1

run eval "$(cat "$EV/p109c.js")" > "$EV/c1.json" 2>&1
echo "---- c1（Ctrl 联动读数）----"; cat "$EV/c1.json"
run screenshot ".td-elnote" "$RAW/c-note-ctrl.png" > "$EV/z8.log" 2>&1

run eval "$(cat "$EV/p109d.js")" > "$EV/d1.json" 2>&1
echo "---- d1（提交 + 稿3 锚点读数）----"; cat "$EV/d1.json"
run screenshot ".td-brw" "$RAW/d-brw-anchored.png" > "$EV/z10.log" 2>&1
run screenshot ".td-elnote" "$RAW/d-note-reopen.png" > "$EV/z11.log" 2>&1
ls -la "$RAW"/b-*.png "$RAW"/c-*.png "$RAW"/d-*.png
