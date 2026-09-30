#!/bin/bash
# r87 视觉回归 / 取证：一次跑完（同一时刻只允许一个 UI 实测进程）
# A. 设置页 @ 默认 14px —— 四条改动取证
# B. 设置页 @ 24px / 13px —— 全局字号机制溢出与截断验证
# C. kanban / req-kanban / task-detail / avatar —— select 三项全站回归
# D. kanban @ 24px —— 密集页字号放大回归
set -u
cd /e/GienCoder/giencoder-design-engineering
AB="/c/Users/Administrator/AppData/Local/npm-cache/_npx/ba0727cbf2d10686/node_modules/.bin/agent-browser"
O=mg-work/r87/ev
F="file:///E:/GienCoder/giencoder-design-engineering/pages"
TS=$(date +%s%N)

"$AB" set viewport 1600 1100 >/dev/null 2>&1

echo "### A. settings @ 14px"
"$AB" open "$F/settings.html?v=$TS" >/dev/null 2>&1
"$AB" wait 1700 >/dev/null 2>&1
"$AB" eval "$(cat $O/p87a.js)" > "$O/p87a.out.txt" 2>&1
"$AB" screenshot "" "$O/a_default_full.png" >/dev/null 2>&1
"$AB" screenshot ".r85-nav-host" "$O/a_nav.png" >/dev/null 2>&1
"$AB" screenshot ".r85-seg" "$O/a_seg.png" >/dev/null 2>&1
"$AB" screenshot ".r85-slider" "$O/a_slider.png" >/dev/null 2>&1
"$AB" screenshot ".r85-actions, .r85-foot, .r85-btn" "$O/a_btns.png" >/dev/null 2>&1

echo "### B. settings @ 24px"
"$AB" eval "(function(){try{localStorage.setItem('gi-ui-fs','24');}catch(e){};document.documentElement.style.setProperty('--ui-fs','24');return 'ok';})()" >/dev/null 2>&1
"$AB" reload >/dev/null 2>&1
"$AB" wait 1700 >/dev/null 2>&1
"$AB" eval "$(cat $O/p87c.js)" > "$O/p87c.out.txt" 2>&1
"$AB" screenshot "" "$O/b_fs24_full.png" >/dev/null 2>&1
"$AB" screenshot ".r85-nav-host" "$O/b_fs24_nav.png" >/dev/null 2>&1

echo "### B2. settings @ 13px"
"$AB" eval "(function(){try{localStorage.setItem('gi-ui-fs','13');}catch(e){};document.documentElement.style.setProperty('--ui-fs','13');return 'ok';})()" >/dev/null 2>&1
"$AB" reload >/dev/null 2>&1
"$AB" wait 1500 >/dev/null 2>&1
"$AB" screenshot "" "$O/c_fs13_full.png" >/dev/null 2>&1
"$AB" eval "(function(){try{localStorage.removeItem('gi-ui-fs');}catch(e){};return 'ok';})()" >/dev/null 2>&1

echo "### C. 其余页 select 回归 @ 14px"
for p in kanban req-kanban task-detail avatar; do
  "$AB" open "$F/$p.html?v=$TS" >/dev/null 2>&1
  "$AB" wait 1700 >/dev/null 2>&1
  "$AB" eval "$(cat $O/p87d.js)" > "$O/d_$p.txt" 2>&1
  "$AB" screenshot "" "$O/d_$p.png" >/dev/null 2>&1
done

echo "### D. kanban @ 24px"
"$AB" open "$F/kanban.html?v=$TS" >/dev/null 2>&1
"$AB" wait 1500 >/dev/null 2>&1
"$AB" eval "(function(){try{localStorage.setItem('gi-ui-fs','24');}catch(e){};document.documentElement.style.setProperty('--ui-fs','24');return 'ok';})()" >/dev/null 2>&1
"$AB" reload >/dev/null 2>&1
"$AB" wait 1900 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({page:location.pathname.split("/").pop(),uiFs:getComputedStyle(document.documentElement).getPropertyValue("--ui-fs").trim()})' > /dev/null 2>&1
"$AB" eval "$(cat $O/p87d.js)" > "$O/e_kanban24.txt" 2>&1
"$AB" screenshot "" "$O/e_kanban24.png" >/dev/null 2>&1
"$AB" eval "(function(){try{localStorage.removeItem('gi-ui-fs');}catch(e){};return 'ok';})()" >/dev/null 2>&1

echo "ALL_SHOTS_DONE"
