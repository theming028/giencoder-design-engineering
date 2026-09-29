#!/bin/bash
# 第 67 轮 B（v2 鼠标版）运行时验收
#  ① 旧版浅点阵（A 层）色彩/位置/尺寸必须与改前逐字一致，且无任何动画
#  ② 深色点阵光斑（D 层）随指针移动，且是「渐进跟随」而非瞬间跳变
#  ③ 布局零位移
set -u
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$PWD/mg-work/r67/ev
mkdir -p "$EV"
VT=1440; VH=900

LAYER='(function(){
  var m=document.querySelector("main.dot-bg");
  var c=getComputedStyle(m);
  var r=m.getBoundingClientRect();
  var k=m.children[0], kr=k.getBoundingClientRect();
  return JSON.stringify({
    mainRect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)],
    A_bgImg:c.backgroundImage, A_bgSize:c.backgroundSize, A_bgPos:c.backgroundPosition,
    A_bgRepeat:c.backgroundRepeat, A_anim:c.animationName,
    transProp:c.transitionProperty, transDur:c.transitionDuration,
    dotX:c.getPropertyValue("--dot-x").trim(), dotY:c.getPropertyValue("--dot-y").trim(),
    kidRect:[Math.round(kr.x),Math.round(kr.y),Math.round(kr.width),Math.round(kr.height)],
    hOverflow:document.documentElement.scrollWidth-window.innerWidth
  });
})()'

# 读伪元素 mask 的圆心百分比
SPOT='(function(){
  var m=document.querySelector("main.dot-bg");
  var p=getComputedStyle(m,"::before");
  var mk=p.maskImage&&p.maskImage!=="none"?p.maskImage:(p.webkitMaskImage||"");
  var g=/at ([0-9.]+)% ([0-9.]+)%/.exec(mk);
  return JSON.stringify({cx:g?+g[1]:null, cy:g?+g[2]:null, maskHead:(mk||"NONE").slice(0,120),
    anim:p.animationName, bgImg:p.backgroundImage.slice(0,110), bgSize:p.backgroundSize});
})()'

# 在 main 内按相对坐标派发指针事件（fraction 0~1）
MOVE() {  # $1=rfx $2=rfy
  echo "(function(){var m=document.querySelector('main.dot-bg');var r=m.getBoundingClientRect();
  m.dispatchEvent(new PointerEvent('pointermove',{clientX:r.left+r.width*$1,clientY:r.top+r.height*$2,bubbles:true}));
  return 'moved to $1/$2';})()"
}

echo "=========== A. 改后初始态 ==========="
$AB open "file://$PWD/pages/base.html" >/dev/null
$AB set viewport $VT $VH >/dev/null
sleep 2.2
echo "-- A 层（旧版波点）与布局 --"; $AB eval "$LAYER"
echo "-- D 层（光斑）--";         $AB eval "$SPOT"
$AB screenshot "$EV/20-mouse-init.png" >/dev/null; echo "saved 20-mouse-init.png"

echo
echo "=========== B. 指针移到右下 (0.80, 0.75) —— 立刻读 vs 到位后读 ==========="
$AB eval "$(MOVE 0.80 0.75)" >/dev/null
sleep 0.05
echo "-- 立刻（应仍在途中，体现过渡是渐进的）--"; $AB eval "$SPOT"
sleep 0.5
echo "-- 0.55s 后（应已到位 ≈ 80% / 75%）--";   $AB eval "$SPOT"
$AB screenshot "$EV/21-mouse-br.png" >/dev/null; echo "saved 21-mouse-br.png"

echo
echo "=========== C. 指针移到左上 (0.16, 0.20) ==========="
$AB eval "$(MOVE 0.16 0.20)" >/dev/null
sleep 0.55
$AB eval "$SPOT"
$AB screenshot "$EV/22-mouse-tl.png" >/dev/null; echo "saved 22-mouse-tl.png"

echo
echo "=========== D. 指针移到中右 (0.62, 0.44) ==========="
$AB eval "$(MOVE 0.62 0.44)" >/dev/null
sleep 0.55
$AB eval "$SPOT"
$AB screenshot "$EV/23-mouse-mid.png" >/dev/null; echo "saved 23-mouse-mid.png"

echo
echo "=========== E. 指针移出 main（移到侧栏）后应保持不动 ==========="
$AB eval '(function(){var el=document.elementFromPoint(150,400)||document.body;el.dispatchEvent(new PointerEvent("pointermove",{clientX:150,clientY:400,bubbles:true}));return "moved out onto "+el.tagName;})()'
sleep 0.4
$AB eval "$SPOT"
