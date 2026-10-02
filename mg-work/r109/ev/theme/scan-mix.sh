#!/usr/bin/env bash
# r109 第四拍 · 侦察：基础工作台 5 页「暗色档下仍发亮的元素」全量 DOM 取证
#
# ★★ 铁律：agent-browser 的 stdout **绝不能接管道**（CLI 把写端交给常驻守护进程 ⇒ 管道永不 EOF）。
#   一律重定向到文件。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/mix4"
mkdir -p "$OUT"

PAGES="${*:-base avatar automation skills settings}"

"$NODE" "$CLI" close --all >"$EV/m4-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/m4-set.log" 2>&1

for pg in $PAGES; do
  TS=$(date +%s%N)
  echo "===== $pg ====="
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/m4-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/m4-wait-$pg.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-mix.js")" >"$OUT/$pg.json" 2>&1
  # 交叉印证：暗色实拍（像素法与 DOM 法两条独立证据）
  "$NODE" "$CLI" eval "window.__giTheme.set('dark'); 'd'" >/dev/null 2>&1
  "$NODE" "$CLI" wait 2200 >/dev/null 2>&1
  "$NODE" "$CLI" screenshot "$OUT/$pg-dark.png" >"$EV/m4-shot-$pg.log" 2>&1
  "$NODE" "$CLI" eval "var e=document.getElementById('probe-notrans'); if(e) e.remove(); window.__giTheme.set('light'); 'ok'" >/dev/null 2>&1
done

"$NODE" "$CLI" close --all >"$EV/m4-close2.log" 2>&1
echo "=== 产物 ==="
ls -la "$OUT"
