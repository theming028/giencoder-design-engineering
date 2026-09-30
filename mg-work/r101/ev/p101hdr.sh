#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/avatar.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1200 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var h=document.querySelector('header[class*=\"h-12\"]');var cs=getComputedStyle(h);var b=h.getBoundingClientRect();return JSON.stringify({page:'avatar.html',size:cs.backgroundSize,pos:cs.backgroundPosition,box:[Math.round(b.width),Math.round(b.height)]});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-hdr-avatar.png" >/dev/null 2>&1
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1200 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var h=document.querySelector('header[class*=\"h-12\"]');var cs=getComputedStyle(h);return JSON.stringify({page:'conversation.html',size:cs.backgroundSize,pos:cs.backgroundPosition});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-hdr-conv.png" >/dev/null 2>&1
