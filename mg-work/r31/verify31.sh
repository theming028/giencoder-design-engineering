#!/usr/bin/env bash
# 第31轮验证：
#   顶栏「转派」→ 成员浮窗（设计稿节点 1345:18366，320×480）
#   组件契约：div.giencoder-popover / .giencoder-input-wrapper / .giencoder-list-item
#             / .giencoder-avatar(-circle -text) / .giencoder-popover-footer
#             / .giencoder-scroll-thin / .giencoder-message
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL_DETAIL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r31/shots"
PROBE="mg-work/r31/probe31.jsonl"
mkdir -p "$OUT"
: > "$PROBE"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},C=function(e){var r=e.getBoundingClientRect();return{x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)}},P2=function(a,e){var p=a.getBoundingClientRect(),b=e.getBoundingClientRect();return{x:+(b.left-p.left).toFixed(1),y:+(b.top-p.top).toFixed(1),w:+b.width.toFixed(1),h:+b.height.toFixed(1)}},CS=function(e,p){return getComputedStyle(e)[p]},RR=function(e,p){return getComputedStyle(e).getPropertyValue(p).trim()},POP=function(){return Q(".td-dp")},BTN=function(){return Q("[data-td-dispatch]")},ROWS=function(){return QA(".td-dp .td-dp-item")},VIS=function(){return ROWS().filter(function(e){return !e.hidden})};'

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
ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }
xy() { "$P" -c "
import json,sys
d=sys.stdin.read().strip()
d=json.loads(d); d=json.loads(d) if isinstance(d,str) else d
print(str(d['x'])+' '+str(d['y']))
"; }
md5of() { "$P" -c "import hashlib,sys;print(hashlib.md5(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }

echo "##################################################"
echo "# 第 31 轮：转派成员浮窗"
echo "##################################################"
$AB open "$URL_DETAIL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "--- 1a. 基线与触发按钮契约 ---"
rec 1a "$(ev 'JSON.stringify((function(){var b=BTN(),ref=b?b.parentNode:null;return{hasBtn:!!b,btnRect:b?R(b):null,btnText:b?b.textContent:null,refClass:ref?ref.className:null,ariaExpanded:b?b.getAttribute("aria-expanded"):null,ariaHasPopup:b?b.getAttribute("aria-haspopup"):null,popExistsBefore:!!POP(),htmlFlagBefore:document.documentElement.hasAttribute("data-td-dp-open"),url:location.href.split("/").pop()};})())')"
$AB screenshot "$OUT/10-dp-btn.png" >/dev/null 2>&1

echo "--- 1b. 点击「转派」→ 浮窗打开（class / 标记 / aria / 位置） ---"
$AB click '[data-td-dispatch]' >/dev/null 2>&1
sleep 0.6
rec 1b "$(ev 'JSON.stringify((function(){var p=POP(),b=BTN();var pr=p.getBoundingClientRect(),br=b.getBoundingClientRect();return{cls:p.className,hasOpen:p.classList.contains("giencoder-popup-open"),rect:R(p),opacity:CS(p,"opacity"),visibility:CS(p,"visibility"),zIndex:CS(p,"z-index"),parentTag:p.parentNode.tagName,leftOffset:+(pr.left-br.left).toFixed(1),topGap:+(pr.top-br.top-br.height).toFixed(1),htmlFlag:document.documentElement.hasAttribute("data-td-dp-open"),ariaExpanded:b.getAttribute("aria-expanded"),role:p.getAttribute("role"),ariaLabel:p.getAttribute("aria-label"),tabindex:p.getAttribute("tabindex"),activeIsPop:document.activeElement===p,scrollbarWidth:CS(p,"scrollbarWidth")};})())')"
$AB screenshot "$OUT/11-dp-open.png" >/dev/null 2>&1
echo "md5 11-dp-open = $(md5of "$OUT/11-dp-open.png")"

echo "--- 1c. 内部结构契约（DS 类名 / role / 尺寸档 / 数量） ---"
rec 1c "$(ev 'JSON.stringify((function(){var p=POP();var t=p.querySelector(".giencoder-popover-title"),c=p.querySelector(".giencoder-popover-content"),w=p.querySelector(".giencoder-input-wrapper"),pf=p.querySelector(".giencoder-input-prefix"),inp=p.querySelector(".giencoder-input"),ls=p.querySelector(".giencoder-list"),ft=p.querySelector(".giencoder-popover-footer"),ok=p.querySelector(".giencoder-btn");var r0=ROWS()[0];var av=r0.querySelector(".giencoder-avatar"),mt=r0.querySelector(".giencoder-list-item-meta"),tl=r0.querySelector(".giencoder-list-item-title"),ac=r0.querySelector(".giencoder-list-item-action"),ck=r0.querySelector(".td-dp-check");return{title:!!t,content:!!c,wrap:!!w,wrapDataSize:w?w.getAttribute("data-size"):null,prefix:!!pf,input:!!inp,inputPlaceholder:inp?inp.getAttribute("placeholder"):null,list:!!ls,listRole:ls?ls.getAttribute("role"):null,listCls:ls?ls.className:null,footer:!!ft,okBtn:!!ok,okCls:ok?ok.className:null,okText:ok?ok.textContent:null,rowCount:ROWS().length,rowCls:r0.className,rowRole:r0.getAttribute("role"),rowSize:r0.getAttribute("data-size"),avatarCls:av?av.className:null,avatarText:av?av.textContent:null,metaCls:mt?mt.className:null,titleCls:tl?tl.className:null,titleText:tl?tl.textContent:null,actionCls:ac?ac.className:null,checkSvgCount:ck?ck.querySelectorAll("svg").length:0};})())')"

echo "--- 1d. 几何真值（面板内相对坐标；设计稿：标题文字盒(16,16)h22/副标题(16,42)h16/搜索288x32@(16,70)/列表@(16,118)h297/行32/头像20/按钮288x32@(16,432)） ---"
rec 1d "$(ev 'JSON.stringify((function(){var p=POP(),ROW=ROWS()[0];var av=ROW.querySelector(".giencoder-avatar");var tt=p.querySelector(".giencoder-popover-title"),tbox=P2(p,tt),tpl=parseFloat(CS(tt,"paddingLeft")),tpt=parseFloat(CS(tt,"paddingTop")),tpr=parseFloat(CS(tt,"paddingRight"));var pr=p.getBoundingClientRect();var ls=p.querySelector(".giencoder-list"),l0=ROWS()[6].getBoundingClientRect();return{panel:R(p),panelRaw:[+(pr.width.toFixed(2)),+(pr.height.toFixed(2))],titleContent:{x:+(tbox.x+tpl).toFixed(1),y:+(tbox.y+tpt).toFixed(1),w:+(tbox.w-tpl-tpr).toFixed(1)},sub:P2(p,p.querySelector(".td-dp-t2")),search:P2(p,p.querySelector(".giencoder-input-wrapper")),prefix:P2(p,p.querySelector(".giencoder-input-prefix")),input:P2(p,p.querySelector(".giencoder-input")),list:P2(p,ls),row0:P2(p,ROWS()[0]),row1:P2(p,ROWS()[1]),row2:P2(p,ROWS()[2]),avatar:P2(p,av),name:P2(p,ROW.querySelector(".td-dp-name")),check0:P2(p,ROWS()[0].querySelector(".td-dp-check")),footer:P2(p,p.querySelector(".giencoder-popover-footer")),ok:P2(p,p.querySelector(".td-dp-ok")),pitch:+(ROWS()[1].getBoundingClientRect().top-ROWS()[0].getBoundingClientRect().top).toFixed(1),rowContentH:Math.round(l0.bottom-ls.getBoundingClientRect().top),listScrollH:ls.scrollHeight,listClientH:ls.clientHeight};})())')"

echo "--- 1e. 配色 / 字号 / 圆角 / 投影真值 ---"
rec 1e "$(ev 'JSON.stringify((function(){var p=POP(),ROW=ROWS()[1],t=p.querySelector(".giencoder-popover-title"),sub=p.querySelector(".td-dp-t2"),w=p.querySelector(".giencoder-input-wrapper"),pf=p.querySelector(".giencoder-input-prefix"),inp=p.querySelector(".giencoder-input"),ls=p.querySelector(".giencoder-list"),ft=p.querySelector(".giencoder-popover-footer"),ok=p.querySelector(".td-dp-ok"),sel=ROWS()[0],av=ROW.querySelector(".giencoder-avatar");return{panelBg:CS(p,"backgroundColor"),panelBorder:CS(p,"borderTopColor"),panelRadius:CS(p,"borderTopLeftRadius"),panelShadow:CS(p,"boxShadow"),titleFs:CS(t,"fontSize"),titleLh:CS(t,"lineHeight"),titleColor:CS(t,"color"),titleWeight:CS(t,"fontWeight"),subFs:CS(sub,"fontSize"),subLh:CS(sub,"lineHeight"),subColor:CS(sub,"color"),searchBorder:CS(w,"borderTopColor"),searchRadius:CS(w,"borderTopLeftRadius"),searchH:CS(w,"height"),prefixColor:CS(pf,"color"),inputFs:CS(inp,"fontSize"),listOverflowY:CS(ls,"overflowY"),listScrollbarWidth:CS(ls,"scrollbarWidth"),rowH:CS(ROW,"height"),rowRadius:CS(ROW,"borderTopLeftRadius"),rowPadding:CS(ROW,"paddingLeft"),nameFs:CS(ROW.querySelector(".td-dp-name"),"fontSize"),nameColor:CS(ROW.querySelector(".td-dp-name"),"color"),idColor:CS(ROW.querySelector(".td-dp-id"),"color"),avW:CS(av,"width"),avH:CS(av,"height"),avBg:CS(av,"backgroundColor"),avColor:CS(av,"color"),avFs:CS(av,"fontSize"),avRadius:CS(av,"borderTopLeftRadius"),selBg:CS(sel,"backgroundColor"),selRing:CS(sel,"boxShadow"),checkDisplay:CS(sel.querySelector(".td-dp-check"),"display"),checkColor:CS(sel.querySelector(".td-dp-check"),"color"),footBorderTop:CS(ft,"borderTopColor"),footBorderW:CS(ft,"borderTopWidth"),okBg:CS(ok,"backgroundColor"),okFs:CS(ok,"fontSize"),okRadius:CS(ok,"borderTopLeftRadius")};})())')"

echo "--- 1f. 默认选中（邵禹铭）+ 唯一对勾 ---"
rec 1f "$(ev 'JSON.stringify((function(){var p=POP();var on=ROWS().filter(function(e){return e.getAttribute("aria-selected")==="true"});return{selectedCount:on.length,selectedName:on.length?on[0].textContent.trim():null,selectedIdx:on.length?on[0].getAttribute("data-td-idx"):null,checkVisibleCount:ROWS().filter(function(e){return CS(e.querySelector(".td-dp-check"),"display")!=="none"}).length};})())')"

echo "--- 1g. 真实 hover 第 4 行（顾帆）→ 底 #F7F7F7 ---"
HO=$($AB eval "$HELP JSON.stringify(C(ROWS()[3]))" 2>&1 | tail -1)
read HX HY <<< "$(printf '%s' "$HO" | xy)"
$AB mouse move "$HX" "$HY" >/dev/null 2>&1
sleep 0.4
rec 1g "$(ev 'JSON.stringify((function(){var p=POP(),r=ROWS()[3];return{hoveredText:r.textContent.trim(),bg:CS(r,"backgroundColor"),cursor:CS(r,"cursor"),selBgUnchanged:CS(ROWS()[0],"backgroundColor")};})())')"
$AB screenshot "$OUT/12-dp-hover.png" >/dev/null 2>&1

echo "--- 1h. 点击「秦怡」行 → 选中转移 + 对勾跟随 ---"
$AB click '.td-dp .td-dp-item[data-td-idx="1"]' >/dev/null 2>&1
sleep 0.35
rec 1h "$(ev 'JSON.stringify((function(){var on=ROWS().filter(function(e){return e.getAttribute("aria-selected")==="true"});return{selectedCount:on.length,selectedName:on.length?on[0].textContent.trim():null,row0Sel:ROWS()[0].getAttribute("aria-selected"),row1Sel:ROWS()[1].getAttribute("aria-selected"),row1Bg:CS(ROWS()[1],"backgroundColor"),row1Ring:CS(ROWS()[1],"boxShadow"),row0Bg:CS(ROWS()[0],"backgroundColor"),check0:CS(ROWS()[0].querySelector(".td-dp-check"),"display"),check1:CS(ROWS()[1].querySelector(".td-dp-check"),"display"),dragging:document.querySelector(".td-root").classList.contains("is-xdrag")};})())')"
$AB screenshot "$OUT/13-dp-selected.png" >/dev/null 2>&1

echo "--- 1i. 搜索过滤：韩 / P00986 / zzz(空态) ---"
$AB fill '.td-dp .giencoder-input' '韩' >/dev/null 2>&1
sleep 0.35
rec 1i_han "$(ev 'JSON.stringify({q:"韩",visCount:VIS().length,visText:VIS().map(function(e){return e.textContent.trim()}),noneHidden:Q(".td-dp-none").hidden})')"
$AB fill '.td-dp .giencoder-input' 'P00986' >/dev/null 2>&1
sleep 0.35
rec 1i_id "$(ev 'JSON.stringify({q:"P00986",visCount:VIS().length})')"
$AB fill '.td-dp .giencoder-input' 'zzz' >/dev/null 2>&1
sleep 0.35
rec 1i_none "$(ev 'JSON.stringify((function(){var n=Q(".td-dp-none");return{q:"zzz",visCount:VIS().length,noneHidden:n.hidden,noneText:n.textContent.trim(),noneFs:CS(n.querySelector(".giencoder-empty-description"),"fontSize"),noneColor:CS(n.querySelector(".giencoder-empty-description"),"color")};})())')"
$AB screenshot "$OUT/14-dp-empty.png" >/dev/null 2>&1
$AB fill '.td-dp .giencoder-input' '' >/dev/null 2>&1
sleep 0.3
rec 1i_reset "$(ev 'JSON.stringify({visCount:VIS().length,noneHidden:Q(".td-dp-none").hidden})')"

echo "--- 1j. 点「确定转派」→ 关闭 + 执行人写回 + DS Message ---"
$AB click '.td-dp .td-dp-ok' >/dev/null 2>&1
sleep 0.5
rec 1j "$(ev 'JSON.stringify((function(){var p=POP();var msg=Q(".td-dp-msg");var rows=QA(".td-attr-row"),who=null;rows.forEach(function(r){var k=r.querySelector(".td-attr-k");if(k&&k.textContent.indexOf("执行人")>=0)who=r.querySelector(".td-attr-v").textContent});return{popOpen:p.classList.contains("giencoder-popup-open"),visibility:CS(p,"visibility"),htmlFlag:document.documentElement.hasAttribute("data-td-dp-open"),ariaExpanded:BTN().getAttribute("aria-expanded"),assignee:who,msgExists:!!msg,msgRole:msg?msg.querySelector(".giencoder-message").getAttribute("role"):null,msgCls:msg?msg.querySelector(".giencoder-message").className:null,msgText:msg?msg.querySelector(".giencoder-message-content").textContent:null,msgIconColor:msg?CS(msg.querySelector(".giencoder-message-icon"),"color"):null};})())')"
$AB screenshot "$OUT/15-dp-msg.png" >/dev/null 2>&1

echo "--- 1k. 重开 → 点浮窗外 → 关闭 ---"
$AB click '[data-td-dispatch]' >/dev/null 2>&1
sleep 0.5
OP=$($AB eval "$HELP JSON.stringify((function(){var r=POP().getBoundingClientRect();return{x:Math.round(Math.min(1440-30,r.right+30)),y:Math.round(r.top+40)}})())" 2>&1 | tail -1)
read OX OY <<< "$(printf '%s' "$OP" | xy)"
rec 1k_open "$(ev 'JSON.stringify({openAfterReopen:POP().classList.contains("giencoder-popup-open"),selectedStill:ROWS().filter(function(e){return e.getAttribute("aria-selected")==="true"}).map(function(e){return e.textContent.trim()}),inputValue:Q(".td-dp .giencoder-input").value})')"
$AB mouse move "$OX" "$OY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.4
rec 1k "$(ev 'JSON.stringify({outsideX:'"$OX"',outsideY:'"$OY"',openAfterOutside:POP().classList.contains("giencoder-popup-open"),htmlFlag:document.documentElement.hasAttribute("data-td-dp-open"),url:location.href.split("/").pop()})')"

echo "--- 1l. 重开 → Esc 只关浮窗（不跳看板） ---"
$AB click '[data-td-dispatch]' >/dev/null 2>&1
sleep 0.5
$AB press Escape >/dev/null 2>&1
sleep 0.4
rec 1l "$(ev 'JSON.stringify({openAfterEsc:POP().classList.contains("giencoder-popup-open"),htmlFlag:document.documentElement.hasAttribute("data-td-dp-open"),url:location.href.split("/").pop()})')"

echo "--- 1l2. 焦点在搜索框内按 Esc 也能关（不被页尾 INPUT 判定吞掉） ---"
$AB click '[data-td-dispatch]' >/dev/null 2>&1
sleep 0.5
$AB click '.td-dp .giencoder-input' >/dev/null 2>&1
sleep 0.3
rec 1l2_focus "$(ev 'JSON.stringify({activeIsInput:document.activeElement===Q(".td-dp .giencoder-input")})')"
$AB press Escape >/dev/null 2>&1
sleep 0.4
rec 1l2 "$(ev 'JSON.stringify({openAfterEscInInput:POP().classList.contains("giencoder-popup-open"),url:location.href.split("/").pop()})')"

echo "--- 1m. 浮窗内按下拖动：不得触发两栏互换 ---"
$AB click '[data-td-dispatch]' >/dev/null 2>&1
sleep 0.5
RW=$($AB eval "$HELP JSON.stringify(C(ROWS()[2]))" 2>&1 | tail -1)
read RX RY <<< "$(printf '%s' "$RW" | xy)"
$AB mouse move "$RX" "$RY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
$AB mouse move $((RX+120)) "$RY" >/dev/null 2>&1
sleep 0.2
rec 1m_drag "$(ev 'JSON.stringify({isXdrag:document.querySelector(".td-root").classList.contains("is-xdrag"),isSwapped:document.querySelector(".td-root").classList.contains("is-swapped"),leftRect:R(Q(".td-left"))})')"
$AB mouse up >/dev/null 2>&1
sleep 0.3
rec 1m "$(ev 'JSON.stringify({afterUp_isSwapped:document.querySelector(".td-root").classList.contains("is-swapped"),openStill:POP().classList.contains("giencoder-popup-open")})')"
$AB press Escape >/dev/null 2>&1
sleep 0.3

echo "--- 1n. 滚动条：list 溢出才出（内容 236 < 视口 297），样式已定义 6px ---"
rec 1n "$(ev 'JSON.stringify((function(){var ls=Q(".td-dp .giencoder-list");var css=Array.prototype.slice.call(document.styleSheets).reduce(function(acc,ss){try{Array.prototype.slice.call(ss.cssRules).forEach(function(r){if(r.cssText&&r.cssText.indexOf("giencoder-scroll-thin")>=0&&r.cssText.indexOf("webkit-scrollbar")>=0)acc.push(r.cssText)});}catch(e){}return acc},[]);return{overflowY:CS(ls,"overflowY"),scrollWidth:ls.scrollWidth,clientWidth:ls.clientWidth,thumbRules:css,scrollbarSize:RR(document.documentElement,"--scrollbar-size"),thumbVar:RR(document.documentElement,"--scrollbar-thumb-bg")};})())')"

echo "##################################################"
echo "# 回归（第 28/29/30 轮）"
echo "##################################################"
echo "--- R1. 两栏布局 1440 真值 ---"
rec R1 "$(ev 'JSON.stringify({left:R(Q(".td-left")),right:R(Q(".td-right")),root:R(Q(".td-root")),bar:R(Q(".td-bar")),titleBg:CS(Q(".td-title"),"backgroundColor"),gutter:R(Q(".td-gutter"))})')"

echo "--- R2. 第 30 轮：描述区配图蒙层预览仍可用 ---"
$AB click '.td-desc .giencoder-image-mask-wrapper' >/dev/null 2>&1
sleep 0.6
rec R2 "$(ev 'JSON.stringify((function(){var ov=Q(".giencoder-image-preview"),im=Q(".giencoder-image-preview-img");return{exists:!!ov,rect:ov?R(ov):null,z:ov?CS(ov,"z-index"):null,opacity:ov?CS(ov,"opacity"):null,imgRect:im?R(im):null,htmlFlag:document.documentElement.hasAttribute("data-td-img-preview")};})())')"
$AB press Escape >/dev/null 2>&1
sleep 0.5
rec R2b "$(ev 'JSON.stringify({url:location.href.split("/").pop(),previewOpen:Q(".giencoder-image-preview").classList.contains("is-open")})')"

echo "--- R3. 第 30 轮：拖动顶栏互换两栏 ---"
BL=$($AB eval "$HELP JSON.stringify((function(){var a=Q(\".td-left\").getBoundingClientRect(),b=Q(\".td-right\").getBoundingClientRect();return{x:Math.round(a.left+120),y:Math.round(a.top+24),dx:Math.round((b.left+b.width/2)-(a.left+a.width/2))}})())" 2>&1 | tail -1)
read BX BY BDX <<< "$(printf '%s' "$BL" | "$P" -c "import json,sys;d=sys.stdin.read().strip();d=json.loads(d);d=json.loads(d) if isinstance(d,str) else d;print(d['x'],d['y'],d['dx'])")"
$AB mouse move "$BX" "$BY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
S=$(( BDX > 0 ? 1 : -1 ))
for i in 1 2 3 4 5 6; do $AB mouse move $((BX + S*i*40)) "$BY" >/dev/null 2>&1; done
sleep 0.2
rec R3_mid "$(ev 'JSON.stringify({isXdrag:document.querySelector(".td-root").classList.contains("is-xdrag"),isArmed:document.querySelector(".td-root").classList.contains("is-xarmed")})')"
$AB mouse up >/dev/null 2>&1
sleep 0.9
rec R3 "$(ev 'JSON.stringify({isSwapped:document.querySelector(".td-root").classList.contains("is-swapped"),left:R(Q(".td-left")),right:R(Q(".td-right"))})')"

echo "--- R4. 第 29 轮：全屏内容宽 860 ---"
$AB click '[data-td-fullscreen]' >/dev/null 2>&1
sleep 0.6
rec R4 "$(ev 'JSON.stringify((function(){var c=Q(".td-chat-inner")||Q(".td-right-body")||Q(".td-chat");return{fs:document.querySelector(".td-root").classList.contains("is-fullscreen"),rect:c?R(c):null};})())')"
$AB press Escape >/dev/null 2>&1
sleep 0.5

echo "--- R5. 第 30 轮：aside 字号 13px ---"
rec R5 "$(ev 'JSON.stringify((function(){var UNIQq=function(a){var o={};a.forEach(function(v){o[v]=1});return Object.keys(o)};var f=function(s){return QA(s).map(function(e){return CS(e,"fontSize")})};return{attr:UNIQq(f(".td-attr-row")),tl1:UNIQq(f(".td-tl-line1")),tlTime:UNIQq(f(".td-tl-time")),h2:UNIQq(f(".td-attr-block h2, .td-side h2"))};})())')"

echo "--- R6. 第二次 Esc → 返回看板 ---"
$AB press Escape >/dev/null 2>&1
sleep 1.2
rec R6 "$(ev 'JSON.stringify({url:location.href.split("/").pop()})')"

echo ""
echo "================ probe31.jsonl ================"
wc -l "$PROBE"
echo "================ shots ================"
ls -la "$OUT"
