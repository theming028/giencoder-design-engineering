#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 1800
echo "=== [$W] 静态读数 ==="
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100b.js)"
echo "=== hover 滚动到底部 ==="
"$NODE" "$AB" hover ".r93-tobottom" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100h_top.js)"
echo "=== hover agent2 ==="
"$NODE" "$AB" hover ".r93-agent2" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100h_agent.js)"
echo "=== hover drow ==="
"$NODE" "$AB" scrollintoview ".r93-dlist .r93-drow" >/dev/null 2>&1
"$NODE" "$AB" hover ".r93-dlist .r93-drow" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100h_drow.js)"
echo "=== 点整行 → 菜单 ==="
"$NODE" "$AB" click ".r93-dlist .r93-drow .r93-dname" >/dev/null 2>&1
"$NODE" "$AB" wait 500
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100ctx.js)"
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r100-menu-rowclick.png" >/dev/null 2>&1
"$NODE" "$AB" press "Escape" >/dev/null 2>&1
"$NODE" "$AB" wait 300
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100ctx.js)"
echo "=== 层级树开合 ==="
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100toggle.js)"
echo "=== done ==="
