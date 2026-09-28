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

echo "########## ① 打开「取消任务」弹窗 ##########"
$AB eval '(function(){
  var b=document.querySelector("[data-td-more]");
  if(b.getAttribute("aria-expanded")!=="true") b.click();
  return "menu expanded="+b.getAttribute("aria-expanded");
})()' >/dev/null
sleep 0.5
$AB eval '(function(){
  var rows=document.querySelectorAll(".td-more .giencoder-dropdown-item");
  rows[1].click();
  return "clicked 取消任务";
})()' >/dev/null
sleep 0.6

echo "--- 几何（应为：面板 480 宽 / 圆角 16 / 内距 20 24 24）---"
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=cancel]");
  if(!m) return "!! 弹窗未创建";
  var p=m.querySelector(".td-modal-panel"), cs=getComputedStyle(p), r=p.getBoundingClientRect();
  var out=[];
  out.push("root.hidden="+m.hidden+"  is-open="+m.classList.contains("is-open")+"  cssClass="+m.className);
  out.push("panel = "+Math.round(r.width)+"x"+Math.round(r.height)+" @ ("+Math.round(r.left)+","+Math.round(r.top)+")");
  out.push("panelRadius="+cs.borderRadius+"  padding="+cs.padding+"  shadow="+cs.boxShadow);
  out.push("panelBg="+cs.backgroundColor+"  display="+cs.display+"  opacity="+cs.opacity);
  out.push("maskBg="+getComputedStyle(m.querySelector(".td-modal-mask")).backgroundColor);
  var t=m.querySelector(".td-modal-title"), tc=getComputedStyle(t);
  out.push("title: fs="+tc.fontSize+" fw="+tc.fontWeight+" lh="+tc.lineHeight+" color="+tc.color+"  文本="+t.textContent);
  var d=m.querySelector(".td-modal-desc"), dc=getComputedStyle(d);
  out.push("desc: fs="+dc.fontSize+" lh="+dc.lineHeight+" color="+dc.color);
  var cb=m.querySelector(".td-modal-close"), cbr=cb.getBoundingClientRect();
  out.push("closeBtn = "+Math.round(cbr.width)+"x"+Math.round(cbr.height)+" @ ("+Math.round(cbr.left)+","+Math.round(cbr.top)+") color="+getComputedStyle(cb).color);
  var ic=cb.querySelector("svg"), icr=ic.getBoundingClientRect();
  out.push("closeIcon = "+Math.round(icr.width)+"x"+Math.round(icr.height)+" rect=("+Math.round(icr.left)+","+Math.round(icr.top)+")");
  var tk=m.querySelector(".td-modal-task"), tr=tk.getBoundingClientRect(), tcs=getComputedStyle(tk);
  out.push("taskCard = "+Math.round(tr.width)+"x"+Math.round(tr.height)+" @ ("+Math.round(tr.left)+","+Math.round(tr.top)+")  radius="+tcs.borderRadius+" pad="+tcs.padding+" bg="+tcs.backgroundColor+" border="+tcs.borderColor);
  out.push("taskLabel color="+getComputedStyle(m.querySelector(".td-modal-task-lbl")).color+"  fs="+getComputedStyle(m.querySelector(".td-modal-task-lbl")).fontSize);
  var sp=m.querySelector(".td-modal-sep"), sr=sp.getBoundingClientRect();
  var line=getComputedStyle(sp,"::before");
  out.push("sep = "+Math.round(sr.width)+"x"+Math.round(sr.height)+" @ y"+Math.round(sr.top)+"  gap="+getComputedStyle(sp).gap+"  lineBg="+line.backgroundColor+"  lineH="+line.height+"  文本="+sp.textContent);
  var ip=m.querySelector(".td-modal-input"), ir=ip.getBoundingClientRect(), ics=getComputedStyle(ip);
  out.push("input = "+Math.round(ir.width)+"x"+Math.round(ir.height)+" @ ("+Math.round(ir.left)+","+Math.round(ir.top)+")  radius="+ics.borderRadius+" pad="+ics.padding+" border="+ics.borderColor+" lh="+ics.lineHeight+" fs="+ics.fontSize);
  var nt=m.querySelector(".td-modal-note"), nr=nt.getBoundingClientRect();
  out.push("note = y"+Math.round(nr.top)+" h"+Math.round(nr.height)+" color="+getComputedStyle(nt).color);
  var ft=m.querySelector(".td-modal-foot"), fr=ft.getBoundingClientRect();
  out.push("foot = y"+Math.round(fr.top)+" gap="+getComputedStyle(ft).gap+"  justify="+getComputedStyle(ft).justifyContent);
  var no=m.querySelector(".td-modal-no"), nr2=no.getBoundingClientRect(), ncs=getComputedStyle(no);
  out.push("btn取消 = "+Math.round(nr2.width)+"x"+Math.round(nr2.height)+" @ x"+Math.round(nr2.left)+"  radius="+ncs.borderRadius+" bg="+ncs.backgroundColor+" border="+ncs.borderColor+" color="+ncs.color);
  var ys=m.querySelector(".td-modal-yes"), yr=ys.getBoundingClientRect(), ycs=getComputedStyle(ys);
  out.push("btn确定 = "+Math.round(yr.width)+"x"+Math.round(yr.height)+" @ x"+Math.round(yr.left)+"  radius="+ycs.borderRadius+" bg="+ycs.backgroundColor+" color="+ycs.color+" fw="+ycs.fontWeight);
  out.push("html.td-modal-lock="+document.documentElement.classList.contains("td-modal-lock")+"  bodyOverflow="+getComputedStyle(document.documentElement).overflow);
  out.push("焦点="+(document.activeElement&&document.activeElement.className));
  return out.join("\n");
})()'

echo ""
echo "########## ② 2× 截图（像素回归用） ##########"
CDP=$($AB get cdp-url 2>/dev/null | tail -1 | tr -d '"')
NODE_PATH=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules $NODE mg-work/r65/shot2x.mjs "$CDP" "pages/task-detail.html" "$EV/10-cancel-1440-2x.png"

echo ""
echo "########## ③ 行为：Esc 关闭 + 焦点归还 ##########"
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=cancel]");
  document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true,cancelable:true}));
  var out=["esc后 is-open="+m.classList.contains("is-open")];
  setTimeout(function(){
    out.push("220ms 后 hidden="+m.hidden+"  lock="+document.documentElement.classList.contains("td-modal-lock"));
    out.push("焦点="+(document.activeElement&&document.activeElement.getAttribute&&document.activeElement.getAttribute("data-td-more")?"更多按钮 ✅":(document.activeElement&&document.activeElement.className)));
    window.__esc=out.join(" | ");
  },320);
  return "dispatched";
})()' >/dev/null
sleep 0.6
$AB eval 'window.__esc'

echo ""
echo "########## ④ 「终止任务」弹窗 ##########"
$AB eval '(function(){
  var b=document.querySelector("[data-td-more]"); b.click(); return "menu";
})()' >/dev/null
sleep 0.5
$AB eval '(function(){
  document.querySelectorAll(".td-more .giencoder-dropdown-item")[0].click(); return "clicked 终止任务";
})()' >/dev/null
sleep 0.6
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=stop]");
  var p=m.querySelector(".td-modal-panel"), r=p.getBoundingClientRect();
  return ["stopPanel="+Math.round(r.width)+"x"+Math.round(r.height)+" @ ("+Math.round(r.left)+","+Math.round(r.top)+")",
          "title="+m.querySelector(".td-modal-title").textContent,
          "desc="+m.querySelector(".td-modal-desc").textContent,
          "sep="+m.querySelector(".td-modal-sep").textContent,
          "ok="+m.querySelector(".td-modal-yes").textContent,
          "note="+m.querySelector(".td-modal-note").textContent,
          "taskCardH="+Math.round(m.querySelector(".td-modal-task").getBoundingClientRect().height),
          "另一弹窗 hidden="+document.querySelector(".td-modal[data-td-modal=cancel]").hidden].join("\n");
})()'
CDP=$($AB get cdp-url 2>/dev/null | tail -1 | tr -d '"')
NODE_PATH=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules $NODE mg-work/r65/shot2x.mjs "$CDP" "pages/task-detail.html" "$EV/11-stop-1440-2x.png"

echo ""
echo "########## ⑤ 行为：遮罩点击关闭 / Tab 焦点锁 / 确认写提示 ##########"
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=stop]");
  var list=Array.prototype.filter.call(m.querySelectorAll("button, textarea"),function(e){return !e.disabled&&e.offsetParent!==null});
  m.querySelector(".td-modal-input").focus();
  var before=document.activeElement.className;
  m.querySelector(".td-modal-input").dispatchEvent(new KeyboardEvent("keydown",{key:"Tab",bubbles:true,cancelable:true}));
  return "可聚焦元素数="+list.length+" 顺序=["+list.map(function(e){return e.className.split(" ")[0]}).join(",")+"]  当前="+before;
})()'
$AB eval '(function(){
  document.querySelector(".td-modal[data-td-modal=stop] .td-modal-mask").click();
  return "mask clicked";
})()' >/dev/null
sleep 0.5
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=stop]");
  return "遮罩点击后 is-open="+m.classList.contains("is-open")+"  lock="+document.documentElement.classList.contains("td-modal-lock");
})()'

echo ""
echo "--- 重新打开并确认（应写 DS Message 提示）---"
$AB eval '(function(){ document.querySelector("[data-td-more]").click(); return "menu"; })()' >/dev/null
sleep 0.5
$AB eval '(function(){ document.querySelectorAll(".td-more .giencoder-dropdown-item")[0].click(); return "stop"; })()' >/dev/null
sleep 0.6
$AB eval '(function(){ document.querySelector(".td-modal[data-td-modal=stop] .td-modal-input").value="资源被占用，暂停推进"; return "typed"; })()' >/dev/null
$AB eval '(function(){ document.querySelector(".td-modal[data-td-modal=stop] .td-modal-yes").click(); return "yes clicked"; })()' >/dev/null
sleep 0.6
$AB eval '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=stop]");
  var msg=document.querySelector(".td-dp-msg");
  return "确认后 is-open="+m.classList.contains("is-open")+"  lock="+document.documentElement.classList.contains("td-modal-lock")
    +"\n提示可见="+(msg?!msg.hidden:false)+"  文案="+(msg?msg.textContent.trim():"-")
    +"\n焦点="+(document.activeElement&&document.activeElement.getAttribute&&document.activeElement.getAttribute("data-td-more")?"更多按钮 ✅":(document.activeElement&&document.activeElement.className));
})()'
echo ""
echo "########## ⑥ 干净加载回归（弹窗 DOM 应尚未创建） ##########"
$AB open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 0.8
$AB eval '(function(){
  var n=document.querySelectorAll(".td-modal").length;
  var b=!!document.querySelector("[data-td-more]");
  return "初始 .td-modal 数="+n+"（应为 0，惰性创建）  更多按钮="+b;
})()'
