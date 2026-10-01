#!/usr/bin/env bash
# 用户报「右栏看不到变化」—— 实测现状：默认开合态 / 标签栏是否渲染 / 按钮是否存在
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"

AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 3000 >/dev/null 2>&1

echo "### 0 页面级：脚本/样式块数 + 标记存在性"
AB eval "JSON.stringify({title:document.title,scripts:document.scripts.length,styles:document.querySelectorAll('style').length})" 2>&1

echo "### 1 默认态（未点任何东西）"
AB eval "JSON.stringify({slotExists:!!document.getElementById('av-browse-slot'),slotPlaced:(document.getElementById('av-browse-slot')||{classList:{contains:function(){return null;}}}).classList.contains('av-slot-placed'),ON:(document.querySelector('div:has(> main)')||{classList:{contains:function(){return null;}}}).classList.contains('av-browse-on'),browseDisplay:(function(){var p=document.querySelector('.td-browse');return p?getComputedStyle(p).display:null;})(),slotRect:(function(){var e=document.getElementById('av-browse-slot');if(!e)return null;var r=e.getBoundingClientRect();return[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];})(),tabs:document.querySelectorAll('.td-browse-tab').length,tabsHTML:(function(){var t=document.querySelector('.td-browse-tabs');return t?t.textContent.trim().slice(0,60):null;})(),toggleBtn:!!document.querySelector('.r93-baract[data-r93-browse]'),toggleRect:(function(){var b=document.querySelector('.r93-baract[data-r93-browse]');if(!b)return null;var r=b.getBoundingClientRect();return[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];})()})" 2>&1

AB screenshot "$OUT/x1-default.png" >/dev/null 2>&1

echo "### 2 点「打开侧栏」后"
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
AB eval "JSON.stringify({ON:(document.querySelector('div:has(> main)')||{classList:{contains:function(){return null;}}}).classList.contains('av-browse-on'),slotW:Math.round(document.getElementById('av-browse-slot').getBoundingClientRect().width),panelRect:(function(){var r=document.querySelector('.td-browse').getBoundingClientRect();return[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];})(),tabCount:document.querySelectorAll('.td-browse-tab').length,tabText:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.textContent.trim();}),addBtn:!!document.querySelector('[data-td-add]'),maxBtn:!!document.querySelector('[data-td-max]'),closeBtn:!!document.querySelector('[data-td-browse-close]')})" 2>&1

AB screenshot "$OUT/x2-opened.png" >/dev/null 2>&1

echo "### 3 打开「+」菜单（看五选一）"
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "JSON.stringify({menuOpen:!!(document.querySelector('.td-mod-menu')&&!document.querySelector('.td-mod-menu').hasAttribute('hidden')),items:[].map.call(document.querySelectorAll('[data-td-open-mod]'),function(b){return b.getAttribute('data-td-open-mod');})})" 2>&1
AB screenshot "$OUT/x3-addmenu.png" >/dev/null 2>&1

echo "### 4 逐一开到审查/终端/浏览器/侧边聊天（各截一张）"
for m in review terminal browser side; do
  AB open "$URL" >/dev/null 2>&1
  AB set viewport 1440 900 >/dev/null 2>&1
  AB wait 2600 >/dev/null 2>&1
  AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
  AB wait 700 >/dev/null 2>&1
  AB click "[data-td-add]" >/dev/null 2>&1
  AB wait 400 >/dev/null 2>&1
  AB click "[data-td-open-mod=\"$m\"]" >/dev/null 2>&1
  AB wait 700 >/dev/null 2>&1
  AB eval "JSON.stringify({mod:'$m',tabs:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.textContent.trim();}),panes:[].map.call(document.querySelectorAll('[data-td-pane]'),function(p){return p.getAttribute('data-td-pane')+(p.hasAttribute('hidden')?':hidden':':VISIBLE');})})" 2>&1
  AB screenshot "$OUT/x4-$m.png" >/dev/null 2>&1
done

echo "### done"
