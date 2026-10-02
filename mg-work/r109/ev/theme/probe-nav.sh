#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/../../../.." || exit 1
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; OUT="mg-work/r109/raw/mix4"; mkdir -p "$OUT"
"$NODE" "$CLI" close --all >"$EV/nv-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
for pg in "$@"; do
  TS=$(date +%s%N)
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/nv-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >/dev/null 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-nav.js")" >"$OUT/nav-$pg.json" 2>&1
done
"$NODE" "$CLI" close --all >"$EV/nv-close2.log" 2>&1
echo done
