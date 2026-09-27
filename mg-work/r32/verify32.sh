#!/usr/bin/env bash
# 第32轮验证（第 1/2/3/4 项；第 5 项「协作」弹窗另见 verify32b.sh）：
#   1) 转派浮窗投影 = Select 弹层投影（--shadow3-down / 0 8px 20px rgba(0,0,0,.1)）
#   2) 两栏拖动：1:1 跟手区放宽（cap=中心距×28%）、无 scale、rAF 合并、反向跟随
#   3) AI 对话框文件卡 与 「3个AI产物」卡 = 同一组件（同视觉 + 同交互）
#   4) 左栏拖窄下限 480px（maxRightW 已扣掉拖动条 8px）
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL_DETAIL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r32/shots"
PROBE="mg-work/r32/probe32.jsonl"
mkdir -p "$OUT"
: > "$PROBE"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},C=function(e){var r=e.getBoundingClientRect();return{x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)}},CS=function(e,p){return getComputedStyle(e)[p]},RR=function(e,p){return getComputedStyle(e).getPropertyValue(p).trim()},T=function(e){return CS(e,"transform")},M=function(e){return new DOMMatrixReadOnly(CS(e,"transform"))},TX=function(e){return Math.round(M(e).m41)},ROOT=function(){return Q(".td-root")},L=function(){return Q(".td-left")},RT=function(){return Q(".td-right")},GT=function(){return Q(".td-gutter")};'

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
nums() { "$P" -c "
import json,sys
d=sys.stdin.read().strip()
d=json.loads(d); d=json.loads(d) if isinstance(d,str) else d
print(' '.join(str(d[k]) for k in sys.argv[1:]))
" "$@"; }
# 重新读取拖动条中心与根容器边界（拖动后拖动条会移动，必须每次重测）
gprobe() { ev 'JSON.stringify((function(){var g=GT().getBoundingClientRect(),s=ROOT().getBoundingClientRect();return{x:Math.round(g.left+g.width/2),y:Math.round(g.top+200),rl:Math.round(s.left),rr:Math.round(s.right)}})())'; }

echo "##################################################"
echo "# 第 32 轮：投影 / 拖动 / 卡片统一 / 左栏下限"
echo "##################################################"
$AB open "$URL_DETAIL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "--- 2a. 基线：两栏几何 + 跟手限幅预期 ---"
rec 2a "$(ev 'JSON.stringify((function(){var l=L(),r=RT(),g=GT(),root=ROOT();var a=l.getBoundingClientRect(),b=r.getBoundingClientRect();var gap=Math.abs((b.left+b.width/2)-(a.left+a.width/2));return{left:R(l),right:R(r),gutter:R(g),root:R(root),leftMinCss:RR(root,"--td-left-min"),gap:Math.round(gap),capExpect:Math.max(48,Math.round(gap*0.28))};})())')"

echo "--- 2b. 按住左栏标题栏拖动 → 1:1 跟手 ---"
BL=$($AB eval "$HELP JSON.stringify((function(){var a=L().getBoundingClientRect();return{x:Math.round(a.left+120),y:Math.round(a.top+24)}})())" 2>&1 | tail -1)
read BX BY <<< "$(printf '%s' "$BL" | nums x y)"
$AB mouse move "$BX" "$BY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1

$AB mouse move $((BX+20)) "$BY" >/dev/null 2>&1; sleep 0.20
rec 2b20 "$(ev 'JSON.stringify({moved:ROOT().classList.contains("is-xdrag"),panelTx:TX(L()),peerTx:TX(RT()),scale:+M(L()).a.toFixed(4),transform:T(L())})')"
$AB mouse move $((BX+120)) "$BY" >/dev/null 2>&1; sleep 0.20
rec 2b120 "$(ev 'JSON.stringify({dx:120,panelTx:TX(L()),peerTx:TX(RT()),armed:ROOT().classList.contains("is-xarmed")})')"
$AB mouse move $((BX+400)) "$BY" >/dev/null 2>&1; sleep 0.20
rec 2b400 "$(ev 'JSON.stringify({dx:400,panelTx:TX(L()),peerTx:TX(RT()),scale:+M(L()).a.toFixed(4),panelShadow:CS(L(),"boxShadow")})')"
$AB mouse move $((BX+20)) "$BY" >/dev/null 2>&1; sleep 0.20
rec 2b_back "$(ev 'JSON.stringify({dx:20,panelTx:TX(L()),peerTx:TX(RT())})')"
$AB mouse up >/dev/null 2>&1; sleep 0.5
rec 2c "$(ev 'JSON.stringify({swapped:ROOT().classList.contains("is-swapped"),leftRect:R(L()),panelTransform:CS(L(),"transform"),inlinePanel:L().getAttribute("style")})')"
$AB screenshot "$OUT/20-drag-tracking.png" >/dev/null 2>&1

echo "--- 2d. 连发多帧位移（rAF 合并后终值须等于最后指针位置对应的位移） ---"
$AB mouse move "$BX" "$BY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for d in 30 60 90 150 180 210; do $AB mouse move $((BX+d)) "$BY" >/dev/null 2>&1; done
sleep 0.30
rec 2d "$(ev 'JSON.stringify({lastDx:210,panelTx:TX(L()),peerTx:TX(RT())})')"
# 先退回阈值内再松手（避免这一手就直接换位，干扰后续步骤）
$AB mouse move $((BX+20)) "$BY" >/dev/null 2>&1; sleep 0.15
$AB mouse up >/dev/null 2>&1; sleep 0.5
rec 2d_after "$(ev 'JSON.stringify({swapped:ROOT().classList.contains("is-swapped"),left:R(L())})')"

echo "--- 2e. 朝对方方向超过阈值松手 → 换位（回归） ---"
SD=$($AB eval "$HELP JSON.stringify((function(){var a=L().getBoundingClientRect(),b=RT().getBoundingClientRect();return{s:((b.left+b.width/2)>=(a.left+a.width/2))?1:-1}})())" 2>&1 | tail -1)
read SGN <<< "$(printf '%s' "$SD" | nums s)"
$AB mouse move "$BX" "$BY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for i in 1 2 3 4 5; do $AB mouse move $((BX + SGN*40*i)) "$BY" >/dev/null 2>&1; done
sleep 0.15
rec 2e_mid "$(ev 'JSON.stringify({sign:'"$SGN"',armed:ROOT().classList.contains("is-xarmed"),panelTx:TX(L())})')"
$AB mouse up >/dev/null 2>&1; sleep 0.9
rec 2e "$(ev 'JSON.stringify({swapped:ROOT().classList.contains("is-swapped"),left:R(L()),right:R(RT())})')"
$AB screenshot "$OUT/21-swap-after.png" >/dev/null 2>&1
# 换位后重载页面复位（交换态下两栏语义左右反转，会干扰第 4 项的拖动条测试）
$AB open "$URL_DETAIL" >/dev/null 2>&1
sleep 3.0
rec 2e_reset "$(ev 'JSON.stringify({swapped:ROOT().classList.contains("is-swapped"),left:R(L()),right:R(RT())})')"

echo "--- 1a. 转派浮窗投影（打开后读 computed shadow） ---"
$AB click '[data-td-dispatch]' >/dev/null 2>&1
sleep 0.6
rec 1a "$(ev 'JSON.stringify((function(){var p=Q(".td-dp");return{exists:!!p,shadow:CS(p,"boxShadow"),shadow3tok:RR(document.documentElement,"--shadow3-down"),shadow2tok:RR(document.documentElement,"--shadow2-down")};})())')"
$AB screenshot "$OUT/10-dp-shadow.png" >/dev/null 2>&1
$AB press Escape >/dev/null 2>&1
sleep 0.4

echo "--- 3a. AI 对话框文件卡 vs 「3个AI产物」同名卡（同组件？） ---"
rec 3a "$(ev 'JSON.stringify((function(){var ai=Q(".td-msg-ai .td-file"),pr=QA(".td-sec .td-file--lg").filter(function(e){return e.textContent.indexOf("任务分析报告")>=0})[0];var f=function(c){var ico=c.querySelector(".td-file-ico"),sep=c.querySelector(".td-file-sep"),body=c.querySelector(".td-file-body"),tx=c.querySelector(".td-file-tx"),sz=c.querySelector(".td-file-size");return{tag:c.tagName,cls:c.className,href:c.getAttribute("href"),rect:R(c),bg:CS(c,"backgroundColor"),radius:CS(c,"borderTopLeftRadius"),icoRect:R(ico),icoColor:CS(ico,"color"),sepRect:sep?R(sep):null,sepColor:sep?CS(sep,"backgroundColor"):null,bodyDisplay:body?CS(body,"display"):null,txFs:tx?CS(tx,"fontSize"):null,txFw:tx?CS(tx,"fontWeight"):null,txColor:tx?CS(tx,"color"):null,sizeFs:sz?CS(sz,"fontSize"):null,sizeColor:sz?CS(sz,"color"):null,kids:Array.prototype.map.call(c.children,function(e){return e.className})}};return{ai:f(ai),prod:f(pr)};})())')"

echo "--- 3b. 两者 hover 交互一致（真实 hover 后比背景色） ---"
P1=$($AB eval "$HELP JSON.stringify(C(Q('.td-msg-ai .td-file')))" 2>&1 | tail -1)
read P1X P1Y <<< "$(printf '%s' "$P1" | nums x y)"
$AB mouse move "$P1X" "$P1Y" >/dev/null 2>&1; sleep 0.35
rec 3b_ai "$(ev 'JSON.stringify({which:"ai",bg:CS(Q(".td-msg-ai .td-file"),"backgroundColor"),cursor:CS(Q(".td-msg-ai .td-file"),"cursor")})')"
$AB screenshot "$OUT/30-ai-card-hover.png" >/dev/null 2>&1
P2=$($AB eval "$HELP JSON.stringify(C(QA('.td-sec .td-file--lg').filter(function(e){return e.textContent.indexOf(\"任务分析报告\")>=0})[0]))" 2>&1 | tail -1)
read P2X P2Y <<< "$(printf '%s' "$P2" | nums x y)"
$AB mouse move "$P2X" "$P2Y" >/dev/null 2>&1; sleep 0.35
rec 3b_prod "$(ev 'JSON.stringify({which:"prod",bg:CS(QA(".td-sec .td-file--lg").filter(function(e){return e.textContent.indexOf("任务分析报告")>=0})[0],"backgroundColor"),cursor:CS(QA(".td-sec .td-file--lg").filter(function(e){return e.textContent.indexOf("任务分析报告")>=0})[0],"cursor")})')"
$AB screenshot "$OUT/31-prod-card-hover.png" >/dev/null 2>&1

echo "--- 4a. 拖动条向左拉到极限 → 左栏应停在 480 ---"
GD=$(gprobe); read GX0 GY RLX RRX <<< "$(printf '%s' "$GD" | nums x y rl rr)"
$AB mouse move "$GX0" "$GY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for i in 1 2 3 4 5 6 7 8; do $AB mouse move $(( GX0 - (GX0-RLX)*i/8 )) "$GY" >/dev/null 2>&1; done
$AB mouse move $((RLX+2)) "$GY" >/dev/null 2>&1
sleep 0.3
rec 4a "$(ev 'JSON.stringify((function(){var root=ROOT(),l=L(),r=RT(),g=GT();var rb=root.getBoundingClientRect(),lb=l.getBoundingClientRect(),rr=r.getBoundingClientRect(),gb=g.getBoundingClientRect();return{left:R(l),right:R(r),gutter:R(g),rightWvar:RR(root,"--td-right-w"),leftMinCss:RR(root,"--td-left-min"),noOverflow:(lb.left>=rb.left-0.5)&&(rr.right<=rb.right+0.5)&&(rr.left>=lb.right-0.5),rootScrollW:root.scrollWidth,rootClientW:root.clientWidth};})())')"
$AB screenshot "$OUT/40-left-min480.png" >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1; sleep 0.4
# 复位：重新测拖动条位置，拖到「右栏 = 480」处
GD=$(gprobe); read GX1 GY1 RLX1 RRX1 <<< "$(printf '%s' "$GD" | nums x y rl rr)"
$AB mouse move "$GX1" "$GY1" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
$AB mouse move $((RRX1-480)) "$GY1" >/dev/null 2>&1
sleep 0.2
$AB mouse up >/dev/null 2>&1; sleep 0.4
rec 4a_reset "$(ev 'JSON.stringify({right:R(RT()),left:R(L()),rightWvar:RR(ROOT(),"--td-right-w")})')"

echo "--- 4b. 拖动条向右拉到极限 → 右栏折叠（回归） ---"
GD=$(gprobe); read GX2 GY2 RLX2 RRX2 <<< "$(printf '%s' "$GD" | nums x y rl rr)"
$AB mouse move "$GX2" "$GY2" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for i in 1 2 3 4 5 6 7 8; do $AB mouse move $(( GX2 + (RRX2-GX2)*i/8 )) "$GY2" >/dev/null 2>&1; done
sleep 0.3
rec 4b_mid "$(ev 'JSON.stringify({collapsed:ROOT().classList.contains("is-collapsed"),right:R(RT())})')"
$AB mouse up >/dev/null 2>&1; sleep 0.4
rec 4b "$(ev 'JSON.stringify({collapsed:ROOT().classList.contains("is-collapsed"),rightW:RR(ROOT(),"--td-right-w")})')"
$AB screenshot "$OUT/41-collapsed.png" >/dev/null 2>&1
$AB click '.td-collapsed' >/dev/null 2>&1; sleep 0.6
rec 4b_reset "$(ev 'JSON.stringify({collapsed:ROOT().classList.contains("is-collapsed"),right:R(RT())})')"

echo ""
echo "================ probe32.jsonl ================"
wc -l "$PROBE"
ls -la "$OUT"
