#!/usr/bin/env bash
# r97：多视口宽度下的横向边界（验证「底部对话框两端变短」是否只在宽视口出现）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PROBE='(function(){
 function r(s){var e=document.querySelector(s);if(!e)return null;var b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.width)];}
 var o={vw:window.innerWidth,
  scroll:r(".r93-scroll"), wrap:r(".r93-wrap"), bottom:r(".r93-bottom"), sb:r(".r93-sb"),
  agents:r(".r93-agents"), card:r(".r93-card"), alert:r(".r93-alert"), bub:r(".r93-bub")};
 var mt8=document.querySelector("main > div > div.flex-1.justify-center > div.mt-8");
 o.mt8=r("main > div > div.flex-1.justify-center > div.mt-8");
 o.composer=mt8&&mt8.firstElementChild?[Math.round(mt8.firstElementChild.getBoundingClientRect().left),Math.round(mt8.firstElementChild.getBoundingClientRect().width)]:null;
 o.agent0=null;var a0=document.querySelector(".r93-agent");if(a0){var b=a0.getBoundingClientRect();o.agent0=[Math.round(b.left),Math.round(b.width)];}
 var a4=document.querySelectorAll(".r93-agent");if(a4.length){var b2=a4[a4.length-1].getBoundingClientRect();o.agentLast=[Math.round(b2.left+b2.width)];}
 return JSON.stringify(o);})()'
for W in 1440 1920 2560; do
  "$NODE" "$AB" set viewport $W 900 >/dev/null
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?w=$W"
  "$NODE" "$AB" wait 1200 >/dev/null
  echo "--- $W ---"
  "$NODE" "$AB" eval "$PROBE"
done
