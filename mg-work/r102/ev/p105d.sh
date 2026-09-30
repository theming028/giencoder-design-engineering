#!/usr/bin/env bash
# r105 ① 现状普查：各页 aside 里到底有几枚按钮、有没有「会话任务」分组
set -u
NODE="/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
V=$(date +%s)

for P in base dev kanban req-kanban task-detail avatar automation skills settings; do
  "$NODE" "$AB" set viewport 1440 900 >/dev/null
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$P.html?v=$V" >/dev/null
  "$NODE" "$AB" wait 2600 >/dev/null
  echo -n "$(printf '%-12s' $P) "
  "$NODE" "$AB" eval "(function(){var a=document.querySelector('aside');if(!a)return 'NO-ASIDE';var bs=[].slice.call(a.querySelectorAll('button'));var sess=bs.filter(function(b){return b.classList.contains('min-w-0')&&b.classList.contains('flex-1')});var heads=bs.filter(function(b){return b.classList.contains('rounded-md')&&b.classList.contains('py-0')});return JSON.stringify({btns:bs.length,sess:sess.length,heads:heads.length,headTxt:heads.map(function(h){return (h.textContent||'').trim().slice(0,8)})});})()"
done
