#!/bin/zsh
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
CLICK_RAIL='[].filter.call(document.querySelectorAll("button,a"),function(e){return e.innerText.trim()==="数字分身"})[0].click();"ok"'
CLICK_CTA='[].filter.call(document.querySelectorAll("button,a"),function(e){return e.innerText.replace(/\s/g,"").indexOf("进入研发工作台")>=0})[0].click();"ok"'
CLICK_TAB='document.querySelector("[data-tab=dev]").click();"ok"'
CLICK_CARD='document.querySelector(".kb-card").click();"ok"'
READ='location.href'
$AB set viewport 1440 900 >/dev/null 2>&1

probe() { # $1=base url  $2=page  $3=clickjs  $4=label
  $AB open "$1/$2" >/dev/null 2>&1; sleep 2
  local before=$($AB eval "$READ" 2>/dev/null | tail -1)
  $AB eval "$3" >/dev/null 2>&1; sleep 2
  local after=$($AB eval "$READ" 2>/dev/null | tail -1)
  echo "  $4 | $before -> $after"
}

echo "===== A. http 预览 (52574) ====="
U=http://127.0.0.1:52574/static-html/22441530f7eeb388
probe $U base.html "$CLICK_RAIL" "base 侧栏 数字分身"
probe $U base.html "$CLICK_TAB"  "base 顶栏 → 研发工作台"
probe $U dev.html  "$CLICK_CTA"  "dev 进入研发工作台"
probe $U kanban.html "$CLICK_CARD" "kanban 卡片 → 详情"
echo "  -- kanban 外壳:"
$AB open "$U/kanban.html" >/dev/null 2>&1; sleep 2
$AB eval 'JSON.stringify({aside:document.querySelectorAll("aside").length,kbWrap:!!document.querySelector(".kb-wrap"),sel:(document.querySelector("[data-tab][aria-selected=true]")||{}).textContent})' 2>/dev/null | tail -1

echo "===== B. file:// ====="
F=file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages
probe $F base.html "$CLICK_RAIL" "base 侧栏 数字分身"
probe $F dev.html  "$CLICK_CTA"  "dev 进入研发工作台"
probe $F kanban.html "$CLICK_CARD" "kanban 卡片 → 详情"

echo "===== C. 链接样式（task-detail） ====="
$AB open "$F/task-detail.html" >/dev/null 2>&1; sleep 2
$AB eval 'var a=document.querySelector(".td-attr-link"),sv=a.querySelector("svg");JSON.stringify({svgDisplay:sv?getComputedStyle(sv).display:"no-svg",textDecoration:getComputedStyle(a).textDecorationLine,offset:getComputedStyle(a).textUnderlineOffset,color:getComputedStyle(a).color})' 2>/dev/null | tail -1
$AB screenshot mg-work/r42/r42-link.png >/dev/null 2>&1
