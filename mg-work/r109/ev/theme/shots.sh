#!/usr/bin/env bash
# r109 第四拍 · 取证：10 页「浅色 + 暗色」成对整屏截图
#
# ★★ 铁律：agent-browser 的 stdout **绝不能接管道**（CLI 把写端交给常驻守护进程 ⇒ 管道永不 EOF）。
#   一律重定向到文件。
#
# 用法： bash mg-work/r109/ev/theme/shots.sh <label> [pages...]
#   label = 产物目录名（mg-work/r109/raw/shots-<label>/）
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
LABEL="${1:-x}"
shift || true
OUT="mg-work/r109/raw/shots-$LABEL"
mkdir -p "$OUT" "$EV/tmp"

PAGES="${*:-base avatar automation skills settings conversation dev kanban req-kanban task-detail}"

"$NODE" "$CLI" close --all >"$EV/tmp/sh-$LABEL-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/tmp/sh-$LABEL-set.log" 2>&1

for pg in $PAGES; do
  TS=$(date +%s%N)
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/tmp/sh-$LABEL-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/tmp/sh-$LABEL-wait-$pg.log" 2>&1
  # 浅色档：显式置 light（清掉上轮可能残留的 localStorage 档位）
  "$NODE" "$CLI" eval "window.__giTheme.set('light'); document.documentElement.removeAttribute('probe-notrans'); 'L'" >/dev/null 2>&1
  "$NODE" "$CLI" wait 1200 >/dev/null 2>&1
  "$NODE" "$CLI" screenshot "$OUT/$pg-light.png" >"$EV/tmp/sh-$LABEL-shotL-$pg.log" 2>&1
  # 暗色档
  "$NODE" "$CLI" eval "window.__giTheme.set('dark'); 'D'" >/dev/null 2>&1
  "$NODE" "$CLI" wait 1600 >/dev/null 2>&1
  "$NODE" "$CLI" screenshot "$OUT/$pg-dark.png" >"$EV/tmp/sh-$LABEL-shotD-$pg.log" 2>&1
  # 复位（浅色 + 恢复 dark 档位记忆，避免污染下一页的 localStorage）
  "$NODE" "$CLI" eval "window.__giTheme.set('light'); 'ok'" >/dev/null 2>&1
  echo "  $pg  ✓"
done

"$NODE" "$CLI" close --all >"$EV/tmp/sh-$LABEL-close2.log" 2>&1
echo "=== $OUT ==="
ls "$OUT" | wc -l
