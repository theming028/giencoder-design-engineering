#!/usr/bin/env zsh
# r66：看板泳道内滚 —— before/after 同参数对照取证
set -e
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$PWD/mg-work/r66/ev
mkdir -p "$EV"

PROBE='(function(){
  var out=[];
  document.querySelectorAll(".kb-col").forEach(function(c,i){
    var body=c.querySelector(".kb-col-body"), head=c.querySelector(".kb-col-head");
    var r=c.getBoundingClientRect(), rb=body.getBoundingClientRect();
    var cards=body.querySelectorAll(".kb-card");
    var last=cards.length?cards[cards.length-1].getBoundingClientRect():null;
    out.push({
      i:i,
      colX:[Math.round(r.left),Math.round(r.right)],
      bodyTop:Math.round(rb.top), bodyBottom:Math.round(rb.bottom),
      bodyW:Math.round(rb.width),
      cardW:cards.length?Math.round(cards[0].getBoundingClientRect().width):null,
      cardN:cards.length,
      scrollH:body.scrollHeight, clientH:body.clientHeight,
      maxScroll:body.scrollHeight-body.clientHeight,
      headY:Math.round(head.getBoundingClientRect().top),
      lastCardBottom: last?Math.round(last.bottom):null,
      ovY:getComputedStyle(body).overflowY, ovX:getComputedStyle(body).overflowX,
      minH:getComputedStyle(body).minHeight
    });
  });
  return JSON.stringify(out,null,1);
})()'

shoot () {
  local FILE="$1" TAG="$2"
  $AB open "file://$PWD/$FILE" >/dev/null
  $AB set viewport 1440 900 >/dev/null
  sleep 1.6
  echo "=== $TAG ==="
  $AB eval "$PROBE"
  $AB screenshot "$EV/$TAG.png" >/dev/null
  echo "saved $TAG.png"
}

# 注意：必须先保证文件名与 pages/kanban.html 同名，否则 file:// 下外壳按文件名查路由表失败 → 落回 base 壳（多出 260px aside 侧栏）
shoot mg-work/r66/before/kanban.html 20-before
shoot pages/kanban.html              21-after

# ===== 滚动后复测：标题栏是否仍固定 + 渐隐类切换 =====
echo "=== 22-after-scrolled (lane0 → bottom) ==="
$AB open "file://$PWD/pages/kanban.html" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 1.6
$AB eval '(function(){var b=document.querySelectorAll(".kb-col-body")[0];b.scrollTop=b.scrollHeight;return "scrolled to "+b.scrollTop;})()'
sleep 0.4
$AB eval "$PROBE"
$AB screenshot "$EV/22-after-scrolled.png" >/dev/null
echo "saved 22-after-scrolled.png"
