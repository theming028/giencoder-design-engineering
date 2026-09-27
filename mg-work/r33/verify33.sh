#!/usr/bin/env bash
# 第33轮验证 v2（6 项）：
#   1) .giencoder-modal-content 白底 + 边框加深一级（border-1 #F2F2F2 → border-2 #E5E5E5）
#   2) .giencoder-steps-item 衔接处 = 向右箭头（段1 右凸尖 + 段2 左凹口）
#   3) .td-coop-dvd-tx 字号 14px = --font-size-body-3
#   4) 详情页「编辑」→ 与看板「创建任务」同一个弹窗（同 CSS/同结构 + 数据预填）
#   5) base.html main 去掉彩色弥散，只留波点
#   6) 看板「进行中」首卡虚线降两级（warning-6 → warning-4）+ 卡片 hover 标题 500
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r33/shots"
PROBE="mg-work/r33/probe33.jsonl"
mkdir -p "$OUT"
: > "$PROBE"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},C=function(e){var r=e.getBoundingClientRect();return{x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)}},CS=function(e,p){return e?getComputedStyle(e)[p]:null},RR=function(e,p){return e?getComputedStyle(e).getPropertyValue(p).trim():null},TXT=function(e){return e?e.textContent.trim():null};'

rec() {
  "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:500]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$PROBE"
}
ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }

echo "############ A. 详情页协作弹窗：内容区 / 步骤条 / 分割线（第 1~3 项） ############"
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0
$AB click '[data-td-coop]' >/dev/null 2>&1
sleep 0.8

rec A1 "$(ev 'JSON.stringify((function(){var c=Q(".td-coop .giencoder-modal-content"),r=document.documentElement;return{bg:CS(c,"backgroundColor"),bg5:RR(r,"--color-bg-5"),border:CS(c,"borderTopColor"),bw:CS(c,"borderTopWidth"),radius:CS(c,"borderTopLeftRadius"),b1:RR(r,"--color-border-1"),b2:RR(r,"--color-border-2")};})())')"

rec A2 "$(ev 'JSON.stringify((function(){var t=Q(".td-coop-dvd-tx"),r=document.documentElement;return{txt:TXT(t),fs:CS(t,"fontSize"),body3:RR(r,"--font-size-body-3"),lh:CS(t,"lineHeight")};})())')"

rec A3 "$(ev 'JSON.stringify((function(){var si=QA("[data-td-step]"),w=Q(".td-coop .giencoder-steps"),g=function(e){return{rect:R(e),clip:CS(e,"clipPath"),margin:CS(e,"margin"),z:CS(e,"zIndex"),bg:CS(e,"backgroundColor"),border:CS(e,"borderTopWidth")+" "+CS(e,"borderTopColor")}};return{wrap:R(w),n:si.length,g0:g(si[0]),g1:g(si[1]),g2:si[2]?g(si[2]):null};})())')"
$AB screenshot "$OUT/A-coop.png" >/dev/null 2>&1
$AB press Escape >/dev/null 2>&1
sleep 0.5

echo "############ B. 详情页「编辑」→ 任务编辑弹窗（第 4 项） ############"
rec B0 "$(ev 'JSON.stringify({btn:!!Q("[data-td-edit]"),modal:!!Q(".kb-crt"),bound:Q("[data-td-edit]")?Q("[data-td-edit]").getAttribute("data-td-edit-bound"):null,hidden:Q(".kb-crt")?Q(".kb-crt").hidden:null,aria:Q("[data-td-edit]")?Q("[data-td-edit]").getAttribute("aria-expanded"):null})')"

$AB click '[data-td-edit]' >/dev/null 2>&1
sleep 0.9
rec B1 "$(ev 'JSON.stringify((function(){var m=Q(".kb-crt"),d=Q(".kb-crt-dialog");return{hidden:m.hidden,open:m.classList.contains("is-open"),isEdit:m.classList.contains("is-edit"),flag:document.documentElement.hasAttribute("data-td-edit-open"),aria:Q("[data-td-edit]").getAttribute("aria-expanded"),crt:R(m),crtPos:CS(m,"position"),varW:RR(m,"--kb-crt-width"),dlg:R(d),dlgW:CS(d,"width"),rTL:CS(d,"borderTopLeftRadius"),rBR:CS(d,"borderBottomRightRadius"),bg:CS(d,"backgroundColor"),shadow:CS(d,"boxShadow").slice(0,120),host:(m.parentElement.className||"").toString().slice(0,60),title:TXT(Q(".kb-crt .giencoder-modal-title")),role:d.getAttribute("role"),ariaModal:d.getAttribute("aria-modal")};})())')"
rec B2 "$(ev 'JSON.stringify((function(){var f=Q(".kb-crt-foot"),bs=QA(".kb-crt-foot button"),keep=Q(".kb-crt-foot [data-crt-keep]");return{foot:R(f),pad:CS(f,"padding"),h:CS(f,"height"),btns:bs.map(function(b){return{tx:TXT(b),rect:R(b),disp:CS(b,"display"),cls:b.className}}),keepDisp:keep?CS(keep,"display"):null};})())')"
rec B3 "$(ev 'JSON.stringify((function(){var type=Q(".kb-crt-type"),ti=Q(".kb-crt-title .giencoder-input"),ta=Q(".kb-crt-textarea"),di=Q(".kb-crt-date-input");var rows=QA(".kb-crt-row").map(function(r){var lbl=r.querySelector(".kb-crt-lbl"),t=r.querySelector(".giencoder-select-view-text"),s=r.querySelector(".giencoder-select");return{lbl:TXT(lbl)||TXT(r.querySelector(".kb-crt-type-lbl")),val:TXT(t),hasValue:s?s.classList.contains("giencoder-select-has-value"):null}});var sel=Q(".kb-crt-type .giencoder-select-option-selected");return{type:{val:TXT(type.querySelector(".giencoder-select-view-text")),hasValue:type.classList.contains("giencoder-select-has-value"),selected:TXT(sel)},rows:rows,titleVal:ti?ti.value:null,descLen:ta?ta.value.length:0,descHead:ta?(ta.value||"").slice(0,40):null,dateVal:di?di.value:null,calSel:TXT(Q(".giencoder-calendar-cell-selected")),upCount:QA(".kb-crt-upitem").length,upNames:QA(".kb-crt-upitem").map(function(u){return TXT(u).replace(/\s+/g," ").slice(0,28)})};})())')"
rec B4 "$(ev 'JSON.stringify((function(){var d=Q(".kb-crt-dialog"),r=d.getBoundingClientRect();var rel=function(e){if(!e)return null;var b=e.getBoundingClientRect();return [Math.round(b.left-r.left),Math.round(b.top-r.top),Math.round(b.width),Math.round(b.height)]};return{head:rel(Q(".kb-crt-head")),headH:CS(Q(".kb-crt-head"),"height"),body:rel(Q(".kb-crt-body")),main:rel(Q(".kb-crt-main")),aside:rel(Q(".kb-crt-aside")),asideHead:rel(Q(".kb-crt-aside-head")),asideBody:rel(Q(".kb-crt-aside-body")),row0:rel(QA(".kb-crt-row")[0]),rows:QA(".kb-crt-row").length,lbl:rel(Q(".kb-crt-lbl")),fld:rel(Q(".kb-crt-fld")),dialogW:Math.round(r.width),dialogH:Math.round(r.height)};})())')"
$AB screenshot "$OUT/B-edit.png" >/dev/null 2>&1

echo "  -- 下拉可交互（Select 契约结构） --"
$AB click '.kb-crt-row .giencoder-select-view' >/dev/null 2>&1
sleep 0.5
rec B5 "$(ev 'JSON.stringify((function(){var p=Q(".kb-crt-row .giencoder-select-popup.giencoder-popup-open");return{open:!!p,display:p?CS(p,"display"):null,aria:Q(".kb-crt-row .giencoder-select-view").getAttribute("aria-expanded"),optCount:p?QA(".kb-crt-row .giencoder-select-option").filter(function(o){return o.closest(".giencoder-select-popup")===p}).length:null};})())')"
$AB click '.kb-crt-row .giencoder-select-popup.giencoder-popup-open .giencoder-select-option' >/dev/null 2>&1
sleep 0.5
rec B5b "$(ev 'JSON.stringify((function(){var r=Q(".kb-crt-row");return{val:TXT(r.querySelector(".giencoder-select-view-text")),popOpen:!!Q(".kb-crt-row .giencoder-select-popup.giencoder-popup-open")};})())')"

echo "  -- Esc 关闭（焦点在标题输入框里） --"
$AB click '.kb-crt-title .giencoder-input' >/dev/null 2>&1
sleep 0.3
$AB press Escape >/dev/null 2>&1
sleep 0.7
rec B6 "$(ev 'JSON.stringify({hidden:Q(".kb-crt").hidden,open:Q(".kb-crt").classList.contains("is-open"),flag:document.documentElement.hasAttribute("data-td-edit-open"),aria:Q("[data-td-edit]").getAttribute("aria-expanded")})')"

echo "  -- 保存（校验通过 → 关闭 + DS Message） --"
$AB click '[data-td-edit]' >/dev/null 2>&1
sleep 0.8
$AB click '[data-crt-submit]' >/dev/null 2>&1
sleep 0.6
rec B7 "$(ev 'JSON.stringify((function(){var m=Q(".td-dp-msg .giencoder-message")||QA(".giencoder-message").filter(function(x){return TXT(x.querySelector(".giencoder-message-content"))==="任务已保存"})[0];return{hidden:Q(".kb-crt").hidden,flag:document.documentElement.hasAttribute("data-td-edit-open"),msgText:m?TXT(m.querySelector(".giencoder-message-content")):null,msgCls:m?m.className:null,msgRole:m?m.getAttribute("role"):null};})())')"

echo "  -- 清空标题后保存 → DS Message 校验提示 --"
$AB click '[data-td-edit]' >/dev/null 2>&1
sleep 0.8
$AB fill '.kb-crt-title .giencoder-input' '' >/dev/null 2>&1
sleep 0.3
$AB click '[data-crt-submit]' >/dev/null 2>&1
sleep 0.5
rec B8 "$(ev 'JSON.stringify((function(){var msgs=Q(".kb-crt-msgs"),t=Q(".kb-crt-msgs [data-err=\u0022title\u0022]");return{msgsHidden:msgs.hidden,errTitleHidden:t?t.hidden:null,errText:t?TXT(t.querySelector(".giencoder-message-content")):null,errRole:t?t.getAttribute("role"):null,inputErr:Q(".kb-crt-title").classList.contains("giencoder-input-error"),modalHidden:Q(".kb-crt").hidden};})())')"
$AB screenshot "$OUT/B-edit-err.png" >/dev/null 2>&1
$AB fill '.kb-crt-title .giencoder-input' '端到端流程初始化：用户输入业务流并触发全链路交付' >/dev/null 2>&1
sleep 0.3
$AB press Escape >/dev/null 2>&1
sleep 0.6

echo "############ C. 看板：创建弹窗基准几何 + 虚线色 + 标题 hover（第 6 项） ############"
$AB open "$BASE/kanban.html" >/dev/null 2>&1
sleep 3.5
$AB click '.kb-create' >/dev/null 2>&1
sleep 0.9
rec C1 "$(ev 'JSON.stringify((function(){var d=Q(".kb-crt-dialog");return{exists:!!Q(".kb-crt"),open:Q(".kb-crt").classList.contains("is-open"),crt:R(Q(".kb-crt")),dlg:R(d),dlgW:CS(d,"width"),radius:CS(d,"borderTopLeftRadius")+" "+CS(d,"borderBottomRightRadius"),headH:CS(Q(".kb-crt-head"),"height"),footH:CS(Q(".kb-crt-foot"),"height"),title:TXT(Q(".kb-crt .giencoder-modal-title")),keepDisp:CS(Q(".kb-crt-foot [data-crt-keep]"),"display"),btns:QA(".kb-crt-foot button").map(function(b){return TXT(b)+":"+CS(b,"display")})};})())')"
$AB press Escape >/dev/null 2>&1
sleep 0.6

rec C2 "$(ev 'JSON.stringify((function(){var d=Q(".kb-card.is-dashed"),r=d?d.querySelector(".kb-card-dash rect"):null,l=d?d.closest(".kb-col"):null,r2=document.documentElement,el=d?d.querySelector(".kb-card-title"):null;return{found:!!d,lane:l?TXT(l.querySelector(".kb-col-name")):null,idxInLane:d?QA(".kb-col").filter(function(c){return c.contains(d)}).length:null,orderInCol:l?Array.prototype.indexOf.call(l.querySelectorAll(".kb-card"),d):null,stroke:r?CS(r,"stroke"):null,dash:r?CS(r,"strokeDasharray"):null,w4:RR(r2,"--color-warning-4"),w6:RR(r2,"--color-warning-6"),restFw:el?CS(el,"fontWeight"):null,restH:el?Math.round(el.closest(".kb-card").getBoundingClientRect().height):null};})())')"

rec C3 "$(ev 'JSON.stringify((function(){return{rest:QA(".kb-card").map(function(c){var t=c.querySelector(".kb-card-title");return{fw:CS(t,"fontWeight"),h:Math.round(c.getBoundingClientRect().height)}}),n:QA(".kb-card").length};})())')"

PT=$($AB eval "$HELP JSON.stringify(C(Q('.kb-card.is-dashed .kb-card-title')))" 2>&1 | tail -1)
"$P" -c "
import json,sys
d=json.loads(sys.argv[1]); d=json.loads(d) if isinstance(d,str) else d
open('mg-work/r33/pt.txt','w').write('%d %d'%(d['x'],d['y']))
" "$PT"
read PX PY < mg-work/r33/pt.txt
$AB mouse move "$PX" "$PY" >/dev/null 2>&1; sleep 0.6
rec C4 "$(ev 'JSON.stringify((function(){var d=Q(".kb-card.is-dashed"),t=d.querySelector(".kb-card-title");return{fw:CS(t,"fontWeight"),h:Math.round(d.getBoundingClientRect().height),stroke:CS(d.querySelector(".kb-card-dash rect"),"stroke")};})())')"
$AB screenshot "$OUT/C-kanban-hover.png" >/dev/null 2>&1

echo "  -- 逐张卡片 hover：标题字重必须都是 500，且卡高与 rest 态一致（不换行） --"
CARDS=$($AB eval "$HELP JSON.stringify(QA('.kb-card').map(function(c){return C(c.querySelector('.kb-card-title'))}))" 2>&1 | tail -1)
echo "$CARDS" > mg-work/r33/cards.json
N=$("$P" -c "
import json
d=json.load(open('mg-work/r33/cards.json'))
if isinstance(d,str): d=json.loads(d)
print(len(d))
")
echo "  卡片数 $N"
i=0
while [ "$i" -lt "$N" ]; do
  PT3=$("$P" -c "
import json,sys
d=json.load(open('mg-work/r33/cards.json'))
if isinstance(d,str): d=json.loads(d)
print(d[int(sys.argv[1])]['x'], d[int(sys.argv[1])]['y'])
" "$i")
  read HX HY <<< "$PT3"
  $AB mouse move "$HX" "$HY" >/dev/null 2>&1
  sleep 0.35
  rec "C6_$i" "$(ev 'JSON.stringify((function(){var i='"$i"',t=QA(".kb-card-title")[i],c=t.closest(".kb-card");return{i:i,fw:CS(t,"fontWeight"),cardH:Math.round(c.getBoundingClientRect().height)}})())')"
  i=$((i+1))
done
$AB mouse move 5 5 >/dev/null 2>&1

echo "############ D. base.html（第 5 项） ############"
$AB open "$BASE/base.html" >/dev/null 2>&1
sleep 4.0
rec D1 "$(ev 'JSON.stringify((function(){var m=Q("main"),bi=CS(m,"backgroundImage");var layers=(bi.match(/radial-gradient/g)||[]).length;return{bgImgLayers:layers,bgImg:bi.slice(0,240),bgRepeat:CS(m,"backgroundRepeat"),bgSize:CS(m,"backgroundSize"),hasDot:bi.indexOf("55, 112, 247")>=0,diffusion:[["magenta","232, 101, 223"],["teal","94, 223, 214"],["purple","168, 113, 227"],["blue","102, 146, 249"]].filter(function(p){return bi.indexOf(p[1])>=0}).map(function(p){return p[0]})};})())')"
rec D2 "$(ev "JSON.stringify((function(){var out=[],els=QA('main, main *');for(var i=0;i<els.length;i++){var e=els[i],bi=CS(e,'backgroundImage');if(bi&&bi!=='none'){out.push({tag:e.tagName,cls:(e.className||'').toString().slice(0,44),pos:CS(e,'position'),layers:(bi.match(/radial-gradient/g)||[]).length})}}return{n:out.length,list:out.slice(0,10)}})())")"
$AB screenshot "$OUT/D-base.png" >/dev/null 2>&1

echo ""
echo "================ probe33.jsonl ================"
wc -l "$PROBE"
