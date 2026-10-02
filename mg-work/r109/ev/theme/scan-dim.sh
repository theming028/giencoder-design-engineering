#!/usr/bin/env bash
# r109 第四拍 · 侦察：10 页暗色档「深色压深色」矢量图形（补齐 p-mix.js 的 SVG 盲区）
# ★★ agent-browser 的 stdout 绝不能接管道（守护进程持写端 ⇒ 管道永不 EOF）⇒ 一律重定向到文件。
set -u
cd "$(dirname "$0")/../../../.." || exit 1
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/dim"
mkdir -p "$OUT" "$EV/tmp"
PAGES="${*:-base avatar automation skills settings conversation dev kanban req-kanban task-detail}"
"$NODE" "$CLI" close --all >"$EV/tmp/dim-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/tmp/dim-set.log" 2>&1
for pg in $PAGES; do
  TS=$(date +%s%N)
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/tmp/dim-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/tmp/dim-wait-$pg.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-dim.js")" >"$OUT/$pg.json" 2>&1
  echo "  $pg ✓"
done
"$NODE" "$CLI" close --all >"$EV/tmp/dim-close2.log" 2>&1
