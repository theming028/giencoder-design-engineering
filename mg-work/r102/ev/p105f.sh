#!/bin/bash
# r105 ③ 页头两枚按钮 + 文件预览栏 + 全屏：结构与几何实测（1440）
cd /e/GienCoder/giencoder-design-engineering || exit 1
NODE=/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe
AB=/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js
R=mg-work/r102/raw
V=$(date +%s)

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$V" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1

echo "=== T0 初始 ==="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/x105-0-init.png" >/dev/null 2>&1

echo
echo "=== T1 点「打开侧栏」 ==="
"$NODE" "$AB" click '[data-r93-browse]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/x105-1-browse.png" >/dev/null 2>&1

echo
echo "=== T2 再点「全屏」（侧栏仍开）==="
"$NODE" "$AB" click '[data-r93-fullscreen]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/x105-2-both.png" >/dev/null 2>&1

echo
echo "=== T3 Esc → 只关预览栏 ==="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/x105-3-fsonly.png" >/dev/null 2>&1

echo
echo "=== T4 Esc → 退出全屏 ==="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/x105-4-back.png" >/dev/null 2>&1
