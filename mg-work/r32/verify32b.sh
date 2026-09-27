#!/usr/bin/env bash
# 第32轮第 5 项验证：顶栏「协作」→ 分步模态弹窗（设计稿节点 622:20081）
# 真值来源：mg-work/r32/design/coop.png（1440×900 1x，量取脚本 measure3/4/5.py）
#   遮罩 rgba(0,0,0,.4) + blur(10px) / 面板 640×640 @(400,130) r16 rgba(255,255,255,.95) shadow3-down
#   纵向节奏 header 46 + 18 + steps 32 + 19 + dvd 24 + 11 + content 410 + footer 80 = 640
#   步进 / 搜索过滤 / 计数 / 4 种关闭途径 / data-td-coop-open 开关 / td:close-coop 事件
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL_DETAIL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r32/shots"
PROBE="mg-work/r32/probe32b.jsonl"
mkdir -p "$OUT"
: > "$PROBE"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},C=function(e){var r=e.getBoundingClientRect();return{x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)}},CS=function(e,p){return getComputedStyle(e)[p]},RR=function(e,p){return getComputedStyle(e).getPropertyValue(p).trim()},NUM=function(e,p){return Math.round(parseFloat(getComputedStyle(e)[p]))},CO=function(){return Q(".td-coop")},DLG=function(){return Q(".td-coop .giencoder-modal")},OPEN=function(){return CO()&&!CO().hidden&&CO().classList.contains("is-open")},FLAG=function(){return document.documentElement.hasAttribute("data-td-coop-open")},VISROWS=function(){return QA("[data-td-midx]").filter(function(r){return !r.hidden}).length},CKENABLED=function(n){return QA("[data-td-pane=\""+n+"\"] .giencoder-checkbox-input").filter(function(c){return c.checked}).length};'

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

echo "##################################################"
echo "# 第 32 轮第 5 项：协作分步模态弹窗"
echo "##################################################"
$AB open "$URL_DETAIL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "--- 5a. 初始：弹窗未打开 ---"
rec 5a_init "$(ev 'JSON.stringify({btn:!!Q("[data-td-coop]"),root:!!CO(),hidden:CO().hidden,open:OPEN(),flag:FLAG(),aria:Q("[data-td-coop]").getAttribute("aria-expanded")})')"

echo "--- 5b. 点「协作」→ 打开（遮罩 + 面板几何/圆角/投影） ---"
$AB click '[data-td-coop]' >/dev/null 2>&1
sleep 0.8
rec 5b "$(ev 'JSON.stringify((function(){var d=DLG(),m=Q(".td-coop .giencoder-modal-mask"),w=Q(".td-coop .giencoder-modal-wrapper");return{open:OPEN(),flag:FLAG(),aria:Q("[data-td-coop]").getAttribute("aria-expanded"),panel:R(d),radius:CS(d,"borderTopLeftRadius"),bg:CS(d,"backgroundColor"),shadow:CS(d,"boxShadow"),transform:CS(d,"transform"),wrapper:R(w),maskBg:CS(m,"backgroundColor"),maskBlur:CS(m,"backdropFilter")+"|"+CS(m,"webkitBackdropFilter"),maskOpacity:CS(m,"opacity"),maskR:R(m),dialogRole:d.getAttribute("role"),ariaModal:d.getAttribute("aria-modal")};})())')"
$AB screenshot "$OUT/50-coop-open.png" >/dev/null 2>&1

echo "--- 5c. 纵向节奏：header / steps / dvd / content / footer 逐段 ---"
rec 5c "$(ev 'JSON.stringify((function(){var h=Q(".td-coop .giencoder-modal-header"),t=Q(".td-coop .giencoder-modal-title"),x=Q("[data-td-coop-close]"),s=Q(".td-coop .giencoder-steps"),si=QA("[data-td-step]"),dv=Q(".td-coop-dvd"),dt=Q("[data-td-coop-hint]"),c=Q(".td-coop .giencoder-modal-content"),f=Q(".td-coop .giencoder-modal-footer"),cnt=Q("[data-td-coop-count]");return{header:R(h),headerPad:CS(h,"padding"),headerBorder:CS(h,"borderBottomWidth"),title:R(t),titleFs:CS(t,"fontSize"),titleFw:CS(t,"fontWeight"),titleInk:R(Q(".td-coop .giencoder-modal-title")),close:R(x),steps:R(s),stepsMargin:CS(s,"margin"),stepCount:si.length,stepRects:si.map(function(e){return R(e)}),step0Bg:CS(si[0],"backgroundColor"),step0Border:CS(si[0],"borderTopColor")+" / "+CS(si[0],"borderTopWidth"),step0Color:CS(si[0],"color"),step1Bg:CS(si[1],"backgroundColor"),step1Color:CS(si[1],"color"),step0After:CS(si[0],"clipPath"),step1Clip:CS(si[1],"clipPath"),step0Active:si[0].classList.contains("is-active"),step0Current:si[0].getAttribute("aria-current"),step0Icon:CS(si[0].querySelector(".giencoder-steps-icon"),"display"),step1Icon:CS(si[1].querySelector(".giencoder-steps-icon"),"display"),dvd:R(dv),dvdText:R(dt),dvdTx:dt.textContent,dvdTextFs:CS(dt,"fontSize"),dvdTextColor:CS(dt,"color"),content:R(c),contentPad:CS(c,"padding"),contentBorder:CS(c,"borderTopWidth"),contentRadius:CS(c,"borderTopLeftRadius"),contentBg:CS(c,"backgroundColor"),contentScrollH:c.scrollHeight,contentClientH:c.clientHeight,footer:R(f),footerPad:CS(f,"padding"),footerBorder:CS(f,"borderTopWidth"),count:R(cnt),countFs:CS(cnt,"fontSize"),countColor:CS(cnt,"color"),countText:cnt.textContent};})())')"

echo "--- 5d. Step1 产物行：pitch / 勾选框 / 文本 ---"
rec 5d "$(ev 'JSON.stringify((function(){var rows=QA("[data-td-pane=\"1\"] .td-coop-row"),r0=rows[0],r1=rows[1],cb=r0.querySelector(".giencoder-checkbox-mask"),tx=r0.querySelector(".td-coop-tx"),inp=r0.querySelector(".giencoder-checkbox-input");return{rowCount:rows.length,row0:R(r0),row1:R(r1),pitch:Math.round(R(r1)[1]-R(r0)[1]),rowPad:CS(r0,"padding"),rowGap:CS(r0,"gap"),rowRadius:CS(r0,"borderTopLeftRadius"),rowBg:CS(r0,"backgroundColor"),rowBg1:CS(r1,"backgroundColor"),cb:R(cb),cbBorder:CS(cb,"borderTopWidth")+" / "+CS(cb,"borderTopColor"),cbRadius:CS(cb,"borderTopLeftRadius"),cbBg:CS(cb,"backgroundColor"),cbShadow:CS(cb,"boxShadow"),tx:R(tx),txFs:CS(tx,"fontSize"),txColor:CS(tx,"color"),checked:inp.checked,checked0:CKENABLED("1"),firstText:tx.textContent};})())')"

echo "--- 5e. 取消一个产物 → 计数实时更新 ---"
$AB click '[data-td-pane="1"] .td-coop-row:first-child .giencoder-checkbox-mask' >/dev/null 2>&1
sleep 0.5
rec 5e "$(ev 'JSON.stringify({checked1:CKENABLED("1"),count:Q("[data-td-coop-count]").textContent})')"
$AB click '[data-td-pane="1"] .td-coop-row:first-child .giencoder-checkbox-mask' >/dev/null 2>&1
sleep 0.5
rec 5e_back "$(ev 'JSON.stringify({checked1:CKENABLED("1"),count:Q("[data-td-coop-count]").textContent})')"

echo "--- 5f. 下一步 → Step2（搜索框 + 成员行 + 底栏按钮切换 + hint 文案） ---"
$AB click '[data-td-coop-next]' >/dev/null 2>&1
sleep 0.6
rec 5f "$(ev 'JSON.stringify((function(){var si=QA("[data-td-step]"),p1=Q("[data-td-pane=\"1\"]"),p2=Q("[data-td-pane=\"2\"]"),iw=Q("[data-td-pane=\"2\"] .giencoder-input-wrapper"),ip=Q("[data-td-pane=\"2\"] .giencoder-input-prefix"),ii=Q("[data-td-pane=\"2\"] .giencoder-input"),rows=QA("[data-td-midx]"),av=rows[0].querySelector(".giencoder-avatar"),nm=rows[0].querySelector(".td-coop-mname"),cb=rows[0].querySelector(".giencoder-checkbox-mask");return{pane1Hidden:p1.hidden,pane2Hidden:p2.hidden,step0Active:si[0].classList.contains("is-active"),step0Finish:si[0].classList.contains("is-finish"),step0Icon:CS(si[0].querySelector(".giencoder-steps-icon"),"display"),step1Active:si[1].classList.contains("is-active"),step1Current:si[1].getAttribute("aria-current"),hint:Q("[data-td-coop-hint]").textContent,count:Q("[data-td-coop-count]").textContent,nextHidden:Q("[data-td-coop-next]").hidden,prevHidden:Q("[data-td-coop-prev]").hidden,submitHidden:Q("[data-td-coop-submit]").hidden,prev:R(Q("[data-td-coop-prev]")),submit:R(Q("[data-td-coop-submit]")),cancel:R(Q("[data-td-coop-cancel]")),iwBox:R(iw),iwPad:CS(iw,"padding"),iwBorder:CS(iw,"borderTopWidth")+" / "+CS(iw,"borderTopColor"),iwRadius:CS(iw,"borderTopLeftRadius"),prefix:R(ip),inpFs:CS(ii,"fontSize"),inpPh:ii.placeholder,rowCount:rows.length,row0:R(rows[0]),row1:R(rows[1]),rowPitch:Math.round(R(rows[1])[1]-R(rows[0])[1]),av:R(av),avRadius:CS(av,"borderTopLeftRadius"),avBg:CS(av,"backgroundColor"),nm:R(nm),nmFs:CS(nm,"fontSize"),cbR:R(cb),cbR2:R(rows[0].querySelector(".td-coop-cb")),visRows:VISROWS()};})())')"
$AB screenshot "$OUT/51-coop-step2.png" >/dev/null 2>&1

echo "--- 5g. 搜索过滤（输入「邵」→ 仅 1 行） ---"
$AB fill '[data-td-pane="2"] .giencoder-input' '邵' >/dev/null 2>&1
sleep 0.5
rec 5g "$(ev 'JSON.stringify({visRows:VISROWS(),val:Q("[data-td-pane=\"2\"] .giencoder-input").value})')"
$AB fill '[data-td-pane="2"] .giencoder-input' 'P00986' >/dev/null 2>&1
sleep 0.5
rec 5g_multi "$(ev 'JSON.stringify({visRows:VISROWS()})')"
$AB fill '[data-td-pane="2"] .giencoder-input' 'zzzz' >/dev/null 2>&1
sleep 0.5
rec 5g_none "$(ev 'JSON.stringify({visRows:VISROWS()})')"
$AB fill '[data-td-pane="2"] .giencoder-input' '' >/dev/null 2>&1
sleep 0.5
rec 5g_reset "$(ev 'JSON.stringify({visRows:VISROWS()})')"

echo "--- 5h. 选 2 位协作者 → 计数 ---"
$AB click '[data-td-midx="0"] .giencoder-checkbox-mask' >/dev/null 2>&1
sleep 0.4
$AB click '[data-td-midx="3"] .giencoder-checkbox-mask' >/dev/null 2>&1
sleep 0.5
rec 5h "$(ev 'JSON.stringify({mChecked:CKENABLED("2"),count:Q("[data-td-coop-count]").textContent})')"

echo "--- 5i. 上一步 → 回 Step1（状态保留 + 底栏按钮回切） ---"
$AB click '[data-td-coop-prev]' >/dev/null 2>&1
sleep 0.6
rec 5i "$(ev 'JSON.stringify({pane1Hidden:Q("[data-td-pane=\"1\"]").hidden,nextHidden:Q("[data-td-coop-next]").hidden,prevHidden:Q("[data-td-coop-prev]").hidden,submitHidden:Q("[data-td-coop-submit]").hidden,hint:Q("[data-td-coop-hint]").textContent,count:Q("[data-td-coop-count]").textContent,keepM:CKENABLED("2"),step0Active:QA("[data-td-step]")[0].classList.contains("is-active")})')"

echo "--- 5j. 点步骤条跳转（clickable） ---"
$AB click '[data-td-step="2"]' >/dev/null 2>&1
sleep 0.5
rec 5j "$(ev 'JSON.stringify({pane2Hidden:Q("[data-td-pane=\"2\"]").hidden,step1Active:QA("[data-td-step]")[1].classList.contains("is-active"),count:Q("[data-td-coop-count]").textContent})')"

echo "--- 5k. 提交 → 关闭 + DS Message 提示 ---"
$AB click '[data-td-coop-submit]' >/dev/null 2>&1
sleep 0.6
rec 5k "$(ev 'JSON.stringify((function(){var b=Q(".td-dp-msg"),m=b&&b.querySelector(".giencoder-message");return{open:OPEN(),rootHidden:CO().hidden,flag:FLAG(),msgHidden:b?b.hidden:null,msgText:m?m.querySelector(".giencoder-message-content").textContent:null,msgRole:m?m.getAttribute("role"):null,msgCls:m?m.className:null};})())')"
$AB screenshot "$OUT/52-coop-submit-toast.png" >/dev/null 2>&1

echo "--- 5l. 取消按钮关闭 ---"
$AB click '[data-td-coop]' >/dev/null 2>&1; sleep 0.7
rec 5l_pre "$(ev 'JSON.stringify({open:OPEN(),step1:Q("[data-td-pane=\"1\"]").hidden===false})')"
$AB click '[data-td-coop-cancel]' >/dev/null 2>&1; sleep 0.6
rec 5l "$(ev 'JSON.stringify({open:OPEN(),rootHidden:CO().hidden,flag:FLAG(),display:CS(CO(),"display")})')"

echo "--- 5m. 右上 X 关闭 ---"
$AB click '[data-td-coop]' >/dev/null 2>&1; sleep 0.7
$AB click '[data-td-coop-close]' >/dev/null 2>&1; sleep 0.6
rec 5m "$(ev 'JSON.stringify({open:OPEN(),rootHidden:CO().hidden,flag:FLAG()})')"

echo "--- 5n. 点遮罩关闭 ---"
$AB click '[data-td-coop]' >/dev/null 2>&1; sleep 0.7
MS=$($AB eval "$HELP JSON.stringify({x:60,y:60})" 2>&1 | tail -1)
read MSX MSY <<< "$(printf '%s' "$MS" | nums x y)"
$AB mouse move "$MSX" "$MSY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 0.6
rec 5n "$(ev 'JSON.stringify({open:OPEN(),rootHidden:CO().hidden,flag:FLAG()})')"

echo "--- 5o. Esc 关闭（页尾 Esc 链 → td:close-coop） ---"
$AB click '[data-td-coop]' >/dev/null 2>&1; sleep 0.7
rec 5o_pre "$(ev 'JSON.stringify({open:OPEN(),flag:FLAG()})')"
$AB press Escape >/dev/null 2>&1
sleep 0.7
rec 5o "$(ev 'JSON.stringify({open:OPEN(),rootHidden:CO().hidden,flag:FLAG()})')"

echo "--- 5p. 事件 td:close-coop 可外部派发 ---"
$AB click '[data-td-coop]' >/dev/null 2>&1; sleep 0.7
$AB eval 'document.dispatchEvent(new CustomEvent("td:close-coop"))' >/dev/null 2>&1
sleep 0.6
rec 5p "$(ev 'JSON.stringify({open:OPEN(),rootHidden:CO().hidden,flag:FLAG()})')"

echo "--- 5q. 重新打开 = 复位到 Step1（不残留上次选择） ---"
$AB click '[data-td-coop]' >/dev/null 2>&1
sleep 0.7
rec 5q "$(ev 'JSON.stringify({open:OPEN(),step1Active:QA("[data-td-step]")[0].classList.contains("is-active"),pane2Hidden:Q("[data-td-pane=\"2\"]").hidden,checked1:CKENABLED("1"),mChecked:CKENABLED("2"),count:Q("[data-td-coop-count]").textContent,hint:Q("[data-td-coop-hint]").textContent})')"

echo ""
echo "================ probe32b.jsonl ================"
wc -l "$PROBE"
ls -la "$OUT" | tail -8
