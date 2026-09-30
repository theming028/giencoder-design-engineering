#!/usr/bin/env bash
set -e
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
for VW in 1440 1920; do
  echo "########## viewport ${VW} ##########"
  "$NODE" "$AB" set viewport $VW 900
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$(date +%s)"
  "$NODE" "$AB" wait 1500
  "$NODE" "$AB" eval "$(cat mg-work/r93/ev/p95b.js)"
done
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$(date +%s)"
"$NODE" "$AB" wait 1500
"$NODE" "$AB" screenshot "" mg-work/r93/raw/r95-full.png
"$NODE" "$AB" screenshot "main > div > div.flex-1.justify-center" mg-work/r93/raw/r95-hero.png
