#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1500 >/dev/null 2>&1
"$NODE" "$AB" eval "var s=document.querySelector('.r93-conv-host .r93-scroll');s.scrollTop=3325;String(s.scrollTop)" >/dev/null 2>&1
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fadeab-on.png" >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var st=document.createElement('style');st.id='r101-fadeab-off';st.textContent='.r93-tbsticky::after{display:none !important;}';document.head.appendChild(st);return 'off';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 260 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fadeab-off.png" >/dev/null 2>&1
echo "  已拍 on/off"
