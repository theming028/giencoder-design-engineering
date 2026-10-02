#!/usr/bin/env bash
# 侦察：**强行**给未适配页挂上护栏 + 暗色，量「混起来会有多脏」（只为评估工作量，不改产物）
set -u
cd "$(dirname "$0")/../../../.." || exit 1
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; OUT="mg-work/r109/raw/mix4"; mkdir -p "$OUT"
"$NODE" "$CLI" close --all >"$EV/f-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
for pg in "$@"; do
  TS=$(date +%s%N)
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/f-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >/dev/null 2>&1
  "$NODE" "$CLI" eval "document.documentElement.setAttribute('data-gi-dark','1'); window.__giTheme.set('dark'); 'forced'" >/dev/null 2>&1
  "$NODE" "$CLI" wait 900 >/dev/null 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-mix.js")" >"$OUT/force-$pg.json" 2>&1
  "$NODE" "$CLI" eval "window.__giTheme.set('dark'); 'd'" >/dev/null 2>&1
  "$NODE" "$CLI" wait 2000 >/dev/null 2>&1
  "$NODE" "$CLI" screenshot "$OUT/force-$pg.png" >"$EV/f-shot-$pg.log" 2>&1
done
"$NODE" "$CLI" close --all >"$EV/f-close2.log" 2>&1
echo done
