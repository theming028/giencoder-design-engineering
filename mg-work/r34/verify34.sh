#!/usr/bin/env bash
# 第 34 轮第 2 项实测：数字分身页右侧 AI 对话栏抽屉
#   实测项：触发器落点 / 抽屉几何与开合态 / 遮罩 / 模块三大弹层 /
#           全屏（内容 860px 居中）/ Esc 分级关闭 / 工具栏不破版
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r34/probe34.jsonl"
SHOT="mg-work/r34/shots"
: > "$OUT"
mkdir -p "$SHOT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},RR=function(e,p){return e?getComputedStyle(e).getPropertyValue(p).trim():null},TXT=function(e){return e?e.textContent.trim():null},VIS=function(e){if(!e)return false;var c=getComputedStyle(e);return !e.hidden&&c.display!=="none"&&c.visibility!=="hidden"&&+c.opacity>0.01};'

rec() { "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:400]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$OUT"; }

ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }
ck() { "$AB" click "$1" >/dev/null 2>&1; }

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5

# ---------- 1. 触发器 ----------
rec trig "$(ev 'JSON.stringify((function(){var b=Q(".av-chat-trigger");var row=Q("div.flex.items-start.justify-between");return{exists:!!b,cls:b?b.className:null,rect:R(b),txt:TXT(b),aria:[b?b.getAttribute("aria-controls"):null,b?b.getAttribute("aria-expanded"):null],toggleAttr:b?b.hasAttribute("data-av-chat-toggle"):null,htmlHasToggle:document.documentElement.hasAttribute("data-av-chat-toggle"),htmlAttrsBefore:document.documentElement.getAttributeNames(),rowJC:row?CS(row,"justifyContent"):null,rowGap:row?CS(row,"gap"):null,rowKids:row?Array.prototype.slice.call(row.children).map(function(e){return{txt:TXT(e).slice(0,14),rect:R(e)}}):null,allRows:QA("div.flex.items-start.justify-between").length};})())')"

# ---------- 2. 关闭态 ----------
rec closed "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer"),m=Q("[data-av-chat-mask]");return{rect:R(d),tf:CS(d,"transform"),opened:document.documentElement.hasAttribute("data-av-chat-open"),ariaHidden:d.getAttribute("aria-hidden"),pos:CS(d,"position"),w:CS(d,"width"),radius:CS(d,"borderRadius"),maskOp:m?CS(m,"opacity"):null,maskPE:m?CS(m,"pointerEvents"):null};})())')"

# ---------- 3. 打开 ----------
ck ".av-chat-trigger"
sleep 0.6
rec opened "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer"),m=Q("[data-av-chat-mask]");return{rect:R(d),tf:CS(d,"transform"),opened:document.documentElement.hasAttribute("data-av-chat-open"),ariaHidden:d.getAttribute("aria-hidden"),maskOp:CS(m,"opacity"),maskPE:CS(m,"pointerEvents"),z:CS(d,"zIndex"),trigExpanded:Q(".av-chat-trigger")?Q(".av-chat-trigger").getAttribute("aria-expanded"):null,bar:R(Q(".td-right-bar")),title:TXT(Q(".td-right-title")),time:TXT(Q(".td-right-time")),htmlAttrs:document.documentElement.getAttributeNames(),htmlAria:document.documentElement.getAttribute("aria-expanded"),roundBtns:QA(".td-round-btn").map(function(b){return[TXT(b)||b.getAttribute("aria-label"),R(b)]})};})())')"
$AB screenshot "$SHOT/01-drawer-open.png" >/dev/null 2>&1

# ---------- 4. 对话框本体 ----------
rec composer "$(ev 'JSON.stringify((function(){var t=Q(".td-composer textarea"),tb=Q(".td-composer .mt-auto"),card=Q(".td-composer > div");return{card:R(card),cardRadius:CS(card,"borderRadius"),cardBorder:CS(card,"borderColor"),cardShadow:CS(card,"boxShadow"),ta:{rect:R(t),minH:CS(t,"minHeight"),ph:t?t.placeholder:null},toolbar:{rect:R(tb),sw:tb?tb.scrollWidth:null,cw:tb?tb.clientWidth:null,overflow:tb?tb.scrollWidth-tb.clientWidth:null},avatar:TXT(Q(".td-composer [aria-label=\"数字分身\"]")),avatarRect:R(Q(".td-composer [aria-label=\"数字分身\"]")),models:QA(".td-composer .giencoder-select-view-text").map(TXT),sendDisabled:(function(){var s=Q(".td-composer [aria-label=\"发送\"]");return s?s.disabled:null})(),msgs:{user:TXT(Q(".td-msg-user")),aiName:TXT(Q(".td-ai-name"))}};})())')"

# ---------- 5. 添加上下文弹层 ----------
ck "[data-td-add-btn]"
sleep 0.45
rec addpop "$(ev 'JSON.stringify((function(){var p=Q("[data-td-add-pop]");return{vis:VIS(p),rect:R(p),radius:CS(p,"borderRadius"),bg:CS(p,"backgroundColor"),items:QA("[data-td-add-pop] [role=menuitem]").map(TXT).slice(0,4)};})())')"
$AB screenshot "$SHOT/02-add-pop.png" >/dev/null 2>&1
ck "[data-td-add-btn]"
sleep 0.35
rec addpopClosed "$(ev 'JSON.stringify((function(){var p=Q("[data-td-add-pop]");return{vis:VIS(p),hidden:p?p.hidden:null,htmlAttr:document.documentElement.hasAttribute("data-td-pop-open")};})())')"

# ---------- 6. 技能面板 ----------
ck "[data-td-skill-btn]"
sleep 0.45
rec skillpop "$(ev 'JSON.stringify((function(){var p=Q("[data-td-skill-pop]");return{vis:VIS(p),rect:R(p),radius:CS(p,"borderRadius"),rows:QA(".td-skill-row").length,groups:QA(".td-skill-group").map(TXT),foot:QA(".td-skill-foot .giencoder-btn").map(TXT)};})())')"
$AB screenshot "$SHOT/03-skill-pop.png" >/dev/null 2>&1
ck "[data-td-skill-close]"
sleep 0.35
rec skillpopClosed "$(ev 'JSON.stringify((function(){var p=Q("[data-td-skill-pop]");return{vis:VIS(p),hidden:p?p.hidden:null};})())')"

# ---------- 7. DS Select 弹层 ----------
# ⚠️ 「标准模式」选择器在 480 宽下按详情页同一约定被 display:none 收起，
#    故这里点的是大模型选择器（:not([style*="96px"]) 那个）。
SEL=".td-composer .giencoder-select:not([style*=\"96px\"])"
ck "${SEL} .giencoder-select-view"
sleep 0.45
rec selpop "$(ev 'JSON.stringify((function(){var p=Q(".td-composer .giencoder-select:not([style*=\"96px\"]) .giencoder-select-popup");return{open:p?p.classList.contains("giencoder-popup-open"):null,vis:VIS(p),rect:R(p),opts:QA(".td-composer .giencoder-select-option").map(TXT).slice(0,6)};})())')"
$AB screenshot "$SHOT/04-select-pop.png" >/dev/null 2>&1
# 选第二项 → 回写文案
ck "${SEL} .giencoder-select-option:nth-child(2)"
sleep 0.4
rec selpick "$(ev 'JSON.stringify((function(){var m=Q(".td-composer .giencoder-select:not([style*=\"96px\"]) .giencoder-select-view-text");var s=Q(".td-composer .giencoder-select[style*=\"96px\"] .giencoder-select-view-text");return{model:TXT(m),stdMode:TXT(s),stdModeDisplay:CS(Q(".td-composer .giencoder-select[style*=\"96px\"]"),"display"),openCount:QA(".giencoder-popup-open").length};})())')"

# ---------- 8. 全屏 ----------
ck "[data-td-fullscreen]"
sleep 0.6
rec fullscreen "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer"),ci=Q(".td-chat-inner"),co=Q(".td-composer"),m=Q("[data-av-chat-mask]");return{cls:d.className.indexOf("is-fullscreen")>=0,drawer:R(d),drawerW:CS(d,"width"),chatAlign:CS(Q(".td-chat"),"alignItems"),chatInner:{rect:R(ci),maxW:CS(ci,"maxWidth"),w:CS(ci,"width")},composer:{rect:R(co),maxW:CS(co,"maxWidth"),ml:CS(co,"marginLeft")},maskOp:CS(m,"opacity"),fsLabel:Q("[data-td-fullscreen]")?Q("[data-td-fullscreen]").getAttribute("title"):null,icoMax:CS(Q(".td-ico-max"),"display"),icoMin:CS(Q(".td-ico-min"),"display")};})())')"
$AB screenshot "$SHOT/05-fullscreen.png" >/dev/null 2>&1

# ---------- 9. Esc 分级：① 全屏 → ② 抽屉 ----------
$AB press Escape >/dev/null 2>&1
sleep 0.6
rec esc1 "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer");return{fullscreen:d.className.indexOf("is-fullscreen")>=0,open:document.documentElement.hasAttribute("data-av-chat-open"),ariaHidden:d.getAttribute("aria-hidden"),rect:R(d)};})())')"
$AB press Escape >/dev/null 2>&1
sleep 0.7
rec esc2 "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer");return{open:document.documentElement.hasAttribute("data-av-chat-open"),ariaHidden:d.getAttribute("aria-hidden"),tf:CS(d,"transform"),maskOp:CS(Q("[data-av-chat-mask]"),"opacity")};})())')"

# ---------- 10. 遮罩点击关闭 ----------
ck ".av-chat-trigger"
sleep 0.6
rec reopen "$(ev 'JSON.stringify({open:document.documentElement.hasAttribute("data-av-chat-open"),rect:R(Q("#av-chat-drawer"))})')"
ck "[data-av-chat-mask]"
sleep 0.7
rec maskClose "$(ev 'JSON.stringify({open:document.documentElement.hasAttribute("data-av-chat-open"),tf:CS(Q("#av-chat-drawer"),"transform")})')"

# ---------- 11. 页面本体未被破坏 ----------
rec pageIntact "$(ev 'JSON.stringify((function(){var c=Q(".mx-auto.flex.w-full.max-w-3xl.flex-col.gap-5");var row=Q("div.flex.items-start.justify-between");return{content:{rect:R(c),maxW:CS(c,"maxWidth"),kids:c?c.children.length:null},cards:c?QA(".mx-auto.flex.w-full.max-w-3xl.flex-col.gap-5 .grid > *").length:null,rowKids:row?row.children.length:null,main:R(Q("main")),asides:QA("aside").map(function(a){return[(a.id||""),R(a)]}),scripts:QA("script").length,styleBlocks:QA("style").length};})())')"

echo OK
cat "$OUT"
