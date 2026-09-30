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
"$NODE" "$AB" wait 120 >/dev/null 2>&1
echo "===== F1) 首帧（应 app=null / sk=true / box.op=0） ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104f.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/f104-early.png" >/dev/null 2>&1
"$NODE" "$AB" wait 2400 >/dev/null 2>&1
echo "===== F2) 就绪后 chat 态 ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104f.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/f104-chat.png" >/dev/null 2>&1
echo "===== F3) 打开模型下拉 ====="
"$NODE" "$AB" eval "(function(){var v=document.querySelectorAll('.giencoder-select-view');for(var i=0;i<v.length;i++){if(/DeepSeek/.test(v[i].textContent)){v[i].closest('.giencoder-select').setAttribute('data-p104r','1');}}return 'ok';})()"
"$NODE" "$AB" click '[data-p104r="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/f104-pop.png" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104f.js)"
"$NODE" "$AB" press Escape >/dev/null 2>&1
echo "===== F4) 切到轨迹（点后 300ms / 900ms 各看一次） ====="
"$NODE" "$AB" click '[data-r93-tab="trace"]' >/dev/null 2>&1
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/f104-trace-mid.png" >/dev/null 2>&1
"$NODE" "$AB" wait 600 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104f.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/f104-trace.png" >/dev/null 2>&1
echo "===== F5) 切回对话 ====="
"$NODE" "$AB" click '[data-r93-tab="chat"]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p104f.js)"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/f104-back.png" >/dev/null 2>&1
