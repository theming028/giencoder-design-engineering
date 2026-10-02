#!/usr/bin/env bash
# r109 第四拍 · 取证：**大模型选择下拉**（本拍改动最"结构化"的地方）
#
# 为什么单点它：这个下拉的每一项来自 bundle 里的**规格数据**数组 `ze`：
#   {text:`DeepSeek-V4-Pro`, textColor:`#1E1E1E`, textToken:`文本/@color-text-1`,
#    bg:`#F3F4F5`, bgToken:`填充/@colorFill-1`, iconPaths:[{d:`…`, fill:`#4D6BFE`}]}
# 本拍把 `textColor` / `bg` / `iconPaths[].fill` 里的字面换成了 `var(--…)`，
# 而 `textToken` / `bgToken`（纯注释）刻意没动。
# ⇒ 判据有四条，缺一不可：
#   ① `getComputedStyle().color` **必须解析成 rgb(...)**（若 var 没解析会掉落成黑色 `rgb(0,0,0)`）；
#   ② 选中行的 `backgroundColor` 必须等于 `--color-fill-1` 在本档的解；
#   ③ iconPaths 的 SVG `getComputedStyle().fill` 必须解析（品牌 logo 色保持字面）；
#   ④ 两档都不出现 `rgb(0, 0, 0)` 兜底色。
#
# ★★ 铁律：agent-browser 的 stdout **绝不能接管道**（守护进程持有写端 ⇒ 管道永不 EOF）。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/model-dd"
mkdir -p "$OUT" "$EV/tmp"

TS=$(date +%s%N)
"$NODE" "$CLI" close --all >"$EV/tmp/md-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/tmp/md-set.log" 2>&1
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/base.html?v=$TS" >"$EV/tmp/md-open.log" 2>&1
"$NODE" "$CLI" wait 4500 >"$EV/tmp/md-wait.log" 2>&1

for MODE in light dark; do
  "$NODE" "$CLI" eval "window.__giTheme.set('$MODE'); 'M'" >"$EV/tmp/md-theme-$MODE.log" 2>&1
  "$NODE" "$CLI" wait 1200 >"$EV/tmp/md-wait2-$MODE.log" 2>&1
  # 打开下拉（真点击）
  "$NODE" "$CLI" click '[aria-label="大模型选择"]' >"$EV/tmp/md-click-$MODE.log" 2>&1
  "$NODE" "$CLI" wait 900 >"$EV/tmp/md-wait3-$MODE.log" 2>&1
  # 读探针
  "$NODE" "$CLI" eval "$(cat "$EV/p-model-dd.js")" >"$OUT/$MODE.json" 2>&1
  "$NODE" "$CLI" screenshot "$OUT/$MODE.png" >"$EV/tmp/md-shot-$MODE.log" 2>&1
  # 收起（点空白处）
  "$NODE" "$CLI" eval "document.body.dispatchEvent(new MouseEvent('pointerdown',{bubbles:true})); 'x'" >/dev/null 2>&1
  "$NODE" "$CLI" wait 500 >/dev/null 2>&1
done

"$NODE" "$CLI" eval "window.__giTheme.set('light'); 'ok'" >/dev/null 2>&1
"$NODE" "$CLI" close --all >"$EV/tmp/md-close2.log" 2>&1
echo "=== $OUT ==="
ls -la "$OUT"
