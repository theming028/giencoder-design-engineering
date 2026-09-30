#!/usr/bin/env bash
# r101 终态一次性取证（单进程：整条链在一个 bash 调用里跑完，避免 agent-browser 标签页串味）
# 用法： bash mg-work/r101/ev/p101fin.sh [宽=1440]
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"

# ---- ⑪ 骨架屏：早期两拍 ----
"$NODE" "$AB" wait 350
echo "=== [⑪] t≈350ms ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101sk.js)"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fin-sk.png" >/dev/null 2>&1
"$NODE" "$AB" wait 1600
echo "=== [⑪] t≈2000ms（应已移除） ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101sk.js)"

# ---- 静态读数（②④⑤⑥⑧⑨⑩ 一次拿全） ----
echo "=== [②④⑤⑥⑧⑨⑩] 静态读数 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101b.js)"

# ---- ⑤ Bash 卡头打标（绿勾计数） ----
echo "=== [⑤] okc 定位 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101shot.js)"

# ---- 打标（fh / ib / art / sb / zip） ----
echo "=== 打标 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101tag.js)"

# ---- ⑩ 状态条：滚进视野后全页截图（供 Pillow 量投影剖面） ----
"$NODE" "$AB" scrollintoview "[data-r101-sb]" >/dev/null 2>&1
"$NODE" "$AB" wait 350
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fin-sb.png" >/dev/null 2>&1

# ---- ①③ hover 展开头 ----
"$NODE" "$AB" scrollintoview "[data-r101-fh]" >/dev/null 2>&1
"$NODE" "$AB" wait 250
"$NODE" "$AB" hover "[data-r101-fh]" >/dev/null 2>&1
"$NODE" "$AB" wait 150
echo "=== [①] hover 展开头 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101hov.js)"

# ---- ③ hover 图标按钮 ----
"$NODE" "$AB" scrollintoview "[data-r101-ib]" >/dev/null 2>&1
"$NODE" "$AB" wait 250
"$NODE" "$AB" hover "[data-r101-ib]" >/dev/null 2>&1
"$NODE" "$AB" wait 150
echo "=== [③] hover 图标按钮 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101hov.js)"

# ---- ④ 折叠前后标题左缘（跳动检查）+ 打标 fc ----
echo "=== [④] 折叠前后 dx ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101jump.js)"

# ---- ① hover 折叠头 ----
"$NODE" "$AB" scrollintoview "[data-r101-fc]" >/dev/null 2>&1
"$NODE" "$AB" wait 250
"$NODE" "$AB" hover "[data-r101-fc]" >/dev/null 2>&1
"$NODE" "$AB" wait 150
echo "=== [①] hover 折叠头 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101hov.js)"

# ---- ⑦ 产物卡右键菜单 ----
"$NODE" "$AB" scrollintoview "[data-r101-art]" >/dev/null 2>&1
"$NODE" "$AB" wait 300
echo "=== [⑦] 右键菜单 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101ctx.js)"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fin-ctx.png" >/dev/null 2>&1

# ---- 整页定版截图 ----
"$NODE" "$AB" eval "document.querySelector('.r93-scroll').scrollTop=0; 'ok'"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fin-${W}.png" >/dev/null 2>&1

echo "=== done ==="
