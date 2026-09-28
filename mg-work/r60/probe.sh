#!/bin/zsh
# r60 运行时验收：浏览态隐藏 .td-side
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
URL="file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html"
EV=/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r60/ev
mkdir -p "$EV"

SNAP='(function(){var r=document.querySelector(".td-root"),L=document.querySelector(".td-left"),M=document.querySelector(".td-main"),S=document.querySelector(".td-side"),B=document.querySelector(".td-right"),P=document.querySelector(".td-browse-slot");function w(e){return e?Math.round(e.getBoundingClientRect().width):-1}function h(e){return e?Math.round(e.getBoundingClientRect().height):-1}var sd=S?getComputedStyle(S).display:"-";return "left="+w(L)+" side="+w(S)+"x"+h(S)+" sideDisplay="+sd+" main="+w(M)+"x"+h(M)+" mainScrollW="+M.scrollWidth+" mainClientW="+M.clientWidth+" overflowX="+(M.scrollWidth>M.clientWidth+1)+" right="+w(B)+" browseSlot="+w(P)+" cls="+r.className})()'

$AB open "$URL" > /dev/null
$AB set viewport 1920 1080 > /dev/null
sleep 0.4

echo "### 1) 普通态（应 sideDisplay=flex，main 与 side 并列）"
$AB eval "$SNAP"

echo ""
echo "### 2) 点「打开侧栏」进入浏览态"
$AB eval '(function(){var b=document.querySelector("[data-td-browse-toggle]");b.click();return "clicked aria-pressed="+b.getAttribute("aria-pressed")})()'
sleep 0.6
echo "### 3) 浏览态（应 sideDisplay=none，main 独占左栏）"
$AB eval "$SNAP"

echo ""
echo "### 4) 正文列是否有横向溢出 / 各段落宽度"
$AB eval '(function(){var M=document.querySelector(".td-main");var out=["main clientW="+M.clientWidth+" scrollW="+M.scrollWidth];Array.prototype.forEach.call(M.querySelectorAll("section,div"),function(e){var cs=getComputedStyle(e);if(e.scrollWidth>e.clientWidth+1&&cs.overflowX!=="visible"){out.push("  OVERFLOW "+e.className+" clientW="+e.clientWidth+" scrollW="+e.scrollWidth)}});return out.slice(0,8).join("\n")})()'

echo ""
echo "### 5) 截图（浏览态 1920）"
$AB screenshot "$EV/10-browse-1920.png" > /dev/null
echo "saved 10-browse-1920.png"

echo ""
echo "### 6) 关闭浏览态"
$AB eval '(function(){var b=document.querySelector("[data-td-browse-toggle]");b.click();return "clicked aria-pressed="+b.getAttribute("aria-pressed")})()'
sleep 0.8
echo "### 7) 关闭后（应 sideDisplay=flex 恢复，is-browse / is-keep-left 都已摘掉）"
$AB eval "$SNAP"

echo ""
echo "### 8) 截图（普通态 1920）"
$AB screenshot "$EV/11-normal-1920.png" > /dev/null
echo "saved 11-normal-1920.png"
