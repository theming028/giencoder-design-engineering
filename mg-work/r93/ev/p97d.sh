#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"
TS=$(date +%s)
"$NODE" "$AB" set viewport "$W" 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 1500
echo "=== viewport $W ==="
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p97d.js)"
if [ "$W" = "1440" ]; then "$NODE" "$AB" screenshot "" mg-work/r93/raw/r97-after-full.png; fi
