#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PROBE='(function(){function r(s){var e=document.querySelector(s);if(!e)return null;var b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.width)];}
var o={vw:window.innerWidth,scroll:[document.querySelector(".r93-scroll").clientWidth],wrap:r(".r93-wrap"),bottom:r(".r93-bottom"),sb:r(".r93-sb"),agents:r(".r93-agents")};
var m=document.querySelector("main > div > div.flex-1.justify-center > div.mt-8");
o.mt8=r("main > div > div.flex-1.justify-center > div.mt-8");
o.composer=m&&m.firstElementChild?[Math.round(m.firstElementChild.getBoundingClientRect().left),Math.round(m.firstElementChild.getBoundingClientRect().width)]:null;
o.cards=Array.prototype.map.call(document.querySelectorAll(".r93-card"),function(e){var b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.width)];}).slice(0,3);
var ag=document.querySelectorAll(".r93-agent");o.agentSpan=ag.length?[Math.round(ag[0].getBoundingClientRect().left),Math.round(ag[ag.length-1].getBoundingClientRect().right)]:null;
return JSON.stringify(o);})()'
W="$1"
"$NODE" "$AB" set viewport $W 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?w=$W"
"$NODE" "$AB" wait 1200
echo "=== $W ==="
"$NODE" "$AB" eval "$PROBE"
