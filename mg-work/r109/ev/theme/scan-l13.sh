#!/usr/bin/env bash
# r109 第十三拍 · 两条真机取证（单页 conversation）
# ★ 铁律：stdout 一律重定向（禁接管道）；同一时刻只跑一个实测进程。
# ★ 时序抓取：open 之后**不等**，立刻按多个时间点采样（150 / 500 / 900 / 1400 / 2600ms），
#   看 `.r93-sk` 是否在文档里、`data-r93-app` 是否 ready、`.zd-host` display 各是什么。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
OUT="mg-work/r109/raw/l13"
mkdir -p "$OUT" "$TMP"
TS=$(date +%s%N)

"$NODE" "$CLI" close --all >"$TMP/l13-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/l13-set.log" 2>&1

# ---- 时序抓取：一次 open，多次采样
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >"$OUT/open.log" 2>&1
for w in 150 350 300 400 600 1000; do
  "$NODE" "$CLI" wait $w >"$TMP/l13-w-$w.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-l13.js")" >"$OUT/t-$w.json" 2>&1
  echo "done t=$w"
done

# ---- 定稿态静态量测（浅色）
"$NODE" "$CLI" eval "$(cat "$EV/p-l13.js")" >"$OUT/static-light.json" 2>&1
echo "done static/light"

# ---- 暗色档
"$NODE" "$CLI" eval "(function(){document.documentElement.setAttribute('giencoder-theme','dark');return 'dark';})()" >"$TMP/l13-td.log" 2>&1
"$NODE" "$CLI" wait 1200 >"$TMP/l13-w2.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-l13.js")" >"$OUT/static-dark.json" 2>&1
echo "done static/dark"

"$NODE" "$CLI" eval "(function(){document.documentElement.removeAttribute('giencoder-theme');return 'light';})()" >"$TMP/l13-tl.log" 2>&1
"$NODE" "$CLI" wait 1200 >"$TMP/l13-w3.log" 2>&1

"$NODE" "$CLI" close --all >"$TMP/l13-close2.log" 2>&1
echo "=== done · 产物 $OUT ==="
