#!/bin/bash
# 第 67 轮 B：动态波点（A+D）运行时验收
# 关键手法：把动画钉在指定相位再截图 ⇒ before/after 可做干净的像素对照
set -u
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$PWD/mg-work/r67/ev
mkdir -p "$EV"

VT=1440
VH=900

PIN() {  # $1 = dotTour 相位(ms)
  echo "(function(T){var out=[];document.getAnimations().forEach(function(a){var n=a.animationName;if(n==='dotDrift'){a.pause();a.currentTime=0;out.push(n+':0');}else if(n==='dotTour'){a.pause();a.currentTime=T;out.push(n+':'+T);}else{try{a.finish();out.push(n+':fin');}catch(e){a.pause();out.push(n+':paused');}}});return JSON.stringify(out);})($1)"
}

GEOM='(function(){
  var m=document.querySelector("main");
  var c=getComputedStyle(m);
  var p=getComputedStyle(m,"::before");
  var k=m.children[0], kr=k.getBoundingClientRect(), r=m.getBoundingClientRect();
  return JSON.stringify({
    mainRect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)],
    mainPos:c.position, mainAnim:c.animationName, mainAnimDur:c.animationDuration,
    mainBgImg:c.backgroundImage.slice(0,120), mainBgSize:c.backgroundSize,
    beContent:p.content, beW:p.width, beH:p.height, bePos:p.position, beInset:p.inset,
    beBgImg:p.backgroundImage.slice(0,140), beBgSize:p.backgroundSize,
    beMask:(p.maskImage&&p.maskImage!=="none"?p.maskImage:(p.webkitMaskImage||"")).slice(0,210),
    beAnim:p.animationName, beAnimDur:p.animationDuration,
    kidRect:[Math.round(kr.x),Math.round(kr.y),Math.round(kr.width),Math.round(kr.height)],
    kidPos:getComputedStyle(k).position, kidZ:getComputedStyle(k).zIndex,
    kidBg:getComputedStyle(k).backgroundColor,
    hOverflow:document.documentElement.scrollWidth-window.innerWidth
  });
})()'

echo "=========== 01 BEFORE（改前基线，无动画）==========="
$AB open "file://$PWD/mg-work/r67/before/base.html" >/dev/null
$AB set viewport $VT $VH >/dev/null
sleep 2.0
$AB eval "$(PIN 0)" >/dev/null
sleep 0.35
$AB eval "$GEOM"
$AB screenshot "$EV/01-base-before.png" >/dev/null
echo "saved 01-base-before.png"

echo
echo "=========== 02 AFTER t=0（光斑在 22%/26%）==========="
$AB open "file://$PWD/pages/base.html" >/dev/null
$AB set viewport $VT $VH >/dev/null
sleep 2.0
$AB eval "$(PIN 0)" >/dev/null
sleep 0.35
$AB eval "$GEOM"
$AB screenshot "$EV/02-base-after-t0.png" >/dev/null
echo "saved 02-base-after-t0.png"

echo
echo "=========== 03 AFTER t=13s（dotTour 50% ⇒ 光斑移到 78%/72%）==========="
$AB eval "$(PIN 13000)" >/dev/null
sleep 0.35
$AB eval '(function(){var p=getComputedStyle(document.querySelector("main"),"::before");return (p.maskImage||p.webkitMaskImage||"NONE").slice(0,210);})()'
$AB screenshot "$EV/03-base-after-t13.png" >/dev/null
echo "saved 03-base-after-t13.png"

echo
echo "=========== 04 AFTER t=6.5s（dotTour 25% ⇒ 光斑移到 74%/22%）==========="
$AB eval "$(PIN 6500)" >/dev/null
sleep 0.35
$AB eval '(function(){var p=getComputedStyle(document.querySelector("main"),"::before");return (p.maskImage||p.webkitMaskImage||"NONE").slice(0,210);})()'
$AB screenshot "$EV/04-base-after-t65.png" >/dev/null
echo "saved 04-base-after-t65.png"
