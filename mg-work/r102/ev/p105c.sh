#!/usr/bin/env bash
# r105 ① 实测：在独立页（settings / kanban / avatar）点 aside 里的会话任务 → 是否跳到 conversation.html
set -u
NODE="/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
V=$(date +%s)
R="mg-work/r102/ev"
SEL="aside button.min-w-0.flex-1"

for P in settings kanban avatar; do
  echo "########## $P.html"
  "$NODE" "$AB" set viewport 1440 900 >/dev/null
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$P.html?v=$V" >/dev/null
  "$NODE" "$AB" wait 2600 >/dev/null
  echo -n "  会话项个数 / 当前页: "
  "$NODE" "$AB" eval "JSON.stringify({n:document.querySelectorAll('$SEL').length, page:location.pathname.split('/').pop()})"
  "$NODE" "$AB" click "$SEL" >/dev/null
  "$NODE" "$AB" wait 1600 >/dev/null
  echo -n "  点击后 → "
  "$NODE" "$AB" eval "location.pathname.split('/').pop()"
done
