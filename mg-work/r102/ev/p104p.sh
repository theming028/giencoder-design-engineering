#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
RAW=mg-work/r102/raw
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 2560 1440 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 3000 >/dev/null 2>&1

echo "===== 2560 浅色 · 结构 ====="
"$NODE" "$AB" eval "(function(){
 var hero=document.querySelector('main > div > div.flex-1.justify-center');
 var host=document.querySelector('.r93-conv-host');
 var box=hero.querySelector(':scope > div.mt-8');
 var t14=document.querySelector('.r93-t14');
 var pill=document.querySelector('.r93-pill');
 var vw=document.querySelector('.giencoder-select-view');
 return JSON.stringify({
  vw:innerWidth+'x'+innerHeight,
  hostZ:getComputedStyle(host).zIndex, heroZ:getComputedStyle(hero).zIndex,
  app:document.documentElement.getAttribute('data-r93-app'),
  tab:document.documentElement.getAttribute('data-r93-tab'),
  boxOp:getComputedStyle(box).opacity, boxPe:getComputedStyle(box).pointerEvents,
  t14:(t14?getComputedStyle(t14).fontSize:'-'),
  pill:(pill?getComputedStyle(pill).fontSize+'/'+getComputedStyle(pill).color:'-'),
  selectView:(vw?JSON.stringify([Math.round(vw.getBoundingClientRect().left),Math.round(vw.getBoundingClientRect().top),Math.round(vw.getBoundingClientRect().width)]):'-')
 });
})()"

echo "===== 2560 浅色 · 打开模型下拉（真鼠标）====="
"$NODE" "$AB" eval "(function(){
 var vs=document.querySelectorAll('.giencoder-select-view');
 for(var i=0;i<vs.length;i++){ var cl=(vs[i].textContent||'').trim();
   if(/DeepSeek|GLM|GPT|Claude|模型/.test(cl)){ vs[i].setAttribute('data-p104m','1'); return 'tag '+cl; } }
 return 'none';
})()"
"$NODE" "$AB" scrollintoview '[data-p104m="1"]' >/dev/null 2>&1
"$NODE" "$AB" click '[data-p104m="1"]' >/dev/null 2>&1
"$NODE" "$AB" sleep 420 >/dev/null 2>&1 || "$NODE" "$AB" wait 420 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
 var p=document.querySelector('.giencoder-select-popup.giencoder-popup-open');
 if(!p) return 'no-popup';
 var r=p.getBoundingClientRect();
 var items=p.querySelectorAll('.giencoder-select-option, li, [role=option]');
 var rows=[].slice.call(items).slice(0,5).map(function(e){var b=e.getBoundingClientRect();return {t:(e.textContent||'').trim().slice(0,20),y:Math.round(b.top),h:Math.round(b.height)};});
 return JSON.stringify({rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],z:getComputedStyle(p).zIndex,op:getComputedStyle(p).opacity,rows:rows});
})()"
"$NODE" "$AB" screenshot "" "$RAW/z2560-pop.png" >/dev/null 2>&1
echo "  shot z2560-pop.png"

echo "===== 2560 切到轨迹（真鼠标）====="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
 var lbs=document.querySelectorAll('.r93-conv-host [data-r93-tab]');
 for(var i=0;i<lbs.length;i++){ if(lbs[i].getAttribute('data-r93-tab')==='trace'){ lbs[i].setAttribute('data-p104tab','1'); return 'tag'; } }
 return 'none';
})()"
"$NODE" "$AB" click '[data-p104tab="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
 var host=document.querySelector('.r93-conv-host');
 var hero=document.querySelector('main > div > div.flex-1.justify-center');
 var box=hero.querySelector(':scope > div.mt-8');
 var tr=host.querySelector('.r93-trace');
 var r=box.getBoundingClientRect();
 return JSON.stringify({tab:document.documentElement.getAttribute('data-r93-tab'),heroDisp:getComputedStyle(hero).display,hostH:Math.round(host.getBoundingClientRect().height),boxRect:[Math.round(r.width),Math.round(r.height)],traceHidden:tr.hidden,traceTf:getComputedStyle(tr).transform});
})()"
"$NODE" "$AB" screenshot "" "$RAW/z2560-trace.png" >/dev/null 2>&1
echo "  shot z2560-trace.png"

echo "===== 2560 暗色 · token ====="
"$NODE" "$AB" eval "(function(){document.documentElement.setAttribute('giencoder-theme','dark');return 'dark';})()"
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
 var cs=getComputedStyle(document.documentElement);
 var ks=['--r93-ioc','--r93-ioc2','--r93-ok','--r93-warn-ic','--r93-tag-ic','--r93-dim','--r93-meta','--r93-line','--r93-pillc'];
 var o={};ks.forEach(function(k){o[k]=cs.getPropertyValue(k).trim();});
 return JSON.stringify(o);
})()"
echo "===== 2560 暗色 · 打开模型下拉 ====="
"$NODE" "$AB" eval "(function(){
 var lbs=document.querySelectorAll('.r93-conv-host [data-r93-tab]');
 for(var i=0;i<lbs.length;i++){ if(lbs[i].getAttribute('data-r93-tab')==='chat'){ lbs[i].click(); } }
 return 'back-chat';
})()" >/dev/null
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
 var vs=document.querySelectorAll('.giencoder-select-view');
 for(var i=0;i<vs.length;i++){ var cl=(vs[i].textContent||'').trim();
   if(/DeepSeek|GLM|GPT|Claude|模型/.test(cl)){ vs[i].setAttribute('data-p104m2','1'); return 'tag '+cl; } }
 return 'none';
})()"
"$NODE" "$AB" scrollintoview '[data-p104m2="1"]' >/dev/null 2>&1
"$NODE" "$AB" click '[data-p104m2="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 420 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
 var p=document.querySelector('.giencoder-select-popup.giencoder-popup-open');
 if(!p) return 'no-popup';
 var r=p.getBoundingClientRect();
 return JSON.stringify({rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],z:getComputedStyle(p).zIndex,bg:getComputedStyle(p).backgroundColor});
})()"
"$NODE" "$AB" screenshot "" "$RAW/z2560-dark-pop.png" >/dev/null 2>&1
echo "  shot z2560-dark-pop.png"
"$NODE" "$AB" screenshot "" "$RAW/z2560-dark.png" >/dev/null 2>&1
echo "  shot z2560-dark.png"
