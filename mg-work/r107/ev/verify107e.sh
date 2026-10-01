#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
EV="$ROOT/mg-work/r107/ev"
AB() { "$NODE" "$CLI" "$@"; }

AB open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1

# ① 开「+」菜单并真鼠标 hover 第二个条目（「终端」）
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB hover '.td-mod-menu .giencoder-dropdown-item:nth-of-type(2)' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB screenshot "$OUT/e4-mod-hover.png" >/dev/null 2>&1

# ② 综合几何 + 态（含 hover 读数；同一进程内紧接上一步）
AB eval "$(cat "$EV/p107e2.js")" > "$EV/e107c.log" 2>&1

# ③ 右键菜单 hover 态截图
AB eval "(function(){var p=document.querySelector('.td-browse');var t=p.querySelector('.td-browse-tab');t.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:1100,clientY:120}));return 'ok';})()" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB hover '.td-ctxmenu .giencoder-dropdown-item:nth-of-type(1)' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB screenshot "$OUT/e5-ctx-hover.png" >/dev/null 2>&1
AB eval "document.dispatchEvent(new MouseEvent('click',{bubbles:true}))" >/dev/null 2>&1

echo "verify-e done"
