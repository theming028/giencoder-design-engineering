#!/usr/bin/env bash
# 第30轮验证：
#   1) 任务详情页描述区配图 → 点击蒙层预览大图（DS Image 契约）
#   2) 左栏/右栏拖动互换位置的手感优化（跟手 + FLIP + 回弹 + 甩动）
#   3) 左栏 aside 里「任务属性」「任务动态」下辖内容文字全部 13px
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL_DETAIL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r30/shots"
PROBE="mg-work/r30/probe30.jsonl"
mkdir -p "$OUT"
: > "$PROBE"

# JS 前置：查询/测量/合成指针事件工具
HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},C=function(e){var r=e.getBoundingClientRect();return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)}},UNIQ=function(a){var o={};a.forEach(function(v){o[String(v)]=1});return Object.keys(o)},FS=function(e){return getComputedStyle(e).fontSize},PE=function(t,x,y,el){(el||Q(".td-bar")).dispatchEvent(new PointerEvent(t,{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:0,buttons:t==="pointerup"?0:1,pointerId:7,pointerType:"mouse",isPrimary:true}))},SPIN=function(ms){var t=Date.now();while(Date.now()-t<ms){}},SG=function(){var L=Q(".td-left").getBoundingClientRect(),Rt=Q(".td-right").getBoundingClientRect();return ((Rt.left+Rt.width/2)>=(L.left+L.width/2))?1:-1};'
# SG() → 参数面板(.td-left)的 dir：正常顺序(左栏在左) = 1，已互换(row-reverse) = -1
# 同值可作 clientX 增量倍数使用（把「朝对栏方向」的位移量换算成 clientX 增量）。

# rec <step> <raw-json>  → 规范化后追加到 jsonl
rec() {
  "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:600]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$PROBE"
}

# xy <raw-json> → "x y"
xy() {
  "$P" -c "
import json,sys
d=sys.stdin.read().strip()
d=json.loads(d)
d=json.loads(d) if isinstance(d,str) else d
print(str(d['x'])+' '+str(d['y']))
"
}

md5of() { "$P" -c "import hashlib,sys;print(hashlib.md5(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }

echo "##################################################"
echo "# 第 1 项：描述区配图 → 蒙层预览大图"
echo "##################################################"
$AB open "$URL_DETAIL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "--- 1a. 基线与组件契约结构 ---"
rec 1a "$($AB eval "$HELP JSON.stringify((function(){var w=Q(\".td-desc .giencoder-image-mask-wrapper\");var box=Q(\".td-desc .giencoder-image\");var im=w?w.querySelector(\".giencoder-image-img\"):null;var hm=w?w.querySelector(\".giencoder-image-mask\"):null;return {hasImage:!!box,hasWrapper:!!w,wrapRect:w?R(w):null,wrapCursor:w?getComputedStyle(w).cursor:null,role:w?w.getAttribute(\"role\"):null,tabindex:w?w.getAttribute(\"tabindex\"):null,ariaLabel:w?w.getAttribute(\"aria-label\"):null,imgClass:im?im.className:null,natural:[im?im.naturalWidth:0,im?im.naturalHeight:0],complete:im?im.complete:null,attrWH:[im?im.getAttribute(\"width\"):null,im?im.getAttribute(\"height\"):null],maskOpacity:hm?getComputedStyle(hm).opacity:null,maskText:hm?hm.textContent:null,previewExistsBefore:!!Q(\".giencoder-image-preview\"),htmlFlagBefore:document.documentElement.hasAttribute(\"data-td-img-preview\")};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/10-desc-img.png" >/dev/null 2>&1
echo "md5 10-desc-img  = $(md5of "$OUT/10-desc-img.png")"

echo "--- 1b. 真实 hover 缩略图 → 悬停蒙层「预览」显形 ---"
CW=$($AB eval "$HELP JSON.stringify(C(Q(\".td-desc .giencoder-image-mask-wrapper\")))" 2>&1 | tail -1)
read WX WY <<< "$(echo "$CW" | xy)"
echo "wrapper center = $WX,$WY"
$AB mouse move "$WX" "$WY" >/dev/null 2>&1
sleep 0.5
rec 1b "$($AB eval "$HELP JSON.stringify((function(){var w=Q(\".td-desc .giencoder-image-mask-wrapper\");var hm=w.querySelector(\".giencoder-image-mask\");var hcs=getComputedStyle(hm);return {maskOpacity:hcs.opacity,maskVisible:hcs.visibility,maskBg:hcs.backgroundColor,maskColor:hcs.color,maskRect:R(hm),svgCount:hm.querySelectorAll(\"svg\").length,hitClass:(document.elementFromPoint($WX,$WY)||{}).className||null};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/11-desc-img-hover.png" >/dev/null 2>&1
echo "md5 11-desc-img-hover = $(md5of "$OUT/11-desc-img-hover.png")"

echo "--- 1c. 点击缩略图 → 打开预览蒙层 ---"
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.7
rec 1c "$($AB eval "$HELP JSON.stringify((function(){var p=Q(\".giencoder-image-preview\");if(!p)return {exists:false};var im=p.querySelector(\".giencoder-image-preview-img\");var thumb=Q(\".td-desc .giencoder-image-img\");var close=Q(\".giencoder-image-preview-close\");var zoom=Q(\".giencoder-image-preview-zoom\");var mask=Q(\".giencoder-image-preview-mask\");return {exists:true,display:getComputedStyle(p).display,opacity:getComputedStyle(p).opacity,isOpen:p.classList.contains(\"is-open\"),htmlFlag:document.documentElement.hasAttribute(\"data-td-img-preview\"),overlayRect:R(p),overlayBg:getComputedStyle(p).backgroundColor,zIndex:getComputedStyle(p).zIndex,position:getComputedStyle(p).position,srcMatch:!!(im&&thumb&&im.getAttribute(\"src\")===thumb.getAttribute(\"src\")),altMatch:!!(im&&thumb&&im.getAttribute(\"alt\")===thumb.getAttribute(\"alt\")),imgRect:R(im),imgMaxW:getComputedStyle(im).maxWidth,closeRect:R(close),zoomRect:R(zoom),maskRect:R(mask),openingClass:im.classList.contains(\"is-opening\")};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/12-preview-open.png" >/dev/null 2>&1
echo "md5 12-preview-open = $(md5of "$OUT/12-preview-open.png")"

echo "--- 1d. 工具栏缩放：点放大一次 → scale 1.25 ---"
ZO=$($AB eval "$HELP JSON.stringify(C(Q(\".giencoder-image-preview-zoom [data-td-zoom=in]\")))" 2>&1 | tail -1)
read ZX ZY <<< "$(echo "$ZO" | xy)"
echo "zoom-in center = $ZX,$ZY"
$AB mouse move "$ZX" "$ZY" >/dev/null 2>&1
sleep 0.3
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.5
rec 1d "$($AB eval "$HELP JSON.stringify((function(){var im=Q(\".giencoder-image-preview-img\");return {transform:getComputedStyle(im).transform,scaleVar:getComputedStyle(im).getPropertyValue(\"--giencoder-image-scale\"),stillOpen:Q(\".giencoder-image-preview\").classList.contains(\"is-open\"),imgRect:R(im)};})())" 2>&1 | tail -1)"

echo "--- 1e. 点右上关闭按钮 → 关闭（等 0.6s 后 display none） ---"
CO=$($AB eval "$HELP JSON.stringify(C(Q(\".giencoder-image-preview-close\")))" 2>&1 | tail -1)
read CX2 CY2 <<< "$(echo "$CO" | xy)"
echo "close center = $CX2,$CY2"
$AB mouse move "$CX2" "$CY2" >/dev/null 2>&1
sleep 0.3
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.6
rec 1e "$($AB eval "$HELP JSON.stringify((function(){var p=Q(\".giencoder-image-preview\");return {display:getComputedStyle(p).display,opacity:getComputedStyle(p).opacity,isOpen:p.classList.contains(\"is-open\"),htmlFlag:document.documentElement.hasAttribute(\"data-td-img-preview\"),url:location.pathname.split(\"/\").pop()};})())" 2>&1 | tail -1)"

echo "--- 1f. 再打开 → 点图片外空白处关闭 ---"
$AB mouse move "$WX" "$WY" >/dev/null 2>&1
sleep 0.3
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.6
rec 1f1 "$($AB eval "$HELP JSON.stringify({reopened:Q(\".giencoder-image-preview\").classList.contains(\"is-open\"),htmlFlag:document.documentElement.hasAttribute(\"data-td-img-preview\")})" 2>&1 | tail -1)"
$AB mouse move 20 20 >/dev/null 2>&1
sleep 0.25
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.6
rec 1f2 "$($AB eval "$HELP JSON.stringify((function(){var p=Q(\".giencoder-image-preview\");return {display:getComputedStyle(p).display,isOpen:p.classList.contains(\"is-open\"),htmlFlag:document.documentElement.hasAttribute(\"data-td-img-preview\"),hitAt2020:(document.elementFromPoint(20,20)||{}).className||null};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/14-after-close.png" >/dev/null 2>&1

echo "--- 1g. 再打开 → Esc 关预览（且不跳回看板） ---"
$AB mouse move "$WX" "$WY" >/dev/null 2>&1
sleep 0.3
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.6
$AB press Escape >/dev/null 2>&1
sleep 0.6
rec 1g "$($AB eval "$HELP JSON.stringify((function(){var p=Q(\".giencoder-image-preview\");return {display:getComputedStyle(p).display,isOpen:p.classList.contains(\"is-open\"),htmlFlag:document.documentElement.hasAttribute(\"data-td-img-preview\"),url:location.pathname.split(\"/\").pop(),detailStillThere:!!Q(\".td-root\"),activeEl:document.activeElement?document.activeElement.className:null};})())" 2>&1 | tail -1)"

echo "--- 1h. 回归：预览已关，再按 Esc → 才回看板 ---"
$AB press Escape >/dev/null 2>&1
sleep 1.6
rec 1h "$($AB eval "$HELP JSON.stringify({url:location.pathname.split(\"/\").pop()})" 2>&1 | tail -1)"

echo ""
echo "##################################################"
echo "# 第 2 项：两栏拖动互换手感"
echo "##################################################"
$AB open "$URL_DETAIL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "--- 2a. 基线：类名 / 过渡属性 / 栏位 ---"
rec 2a "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),Rt=Q(\".td-right\"),bar=Q(\".td-bar\");var cs=getComputedStyle(L);return {swapped:root.classList.contains(\"is-swapped\"),flex:getComputedStyle(root).flexDirection,leftRect:R(L),rightRect:R(Rt),gapW:Math.round(Q(\".td-gutter\").getBoundingClientRect().width),cursor:getComputedStyle(bar).cursor,touchAction:getComputedStyle(bar).touchAction,transitionProp:cs.transitionProperty,transitionDur:cs.transitionDuration,outlineColor:cs.outlineColor,willChange:cs.willChange,leftTransform:cs.transform,rightTransform:getComputedStyle(Rt).transform};})())" 2>&1 | tail -1)"

echo "--- 2b. 跟手（限幅位移）+ 未达阈值回弹 ---"
rec 2b "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),Rt=Q(\".td-right\"),bar=Q(\".td-bar\");var r=bar.getBoundingClientRect();var y=Math.round(r.top+r.height/2),x=Math.round(r.left+220);var sg=SG();var o={x:x,y:y,dir:SG(),sg:sg};
PE(\"pointerdown\",x,y);SPIN(70);PE(\"pointermove\",x+sg*20,y);
o.at20={left:getComputedStyle(L).transform,peer:getComputedStyle(Rt).transform,xdrag:root.classList.contains(\"is-xdrag\"),cursor:getComputedStyle(bar).cursor};
SPIN(70);PE(\"pointermove\",x+sg*40,y);
o.at40={left:getComputedStyle(L).transform,peer:getComputedStyle(Rt).transform,armed:root.classList.contains(\"is-xarmed\"),outline:getComputedStyle(L).outlineColor,peerOpacity:getComputedStyle(Rt).opacity};
PE(\"pointerup\",x+sg*40,y);
o.released={swapped:root.classList.contains(\"is-swapped\"),left:getComputedStyle(L).transform,peer:getComputedStyle(Rt).transform,fly:root.classList.contains(\"is-swap-fly\"),xdrag:root.classList.contains(\"is-xdrag\")};
return o;})())" 2>&1 | tail -1)"
sleep 0.8
rec 2b2 "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),Rt=Q(\".td-right\");return {left:getComputedStyle(L).transform,peer:getComputedStyle(Rt).transform,swapped:root.classList.contains(\"is-swapped\"),xdrag:root.classList.contains(\"is-xdrag\"),armed:root.classList.contains(\"is-xarmed\")};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/20-drag-rebound.png" >/dev/null 2>&1

echo "--- 2c. 越阈值 → 跟手限幅 + armed 描边 ---"
rec 2c "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),Rt=Q(\".td-right\"),bar=Q(\".td-bar\");var r=bar.getBoundingClientRect();var y=Math.round(r.top+r.height/2),x=Math.round(r.left+220);var sg=SG();var o={x:x,y:y,sg:sg};
o.before={left:R(L),right:R(Rt),rootX:Math.round(Q(\".td-root\").getBoundingClientRect().left),gap:Math.round(Q(\".td-gutter\").getBoundingClientRect().width)};
PE(\"pointerdown\",x,y);SPIN(50);PE(\"pointermove\",x+sg*30,y);SPIN(50);PE(\"pointermove\",x+sg*120,y);
o.dragging={left:getComputedStyle(L).transform,peer:getComputedStyle(Rt).transform,peerOpacity:getComputedStyle(Rt).opacity,armed:root.classList.contains(\"is-xarmed\"),xdrag:root.classList.contains(\"is-xdrag\"),outlineNow:getComputedStyle(L).outlineColor};
SPIN(50);PE(\"pointermove\",x+sg*400,y);
o.draggingFar={left:getComputedStyle(L).transform,peer:getComputedStyle(Rt).transform};
return o;})())" 2>&1 | tail -1)"
sleep 0.35
rec 2c1b "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),Rt=Q(\".td-right\");return {held:root.classList.contains(\"is-xdrag\"),armed:root.classList.contains(\"is-xarmed\"),outline:getComputedStyle(L).outlineColor,outlineWidth:getComputedStyle(L).outlineWidth,peerOpacity:getComputedStyle(Rt).opacity,willChange:getComputedStyle(L).willChange,left:getComputedStyle(L).transform};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/21-drag-armed.png" >/dev/null 2>&1
rec 2c1c "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),Rt=Q(\".td-right\"),bar=Q(\".td-bar\");var r=bar.getBoundingClientRect();var y=Math.round(r.top+r.height/2),x=Math.round(r.left+220);var sg=SG();
PE(\"pointerup\",x+sg*120,y);
return {swapped:root.classList.contains(\"is-swapped\"),fly:root.classList.contains(\"is-swap-fly\"),flyLeft:root.classList.contains(\"is-fly-left\"),flyRight:root.classList.contains(\"is-fly-right\"),flex:getComputedStyle(root).flexDirection,left:getComputedStyle(L).transform,right:getComputedStyle(Rt).transform,zRight:getComputedStyle(Rt).zIndex,zLeft:getComputedStyle(L).zIndex,boxLeft:getComputedStyle(L).boxShadow!==\"none\",xdrag:root.classList.contains(\"is-xdrag\"),armed:root.classList.contains(\"is-xarmed\")};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/21-swap-mid-flight.png" >/dev/null 2>&1
sleep 0.9
rec 2c2 "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),Rt=Q(\".td-right\");return {swapped:root.classList.contains(\"is-swapped\"),fly:root.classList.contains(\"is-swap-fly\"),flex:getComputedStyle(root).flexDirection,leftRect:R(L),rightRect:R(Rt),leftTransform:getComputedStyle(L).transform,rightTransform:getComputedStyle(Rt).transform,zLeft:getComputedStyle(L).zIndex,zRight:getComputedStyle(Rt).zIndex,rootX:Math.round(Q(\".td-root\").getBoundingClientRect().left)};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/22-swap-done.png" >/dev/null 2>&1

echo "--- 2d. 纯点击（位移 <6px）不换位、不进拖动态 ---"
rec 2d "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),bar=Q(\".td-bar\");var r=bar.getBoundingClientRect();var y=Math.round(r.top+r.height/2),x=Math.round(r.left+220);var sg=SG();var before=root.classList.contains(\"is-swapped\");
PE(\"pointerdown\",x,y);PE(\"pointermove\",x+sg*2,y);PE(\"pointerup\",x+sg*2,y);
return {swappedBefore:before,swappedAfter:root.classList.contains(\"is-swapped\"),xdrag:root.classList.contains(\"is-xdrag\"),armed:root.classList.contains(\"is-xarmed\"),left:getComputedStyle(L).transform,fly:root.classList.contains(\"is-swap-fly\")};})())" 2>&1 | tail -1)"

echo "--- 2e. 点栏内按钮不触发拖动 ---"
rec 2e "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\");var btn=QA(\".td-bar .td-btn\")[1];var c=C(btn);var sg=SG();var before=root.classList.contains(\"is-swapped\");
PE(\"pointerdown\",c.x,c.y,btn);PE(\"pointermove\",c.x+sg*160,c.y,btn);
var mid={xdrag:root.classList.contains(\"is-xdrag\"),left:getComputedStyle(L).transform,armed:root.classList.contains(\"is-xarmed\")};
PE(\"pointercancel\",c.x+sg*160,c.y,btn);
return {target:btn.textContent,swappedBefore:before,mid:mid,after:{swapped:root.classList.contains(\"is-swapped\"),url:location.pathname.split(\"/\").pop()}};})())" 2>&1 | tail -1)"

echo "--- 2f. 甩动（位移不足、速度够）也能换位 ---"
rec 2f "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),bar=Q(\".td-bar\");var r=bar.getBoundingClientRect();var y=Math.round(r.top+r.height/2),x=Math.round(r.left+220);var sg=SG();var before=root.classList.contains(\"is-swapped\");
PE(\"pointerdown\",x,y);PE(\"pointermove\",x+sg*2,y);PE(\"pointermove\",x+sg*40,y);
var mid={dx:40,sg:sg,armed:root.classList.contains(\"is-xarmed\"),left:getComputedStyle(L).transform};
PE(\"pointerup\",x+sg*40,y);
return {swappedBefore:before,mid:mid,swappedAfter:root.classList.contains(\"is-swapped\"),fly:root.classList.contains(\"is-swap-fly\")};})())" 2>&1 | tail -1)"
sleep 0.9
rec 2f2 "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\");return {swapped:root.classList.contains(\"is-swapped\"),flex:getComputedStyle(root).flexDirection};})())" 2>&1 | tail -1)"

echo "--- 2g. 全屏态下禁止拖动（互斥） ---"
rec 2g "$($AB eval "$HELP JSON.stringify((function(){var root=Q(\".td-root\"),L=Q(\".td-left\"),bar=Q(\".td-bar\");var sg=SG();
Q(\"[data-td-fullscreen]\").click();
var fs=root.classList.contains(\"is-fullscreen\");
PE(\"pointerdown\",100,100);PE(\"pointermove\",100+sg*160,100);
var mid={xdrag:root.classList.contains(\"is-xdrag\"),left:getComputedStyle(L).transform,armed:root.classList.contains(\"is-xarmed\")};
PE(\"pointercancel\",100+sg*160,100);
var swapped=root.classList.contains(\"is-swapped\");
Q(\"[data-td-fullscreen]\").click();
return {fullscreen:fs,mid:mid,swappedDuringFs:swapped,fullscreenAfterExit:root.classList.contains(\"is-fullscreen\")};})())" 2>&1 | tail -1)"

echo "--- 2h. 回归：全屏后内容区仍 860 居中（第 29 轮） ---"
$AB eval "$HELP (function(){Q(\"[data-td-fullscreen]\").click();})()" >/dev/null 2>&1
sleep 0.7
rec 2h "$($AB eval "$HELP JSON.stringify((function(){var right=Q(\".td-right\"),inner=Q(\".td-chat-inner\"),comp=Q(\".td-composer\");var rb=right.getBoundingClientRect(),ib=inner.getBoundingClientRect(),cb=comp.getBoundingClientRect();function m(r){return Math.round((r.left+r.right)/2*10)/10}return {rightW:Math.round(rb.width),inner:[Math.round(ib.left),Math.round(ib.right),Math.round(ib.width)],composer:[Math.round(cb.left),Math.round(cb.right),Math.round(cb.width)],innerVsRightCenter:Math.round((m(ib)-m(rb))*10)/10,composerVsRightCenter:Math.round((m(cb)-m(rb))*10)/10,innerEqComposer:Math.abs(ib.left-cb.left)<=1&&Math.abs(ib.right-cb.right)<=1};})())" 2>&1 | tail -1)"
$AB eval "$HELP (function(){Q(\"[data-td-fullscreen]\").click();})()" >/dev/null 2>&1
sleep 0.5

echo ""
echo "##################################################"
echo "# 第 3 项：aside 内容文字 13px"
echo "##################################################"
rec 3 "$($AB eval "$HELP JSON.stringify((function(){var attr=QA(\".td-attr-row\"),tl1=QA(\".td-tl-line1\"),tlt=QA(\".td-tl-time\"),h2=QA(\".td-side h2\"),prio=QA(\".td-tag-prio\"),k=QA(\".td-attr-k\"),v=QA(\".td-attr-v\"),who=QA(\".td-tl-who\"),what=QA(\".td-tl-what\"),foot=QA(\".td-side-foot .td-attr-row\"),sideAttr=QA(\".td-side-attr .td-attr-row\"),sideDyn=QA(\".td-side-dyn .td-tl-line1\");return {tokenBody2:getComputedStyle(document.documentElement).getPropertyValue(\"--font-size-body-2\").trim(),tokenBody3:getComputedStyle(document.documentElement).getPropertyValue(\"--font-size-body-3\").trim(),attrCount:attr.length,attrFs:UNIQ(attr.map(FS)),attrLh:UNIQ(attr.map(function(e){return getComputedStyle(e).lineHeight})),sideAttrFs:UNIQ(sideAttr.map(FS)),kFs:UNIQ(k.map(FS)),vFs:UNIQ(v.map(FS)),tl1Count:tl1.length,tl1Fs:UNIQ(tl1.map(FS)),tl1Lh:UNIQ(tl1.map(function(e){return getComputedStyle(e).lineHeight})),sideDynFs:UNIQ(sideDyn.map(FS)),whoFs:UNIQ(who.map(FS)),whatFs:UNIQ(what.map(FS)),tltCount:tlt.length,tltFs:UNIQ(tlt.map(FS)),tltLh:UNIQ(tlt.map(function(e){return getComputedStyle(e).lineHeight})),footCount:foot.length,footFs:UNIQ(foot.map(FS)),h2Count:h2.length,h2Fs:UNIQ(h2.map(FS)),prioCount:prio.length,prioFs:UNIQ(prio.map(FS))};})())" 2>&1 | tail -1)"
$AB screenshot "$OUT/30-side-13px.png" >/dev/null 2>&1

echo ""
echo "##################################################"
echo "# 回归：第 28 轮基线几何"
echo "##################################################"
$AB open "$URL_DETAIL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0
rec R1 "$($AB eval "$HELP JSON.stringify((function(){return {barH:Math.round(Q(\".td-bar\").getBoundingClientRect().height),leftW:Math.round(Q(\".td-left\").getBoundingClientRect().width),rightW:Math.round(Q(\".td-right\").getBoundingClientRect().width),main:Math.round(Q(\".td-main\").getBoundingClientRect().width),side:Math.round(Q(\".td-side\").getBoundingClientRect().width),gap:Math.round(Q(\".td-gutter\").getBoundingClientRect().width),titleBg:getComputedStyle(Q(\".td-title\")).backgroundColor,sideLeftBorder:getComputedStyle(Q(\".td-side\")).borderLeftColor};})())" 2>&1 | tail -1)"
rec R2 "$($AB eval "$HELP JSON.stringify((function(){var b=Q(\".td-desc-body\");var before=b.getBoundingClientRect().height;Q(\"[data-td-desc-toggle]\").click();var open=b.classList.contains(\"is-open\");return {before:Math.round(before),open:open,label:Q(\"[data-td-desc-toggle]\").textContent.trim()};})())" 2>&1 | tail -1)"
rec R3 "$($AB eval "$HELP JSON.stringify((function(){var s=Q(\".td-side .giencoder-select-view\");var f=QA(\"[data-td-fullscreen]\").length;return {hasAsideSelect:!!s,fullscreenBtn:f};})())" 2>&1 | tail -1)"

echo ""
echo "================ probe30.jsonl ================"
wc -l "$PROBE"
ls -la "$OUT"
