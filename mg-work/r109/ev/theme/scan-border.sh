#!/usr/bin/env bash
# r109 第十拍 · 描边令牌**真机双档**复验：逐页开 → 读浅档 → 切暗档 → 读暗档
# ★ 用页面自带的 window.__giTheme.set('dark')（比探针 __setDark 更贴近真实交互）
# ★ 铁律：stdout 一律重定向（禁接管道）；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
OUT="mg-work/r109/raw/bd10"
mkdir -p "$OUT" "$TMP"

PAGES="$*"
[ -z "$PAGES" ] && PAGES="base conversation settings"
TS=$(date +%s%N)

"$NODE" "$CLI" close --all >"$TMP/b-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/b-set.log" 2>&1

for PG in $PAGES; do
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/open-$PG.log" 2>&1
  "$NODE" "$CLI" wait 4500 >"$TMP/b-w-$PG.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-border.js")" >"$OUT/init-$PG.log" 2>&1
  "$NODE" "$CLI" eval "window.__giTheme.set('light'); 'T'" >"$TMP/b-l-$PG.log" 2>&1
  "$NODE" "$CLI" wait 1200 >"$TMP/b-wl-$PG.log" 2>&1
  "$NODE" "$CLI" eval "window.__btok()" >"$OUT/$PG-light.json" 2>&1
  "$NODE" "$CLI" eval "window.__giTheme.set('dark'); 'T'" >"$TMP/b-d-$PG.log" 2>&1
  "$NODE" "$CLI" wait 1200 >"$TMP/b-wd-$PG.log" 2>&1
  "$NODE" "$CLI" eval "window.__btok()" >"$OUT/$PG-dark.json" 2>&1
  "$NODE" "$CLI" screenshot "$OUT/$PG-dark.png" >"$TMP/b-shot-$PG.log" 2>&1
  echo "done $PG"
done

"$NODE" "$CLI" close --all >"$TMP/b-close2.log" 2>&1
echo "=== done · 产物 $OUT ==="
