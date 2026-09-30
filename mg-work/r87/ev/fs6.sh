#!/bin/bash
# 6 级字号实测：对每个档位设 localStorage → reload → 元素截图（导航 + 内容首行）
set -u
cd /e/GienCoder/giencoder-design-engineering
AB="/c/Users/Administrator/AppData/Local/npm-cache/_npx/ba0727cbf2d10686/node_modules/.bin/agent-browser"
O=mg-work/r87/ev
TS=$(date +%s%N)
"$AB" set viewport 1600 1100 >/dev/null 2>&1
"$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html?v=$TS" >/dev/null 2>&1
"$AB" wait 1700 >/dev/null 2>&1

for px in 13 14 16 18 20 24; do
  "$AB" eval "(function(){try{localStorage.setItem('gi-ui-fs','$px');}catch(e){};document.documentElement.style.setProperty('--ui-fs','$px');return 'ok';})()" >/dev/null 2>&1
  "$AB" reload >/dev/null 2>&1
  "$AB" wait 1500 >/dev/null 2>&1
  "$AB" eval 'window.scrollTo(0,0);"ok"' >/dev/null 2>&1
  "$AB" wait 250 >/dev/null 2>&1
  "$AB" screenshot ".r85-nav-host" "$O/fs_${px}_nav.png" >/dev/null 2>&1
  "$AB" screenshot ".r85-card" "$O/fs_${px}_card.png" >/dev/null 2>&1
  "$AB" eval "$(cat $O/p87rect.js)" > "$O/fs_${px}.txt" 2>&1
done
"$AB" eval "(function(){try{localStorage.removeItem('gi-ui-fs');}catch(e){};return 'ok';})()" >/dev/null 2>&1
echo FS6_DONE
