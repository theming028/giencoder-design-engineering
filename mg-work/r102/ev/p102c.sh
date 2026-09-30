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
"$NODE" "$AB" wait 1900 >/dev/null 2>&1

echo "===== A) ③ 折叠收起：页面内 rAF 逐帧高度曲线（铁证） ====="
"$NODE" "$AB" eval "(function(){var folds=document.querySelectorAll('.r93-fold');var f=folds[1]||folds[0];f.scrollIntoView({block:'center'});var fb=f.querySelector(':scope > .r93-fb');window.__rec=[];var t0=performance.now();function snap(){var c=getComputedStyle(fb);window.__rec.push([Math.round(performance.now()-t0),Math.round(fb.getBoundingClientRect().height),c.maxHeight,c.opacity]);if(performance.now()-t0<760){requestAnimationFrame(snap);}}requestAnimationFrame(snap);f.querySelector(':scope > .r93-fh').click();return JSON.stringify({clicked:'fold#1',bh:fb.style.getPropertyValue('--r93-fbh'),open:f.getAttribute('data-open')});})()"
"$NODE" "$AB" wait 1000 >/dev/null 2>&1
echo "[曲线]"
"$NODE" "$AB" eval "JSON.stringify(window.__rec)"

echo
echo "===== B) ③ 展开：再点回去，看反向曲线 ====="
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.r93-fold')[1];var fb=f.querySelector(':scope > .r93-fb');window.__rec2=[];var t0=performance.now();function snap(){window.__rec2.push([Math.round(performance.now()-t0),Math.round(fb.getBoundingClientRect().height),getComputedStyle(fb).maxHeight]);if(performance.now()-t0<760){requestAnimationFrame(snap);}}requestAnimationFrame(snap);f.querySelector(':scope > .r93-fc').click();return f.getAttribute('data-open');})()"
"$NODE" "$AB" wait 1000 >/dev/null 2>&1
echo "[曲线]"
"$NODE" "$AB" eval "JSON.stringify(window.__rec2)"
echo "[终态]"
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.r93-fold')[1];var fb=f.querySelector(':scope > .r93-fb');var c=getComputedStyle(fb);return JSON.stringify({open:f.getAttribute('data-open'),h:Math.round(fb.getBoundingClientRect().height),ovf:c.overflow,cls:fb.className,maxH:c.maxHeight});})()"

echo
echo "===== C) ⑥ 带 meta 的折叠头 hover（先收起它） ====="
"$NODE" "$AB" eval "(function(){function fwm(){return [].filter.call(document.querySelectorAll('.r93-fold'),function(x){return x.querySelector(':scope > .r93-fc .r93-t12l.r93-fm');});}var f=fwm()[0];if(!f)return 'none';f.id='r102fc';f.setAttribute('data-open','0');f.scrollIntoView({block:'center'});window.__fm=f;return JSON.stringify({meta:f.querySelector(':scope > .r93-fc .r93-t12l.r93-fm').textContent});})()"
"$NODE" "$AB" wait 1200 >/dev/null 2>&1
echo "[hover 前：命中测试]"
"$NODE" "$AB" eval "(function(){var fc=document.querySelector('#r102fc > .r93-fc');var r=fc.getBoundingClientRect();var cx=Math.round(r.left+r.width/2),cy=Math.round(r.top+r.height/2);var hit=document.elementFromPoint(cx,cy);return JSON.stringify({rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],cx:cx,cy:cy,hitCls:hit?hit.className:null,hitTag:hit?hit.tagName:null,inFc:!!(hit&&fc.contains(hit)),vh:window.innerHeight,hov:fc.matches(':hover')});})()"
"$NODE" "$AB" hover "#r102fc > .r93-fc" >/dev/null 2>&1
"$NODE" "$AB" wait 360 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var f=window.__fm;var fc=f.querySelector(':scope > .r93-fc');var m=fc.querySelector('.r93-t12l.r93-fm');var hit=document.elementFromPoint(Math.round(fc.getBoundingClientRect().left+5),Math.round(fc.getBoundingClientRect().top+11));return JSON.stringify({hov:fc.matches(':hover'),metaColor:m?getComputedStyle(m).color:'no-meta',metaTxt:m?(m.textContent||'').slice(0,18):null,titleColor:getComputedStyle(fc.querySelector('.r93-t14')).color,chevOp:getComputedStyle(fc.querySelector('.r93-fchev')).opacity,hitNow:hit?hit.className:null});})()"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102c-fcmeta-${W}.png" >/dev/null 2>&1
echo "  shot p102c-fcmeta-${W}.png"

echo
echo "===== D) ⑥ 带 meta 的展开头 hover ====="
"$NODE" "$AB" eval "(function(){var f=window.__fm;f.setAttribute('data-open','1');return 'opened';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 420 >/dev/null 2>&1
"$NODE" "$AB" hover "#r102fc > .r93-fh" >/dev/null 2>&1
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var fh=window.__fm.querySelector(':scope > .r93-fh');var m=fh.querySelector('.r93-t12l.r93-fm');return JSON.stringify({hov:fh.matches(':hover'),metaColor:m?getComputedStyle(m).color:'no-meta',metaTxt:m?(m.textContent||'').slice(0,18):null,titleColor:getComputedStyle(fh.querySelector('.r93-t14')).color});})()"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102c-fhmeta-${W}.png" >/dev/null 2>&1
echo "  shot p102c-fhmeta-${W}.png"
