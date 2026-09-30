#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"; H="${2:-900}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" "$H" >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1
echo "===== D1) 未聚焦：textarea 祖先链 ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103d.js)"
echo
echo "===== D2) 真鼠标点击 textarea 后 ====="
"$NODE" "$AB" click "textarea" >/dev/null 2>&1
"$NODE" "$AB" wait 600 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var ae=document.activeElement;return JSON.stringify({tag:ae?ae.tagName:null,cls:ae?((ae.className&&ae.className.baseVal!==undefined?ae.className.baseVal:ae.className)||'').slice(0,60):null});})()"
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103d.js)"
echo
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p103d-focus-${W}.png" >/dev/null 2>&1
echo "  shot p103d-focus-${W}.png"
