#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
AB() { "$NODE" "$CLI" "$@"; }
CTX() { AB eval "(function(){var el=document.querySelector('$1');if(!el)return 'miss';el.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:$2,clientY:$3}));return 'ok';})()" >/dev/null 2>&1; }
SHUT() { AB eval "document.dispatchEvent(new MouseEvent('click',{bubbles:true}))" >/dev/null 2>&1; AB wait 250 >/dev/null 2>&1; }

AB open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1

# ① 摘要「来源」条目右键（3 项）
CTX ".td-browse .td-sum-src" 980 320
AB wait 420 >/dev/null 2>&1
AB screenshot "$OUT/d5-ctx-src.png" >/dev/null 2>&1
SHUT

# ② 审查模块 → 文件头右键（7 项）
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 320 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
CTX ".td-browse .td-diff-h" 980 300
AB wait 420 >/dev/null 2>&1
AB screenshot "$OUT/d6-ctx-file.png" >/dev/null 2>&1
SHUT

# ③ 浏览器模块 → 页面元素右键（6 项）
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 320 >/dev/null 2>&1
AB click '[data-td-open-mod="browser"]' >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
CTX ".td-browse [data-td-el]" 980 360
AB wait 420 >/dev/null 2>&1
AB screenshot "$OUT/d7-ctx-el.png" >/dev/null 2>&1
SHUT

echo "shots-e done"
