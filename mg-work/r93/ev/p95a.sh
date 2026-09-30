#!/usr/bin/env bash
set -e
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
for VW in 1440 1920; do
  echo "########## viewport ${VW} ##########"
  "$NODE" "$AB" set viewport $VW 900
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$(date +%s)"
  "$NODE" "$AB" wait 1400
  "$NODE" "$AB" eval "$(cat mg-work/r93/ev/p95a.js)"
done
