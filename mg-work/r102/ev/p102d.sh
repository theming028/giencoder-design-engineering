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
"$NODE" "$AB" wait 2200 >/dev/null 2>&1
echo "===== ⑥ 折叠头 hover（目标=标题文字，避开叠加元素） ====="
"$NODE" "$AB" eval "(function(){function fwm(){return [].filter.call(document.querySelectorAll('.r93-fold'),function(x){return x.querySelector(':scope > .r93-fc .r93-t12l.r93-fm');});}var f=fwm()[0];if(!f)return 'none';f.id='r102fc';f.scrollIntoView({block:'center'});window.__fm=f;return JSON.stringify({meta:f.querySelector(':scope > .r93-fc .r93-t12l.r93-fm').textContent});})()"
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" click "#r102fc > .r93-fh" >/dev/null 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
echo "[折叠后状态]"
"$NODE" "$AB" eval "(function(){var f=window.__fm;var fc=f.querySelector(':scope > .r93-fc');var r=fc.getBoundingClientRect();return JSON.stringify({open:f.getAttribute('data-open'),fcRect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],fcDisp:getComputedStyle(fc).display,titleRect:(function(){var t=fc.querySelector('.r93-t14');var b=t.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)];})(),hitAtTitle:(function(){var t=fc.querySelector('.r93-t14');var b=t.getBoundingClientRect();var e=document.elementFromPoint(Math.round(b.left+b.width/2),Math.round(b.top+b.height/2));return e?e.className:'null';})()});})()"
"$NODE" "$AB" hover "#r102fc > .r93-fc > .r93-t14" >/dev/null 2>&1
"$NODE" "$AB" wait 380 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var f=window.__fm;var fc=f.querySelector(':scope > .r93-fc');var m=fc.querySelector('.r93-t12l.r93-fm');var ch=fc.querySelector('.r93-fchev');return JSON.stringify({hovFc:fc.matches(':hover'),hovTitle:fc.querySelector('.r93-t14').matches(':hover'),metaColor:m?getComputedStyle(m).color:'no-meta',metaTxt:m?(m.textContent||'').slice(0,20):null,titleColor:getComputedStyle(fc.querySelector('.r93-t14')).color,chevOp:getComputedStyle(ch).opacity,chevML:getComputedStyle(ch).marginLeft,chevTitleGap:Math.round(ch.getBoundingClientRect().left-fc.querySelector('.r93-t14').getBoundingClientRect().right)});})()"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102d-fchover-${W}.png" >/dev/null 2>&1
echo "  shot p102d-fchover-${W}.png"
