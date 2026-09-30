#!/usr/bin/env bash
# r101 运行态取证（单进程：一次 bash 调用跑完整条链，避免标签页串味）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"

"$NODE" "$AB" wait 400
echo "=== [⑪] t≈400ms ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101sk.js)"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-sk-400.png" >/dev/null 2>&1

"$NODE" "$AB" wait 600
echo "=== [⑪] t≈1000ms ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101sk.js)"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-sk-1000.png" >/dev/null 2>&1

"$NODE" "$AB" wait 1200
echo "=== [⑪] t≈2200ms（骨架屏应已移除） ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101sk.js)"

echo "=== [①②③④⑤⑥⑧⑨⑩] 静态读数 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101b.js)"

echo "=== 打标 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101tag.js)"

echo "=== [①③] hover 展开头 ==="
"$NODE" "$AB" scrollintoview "[data-r101-fh]" >/dev/null 2>&1
"$NODE" "$AB" hover "[data-r101-fh]" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101h.js)"

echo "=== [③] hover 图标按钮 ==="
"$NODE" "$AB" scrollintoview "[data-r101-ib]" >/dev/null 2>&1
"$NODE" "$AB" hover "[data-r101-ib]" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101h.js)"

echo "=== [④] 折叠前后标题左缘（跳动检查） ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101jump.js)"

echo "=== [①] hover 折叠头 ==="
"$NODE" "$AB" hover "[data-r101-fc]" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101h.js)"

echo "=== [⑥] 渐隐处截图（滚到中段，药丸应出现） ==="
"$NODE" "$AB" scrollintoview "[data-r101-sb]" >/dev/null 2>&1
"$NODE" "$AB" wait 400
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101b.js)"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fade.png" >/dev/null 2>&1

echo "=== [⑦] 产物卡右键菜单 ==="
"$NODE" "$AB" scrollintoview "[data-r101-art]" >/dev/null 2>&1
"$NODE" "$AB" wait 300
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101ctx.js)"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-ctx.png" >/dev/null 2>&1

echo "=== done ==="
