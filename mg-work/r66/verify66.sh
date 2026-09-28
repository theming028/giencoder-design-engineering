#!/usr/bin/env zsh
# r66：需求 2（蒙层全局统一 + .td-modal-panel 面板材质）运行时计算样式验收
set -e
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$PWD/mg-work/r66/ev
mkdir -p "$EV"

STYLE='(function(){
  function g(sel){ var el=document.querySelector(sel); if(!el) return null;
    var c=getComputedStyle(el);
    return {
      sel: sel,
      background: c.backgroundColor,
      bd: (c.backdropFilter||c.webkitBackdropFilter),
      wbd: c.webkitBackdropFilter,
      shadow: c.boxShadow,
      radius: c.borderRadius,
      opacity: c.opacity,
      color: c.color
    };
  }
  return JSON.stringify({
    mask:      g(".td-modal:not([hidden]) .td-modal-mask"),
    panel:     g(".td-modal:not([hidden]) .td-modal-panel"),
    tokens:    (function(){ var s=getComputedStyle(document.documentElement);
                 return { "mask-bg": s.getPropertyValue("--color-mask-bg").trim(),
                          "bg-2": s.getPropertyValue("--color-bg-2").trim() }; })()
  },null,1);
})()'

echo "############ A. task-detail · 终止任务弹窗 ############"
$AB open "file://$PWD/pages/task-detail.html" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 2.0
$AB eval '(function(){var b=document.querySelector("[data-td-more]"); if(!b) return "NO [data-td-more]"; b.click(); return "clicked more";})()'
sleep 0.5
$AB eval '(function(){var rows=document.querySelectorAll(".td-more-item,.td-more-row,[data-td-more-item]"); var t=null;
  document.querySelectorAll("button,div,li,a").forEach(function(e){ var s=(e.textContent||"").trim(); if(s==="终止任务"&&e.offsetParent!==null) t=e; });
  if(!t) return "NO row: found "+document.querySelectorAll(".td-more-item").length+" items";
  t.click(); return "clicked 终止任务"; })()'
sleep 0.6
$AB eval "$STYLE"
$AB screenshot "$EV/30-td-stop-modal.png" >/dev/null
echo "saved 30-td-stop-modal.png"

echo "############ B. task-detail · 取消任务弹窗 ############"
$AB open "file://$PWD/pages/task-detail.html" >/dev/null
sleep 1.6
$AB eval '(function(){var b=document.querySelector("[data-td-more]"); b.click(); return "more";})()'
sleep 0.5
$AB eval '(function(){ var t=null;
  document.querySelectorAll("button,div,li,a").forEach(function(e){ var s=(e.textContent||"").trim(); if(s==="取消任务"&&e.offsetParent!==null) t=e; });
  if(!t) return "NO"; t.click(); return "clicked 取消任务"; })()'
sleep 0.6
$AB eval "$STYLE"
$AB screenshot "$EV/31-td-cancel-modal.png" >/dev/null
echo "saved 31-td-cancel-modal.png"

echo "############ C. task-detail · 协作(task-detail 内 giencoder-modal) ############"
$AB open "file://$PWD/pages/task-detail.html" >/dev/null
sleep 1.6
$AB eval '(function(){
  var el=document.querySelector(".td-coop .giencoder-modal-mask") || document.querySelector(".giencoder-modal-mask");
  if(!el) return "NO .giencoder-modal-mask";
  var c=getComputedStyle(el);
  return JSON.stringify({sel:el.className, background:c.backgroundColor, bd:c.backdropFilter, wbd:c.webkitBackdropFilter, opacity:c.opacity});
})()'

echo "############ D. kanban · 全局 .giencoder-modal-mask 口径 ############"
$AB open "file://$PWD/pages/kanban.html" >/dev/null
sleep 1.6
$AB eval '(function(){
  var list=document.querySelectorAll(".giencoder-modal-mask");
  var out=[];
  list.forEach(function(el,i){ var c=getComputedStyle(el);
    out.push({i:i, parent:el.parentElement.className.slice(0,60), bg:c.backgroundColor, bd:c.backdropFilter, wbd:c.webkitBackdropFilter, op:c.opacity}); });
  var s=getComputedStyle(document.documentElement);
  return JSON.stringify({maskToken:s.getPropertyValue("--color-mask-bg").trim(), list:out},null,1);
})()'
$AB screenshot "$EV/32-kanban-coop.png" >/dev/null
echo "saved 32-kanban-coop.png"
