#!/bin/bash
# 在同一口径下跑「改前 r86 态」基线与「改后 r87 态」对照（同文件名 ⇒ 外壳路由不落 base 壳）
set -u
cd /e/GienCoder/giencoder-design-engineering
AB="/c/Users/Administrator/AppData/Local/npm-cache/_npx/ba0727cbf2d10686/node_modules/.bin/agent-browser"
O=mg-work/r87/ev
TS=$(date +%s%N)
"$AB" set viewport 1600 1100 >/dev/null 2>&1

for p in kanban req-kanban task-detail avatar; do
  "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$p.html?v=$TS" >/dev/null 2>&1
  "$AB" wait 1600 >/dev/null 2>&1
  "$AB" eval "$(cat $O/p87d.js)" > "$O/g_$p.now.txt" 2>&1
  "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/mg-work/r87/before/$p.html?v=$TS" >/dev/null 2>&1
  "$AB" wait 1600 >/dev/null 2>&1
  "$AB" eval "$(cat $O/p87d.js)" > "$O/g_$p.bef.txt" 2>&1
done

# settings：只跑字号机制（before 里 select 还是 r86 态）
"$AB" open "file:///E:/GienCoder/giencoder-design-engineering/mg-work/r87/before/settings.html?v=$TS" >/dev/null 2>&1
"$AB" wait 1600 >/dev/null 2>&1
"$AB" eval "$(cat $O/p87d.js)" > "$O/g_settings.bef.txt" 2>&1
"$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html?v=$TS" >/dev/null 2>&1
"$AB" wait 1600 >/dev/null 2>&1
"$AB" eval "$(cat $O/p87d.js)" > "$O/g_settings.now.txt" 2>&1
echo BASE_DONE
