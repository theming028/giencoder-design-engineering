#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
P='(function(){var c=document.querySelectorAll(".r93-card");var o=[];for(var i=0;i<c.length;i++){var b=c[i].getBoundingClientRect();o.push([Math.round(b.height),c[i].scrollHeight-c[i].clientHeight]);}return JSON.stringify({u:location.href.split("/").pop().split("?")[0],cards:o});})()'
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/mg-work/r93/before/conversation-r96.html"
"$NODE" "$AB" wait 1500
echo "--- r96 baseline ---"
"$NODE" "$AB" eval "$P"
