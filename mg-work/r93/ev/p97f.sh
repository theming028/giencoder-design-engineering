#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
P='(function(){function m(){var c=document.querySelectorAll(".r93-card");var o=[];for(var i=0;i<c.length;i++){o.push([Math.round(c[i].getBoundingClientRect().height),c[i].scrollHeight-c[i].clientHeight]);}return o;}
var a=m();
var s=document.createElement("style");s.textContent=".r93-card.r93-card *{font-size:var(--font-size-body-1)}";document.head.appendChild(s);
var b=m();s.remove();
return JSON.stringify({r97:a,r96font:b});})()'
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?ff=1"
"$NODE" "$AB" wait 1500
"$NODE" "$AB" eval "$P"
