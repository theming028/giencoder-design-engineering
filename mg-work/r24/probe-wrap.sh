#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/task-detail.html"
$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8
echo "=== 卡片是否换行（设计稿：2 个附件并排，卡片 294 宽 / gap 8） ==="
$AB eval "JSON.stringify((function(){var out=[];document.querySelectorAll('.td-files').forEach(function(f,i){var cs=f.querySelectorAll('.td-file');out.push({sec:i,n:cs.length,tops:Array.from(cs).map(function(c){return Math.round(c.getBoundingClientRect().top);}),lefts:Array.from(cs).map(function(c){return Math.round(c.getBoundingClientRect().left);}),ws:Array.from(cs).map(function(c){return Math.round(c.getBoundingClientRect().width);}),wrapW:Math.round(f.getBoundingClientRect().width),scrollW:f.scrollWidth});});return out;})())"
echo ""
echo "=== 附件区可用宽 vs 2 卡所需宽 ==="
$AB eval "JSON.stringify((function(){var f=document.querySelector('.td-files');var c=f.querySelector('.td-file--lg');var need=c.getBoundingClientRect().width*2+8;return {available:Math.round(f.getBoundingClientRect().width),need:Math.round(need),fits:need<=f.getBoundingClientRect().width};})())"
$AB screenshot "mg-work/r24/r24-probe.png" >/dev/null 2>&1
echo "shot ok"
