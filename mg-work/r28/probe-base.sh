#!/usr/bin/env bash
# 抓 pages/base.html 对话框底部「添加 / 技能 / 选择大模型」的真实弹层 DOM 与行为
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/base.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4

echo "=== A. 找到底部工具栏的三个按钮 ==="
$AB eval "JSON.stringify((function(){var out=[].map.call(document.querySelectorAll('button[aria-label]'),function(b){var r=b.getBoundingClientRect();return {label:b.getAttribute('aria-label'),x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),exp:b.getAttribute('aria-expanded')};});return out.filter(function(o){return /添加|技能|大模型|发送|提示词|分身/.test(o.label);});})())"

echo ""
echo "=== B. 点「添加」后 ==="
$AB eval "(function(){var b=[].find.call(document.querySelectorAll('button[aria-label=添加]'),function() {return true;});return 1;})()" >/dev/null 2>&1
$AB click "button[aria-label='添加']" >/dev/null 2>&1
sleep 0.7
$AB eval "JSON.stringify((function(){var b=document.querySelector('button[aria-label=添加]');var box=b.parentElement;var pop=box.querySelector('[role=menu],[role=listbox],[class*=popup]');return {expanded:b.getAttribute('aria-expanded'),siblingCount:box.children.length,popup:pop?{cls:pop.className,role:pop.getAttribute('role'),html:pop.outerHTML.slice(0,3000),display:getComputedStyle(pop).display,vis:getComputedStyle(pop).visibility,op:getComputedStyle(pop).opacity}:null};})())"

echo ""
echo "=== C. 点「技能」后 ==="
$AB eval "document.body.click();1" >/dev/null 2>&1
sleep 0.4
$AB click "button[aria-label='技能']" >/dev/null 2>&1
sleep 0.7
$AB eval "JSON.stringify((function(){var b=document.querySelector('button[aria-label=技能]');var box=b.parentElement;return {expanded:b.getAttribute('aria-expanded'),cls:b.className.slice(0,200),parentCls:box.className,parentHTML:box.outerHTML.slice(0,3500)};})())"
$AB screenshot "mg-work/r28/base-skills.png" >/dev/null 2>&1

echo ""
echo "=== D. 点大模型选择 ==="
$AB eval "document.body.click();1" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var cs=document.querySelectorAll('.giencoder-select');var out=[];for(var i=0;i<cs.length;i++){var v=cs[i].querySelector('.giencoder-select-view-text');if(v&&/DeepSeek|GLM|模型/.test(v.textContent)){out.push({idx:i,text:v.textContent,html:cs[i].outerHTML.slice(0,1200)});}}return out;})())"
