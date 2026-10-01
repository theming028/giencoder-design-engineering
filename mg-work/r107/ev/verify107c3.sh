#!/usr/bin/env bash
# r107 第三拍 · 补测 J：「折叠 N 行未改动」—— 上一轮点在**被隐藏**的统一视图折叠条上（当时是并排态）⇒ 补测
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"

AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2800 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1

echo "############ J 折叠 N 行未改动（统一视图） ############"
echo "--- J0 前置：视图=统一，可见折叠条数"
AB eval "JSON.stringify({split:document.querySelector('.td-rv-body').classList.contains('is-split'),visibleMore:[].filter.call(document.querySelectorAll('[data-td-more]'),function(b){return b.offsetParent!==null;}).length})" 2>&1
echo "--- J1 点第 1 个折叠条 → 文案翻 + 放出 4 行"
AB click ".td-diff-rows:not(.td-diff-split) [data-td-more]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({rowsShown:document.querySelectorAll('[data-td-more-row]:not([hidden])').length,label:document.querySelector('.td-diff-rows:not(.td-diff-split) [data-td-more]').textContent})" 2>&1
AB screenshot "$OUT/y12-more-expanded.png" >/dev/null 2>&1
echo "--- J2 再点 → 收起"
AB click ".td-diff-rows:not(.td-diff-split) [data-td-more]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({rowsShown:document.querySelectorAll('[data-td-more-row]:not([hidden])').length,label:document.querySelector('.td-diff-rows:not(.td-diff-split) [data-td-more]').textContent})" 2>&1
echo "--- J3 切并排后，并排里那枚同样可点（两个 more 互不干扰）"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB click '[data-td-rv-view="split"]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB click ".td-diff-split [data-td-more]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({rowsShown:document.querySelectorAll('[data-td-more-row]:not([hidden])').length,label:document.querySelector('.td-diff-split [data-td-more]').textContent})" 2>&1
AB screenshot "$OUT/y13-more-split.png" >/dev/null 2>&1

echo
echo "############ L 暗色档：摘要模块 ############"
AB eval "document.documentElement.setAttribute('giencoder-theme','dark');'ok'" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="summary"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
AB eval "JSON.stringify({body:getComputedStyle(document.querySelector('.td-sum-body')).color,srcBg:getComputedStyle(document.querySelector('.td-sum-src')).backgroundColor,artIco:getComputedStyle(document.querySelector('.td-sum-arti')).backgroundColor,planDone:getComputedStyle(document.querySelector('.td-sum-plan li.is-done'),'::before').backgroundColor})" 2>&1
AB screenshot "$OUT/y14-summary-dark.png" >/dev/null 2>&1

echo "############ done ############"
