#!/usr/bin/env bash
# r109 ③-c 基础工作台 5 页：浅/暗双档真机取证（量值 + 截图）
#
# ★★ 铁律：agent-browser 的 stdout **绝不能接管道**。
#   CLI 会把 stdout 写端交给它 fork 的常驻守护进程 ⇒ 管道永不 EOF ⇒ `| tail` 永久等待
#   （症状 = 命令「挂死」、无输出、SIGTERM）。**一律重定向到文件**。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
RAW="mg-work/r109/raw/theme"
mkdir -p "$EV" "$RAW/light" "$RAW/dark"

PAGES="base avatar automation skills settings"

"$NODE" "$CLI" close --all >"$EV/d2-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/d2-set.log" 2>&1

for pg in $PAGES; do
  TS=$(date +%s%N)
  echo "===== $pg ====="
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/d2-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/d2-wait-$pg.log" 2>&1

  # ① 双档量值（探针内部会切档，收尾复位 light）
  "$NODE" "$CLI" eval "$(cat "$EV/p-verify.js")" >"$EV/v-$pg.json" 2>&1

  # ② 摘掉探针钉死的 transition，免得影响截图观感
  "$NODE" "$CLI" eval "var e=document.getElementById('probe-notrans'); if(e) e.remove(); 'ok'" >/dev/null 2>&1

  # ③ 浅色截图
  "$NODE" "$CLI" wait 900 >/dev/null 2>&1
  "$NODE" "$CLI" screenshot "$RAW/light/$pg.png" >"$EV/d2-shot-l-$pg.log" 2>&1

  # ④ 暗色截图
  "$NODE" "$CLI" eval "window.__giTheme.set('dark'); window.__giTheme.get()" >"$EV/d2-dark-$pg.log" 2>&1
  "$NODE" "$CLI" wait 2600 >/dev/null 2>&1
  "$NODE" "$CLI" screenshot "$RAW/dark/$pg.png" >"$EV/d2-shot-d-$pg.log" 2>&1
done

"$NODE" "$CLI" close --all >"$EV/d2-close2.log" 2>&1
echo "=== 截图产物 ==="
ls -la "$RAW/light" "$RAW/dark"
