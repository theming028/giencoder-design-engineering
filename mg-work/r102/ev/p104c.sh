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
echo "== tag =="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104c.js)"
echo "== click b0 (左1圆钮) =="
"$NODE" "$AB" click '[data-p104^="b0-"]' >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/c104-plus.png" >/dev/null 2>&1
echo "  shot c104-plus.png"
echo "== close / click 模型下拉 =="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" click '[data-p104^="s4-"]' >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/c104-model.png" >/dev/null 2>&1
echo "  shot c104-model.png"
echo "== 模型下拉 rect =="
"$NODE" "$AB" eval "(function(){var p=document.querySelectorAll('.giencoder-select-popup');var o=[];[].forEach.call(p,function(e){var r=e.getBoundingClientRect();var c=getComputedStyle(e);o.push({x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),op:c.opacity,z:c.zIndex,disp:c.display});});return JSON.stringify(o);})()"
