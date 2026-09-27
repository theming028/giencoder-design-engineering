#!/usr/bin/env bash
# 第27轮第4项复测：任务看板三标签配色（亮/暗两态）
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3

echo "=== 亮色：三标签实测 ==="
$AB eval "JSON.stringify((function(){var want=['拆分需求项','拆分需求条目','拆分子条目'];var seen={},ts=document.querySelectorAll('.kb-tag');for(var i=0;i<ts.length;i++){var t=ts[i],k=t.textContent.trim();if(want.indexOf(k)<0||seen[k])continue;var c=getComputedStyle(t);var r=t.getBoundingClientRect();seen[k]={cls:t.className,bg:c.backgroundColor,color:c.color,w:Math.round(r.width),h:Math.round(r.height),fs:c.fontSize,pad:c.padding};}return seen;})())"

echo ""
echo "=== 对照：TASK 灰标签 / 优先级标签未被误伤 ==="
$AB eval "JSON.stringify((function(){var o={};var n=document.querySelector('.kb-tag--num');var hn=document.querySelector('.kb-tag--high');var mn=document.querySelector('.kb-tag--mid');var ln=document.querySelector('.kb-tag--low');o.num=n?{bg:getComputedStyle(n).backgroundColor,color:getComputedStyle(n).color}:null;o.high=hn?{bg:getComputedStyle(hn).backgroundColor,color:getComputedStyle(hn).color}:null;o.mid=mn?{bg:getComputedStyle(mn).backgroundColor,color:getComputedStyle(mn).color}:null;o.low=ln?{bg:getComputedStyle(ln).backgroundColor,color:getComputedStyle(ln).color}:null;return o;})())"

echo ""
echo "=== 暗色：三标签与暗色前保持一致（token 自适应） ==="
$AB eval "document.documentElement.setAttribute('giencoder-theme','dark');1" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var want=['拆分需求项','拆分需求条目','拆分子条目'];var seen={},ts=document.querySelectorAll('.kb-tag');for(var i=0;i<ts.length;i++){var t=ts[i],k=t.textContent.trim();if(want.indexOf(k)<0||seen[k])continue;var c=getComputedStyle(t);seen[k]={bg:c.backgroundColor,color:c.color};}return seen;})())"
$AB screenshot "mg-work/r27/verify-kanban-dark.png" >/dev/null 2>&1
$AB eval "document.documentElement.setAttribute('giencoder-theme','light');1" >/dev/null 2>&1

echo ""
echo "=== 截图 ==="
$AB screenshot "mg-work/r27/verify-kanban2.png" >/dev/null 2>&1
echo "  -> mg-work/r27/verify-kanban2.png"
