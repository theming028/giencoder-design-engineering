#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2800 >/dev/null 2>&1
echo "===== I1) 浅色 chat ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104i.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/m104-chat.png" >/dev/null 2>&1
echo "===== I2) 折叠仍可开合（点第 1 个折叠头） ====="
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');f.querySelector('.r93-fh').setAttribute('data-p104h','1');return f.getAttribute('data-r93-open');})()"
"$NODE" "$AB" click '[data-p104h="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');var fb=f.querySelector('.r93-fb');var c=getComputedStyle(fb);return JSON.stringify({open:f.getAttribute('data-r93-open'),maxH:c.maxHeight,op:c.opacity});})()"
"$NODE" "$AB" click '[data-p104h="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');var fb=f.querySelector('.r93-fb');var c=getComputedStyle(fb);return JSON.stringify({open:f.getAttribute('data-r93-open'),maxH:c.maxHeight,op:c.opacity});})()"
echo "===== I3) 暗色 ====="
"$NODE" "$AB" eval "document.documentElement.setAttribute('giencoder-theme','dark');'ok'"
"$NODE" "$AB" wait 600 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104i.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/m104-dark.png" >/dev/null 2>&1
