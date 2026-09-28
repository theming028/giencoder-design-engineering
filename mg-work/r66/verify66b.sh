#!/usr/bin/env zsh
# r66：需求 2 改前/改后对照 —— task-detail 终止任务弹窗（HEAD 版 vs 本轮）
set -e
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$PWD/mg-work/r66/ev
mkdir -p mg-work/r66/before

git show HEAD:pages/task-detail.html > mg-work/r66/before/task-detail.html

drive () {
  local FILE="$1" OUT="$2"
  $AB open "file://$PWD/$FILE" >/dev/null
  $AB set viewport 1440 900 >/dev/null
  sleep 2.0
  $AB eval '(function(){var b=document.querySelector("[data-td-more]"); if(!b) return "NO more"; b.click(); return "more";})()' >/dev/null
  sleep 0.5
  $AB eval '(function(){ var t=null;
    document.querySelectorAll("button,div,li,a").forEach(function(e){ var s=(e.textContent||"").trim(); if(s==="终止任务"&&e.offsetParent!==null) t=e; });
    if(!t) return "NO item"; t.click(); return "clicked"; })()'
  sleep 0.7
  $AB eval '(function(){var e=document.querySelector(".td-modal:not([hidden]) .td-modal-mask"); if(!e) return "NO mask"; var c=getComputedStyle(e);
    return JSON.stringify({bg:c.backgroundColor, bd:c.backdropFilter, wbd:c.webkitBackdropFilter});})()'
  $AB screenshot "$EV/$OUT.png" >/dev/null
  echo "saved $OUT.png"
}

echo "--- HEAD 版（无模糊）---"
drive mg-work/r66/before/task-detail.html 40-modal-before
echo "--- 本轮（高斯模糊）---"
drive pages/task-detail.html 41-modal-after
