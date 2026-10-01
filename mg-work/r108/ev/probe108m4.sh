#!/usr/bin/env bash
# 第十二拍边界验证：① 抽屉头部几何+字号 · ② 并排视图下 diff 卡的 border-top · ③ --ui-fs 杠杆 · ④ 窄档 86%
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
run()  { "$NODE" "$CLI" "$@" 2>&1; }

step open "$URL"; step set viewport 1440 900; step wait 2800
step click ".r93-baract[data-r93-browse]"; step wait 1400
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 700

echo "=== [A] 抽屉头部几何 / 字号（开着抽屉量） ==="
step click "[data-td-rv-act='tree']"; step wait 500
run eval "(function(){var h=document.querySelector('.td-tree-h'),t=document.querySelector('.td-tree-t'),r=document.querySelector('.td-tf');var g=function(e){var s=getComputedStyle(e);return {h:Math.round(e.getBoundingClientRect().height),fs:s.fontSize,lh:s.lineHeight};};return JSON.stringify({head:g(h),title:g(t),row:g(r),panelW:Math.round(document.querySelector('.td-tree-panel').getBoundingClientRect().width)});})()" | tail -1
step eval "document.querySelector('[data-td-tree-x]').click()"; step wait 500

echo "=== [B] 并排视图下：统一行 / 并排行 的 border-top（应只有并排行有） ==="
step eval "document.querySelector('[data-td-rv-view=\"split\"]')||(function(){var o=document.querySelector('[data-td-rv-opts]');o.click();return document.querySelector('[data-td-rv-view=\"split\"]');})().click()"
step wait 700
run eval "(function(){var c=document.querySelector('.td-diff');var u=c.querySelector('.td-diff-rows:not(.td-diff-split)'),s=c.querySelector('.td-diff-split');var gu=getComputedStyle(u),gs=getComputedStyle(s);var b=document.querySelector('.td-rv-body');return JSON.stringify({isSplit:b.classList.contains('is-split'),uniDisplay:gu.display,uniBorder:gu.borderTopWidth,splitDisplay:gs.display,splitBorder:gs.borderTopWidth});})()" | tail -1

echo "=== [C] --ui-fs = 18 杠杆（行高 28 → 36？） ==="
run eval "(function(){document.documentElement.style.setProperty('--ui-fs','18');return 'set';})()" | tail -1
step wait 600
run eval "(function(){var r=document.querySelector('.td-tf');var s=getComputedStyle(r);var t=document.querySelector('.td-tree-h');return JSON.stringify({rowH:Math.round(r.getBoundingClientRect().height),rowFS:s.fontSize,headH:Math.round(t.getBoundingClientRect().height),ratio:getComputedStyle(document.documentElement).getPropertyValue('--ui-fs-ratio')});})()" | tail -1

echo "=== [D] 窄档 1024 下抽屉宽（min(296, 86%)） ==="
run eval "(function(){document.documentElement.style.removeProperty('--ui-fs');return 'reset';})()" | tail -1
step set viewport 900 800
step wait 800
step click ".r93-baract[data-r93-browse]"; step wait 900
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 700
step click "[data-td-rv-act='tree']"; step wait 500
run eval "(function(){var p=document.querySelector('.td-tree-panel'),n=document.querySelector('.td-browse');return JSON.stringify({panelW:Math.round(p.getBoundingClientRect().width),paneW:Math.round(n.getBoundingClientRect().width),pct:Math.round(p.getBoundingClientRect().width/n.getBoundingClientRect().width*100)});})()" | tail -1
echo done
