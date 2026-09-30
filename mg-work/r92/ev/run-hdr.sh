#!/bin/bash
# r92 ① 实测：顶栏 header 背景图（基础工作台 5 页应有 / 研发工作台 4 页应无）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
O=mg-work/r92/ev
PROBE='JSON.stringify((function(){var h=document.querySelector("header[class*=h-12]");if(!h)return{err:1};var c=getComputedStyle(h);var r=h.getBoundingClientRect();var nh=document.querySelectorAll("header").length;return{cls:h.className,bgi:c.backgroundImage,rep:c.backgroundRepeat,pos:c.backgroundPosition,size:c.backgroundSize,bgc:c.backgroundColor,w:+r.width.toFixed(1),h:+r.height.toFixed(1),hdrCount:nh,innerW:window.innerWidth};})())'

: > "$O/p92-hdr-out.txt"
"$NODE" "$AB" set viewport 1920 900 >/dev/null 2>&1

for pg in base settings avatar skills automation dev kanban req-kanban task-detail; do
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$(date +%s%N)" >/dev/null 2>&1
  "$NODE" "$AB" wait 1800 >/dev/null 2>&1
  echo "##### $pg" >> "$O/p92-hdr-out.txt"
  "$NODE" "$AB" eval "$PROBE" >> "$O/p92-hdr-out.txt" 2>&1
  echo >> "$O/p92-hdr-out.txt"
done

# 三张顶栏元素截图（全页宽 1920）
for pg in base settings dev; do
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$(date +%s%N)" >/dev/null 2>&1
  "$NODE" "$AB" wait 1800 >/dev/null 2>&1
  "$NODE" "$AB" screenshot "header[class*=h-12]" "$O/../raw/web-hdr-r92-$pg.png" >/dev/null 2>&1
done
echo DONE
