set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

# 审查页：④⑤ 一处见证（展开=500 / 折叠=400，同屏对比）+ ⑤ 13px
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-open-mod='review']" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".td-browse" "$RAW/i3-review-panel.png" >/dev/null 2>&1
# 摘要页：③ 15px 区块标题 + ⑥ 统计行
"$NODE" "$CLI" click "[data-td-open-mod='summary']" >/dev/null 2>&1
"$NODE" "$CLI" wait 800 >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".td-browse" "$RAW/i3-summary-panel.png" >/dev/null 2>&1
# ① 窄栏（230px）在同一页
"$NODE" "$CLI" eval "(function(){document.getElementById('av-browse-slot').style.setProperty('--av-browse-w','230px');return 'ok';})()" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".td-browse" "$RAW/i3-panel230-summary.png" >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-open-mod='review']" >/dev/null 2>&1
"$NODE" "$CLI" wait 800 >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".td-browse" "$RAW/i3-panel230-review.png" >/dev/null 2>&1
echo done
