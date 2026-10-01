#!/usr/bin/env bash
# 两问诊断：
#   ① 审查「显示选项」(.td-rv-opts) 点开后关不掉
#   ② 侧边聊天样式与主对话（r93-scroll）不一致
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"

CS='function cs(sel,sub){var e=sub?document.querySelector(sel):document.querySelector(sel);if(!e)return null;var c=getComputedStyle(e);return{fs:c.fontSize,lh:c.lineHeight,color:c.color,bg:c.backgroundColor,pad:c.padding,br:c.borderRadius,fw:c.fontWeight,gap:c.gap,bor:c.border,ff:c.fontFamily.slice(0,24)};}'

echo "############ A 显示选项浮窗开合 ############"
AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2800 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1

echo "--- A1 初始（应 hidden）"
AB eval "JSON.stringify({hidden:document.querySelector('.td-rv-opts').hasAttribute('hidden'),inBar:!!document.querySelector('.td-browse-bar .td-rv-opts'),inPane:!!document.querySelector('.td-browse-body ~ * .td-rv-opts')||!!document.querySelector('[data-td-pane=\"review\"] .td-rv-opts'),optsParent:(function(){var e=document.querySelector('.td-rv-opts');return e?e.parentElement.className:null;})()})" 2>&1

echo "--- A2 点 ⋯ 打开"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({hidden:document.querySelector('.td-rv-opts').hasAttribute('hidden'),display:getComputedStyle(document.querySelector('.td-rv-opts')).display,rect:(function(){var r=document.querySelector('.td-rv-opts').getBoundingClientRect();return[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];})()})" 2>&1
AB screenshot "$OUT/y1-opts-open.png" >/dev/null 2>&1

echo "--- A3 点空白处（主对话区）—— 应关闭"
AB eval "document.querySelector('.r93-scroll').getBoundingClientRect().x" >/dev/null 2>&1
AB click ".r93-scroll" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({hidden:document.querySelector('.td-rv-opts').hasAttribute('hidden')})" 2>&1
AB screenshot "$OUT/y2-opts-after-outside.png" >/dev/null 2>&1

echo "--- A4 再点 ⋯ 打开，然后 Esc —— 应关闭"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({afterOpen:document.querySelector('.td-rv-opts').hasAttribute('hidden')})" 2>&1
AB press Escape >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({afterEsc:document.querySelector('.td-rv-opts').hasAttribute('hidden')})" 2>&1

echo "--- A5 打开后选「并排」—— 菜单应关闭"
AB eval "JSON.stringify({hidden0:document.querySelector('.td-rv-opts').hasAttribute('hidden')})" 2>&1
AB click '[data-td-rv-view="split"]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({afterPick:document.querySelector('.td-rv-opts').hasAttribute('hidden'),split:document.querySelector('.td-rv-body').classList.contains('is-split')})" 2>&1
AB screenshot "$OUT/y3-opts-after-pick.png" >/dev/null 2>&1

echo
echo "############ B 侧边聊天 vs 主对话 ############"
AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2800 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 700 >/dev/null 2>&1
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="side"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1

echo "--- B1 主对话（r93-scroll 内）"
AB eval "$CS"'JSON.stringify({userBub:cs(".r93-bubi"),userTxt:cs(".r93-bubi .r93-t14"),pill:cs(".r93-pill"),asstHead:cs(".r93-ahd2",true),asstT14:cs(".r93-it .r93-t14"),asstT14b:cs(".r93-it .r93-t14b"),t12:cs(".r93-t12"),t12l:cs(".r93-t12l"),att:cs(".r93-att"),umeta:cs(".r93-umeta"),it:cs(".r93-it")})' 2>&1

echo "--- B2 侧边聊天"
AB eval "$CS"'JSON.stringify({tag:cs(".td-side-tag"),hint:cs(".td-side-hint"),body:cs(".td-side-body"),quote:cs(".td-side-quote"),av:cs(".td-side-av"),bubAI:cs(".td-side-msg:not(.is-user) .td-side-bub"),bubUser:cs(".td-side-msg.is-user .td-side-bub"),ta:cs(".td-side-ta"),send:cs(".td-side-send"),in:cs(".td-side-in")})' 2>&1

echo "--- B3 侧边聊天 HTML 结构"
AB eval "document.querySelector('.td-side').outerHTML.slice(0,1800)" 2>&1
AB screenshot "$OUT/y4-sidechat.png" >/dev/null 2>&1

echo "--- B4 全局：AI 侧「助手正文」用的类（确认 15px 档）"
AB eval "JSON.stringify({t14:getComputedStyle(document.querySelector('.r93-it .r93-t14')).fontSize,t12l:(function(){var e=document.querySelector('.r93-t12l');return e?getComputedStyle(e).fontSize:null;})(),body3:getComputedStyle(document.documentElement).getPropertyValue('--font-size-body-3'),body2:getComputedStyle(document.documentElement).getPropertyValue('--font-size-body-2'),body1:getComputedStyle(document.documentElement).getPropertyValue('--font-size-body-1'),uiFs:getComputedStyle(document.documentElement).getPropertyValue('--ui-fs')})" 2>&1

echo "############ done ############"
