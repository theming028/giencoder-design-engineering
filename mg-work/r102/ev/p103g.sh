#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"; H="${2:-900}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" "$H" >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1
echo "===== G1) 静态读数（①②③④⑤⑥） ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103g.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/g103-${W}.png" >/dev/null 2>&1
echo "  shot g103-${W}.png"
echo
echo "===== G2) 折叠逐帧（fold0 收起 / fold0 展开 / fold4 收起） ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103f.js)" >/dev/null 2>&1
"$NODE" "$AB" eval "window.__run(0,'c0')" >/dev/null 2>&1
"$NODE" "$AB" wait 1200 >/dev/null 2>&1
"$NODE" "$AB" eval "window.__run(0,'e0','expand')" >/dev/null 2>&1
"$NODE" "$AB" wait 1200 >/dev/null 2>&1
"$NODE" "$AB" eval "window.__run(4,'c4')" >/dev/null 2>&1
"$NODE" "$AB" wait 1200 >/dev/null 2>&1
"$NODE" "$AB" eval "JSON.stringify(window.__rec)"
echo
echo "===== G3) composer 聚焦态截图 ====="
"$NODE" "$AB" click "textarea" >/dev/null 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/g103-focus-${W}.png" >/dev/null 2>&1
echo "  shot g103-focus-${W}.png"
