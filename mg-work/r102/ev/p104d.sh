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
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104c.js)" >/dev/null 2>&1
echo "===== D1) 点 b1（圆钮2） ====="
"$NODE" "$AB" click '[data-p104^="b1-"]' >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/d104-b1.png" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104d.js)"
echo "===== D2) 点模型选择器根 ====="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var v=document.querySelector('[data-p104^=\"s1-\"]');var r=v.closest('.giencoder-select')||v.parentElement;r.setAttribute('data-p104r','1');return r.className;})()"
"$NODE" "$AB" click '[data-p104r="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/d104-model.png" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104d.js)"
