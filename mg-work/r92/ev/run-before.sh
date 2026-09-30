#!/bin/bash
# r92 改前基线实测（用 mg-work/r92/before/*.html，文件名与原页同名以免壳层路由落回 base）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
O=mg-work/r92/ev

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1

"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/mg-work/r92/before/settings.html?v=$(date +%s%N)" >/dev/null 2>&1
"$NODE" "$AB" wait 1800 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat $O/p92-nav.js)" > "$O/p92-before-settings.txt" 2>&1
"$NODE" "$AB" screenshot "aside" "$O/../raw/web-aside-r91sat.png" >/dev/null 2>&1

"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/mg-work/r92/before/base.html?v=$(date +%s%N)" >/dev/null 2>&1
"$NODE" "$AB" wait 1800 >/dev/null 2>&1
"$NODE" "$AB" eval 'JSON.stringify((function(){var h=document.querySelector("header[class*=h-12]");var c=getComputedStyle(h);return{bgi:c.backgroundImage,rep:c.backgroundRepeat,pos:c.backgroundPosition};})())' > "$O/p92-before-base-hdr.txt" 2>&1
echo DONE
