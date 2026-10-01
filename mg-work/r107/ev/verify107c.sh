#!/usr/bin/env bash
# r107 第三拍验收：① 侧边聊天彻底移除 ② 并排视图折叠 ③ 折叠全部⇄展开全部
#                  ④ 审查显示选项八项 / 范围 / 提交下拉 / 暂存·撤销 ⑤ 摘要模块 ⑥ 快捷键
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"

CS='function cs(s){var e=document.querySelector(s);if(!e)return null;var c=getComputedStyle(e);return{fs:c.fontSize,lh:c.lineHeight,color:c.color,bg:c.backgroundColor,ws:c.whiteSpace,op:c.opacity,d:c.display};}'
# .td-rv-body 上的开关类；折叠文案；第 1 个文件的折叠态
RV="JSON.stringify({wrap:document.querySelector('.td-rv-body').classList.contains('is-wrap'),hidws:document.querySelector('.td-rv-body').classList.contains('is-hidws'),worddiff:document.querySelector('.td-rv-body').classList.contains('is-worddiff'),split:document.querySelector('.td-rv-body').classList.contains('is-split')})"
FOLD="document.querySelector('[data-td-rv-fold-name]').textContent"
SPLITD="getComputedStyle(document.querySelector('.td-diff-split')).display"
D1D="getComputedStyle(document.querySelector('.td-diff')).display"

openpanel() {
  AB open "$URL" >/dev/null 2>&1
  AB set viewport 1440 900 >/dev/null 2>&1
  AB wait 2800 >/dev/null 2>&1
  AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
  AB wait 800 >/dev/null 2>&1
}

echo "############ A 侧边聊天：彻底移除 ############"
openpanel
echo "--- A1 打开 + 菜单，列出全部模块项"
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "'count='+document.querySelectorAll('[data-td-open-mod]').length+' | '+[].map.call(document.querySelectorAll('[data-td-open-mod]'),function(b){return b.getAttribute('data-td-open-mod')+':'+b.querySelector('.td-mm-name').textContent;}).join(', ')" 2>&1
AB screenshot "$OUT/y1-modmenu5.png" >/dev/null 2>&1
echo "--- A2 残留探测（期望全 0）"
AB eval "JSON.stringify({sideMod:document.querySelectorAll('[data-td-open-mod=\"side\"]').length,sideSec:document.querySelectorAll('.td-side').length,selbar:document.querySelectorAll('.td-selbar').length,sideTab:document.querySelectorAll('[data-td-mod=\"side\"]').length})" 2>&1

echo
echo "--- A3 打开「摘要」模块，四段小节"
AB click '[data-td-open-mod="summary"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
AB eval "JSON.stringify({tabName:document.querySelector('.td-browse-tab.is-active .td-tab-name').textContent,secs:[].map.call(document.querySelectorAll('.td-sum-h'),function(h){return h.textContent.trim();}),planDone:document.querySelectorAll('.td-sum-plan li.is-done').length,srcs:document.querySelectorAll('.td-sum-src').length,arts:document.querySelectorAll('.td-sum-art').length,hidden:document.querySelector('#av-browse-pane-summary').hasAttribute('hidden')})" 2>&1
AB screenshot "$OUT/y2-summary.png" >/dev/null 2>&1

echo
echo "############ B ★ 并排视图下的折叠（邵先生报的 bug） ############"
openpanel
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
echo "--- B1 切「并排视图」"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-rv-view="split"]' >/dev/null 2>&1
AB wait 550 >/dev/null 2>&1
AB eval "$RV" 2>&1
AB eval "JSON.stringify({splitRows:$SPLITD,unifiedRows:$D1D})" 2>&1
echo "--- B2 点第 1 个文件头 → 折叠（期望 split 行 display=none）"
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({open:document.querySelector('[data-td-diff]').classList.contains('is-open'),splitRows:$SPLITD,unifiedRows:$D1D})" 2>&1
AB screenshot "$OUT/y3-split-collapsed.png" >/dev/null 2>&1
echo "--- B3 再点一次 → 展开（期望 split 行 display=block）"
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({open:document.querySelector('[data-td-diff]').classList.contains('is-open'),splitRows:$SPLITD,unifiedRows:$D1D})" 2>&1
echo "--- B4 回归：切回「统一视图」折叠仍正常"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB click '[data-td-rv-view="unified"]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({open:document.querySelector('[data-td-diff]').classList.contains('is-open'),unifiedRows:$D1D})" 2>&1
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1

echo
echo "############ C ★ 折叠全部文件 ⇄ 展开全部文件 ############"
echo "--- C1 初始（2 开 2 折）文案 + 当前展开数"
AB eval "$FOLD+' | openCount='+document.querySelectorAll('.td-diff.is-open').length" 2>&1
echo "--- C2 点一次 → 全展开"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB click "[data-td-rv-fold]" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "$FOLD+' | openCount='+document.querySelectorAll('.td-diff.is-open').length" 2>&1
echo "--- C3 再开菜单看一眼文案，点一次 → 全折叠"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "$FOLD" 2>&1
AB click "[data-td-rv-fold]" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB screenshot "$OUT/y4-fold-all.png" >/dev/null 2>&1
AB eval "$FOLD+' | openCount='+document.querySelectorAll('.td-diff.is-open').length" 2>&1
echo "--- C4 单独点开一个文件头 → 文案回到「展开全部文件」"
AB click "[data-td-diff]:nth-child(3) [data-td-diff-h]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "$FOLD+' | openCount='+document.querySelectorAll('.td-diff.is-open').length" 2>&1

echo
echo "############ D 显示选项：八项 + 真生效的三个开关 ############"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "'items='+document.querySelectorAll('.td-rv-opts .td-mm-item').length+' | '+[].map.call(document.querySelectorAll('.td-rv-opts .td-mm-item'),function(b){return (b.classList.contains('is-checked')?'[x]':'[ ]')+b.querySelector('.td-mm-name').textContent;}).join(' / ')" 2>&1
AB screenshot "$OUT/y5-opts-full.png" >/dev/null 2>&1
echo "--- D1 初始开关态"
AB eval "$RV" 2>&1
AB eval "$CS"'JSON.stringify({drT:cs(".td-dr-t"),mark:cs(".td-dr-wd"),wsSpan:cs(".td-dr-ws")})' 2>&1
echo "--- D2 开「自动换行」+「隐藏空白」，关「词级差异」"
AB click '[data-td-rv-tog="wrap"]' >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB click '[data-td-rv-tog="hidws"]' >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB click '[data-td-rv-tog="worddiff"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "$RV" 2>&1
AB eval "$CS"'JSON.stringify({drT:cs(".td-dr-t"),mark:cs(".td-dr-wd"),wsSpan:cs(".td-dr-ws")})' 2>&1
echo "--- D3 复位（关 wrap / hidws，开 worddiff）"
AB click '[data-td-rv-tog="wrap"]' >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-rv-tog="hidws"]' >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-rv-tog="worddiff"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "$RV" 2>&1
echo "--- D4 菜单是否仍开着（复选开关不自动收菜单 = 期望 true）"
AB eval "!document.querySelector('.td-rv-opts').hasAttribute('hidden')" 2>&1
AB click ".r93-scroll" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1

echo
echo "############ E 对比范围 / 提交下拉 / 暂存 · 撤销 ############"
echo "--- E1 范围菜单"
AB click "[data-td-rv-scope]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({open:!document.querySelector('.td-rv-scope-menu').hasAttribute('hidden'),items:[].map.call(document.querySelectorAll('[data-td-rv-range] .td-mm-name'),function(e){return e.textContent;})})" 2>&1
AB screenshot "$OUT/y6-scope-menu.png" >/dev/null 2>&1
AB click '[data-td-rv-range="all"]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({btnText:document.querySelector('[data-td-rv-scope-name]').textContent,checked:document.querySelector('[data-td-rv-range=\"all\"]').getAttribute('aria-checked'),menuClosed:document.querySelector('.td-rv-scope-menu').hasAttribute('hidden')})" 2>&1
echo "--- E2 提交下拉 → 提交模态"
AB click "[data-td-commit]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({menuOpen:!document.querySelector('.td-commit-menu').hasAttribute('hidden'),items:[].map.call(document.querySelectorAll('[data-td-commit-act] .td-mm-name'),function(e){return e.textContent;})})" 2>&1
AB screenshot "$OUT/y7-commit-menu.png" >/dev/null 2>&1
AB click '[data-td-commit-act="commit"]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({modalOpen:!document.querySelector('.td-commit').hasAttribute('hidden'),menuClosed:document.querySelector('.td-commit-menu').hasAttribute('hidden')})" 2>&1
AB press Escape >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "document.querySelector('.td-commit').hasAttribute('hidden')" 2>&1
echo "--- E3 暂存 / 撤销"
AB click '[data-td-stage]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({txt:document.querySelector('[data-td-stage]').textContent,staged:document.querySelector('[data-td-stage]').classList.contains('is-staged'),toast:document.querySelector('.td-toast').textContent,toastShown:!document.querySelector('.td-toast').hasAttribute('hidden'),foldOpen:document.querySelector('[data-td-diff]').classList.contains('is-open')})" 2>&1
AB click '[data-td-revert]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({reverted:document.querySelector('[data-td-diff]').classList.contains('is-reverted'),opacity:getComputedStyle(document.querySelector('[data-td-diff]')).opacity})" 2>&1
AB click '[data-td-revert]' >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1

echo
echo "############ F 快捷键 ############"
echo "--- F1 派发 Ctrl+Shift+G（期望打开「审查」标签）"
AB eval "window.dispatchEvent(new KeyboardEvent('keydown',{key:'G',ctrlKey:true,shiftKey:true,bubbles:true}));'sent'" >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "'tabs='+[].map.call(document.querySelectorAll('.td-browse-tab .td-tab-name'),function(e){return e.textContent;}).join(',')+' | active='+document.querySelector('.td-browse-tab.is-active .td-tab-name').textContent" 2>&1
echo "--- F2 派发 Ctrl+\`（期望打开「终端」标签）"
AB eval "window.dispatchEvent(new KeyboardEvent('keydown',{key:'\`',ctrlKey:true,bubbles:true}));'sent'" >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "document.querySelector('.td-browse-tab.is-active .td-tab-name').textContent" 2>&1
echo "--- F3 终端回声回归（真键盘逐键）"
AB click '[data-td-term]' >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB press l >/dev/null 2>&1
AB press s >/dev/null 2>&1
AB press Enter >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({active:document.activeElement.className,outs:document.querySelectorAll('.td-term-out').length,last:document.querySelectorAll('.td-term-out')[document.querySelectorAll('.td-term-out').length-1].textContent})" 2>&1

echo
echo "############ G 暗色档 + 字号杠杆 ############"
AB eval "document.documentElement.setAttribute('giencoder-theme','dark');'ok'" >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "window.dispatchEvent(new KeyboardEvent('keydown',{key:'G',ctrlKey:true,shiftKey:true,bubbles:true}));'ok'" >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "$CS"'JSON.stringify({addRow:cs(".td-dr.is-add"),delRow:cs(".td-dr.is-del"),wd:cs(".td-dr-wd"),toast:cs(".td-toast")})' 2>&1
AB screenshot "$OUT/y8-dark.png" >/dev/null 2>&1
AB eval "document.documentElement.removeAttribute('giencoder-theme');'ok'" >/dev/null 2>&1
echo "--- G2 --ui-fs=18：字号杠杆 + 溢出"
AB eval "document.documentElement.style.setProperty('--ui-fs','18');'ok'" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "$CS"'JSON.stringify({dr:cs(".td-dr"),path:cs(".td-diff-path"),lh:getComputedStyle(document.querySelector(".td-dr")).lineHeight,modBarOverflow:document.querySelector(".td-mod-bar").scrollWidth-document.querySelector(".td-mod-bar").clientWidth,tabsOverflow:document.querySelector(".td-browse-tabs").scrollWidth-document.querySelector(".td-browse-tabs").clientWidth})' 2>&1
AB screenshot "$OUT/y9-fs18.png" >/dev/null 2>&1
AB eval "document.documentElement.style.removeProperty('--ui-fs');'ok'" >/dev/null 2>&1

echo "############ done ############"
