#!/usr/bin/env bash
# 抓 base.html 对话框三个弹层的完整 DOM（落盘，避免输出截断）
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/base.html"
OUT="mg-work/r28/base-dumps"
mkdir -p "$OUT"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4

echo "=== 1. 添加 menu 完整 HTML ==="
$AB click "button[aria-label='添加']" >/dev/null 2>&1
sleep 0.8
$AB eval "document.querySelector('[role=menu][aria-label=\"添加内容\"]').outerHTML" > "$OUT/add-menu.html" 2>&1
wc -c "$OUT/add-menu.html"
$AB screenshot "mg-work/r28/base-add.png" >/dev/null 2>&1

echo ""
echo "=== 2. 技能 弹层 ==="
$AB eval "document.body.click();1" >/dev/null 2>&1
sleep 0.5
$AB click "button[aria-label='技能']" >/dev/null 2>&1
sleep 0.9
$AB eval "JSON.stringify((function(){var out=[];var all=document.querySelectorAll('div,ul');for(var i=0;i<all.length;i++){var e=all[i];if(e.children.length>0&&e.getBoundingClientRect().width>150&&/技能/.test(e.textContent)&&e.getBoundingClientRect().height>80&&e.getBoundingClientRect().height<520){out.push({cls:e.className&&e.className.slice?e.className.slice(0,80):'',role:e.getAttribute('role'),w:Math.round(e.getBoundingClientRect().width),h:Math.round(e.getBoundingClientRect().height),x:Math.round(e.getBoundingClientRect().left),y:Math.round(e.getBoundingClientRect().top)});}}return out.slice(0,8);})())"
$AB eval "(function(){var best=null;var all=document.querySelectorAll('div,ul');for(var i=0;i<all.length;i++){var e=all[i];var r=e.getBoundingClientRect();if(e.children.length>0&&r.width>150&&r.height>80&&r.height<520&&/技能/.test(e.textContent)){if(!best||r.width*r.height<best.getBoundingClientRect().width*best.getBoundingClientRect().height)best=e;}}return best?best.outerHTML:'NONE';})()" > "$OUT/skills.html" 2>&1
wc -c "$OUT/skills.html"
$AB screenshot "mg-work/r28/base-skills.png" >/dev/null 2>&1

echo ""
echo "=== 3. 大模型 popup 完整 HTML ==="
$AB eval "document.body.click();1" >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify([].map.call(document.querySelectorAll('.giencoder-select'),function(s,i){var t=s.querySelector('.giencoder-select-view-text');return t?{i:i,t:t.textContent}:null;}).filter(Boolean))"
$AB eval "(function(){var cs=document.querySelectorAll('.giencoder-select');for(var i=0;i<cs.length;i++){var t=cs[i].querySelector('.giencoder-select-view-text');if(t&&/DeepSeek/.test(t.textContent)){cs[i].querySelector('.giencoder-select-view').click();return 'clicked '+i;}}return 'not found';})()" >/dev/null 2>&1
sleep 0.8
$AB eval "(function(){var cs=document.querySelectorAll('.giencoder-select');for(var i=0;i<cs.length;i++){var t=cs[i].querySelector('.giencoder-select-view-text');if(t&&/DeepSeek/.test(t.textContent)){return cs[i].outerHTML;}}return 'NONE';})()" > "$OUT/model.html" 2>&1
wc -c "$OUT/model.html"
$AB screenshot "mg-work/r28/base-model.png" >/dev/null 2>&1
echo done
