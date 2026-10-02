#!/usr/bin/env bash
# r109 第十五拍 · 真机取证（单页 conversation，四条一起验）
# ★ 铁律：stdout 一律重定向（**禁接管道** —— 守护进程让管道永不 EOF）；
#   同一时刻只跑一个实测进程；整链一次 bash 内跑完。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
OUT="mg-work/r109/raw/l15"
mkdir -p "$OUT" "$TMP"
TS=$(date +%s%N)

"$NODE" "$CLI" close --all >"$TMP/l15-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/l15-set.log" 2>&1

"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >"$OUT/open.log" 2>&1
"$NODE" "$CLI" wait 2200 >"$TMP/l15-w0.log" 2>&1

# ---- 主探针（浅色 · 定稿态）
"$NODE" "$CLI" eval "$(cat "$EV/p-l15.js")" >"$OUT/light.json" 2>&1
echo "done light"

# ---- 暗色档
"$NODE" "$CLI" eval "(function(){document.documentElement.setAttribute('giencoder-theme','dark');return 'dark';})()" >"$TMP/l15-td.log" 2>&1
"$NODE" "$CLI" wait 1200 >"$TMP/l15-w1.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-l15.js")" >"$OUT/dark.json" 2>&1
echo "done dark"

"$NODE" "$CLI" eval "(function(){document.documentElement.removeAttribute('giencoder-theme');return 'light';})()" >"$TMP/l15-tl.log" 2>&1
"$NODE" "$CLI" wait 900 >"$TMP/l15-w2.log" 2>&1

"$NODE" "$CLI" close --all >"$TMP/l15-close2.log" 2>&1
echo "=== done · 产物 $OUT ==="
