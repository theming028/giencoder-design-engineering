#!/bin/bash
# 第 68 轮运行时验收：数字分身右栏 vs 任务详情页右栏 逐项对照
cd "$(dirname "$0")/../.."
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$PWD/mg-work/r68/ev

PROBE='(function(){
  var q=function(s){return document.querySelector(s);};
  var cs=function(el){return el?getComputedStyle(el):null;};
  function box(el){if(!el)return null;var r=el.getBoundingClientRect();return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];}
  var acts=Array.prototype.slice.call(document.querySelectorAll(".td-right-acts .td-round-btn"));
  var meta=q(".td-ai-meta"), metaA=meta?meta.querySelector("a"):null;
  var rule=q(".td-ai-rule"), ctx=q(".td-ai-ctx");
  var foot=q(".td-ai-foot"), fico=q(".td-file-ico");
  var fsvg=fico?fico.querySelector("svg"):null;
  var panel=q(".td-right")||q(".av-chat-drawer");
  var bar=q(".td-right-bar");
  var actsBox=[]; acts.forEach(function(b){actsBox.push(box(b));});
  return JSON.stringify({
    panelBorder: cs(panel).border,
    panelShadow: cs(panel).boxShadow.slice(0,58),
    barGap: cs(bar).columnGap,
    actsCount: acts.length,
    actSize: acts[0]?[cs(acts[0]).width, cs(acts[0]).height]:null,
    actSvg: (acts[0]&&acts[0].querySelector("svg"))?[cs(acts[0].querySelector("svg")).width, cs(acts[0].querySelector("svg")).height]:null,
    actBox: actsBox,
    metaMarginTop: meta?cs(meta).marginTop:null,
    metaText: meta?meta.textContent.trim():null,
    metaAGap: metaA?cs(metaA).columnGap:null,
    metaALine: metaA?cs(metaA).lineHeight:null,
    metaBox: box(meta),
    ruleH: rule?cs(rule).height:null,
    ruleBox: box(rule),
    ruleBg: rule?cs(rule).backgroundColor:null,
    ctxText: ctx?ctx.textContent.trim():null,
    ctxColor: ctx?cs(ctx).color:null,
    ctxGap: ctx?cs(ctx).columnGap:null,
    ctxH: ctx?cs(ctx).height:null,
    ctxBox: box(ctx),
    footFont: foot?cs(foot).fontSize:null,
    footText: foot?foot.textContent.replace(/\s+/g," ").trim().slice(0,40):null,
    ico: fico?[cs(fico).width, cs(fico).height]:null,
    icoSvg: fsvg?[cs(fsvg).width, cs(fsvg).height, cs(fsvg).fill]:null,
    icoBox: box(fico)
  });
})()'

echo "======================= 任务详情页（目标） ======================="
$AB open "file://$PWD/pages/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.4
$AB eval "$PROBE"
$AB screenshot "$EV/10-td-target.png" >/dev/null

echo
echo "======================= 数字分身（改后） ======================="
$AB open "file://$PWD/pages/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.4
$AB eval '(function(){var b=document.querySelector("[data-av-chat-toggle]"); if(b) b.click(); return 1;})()' >/dev/null
sleep 0.9
$AB eval "$PROBE"
$AB screenshot "$EV/11-av-after.png" >/dev/null
echo "（截图已落 mg-work/r68/ev/）"
