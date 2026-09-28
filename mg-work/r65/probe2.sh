#!/usr/bin/env zsh
set -e
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
NODE=/Users/shaoyuming/.workbuddy/binaries/node/versions/22.22.2-3/bin/node
EV=$PWD/mg-work/r65/ev
mkdir -p "$EV"

$AB open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 0.8

echo "########## 取消任务：几何复测 ##########"
$AB eval '(function(){ document.querySelector("[data-td-more]").click(); return 1 })()' >/dev/null
sleep 0.5
$AB eval '(function(){ document.querySelectorAll(".td-more .giencoder-dropdown-item")[1].click(); return 1 })()' >/dev/null
sleep 0.6
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=cancel]");
  var p=m.querySelector(".td-modal-panel"), r=p.getBoundingClientRect();
  function rel(el){var q=el.getBoundingClientRect();return "x"+(q.left-r.left)+" y"+(q.top-r.top)+" "+Math.round(q.width)+"x"+Math.round(q.height);}
  var out=[];
  out.push("panel = "+Math.round(r.width)+"x"+Math.round(r.height)+"   设计稿 480x454（2 行卡）；本页标题 1 行 ⇒ 期望 432");
  out.push("head     "+rel(m.querySelector(".td-modal-head"))+"   期望 x24 y20 432x28");
  out.push("title    "+rel(m.querySelector(".td-modal-title"))+"   期望 x24 y20 432x24");
  out.push("close    "+rel(m.querySelector(".td-modal-close"))+"   期望 x428 y20 28x28");
  out.push("desc     "+rel(m.querySelector(".td-modal-desc"))+"   期望 x24 y48 432x22");
  out.push("card     "+rel(m.querySelector(".td-modal-task"))+"   期望 x24 y90 432x78");
  out.push("label    "+rel(m.querySelector(".td-modal-task-lbl"))+"   期望 x44 y106 392x16");
  out.push("sep      "+rel(m.querySelector(".td-modal-sep"))+"   期望 x24 y192 432x22");
  out.push("input    "+rel(m.querySelector(".td-modal-input"))+"   期望 x24 y226 432x88");
  out.push("note     "+rel(m.querySelector(".td-modal-note"))+"   期望 x24 y322 432x22");
  out.push("foot     "+rel(m.querySelector(".td-modal-foot"))+"   期望 x24 y376 432x32");
  out.push("btn取消  "+rel(m.querySelector(".td-modal-no"))+"   期望 x300 y376 60x32");
  out.push("btn确定  "+rel(m.querySelector(".td-modal-yes"))+"   期望 x368 y376 88x32");
  return out.join("\n");
})()'

echo ""
echo "--- 失焦后 2× 截图（与设计稿同为默认态） ---"
$AB eval '(function(){ if(document.activeElement&&document.activeElement.blur)document.activeElement.blur(); return "blurred" })()' >/dev/null
sleep 0.3
CDP=$($AB get cdp-url 2>/dev/null | tail -1 | tr -d '"')
NODE_PATH=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules $NODE mg-work/r65/shot2x.mjs "$CDP" "pages/task-detail.html" "$EV/20-cancel-2x.png"
echo "面板在 1440 视口内，取面板矩形供裁剪"
$AB eval '(function(){
  var p=document.querySelector(".td-modal[data-td-modal=cancel] .td-modal-panel"), r=p.getBoundingClientRect();
  return JSON.stringify({left:Math.round(r.left),top:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)});
})()'

echo ""
echo "########## 终止任务：几何 + 截图 ##########"
$AB eval '(function(){ document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true,cancelable:true})); return 1 })()' >/dev/null
sleep 0.5
$AB eval '(function(){ document.querySelector("[data-td-more]").click(); return 1 })()' >/dev/null
sleep 0.5
$AB eval '(function(){ document.querySelectorAll(".td-more .giencoder-dropdown-item")[0].click(); return 1 })()' >/dev/null
sleep 0.6
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=stop]");
  var p=m.querySelector(".td-modal-panel"), r=p.getBoundingClientRect();
  function rel(el){var q=el.getBoundingClientRect();return "x"+(q.left-r.left)+" y"+(q.top-r.top)+" "+Math.round(q.width)+"x"+Math.round(q.height);}
  var out=["panel = "+Math.round(r.width)+"x"+Math.round(r.height)+"  设计稿(终止) 480x416 ⇒ 本页因「卡片↔分隔线 24」多 16 ⇒ 432"];
  out.push("card  "+rel(m.querySelector(".td-modal-task"))+"  期望 x24 y90 432x78");
  out.push("sep   "+rel(m.querySelector(".td-modal-sep"))+"  期望 x24 y192 432x22");
  out.push("input "+rel(m.querySelector(".td-modal-input"))+"  期望 x24 y226 432x88");
  out.push("note  "+rel(m.querySelector(".td-modal-note"))+"  期望 x24 y322 432x22");
  out.push("foot  "+rel(m.querySelector(".td-modal-foot"))+"  期望 x24 y376 432x32");
  return out.join("\n");
})()'
$AB eval '(function(){ if(document.activeElement&&document.activeElement.blur)document.activeElement.blur(); return 1 })()' >/dev/null
sleep 0.3
CDP=$($AB get cdp-url 2>/dev/null | tail -1 | tr -d '"')
NODE_PATH=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules $NODE mg-work/r65/shot2x.mjs "$CDP" "pages/task-detail.html" "$EV/21-stop-2x.png"

echo ""
echo "########## 行为复测 ##########"
echo "--- Tab 焦点锁（在最后一个按钮上按 Tab → 应回到关闭按钮）---"
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=stop]");
  var ys=m.querySelector(".td-modal-yes"); ys.focus();
  var before=document.activeElement.className.split(" ")[0];
  ys.dispatchEvent(new KeyboardEvent("keydown",{key:"Tab",bubbles:true,cancelable:true}));
  var after=document.activeElement.className.split(" ")[0];
  var cb=m.querySelector(".td-modal-close"); cb.focus();
  var b2=document.activeElement.className.split(" ")[0];
  cb.dispatchEvent(new KeyboardEvent("keydown",{key:"Tab",shiftKey:true,bubbles:true,cancelable:true}));
  var a2=document.activeElement.className.split(" ")[0];
  return "末元素["+before+"] +Tab → ["+after+"]（期望 td-modal-close）  首元素["+b2+"] +Shift+Tab → ["+a2+"]（期望 td-modal-yes）";
})()'

echo "--- Esc 关闭 + 焦点归还更多按钮 ---"
$AB eval '(function(){
  document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true,cancelable:true}));
  return "esc";
})()' >/dev/null
sleep 0.5
$AB eval '(function(){
  var ae=document.activeElement;
  return "焦点 = "+(ae&&ae.getAttribute&&ae.getAttribute("data-td-more")?"更多按钮 ✅":(ae&&ae.className));
})()'

echo "--- 打开时锁定滚动 / 关闭后释放 ---"
$AB eval '(function(){ document.querySelector("[data-td-more]").click(); return 1 })()' >/dev/null
sleep 0.4
$AB eval '(function(){ document.querySelectorAll(".td-more .giencoder-dropdown-item")[0].click(); return 1 })()' >/dev/null
sleep 0.5
$AB eval '(function(){
  var a=document.documentElement.classList.contains("td-modal-lock")+" / "+getComputedStyle(document.documentElement).overflow;
  var m=document.querySelector(".td-modal[data-td-modal=stop]");
  m.querySelector(".td-modal-close").click();
  var s0=a;
  setTimeout(function(){ window.__lock=s0+"  →  关闭后 "+document.documentElement.classList.contains("td-modal-lock")+" / "+getComputedStyle(document.documentElement).overflow; },300);
  return "打开时 lock="+a;
})()'
sleep 0.6
$AB eval 'window.__lock'

echo "--- z-index 与遮罩覆盖 ---"
$AB eval '(function(){ document.querySelector("[data-td-more]").click(); return 1 })()' >/dev/null
sleep 0.4
$AB eval '(function(){ document.querySelectorAll(".td-more .giencoder-dropdown-item")[1].click(); return 1 })()' >/dev/null
sleep 0.5
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=cancel]");
  var cs=getComputedStyle(m);
  var mask=m.querySelector(".td-modal-mask").getBoundingClientRect();
  var top=document.elementFromPoint(200,120);
  return "modal z-index="+cs.zIndex+"  position="+cs.position
    +"\n遮罩 rect="+Math.round(mask.width)+"x"+Math.round(mask.height)+" @("+Math.round(mask.left)+","+Math.round(mask.top)+")"
    +"\n面板外 (200,120) 命中 = "+(top?top.className||top.tagName:"-");
})()'
echo "--- 关闭 ---"
$AB eval '(function(){ document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true,cancelable:true})); return 1 })()' >/dev/null
sleep 0.4
$AB eval '(function(){ return "残留 td-modal-lock="+document.documentElement.classList.contains("td-modal-lock"); })()'
