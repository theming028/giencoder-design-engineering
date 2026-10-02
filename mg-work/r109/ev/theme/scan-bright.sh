#!/usr/bin/env bash
# r109 第四拍（裁决③）· 侦察：暗色档「亮面压暗底」逐状态审计（10 页）
#
# ★ 与 scan-dim.sh 是镜像：③ 探针找「暗底上发暗的图形」，本脚本找「暗底上发亮的面」。
# ★★ 铁律：agent-browser 的 stdout 绝不能接管道（守护进程持有写端 ⇒ 管道永不 EOF）。一律重定向。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/bright4"
mkdir -p "$OUT"

PAGES="${*:-base avatar automation skills settings conversation dev kanban req-kanban task-detail}"

"$NODE" "$CLI" close --all >"$EV/br-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/br-set.log" 2>&1

for pg in $PAGES; do
  TS=$(date +%s%N)
  echo "===== $pg ====="
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/br-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/br-wait-$pg.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-bright.js")" >"$OUT/$pg.json" 2>&1
  "$NODE" "$CLI" eval "var e=document.getElementById('probe-notrans'); if(e) e.remove(); window.__giTheme.set('light'); 'ok'" >/dev/null 2>&1
done

"$NODE" "$CLI" close --all >"$EV/br-close2.log" 2>&1
echo "=== 产物 ==="
ls -la "$OUT"
