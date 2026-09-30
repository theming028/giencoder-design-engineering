#!/bin/bash
# r87 改前/改后对照素材：对 .r85-page / .r85-nav-host 做**元素截图**（自动裁到元素边界，
# 免除全页截图可能出现的滚动/外壳偏移）。同一视口、同一链路内跑完。
set -u
cd /e/GienCoder/giencoder-design-engineering
AB="/c/Users/Administrator/AppData/Local/npm-cache/_npx/ba0727cbf2d10686/node_modules/.bin/agent-browser"
O=mg-work/r87/ev
TS=$(date +%s%N)
"$AB" set viewport 1600 1100 >/dev/null 2>&1

for w in before now; do
  if [ "$w" = "before" ]; then U="file:///E:/GienCoder/giencoder-design-engineering/mg-work/r87/before/settings.html"; else U="file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html"; fi
  "$AB" open "$U?v=$TS" >/dev/null 2>&1
  "$AB" wait 1900 >/dev/null 2>&1
  "$AB" eval 'window.scrollTo(0,0);"ok"' >/dev/null 2>&1
  "$AB" wait 300 >/dev/null 2>&1
  "$AB" screenshot ".r85-page" "$O/el_${w}_page.png" >/dev/null 2>&1
  "$AB" screenshot ".r85-nav-host" "$O/el_${w}_nav.png" >/dev/null 2>&1
  "$AB" eval "$(cat $O/p87rect.js)" > "$O/rect_$w.txt" 2>&1
done
echo EL_SHOTS_DONE
