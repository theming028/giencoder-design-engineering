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
"$NODE" "$AB" wait 2800 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var t=document.querySelector('textarea');t.setAttribute('data-p104t','1');var r=t.getBoundingClientRect();return JSON.stringify({x:Math.round(r.left),y:Math.round(r.top)});})()"
"$NODE" "$AB" click '[data-p104t="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/h104-focus-${W}.png" >/dev/null 2>&1
echo "  shot h104-focus-${W}.png"
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104f.js)"
