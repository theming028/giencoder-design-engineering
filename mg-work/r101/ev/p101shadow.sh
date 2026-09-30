#!/usr/bin/env bash
# ⑩ 状态条投影：同一浏览器会话里内联试 4 档（含当前档），各拍一张，再逐行比对设计稿剖面。
# 设计稿剖面（下方 rel+0..+9 平均灰度）：244 245 246 248 249 251 252 253 254 255（背景 255）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 2200
"$NODE" "$AB" scrollintoview "[data-r101-sb]" >/dev/null 2>&1
"$NODE" "$AB" wait 500

setbox () {
  "$NODE" "$AB" eval "(function(){var s=document.querySelector('.r93-sb');s.style.boxShadow=arguments[0];return s.style.boxShadow;})('$1')" >/dev/null 2>&1
  "$NODE" "$AB" wait 250
  "$NODE" "$AB" screenshot "" "mg-work/r101/raw/sh-$2.png" >/dev/null 2>&1
  echo "  拍完 [$2] $1"
}

setbox "0 2px 6px rgba(0,0,0,0.06)"  a6x06
setbox "0 2px 9px rgba(0,0,0,0.07)"  b9x07
setbox "0 2px 10px rgba(0,0,0,0.07)" c10x07
setbox "0 2px 12px rgba(0,0,0,0.08)" d12x08
echo "=== done ==="
