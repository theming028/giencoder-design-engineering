#!/usr/bin/env bash
# 第十三拍边界与回归：① 面板不再遮挡 main 顶部工具条 · ② 审查模块里 diff 折叠图标的可见几何 ·
#                     ③ 暗色档配色 · ④ `--ui-fs=18` 字号杠杆 · ⑤ 窄档。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108n.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS" | tail -1; }
fmt() { python -c "
import sys, json
for ln in sys.stdin:
    ln = ln.strip()
    if ln.startswith('\"{'):
        try: print(json.dumps(json.loads(json.loads(ln)), ensure_ascii=False))
        except Exception: print('PARSE-FAIL', ln[:100])
    elif ln: print(ln)
"; }

echo "### open（保持右栏关闭）"
run open "$URL" >/dev/null
run set viewport 1440 900 >/dev/null
run wait 3800 >/dev/null

echo "=== [A] 遮挡回归：面板没盖住工具条上那两枚按钮 ==="
run eval "JSON.stringify((function(){
  function R(e){var b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)];}
  var out={};
  [['全屏','button[aria-label=\\\"全屏\\\"]'],['打开侧栏','.r93-baract[data-r93-browse]']].forEach(function(p){
    var b=document.querySelector(p[1]);
    if(!b){out[p[0]]={found:false};return;}
    var r=b.getBoundingClientRect();
    var t=document.elementFromPoint(r.x+r.width/2, r.y+r.height/2);
    out[p[0]]={rect:R(b), hitSelf: !!(t && b.contains(t)), hit: t?String(t.className).slice(0,40):null};
  });
  var host=document.getElementById('av-zd-status');
  out.zdTop = host ? Math.round(host.getBoundingClientRect().y) : null;
  return out;})())" | fmt

echo "=== [B] 切到「审查」模块 ⇒ 量 diff 折叠图标的可见几何 ==="
run click ".r93-baract[data-r93-browse]" >/dev/null
run wait 1000 >/dev/null
run click ".td-browse-add" >/dev/null
run wait 400 >/dev/null
run click "[data-td-open-mod='review']" >/dev/null
run wait 800 >/dev/null
run eval "JSON.stringify((function(){
  var cv=document.querySelector('.td-diff-cv');
  if(!cv) return {found:false};
  var b=cv.getBoundingClientRect(); var c=getComputedStyle(cv);
  var tg=document.querySelector('.td-diff-toggle');
  var tc=tg?getComputedStyle(tg):null;
  return {found:true, rect:[Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)],
          color:c.color, w:c.width, h:c.height,
          toggleColor: tc?tc.color:null, toggleDisplay: tc?tc.display:null,
          cardCount: document.querySelectorAll('.td-diff').length,
          firstCard: (function(){var d=document.querySelector('.td-diff'); if(!d)return null; var r=d.getBoundingClientRect(); var s=getComputedStyle(d);
            return {rect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)], radius:s.borderTopLeftRadius, border:s.borderTopColor, bg:s.backgroundColor};})()};
})())" | fmt

echo "=== [C] 暗色档 ==="
run eval "document.documentElement.setAttribute('giencoder-theme','dark'); 'ok'" >/dev/null
run wait 500 >/dev/null
run eval "JSON.stringify((function(){
  function S(e){return e?getComputedStyle(e):null;}
  var host=document.getElementById('av-zd-status');
  var card=host?host.querySelector('[data-zd-card]'):null;
  var cs=S(card);
  var t=host?host.querySelector('.zd-sec-t'):null;
  var mini=host?host.querySelector('[data-zd-mini]'):null;
  return {cardBg:cs?cs.backgroundColor:null, cardBorder:cs?cs.borderTopColor:null, nameColor:host?S(host.querySelector('.zd-name')).color:null,
          secColor:t?S(t).color:null, miniBg:mini?S(mini).backgroundColor:null, miniBorder:mini?S(mini).borderTopColor:null,
          todoColor:host?S(host.querySelector('.zd-todo li')).color:null};
})())" | fmt
run eval "document.documentElement.removeAttribute('giencoder-theme'); 'ok'" >/dev/null
run wait 300 >/dev/null

echo "=== [D] 字号杠杆 --ui-fs = 18 ==="
run eval "document.documentElement.style.setProperty('--ui-fs','18'); 'ok'" >/dev/null
run wait 600 >/dev/null
run eval "JSON.stringify((function(){
  function S(e){return e?getComputedStyle(e):null;} function R(e){var b=e.getBoundingClientRect();return [Math.round(b.width),Math.round(b.height)];}
  var host=document.getElementById('av-zd-status');
  var head=host.querySelector('.zd-head'), secH=host.querySelector('.zd-sec-h'), row=host.querySelector('.zd-row');
  return {ratio:S(document.documentElement).getPropertyValue('--ui-fs-ratio').trim(),
          headH:Math.round(head.getBoundingClientRect().height), headFS:S(head).fontSize,
          secHH:Math.round(secH.getBoundingClientRect().height), secHFS:S(secH).fontSize,
          rowH:Math.round(row.getBoundingClientRect().height), rowFS:S(row).fontSize,
          cardR:R(host.querySelector('[data-zd-card]')), miniR:R(host.querySelector('[data-zd-mini]'))};
})())" | fmt
run eval "document.documentElement.style.removeProperty('--ui-fs'); 'ok'" >/dev/null

echo "=== [E] 窄档 620 宽 ==="
run set viewport 620 900 >/dev/null
run wait 700 >/dev/null
run eval "JSON.stringify((function(){
  function R(e){var b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)];}
  var m=document.querySelector('main'), host=document.getElementById('av-zd-status'), card=host.querySelector('[data-zd-card]');
  return {mainR:R(m), cardR:R(card), overflowRight: (R(card)[0]+R(card)[2]) - (R(m)[0]+R(m)[2])};
})())" | fmt
