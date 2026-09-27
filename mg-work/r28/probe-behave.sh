#!/usr/bin/env bash
# 探测 base.html 三个功能的点击结果（写入 textarea？开关状态？）
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/base.html"

TA='JSON.stringify((function(){var t=document.querySelector("textarea");return t?t.value:"NO-TEXTAREA";})())'

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4

echo "=== 0. 初始 textarea ==="
$AB eval "$TA"

echo ""
echo "=== 1. 添加 → 点「添加本地文件」 ==="
$AB click "button[aria-label='添加']" >/dev/null 2>&1; sleep 0.7
echo "  菜单项文案: $($AB eval "JSON.stringify([].map.call(document.querySelectorAll('.add-menu-item'),function(e){return e.textContent.trim();}))")"
echo "  有无隐藏 file input: $($AB eval "JSON.stringify([].map.call(document.querySelectorAll('input[type=file]'),function(e){return {cls:e.className,hidden:e.hidden,disp:getComputedStyle(e).display};}))")"
$AB eval "(function(){var it=document.querySelectorAll('.add-menu-item')[0];it.dispatchEvent(new MouseEvent('click',{bubbles:true}));return 1;})()" >/dev/null 2>&1
sleep 0.8
echo "  点击后 textarea: $($AB eval "$TA")"
echo "  菜单仍开? $($AB eval "JSON.stringify({menuItems:document.querySelectorAll('.add-menu-item').length,expanded:document.querySelector('button[aria-label=添加]').getAttribute('aria-expanded')})")"

echo ""
echo "=== 2. 技能 → 点第 3 行（第一个真技能） ==="
$AB eval "document.body.click();1" >/dev/null 2>&1; sleep 0.5
$AB click "button[aria-label='技能']" >/dev/null 2>&1; sleep 0.9
echo "  技能行文案: $($AB eval "JSON.stringify([].map.call(document.querySelectorAll('.skill-row'),function(e){return e.textContent.trim().slice(0,40);}))")"
$AB eval "(function(){var rs=document.querySelectorAll('.skill-row');var i=rs.length>2?2:0;rs[i].dispatchEvent(new MouseEvent('click',{bubbles:true}));return i;})()" >/dev/null 2>&1
sleep 0.8
echo "  点击后 textarea: $($AB eval "$TA")"
echo "  面板仍开? $($AB eval "JSON.stringify({pop:!!document.querySelector('.skill-pop-list'),expanded:document.querySelector('button[aria-label=技能]').getAttribute('aria-expanded')})")"

echo ""
echo "=== 3. Esc / 外部点击 关闭 ==="
$AB click "button[aria-label='技能']" >/dev/null 2>&1; sleep 0.7
$AB eval "document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));1" >/dev/null 2>&1; sleep 0.6
echo "  Esc 后: $($AB eval "JSON.stringify({pop:!!document.querySelector('.skill-pop-list'),expanded:document.querySelector('button[aria-label=技能]').getAttribute('aria-expanded')})")"
$AB click "button[aria-label='技能']" >/dev/null 2>&1; sleep 0.7
$AB eval "document.querySelector('main').dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));document.querySelector('main').click();1" >/dev/null 2>&1; sleep 0.6
echo "  外部点击后: $($AB eval "JSON.stringify({pop:!!document.querySelector('.skill-pop-list'),expanded:document.querySelector('button[aria-label=技能]').getAttribute('aria-expanded')})")"

echo ""
echo "=== 4. 大模型：打开 → 选第二项 ==="
$AB eval "document.body.click();1" >/dev/null 2>&1; sleep 0.5
$AB eval "(function(){var cs=document.querySelectorAll('.giencoder-select');for(var i=0;i<cs.length;i++){var t=cs[i].querySelector('.giencoder-select-view-text');if(t&&/DeepSeek/.test(t.textContent)){cs[i].querySelector('.giencoder-select-view').click();return 1;}}return 0;})()" >/dev/null 2>&1
sleep 0.7
echo "  打开态: $($AB eval "JSON.stringify((function(){var cs=document.querySelectorAll('.giencoder-select');for(var i=0;i<cs.length;i++){var t=cs[i].querySelector('.giencoder-select-view-text');if(t&&/DeepSeek/.test(t.textContent)){var p=cs[i].querySelector('.giencoder-select-popup');return {popCls:p.className,disp:getComputedStyle(p).display,exp:cs[i].querySelector('.giencoder-select-view').getAttribute('aria-expanded'),opts:[].map.call(p.querySelectorAll('.model-dropdown-menu-item'),function(e){return e.textContent.trim();})};}}return null;})())")"
$AB eval "(function(){var cs=document.querySelectorAll('.giencoder-select');for(var i=0;i<cs.length;i++){var t=cs[i].querySelector('.giencoder-select-view-text');if(t&&/DeepSeek/.test(t.textContent)){var it=cs[i].querySelectorAll('.model-dropdown-menu-item');if(it.length>1){it[1].dispatchEvent(new MouseEvent('click',{bubbles:true}));}return 1;}}return 0;})()" >/dev/null 2>&1
sleep 0.7
echo "  选第二项后: $($AB eval "JSON.stringify((function(){var out=[];var cs=document.querySelectorAll('.giencoder-select');for(var i=0;i<cs.length;i++){var t=cs[i].querySelector('.giencoder-select-view-text');if(t)out.push({text:t.textContent,pop:getComputedStyle(cs[i].querySelector('.giencoder-select-popup')).display,exp:cs[i].querySelector('.giencoder-select-view').getAttribute('aria-expanded')});}return out;})())")"

echo ""
echo "=== 5. 技能面板的键盘导航是否绑定 ==="
$AB eval "document.body.click();1" >/dev/null 2>&1; sleep 0.5
$AB click "button[aria-label='技能']" >/dev/null 2>&1; sleep 0.8
echo "  初始 active 行: $($AB eval "JSON.stringify([].map.call(document.querySelectorAll('.skill-row'),function(e,i){return e.classList.contains('skill-row-active')?i:null;}).filter(function(v){return v!==null;}))")"
$AB eval "var ta=document.querySelector('textarea');if(ta){ta.focus();}1" >/dev/null 2>&1
$AB eval "document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowDown',bubbles:true}));1" >/dev/null 2>&1; sleep 0.3
echo "  ArrowDown 后 active 行: $($AB eval "JSON.stringify([].map.call(document.querySelectorAll('.skill-row'),function(e,i){return e.classList.contains('skill-row-active')?i:null;}).filter(function(v){return v!==null;}))")"
