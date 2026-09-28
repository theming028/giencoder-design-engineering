#!/usr/bin/env zsh
# r65 取证截图：分别打开两个弹窗，失焦后 2× 截图（与设计稿同为默认态）
set -e
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
NODE=/Users/shaoyuming/.workbuddy/binaries/node/versions/22.22.2-3/bin/node
EV=$PWD/mg-work/r65/ev
URL="file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html"
mkdir -p "$EV"

shot() {   # $1=out  $2=probe
  local HREF=$($AB eval 'location.href' 2>/dev/null | tail -1 | tr -d '"')
  local CDP=$($AB get cdp-url 2>/dev/null | tail -1 | tr -d '"')
  NODE_PATH=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules $NODE mg-work/r65/shot2x.mjs "$CDP" "pages/task-detail.html" "$EV/$1" "$HREF" "$2"
}

$AB open "$URL" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 0.9

echo "=== 取消任务 ==="
$AB eval '(function(){ document.querySelector("[data-td-more]").click(); return 1 })()' >/dev/null
sleep 0.5
$AB eval '(function(){ document.querySelectorAll(".td-more .giencoder-dropdown-item")[1].click(); return 1 })()' >/dev/null
sleep 0.6
$AB eval '(function(){ if(document.activeElement&&document.activeElement.blur)document.activeElement.blur(); return 1 })()' >/dev/null
sleep 0.3
shot "20-cancel-2x.png" '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=cancel]"); if(!m) return "无 cancel 弹窗";
  var p=m.querySelector(".td-modal-panel"), r=p.getBoundingClientRect();
  return "open="+(m.classList.contains("is-open")&&!m.hidden)+" rect="+Math.round(r.left)+","+Math.round(r.top)+","+Math.round(r.width)+"x"+Math.round(r.height);
})()'
$AB eval '(function(){ document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true,cancelable:true})); return 1 })()' >/dev/null
sleep 0.5

echo ""
echo "=== 终止任务 ==="
$AB eval '(function(){ document.querySelector("[data-td-more]").click(); return 1 })()' >/dev/null
sleep 0.5
$AB eval '(function(){ document.querySelectorAll(".td-more .giencoder-dropdown-item")[0].click(); return 1 })()' >/dev/null
sleep 0.6
$AB eval '(function(){ if(document.activeElement&&document.activeElement.blur)document.activeElement.blur(); return 1 })()' >/dev/null
sleep 0.3
shot "21-stop-2x.png" '(function(){
  var m=document.querySelector(".td-modal[data-td-modal=stop]"); if(!m) return "无 stop 弹窗";
  var p=m.querySelector(".td-modal-panel"), r=p.getBoundingClientRect();
  return "open="+(m.classList.contains("is-open")&&!m.hidden)+" rect="+Math.round(r.left)+","+Math.round(r.top)+","+Math.round(r.width)+"x"+Math.round(r.height);
})()'
