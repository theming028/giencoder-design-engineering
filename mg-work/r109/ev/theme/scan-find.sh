#!/usr/bin/env bash
# r109 第十一拍 · 单页「波点背景 + 顶栏 LOGO」DOM 侦察（浅暗双档）
# 用法：bash scan-find.sh settings [light]
# ★ 铁律：stdout 一律重定向（禁接管道）；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
PG="${1:-settings}"; THEME="${2:-light}"
OUT="mg-work/r109/raw/find11"
mkdir -p "$OUT" "$TMP"
TS=$(date +%s%N)

"$NODE" "$CLI" close --all >"$TMP/f-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/f-set.log" 2>&1
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/open-$PG.log" 2>&1
"$NODE" "$CLI" wait 4500 >"$TMP/f-w.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-find.js")" >"$OUT/init-$PG.log" 2>&1

for TH in light dark; do
  "$NODE" "$CLI" eval "window.__giTheme.set('$TH'); 'T'" >"$TMP/f-t-$TH.log" 2>&1
  "$NODE" "$CLI" wait 1400 >"$TMP/f-w-$TH.log" 2>&1
  "$NODE" "$CLI" eval "window.__find()" >"$OUT/$PG-$TH-dots.json" 2>&1
  "$NODE" "$CLI" eval "window.__logo()" >"$OUT/$PG-$TH-logo.json" 2>&1
  "$NODE" "$CLI" eval "window.__hdr()"  >"$OUT/$PG-$TH-hdr.json" 2>&1
  "$NODE" "$CLI" screenshot "$OUT/$PG-$TH.png" >"$TMP/f-shot-$TH.log" 2>&1
  echo "done $PG/$TH"
done

"$NODE" "$CLI" close --all >"$TMP/f-close2.log" 2>&1
echo "=== done · 产物 $OUT ==="
