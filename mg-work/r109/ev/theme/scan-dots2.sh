#!/usr/bin/env bash
# r109 第十一拍 · 波点精确侦察（多页 × 双档）
# 用法：bash scan-dots2.sh settings base conversation dev kanban req-kanban task-detail
# ★ 铁律：stdout 一律重定向（禁接管道）；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
OUT="mg-work/r109/raw/dots11"
mkdir -p "$OUT" "$TMP"
TS=$(date +%s%N)

PAGES="${*:-settings}"

"$NODE" "$CLI" close --all >"$TMP/d2-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/d2-set.log" 2>&1

for PG in $PAGES; do
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/open-$PG.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$TMP/d2-w-$PG.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-dots2.js")" >"$TMP/d2-init-$PG.log" 2>&1
  for TH in light dark; do
    "$NODE" "$CLI" eval "window.__giTheme.set('$TH'); 'T'" >"$TMP/d2-t-$PG-$TH.log" 2>&1
    "$NODE" "$CLI" wait 1200 >"$TMP/d2-w-$PG-$TH.log" 2>&1
    "$NODE" "$CLI" eval "window.__dots()" >"$OUT/$PG-$TH.json" 2>&1
    echo "done $PG/$TH"
  done
done

"$NODE" "$CLI" close --all >"$TMP/d2-close2.log" 2>&1
echo "=== done · 产物 $OUT ==="
