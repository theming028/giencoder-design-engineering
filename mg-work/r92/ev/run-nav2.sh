#!/bin/bash
# r92 回归取证：设置页 aside 三态元素截图（与 r91 的 web-nav-r91-*.png 同口径 256×844）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
O=mg-work/r92/raw

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html?v=$(date +%s%N)" >/dev/null 2>&1
"$NODE" "$AB" wait 1800 >/dev/null 2>&1
"$NODE" "$AB" eval 'JSON.stringify({innerH:window.innerHeight,innerW:window.innerWidth})' > mg-work/r92/ev/p92-shot-env.txt 2>&1
"$NODE" "$AB" screenshot "aside" "$O/web-aside-r92-def.png" >/dev/null 2>&1

"$NODE" "$AB" hover ".r85-back" >/dev/null 2>&1
"$NODE" "$AB" wait 600 >/dev/null 2>&1
"$NODE" "$AB" screenshot "aside" "$O/web-aside-r92-backhover.png" >/dev/null 2>&1

"$NODE" "$AB" eval 'window.scrollTo(0,0);1' >/dev/null 2>&1
"$NODE" "$AB" hover "[data-set-tab=model]" >/dev/null 2>&1
"$NODE" "$AB" wait 600 >/dev/null 2>&1
"$NODE" "$AB" screenshot "aside" "$O/web-aside-r92-navihover.png" >/dev/null 2>&1
echo DONE
