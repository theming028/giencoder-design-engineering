#!/bin/bash
# r92 ②③ 实测：设置页 aside 返回钮颜色 / r85-gt 左间距
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
O=mg-work/r92/ev

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html?v=$(date +%s%N)" >/dev/null 2>&1
"$NODE" "$AB" wait 1800 >/dev/null 2>&1
"$NODE" "$AB" eval 'JSON.stringify({innerH:window.innerHeight,innerW:window.innerWidth})' > "$O/p92-nav-env.txt" 2>&1
"$NODE" "$AB" eval "$(cat $O/p92-nav.js)" > "$O/p92-nav-def.txt" 2>&1

# hover 返回钮（真鼠标），确认图标/文字色不因 hover 变化
"$NODE" "$AB" hover ".r85-back" >/dev/null 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat $O/p92-nav.js)" > "$O/p92-nav-hover.txt" 2>&1

# 元素截图：整条 aside（默认态）
"$NODE" "$AB" eval 'JSON.stringify({note:"reset"})' >/dev/null 2>&1
"$NODE" "$AB" screenshot "aside" "$O/../raw/web-aside-r92.png" >/dev/null 2>&1
"$NODE" "$AB" screenshot ".r85-nav-host" "$O/../raw/web-navhost-r92.png" >/dev/null 2>&1
echo DONE
ls -la "$O/../raw/" | tail -5
