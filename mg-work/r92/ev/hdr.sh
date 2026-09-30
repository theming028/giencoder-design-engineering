#!/bin/bash
# r92 侦察：9 页顶栏 header 的类名/背景色/几何 + 页签分组
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
O=mg-work/r92/ev
: > "$O/hdr-out.txt"

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1

for pg in base settings avatar skills automation dev kanban req-kanban task-detail; do
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$(date +%s%N)" >/dev/null 2>&1
  "$NODE" "$AB" wait 1500 >/dev/null 2>&1
  echo "##### $pg" >> "$O/hdr-out.txt"
  "$NODE" "$AB" eval "$(cat $O/hdr.js)" >> "$O/hdr-out.txt" 2>&1
  echo >> "$O/hdr-out.txt"
done
echo DONE
