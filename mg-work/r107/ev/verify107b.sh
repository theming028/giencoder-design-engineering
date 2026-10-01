#!/usr/bin/env bash
# r107 第二拍验收：① 显示选项浮窗四条关闭路径 ② 侧边聊天逐值对齐主对话
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"

# 简单探针（每条都是独立表达式，避免引号嵌套）
HID="document.querySelector('.td-rv-opts').hasAttribute('hidden')"
PANEL="document.querySelector('div:has(> main)').classList.contains('av-browse-on')"
MODHID="document.querySelector('.td-mod-menu').hasAttribute('hidden')"
CS='function cs(s){var e=document.querySelector(s);if(!e)return null;var c=getComputedStyle(e);return{fs:c.fontSize,lh:c.lineHeight,color:c.color,bg:c.backgroundColor,pad:c.padding,br:c.borderRadius};}'

openreview() {
  AB open "$URL" >/dev/null 2>&1
  AB set viewport 1440 900 >/dev/null 2>&1
  AB wait 2800 >/dev/null 2>&1
  AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
  AB wait 800 >/dev/null 2>&1
  AB click "[data-td-add]" >/dev/null 2>&1
  AB wait 400 >/dev/null 2>&1
  AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
  AB wait 900 >/dev/null 2>&1
}

echo "############ A 显示选项浮窗：四条关闭路径 ############"
echo "--- A1 初始 hidden（期望 true）"
openreview
AB eval "$HID" 2>&1

echo "--- A2 点 ⋯ 后 hidden（期望 false）"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "$HID" 2>&1
AB screenshot "$OUT/z1-opts-open.png" >/dev/null 2>&1

echo "--- A3 ★ 点浮窗外空白后 hidden（期望 true）"
AB click ".r93-scroll" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "$HID" 2>&1

echo "--- A4 ★ 打开后点菜单项「并排视图」：hidden + is-split + aria-checked"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-rv-view="split"]' >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "document.querySelector('.td-rv-opts').hasAttribute('hidden')+' | ' + document.querySelector('.td-rv-body').classList.contains('is-split') + ' | ' + document.querySelector('[data-td-rv-view=\"split\"]').getAttribute('aria-checked')" 2>&1
AB screenshot "$OUT/z2-opts-split.png" >/dev/null 2>&1

echo "--- A5 ★ 打开后按 Esc：浮窗关、侧栏留"
AB click '[data-td-rv-view="unified"]' >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({before_hidden:$HID,panelOn:$PANEL})" 2>&1
AB press Escape >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({after_hidden:$HID,panelOn:$PANEL})" 2>&1
AB screenshot "$OUT/z3-esc-scoped.png" >/dev/null 2>&1

echo "--- A6 回归：再按一次 Esc 关整条侧栏（期望 false）"
AB press Escape >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "$PANEL" 2>&1

echo "--- A7 回归：`+` 模块菜单外点仍可关（期望 true）"
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 700 >/dev/null 2>&1
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "$MODHID" 2>&1
AB click ".r93-scroll" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "$MODHID" 2>&1

echo
echo "############ B 侧边聊天 vs 主对话（逐值） ############"
AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2800 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 700 >/dev/null 2>&1
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="side"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1

echo "--- B1 主对话基准（对照用）"
AB eval "$CS"'JSON.stringify({userTxt:cs(".r93-bubi .r93-t14"),userBub:cs(".r93-bubi"),asst:cs(".r93-it .r93-t14"),t12l:cs(".r93-t12l")})' 2>&1

echo "--- B2 侧边聊天（改后）"
AB eval "$CS"'JSON.stringify({ai:cs(".td-side-msg.is-ai .td-side-bub"),user:cs(".td-side-msg.is-user .td-side-bub"),quote:cs(".td-side-quote"),ta:cs(".td-side-ta"),av:(function(){var e=document.querySelector(".td-side-av");if(!e)return null;var c=getComputedStyle(e);return{w:c.width,h:c.height,bg:c.backgroundColor,hasSvg:!!e.querySelector("svg")};})()})' 2>&1

echo "--- B3 头像注入 / 消息计数"
AB eval "JSON.stringify({avCount:document.querySelectorAll('.td-side-av').length,avWithSvg:document.querySelectorAll('.td-side-av > svg').length,aiMsg:document.querySelectorAll('.td-side-msg.is-ai').length,userMsg:document.querySelectorAll('.td-side-msg.is-user').length,avTextLen:document.querySelector('.td-side-av').textContent.length})" 2>&1
AB screenshot "$OUT/z4-sidechat-new.png" >/dev/null 2>&1

echo "--- B4 暗色档（用户气泡应 = --r93-bubble 暗档 #24314C = rgb(36,49,76)）"
AB eval "document.documentElement.setAttribute('giencoder-theme','dark');'ok'" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "$CS"'JSON.stringify({user:cs(".td-side-msg.is-user .td-side-bub"),ai:cs(".td-side-msg.is-ai .td-side-bub"),mainUser:cs(".r93-bubi")})' 2>&1
AB screenshot "$OUT/z5-sidechat-dark.png" >/dev/null 2>&1
AB eval "document.documentElement.removeAttribute('giencoder-theme');'ok'" >/dev/null 2>&1

echo "--- B5 字号杠杆 --ui-fs=18（侧聊 ✕ 主对话 ✕ 溢出）"
AB eval "document.documentElement.style.setProperty('--ui-fs','18');'ok'" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "$CS"'JSON.stringify({sideAI:cs(".td-side-msg.is-ai .td-side-bub"),sideUser:cs(".td-side-msg.is-user .td-side-bub"),sideTa:cs(".td-side-ta"),sideQuote:cs(".td-side-quote"),mainT14:cs(".r93-it .r93-t14"),mainT12l:cs(".r93-t12l"),mainComposer:(function(){var e=document.querySelector("textarea[placeholder*=\u63cf\u8ff0]");return e?getComputedStyle(e).fontSize+"/"+getComputedStyle(e).lineHeight:null;})(),av:getComputedStyle(document.querySelector(".td-side-av")).width,overflow:document.querySelector(".td-side").scrollWidth-document.querySelector(".td-side").clientWidth})' 2>&1
AB screenshot "$OUT/z6-sidechat-fs18.png" >/dev/null 2>&1
AB eval "document.documentElement.style.removeProperty('--ui-fs');'ok'" >/dev/null 2>&1

echo "############ done ############"
