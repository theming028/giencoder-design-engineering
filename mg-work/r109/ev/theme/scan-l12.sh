#!/usr/bin/env bash
# r109 第十二拍 · 四条真机取证（单页 conversation）
# ★ 铁律：stdout 一律重定向（禁接管道）；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
OUT="mg-work/r109/raw/l12"
mkdir -p "$OUT" "$TMP"
TS=$(date +%s%N)

"$NODE" "$CLI" close --all >"$TMP/l12-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/l12-set.log" 2>&1
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >"$OUT/open.log" 2>&1
"$NODE" "$CLI" wait 4200 >"$TMP/l12-w.log" 2>&1

# 第一份：静态量测（浅色档）
"$NODE" "$CLI" eval "$(cat "$EV/p-l12.js")" >"$OUT/static-light.json" 2>&1
echo "done static/light"

# 暗色档静态量测
"$NODE" "$CLI" eval "(function(){document.documentElement.setAttribute('giencoder-theme','dark');return 'dark';})()" >"$TMP/l12-td.log" 2>&1
"$NODE" "$CLI" wait 1400 >"$TMP/l12-w2.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-l12.js")" >"$OUT/static-dark.json" 2>&1
echo "done static/dark"

# 回浅色，做交互取证
"$NODE" "$CLI" eval "(function(){document.documentElement.removeAttribute('giencoder-theme');return 'light';})()" >"$TMP/l12-tl.log" 2>&1
"$NODE" "$CLI" wait 1400 >"$TMP/l12-w3.log" 2>&1

# ④ 点右侧死区（逐个分区），每次重新取探针（因为 NodeList 会随 DOM 变化失效）
for i in 0 1 2 3; do
  "$NODE" "$CLI" eval "window.__l12.tapRight($i)" >"$OUT/tapRight-$i.json" 2>&1
  echo "done tapRight/$i"
done

# ④b 点标题按钮（应只 toggle 一次）
"$NODE" "$CLI" eval "window.__l12.tapTitle(0)" >"$OUT/tapTitle-0.json" 2>&1
echo "done tapTitle/0"
"$NODE" "$CLI" eval "window.__l12.tapTitle(0)" >"$OUT/tapTitle-0b.json" 2>&1
echo "done tapTitle/0b"

# ② 点附件卡 → 右栏预览
"$NODE" "$CLI" eval "$(cat "$EV/p-l12.js")" >"$TMP/l12-refresh.log" 2>&1
"$NODE" "$CLI" eval "window.__l12.tapAtt(1)" >"$OUT/tapAtt-1.log" 2>&1
"$NODE" "$CLI" wait 1200 >"$TMP/l12-w4.log" 2>&1
"$NODE" "$CLI" eval "window.__l12.prev()" >"$OUT/prev-md.json" 2>&1
echo "done tapAtt/1(md)"

"$NODE" "$CLI" eval "window.__l12.tapAtt(2)" >"$OUT/tapAtt-2.log" 2>&1
"$NODE" "$CLI" wait 1200 >"$TMP/l12-w5.log" 2>&1
"$NODE" "$CLI" eval "window.__l12.prev()" >"$OUT/prev-xlsx.json" 2>&1
echo "done tapAtt/2(xlsx)"

"$NODE" "$CLI" close --all >"$TMP/l12-close2.log" 2>&1
echo "=== done · 产物 $OUT ==="
