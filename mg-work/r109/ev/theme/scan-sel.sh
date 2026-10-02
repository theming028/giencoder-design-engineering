#!/usr/bin/env bash
# r109 第八拍补测 · 「.giencoder-select」家族下拉：点开 → hover 选项 → 浅/暗两档读数
# 用法：bash scan-sel.sh [页名] [select 索引] [标签]
#   settings#1 = Workspace Write ≡ 基准「默认权限」（权限语义最接近）
# ★ 铁律：agent-browser stdout 一律重定向；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
EV="mg-work/r109/ev/theme"; OUT="mg-work/r109/raw/lit8"; TMP="$EV/tmp"
mkdir -p "$OUT" "$TMP"

PG="${1:-settings}"; IDX="${2:-1}"; TAG="${3:-sel-$PG-$IDX}"
TS=$(date +%s%N)

# 从「JSON 套 JSON」产物里取第 i 件的 x/y（越界取末件）
jxy () {
  "$PY" -c "
import json,sys
raw=open(sys.argv[1],encoding='utf-8').read().strip()
d=[]
try: d=json.loads(raw)
except Exception: d=[]
if isinstance(d,str):
    try: d=json.loads(d)
    except Exception: d=[]
if not isinstance(d,list): d=[]
i=int(sys.argv[2])
if not d: print('0 0')
else:
    i=min(i,len(d)-1)
    print('%d %d' % (d[i]['x'], d[i]['y']))
" "$1" "$2" 2>/dev/null
}

"$NODE" "$CLI" close --all >"$TMP/q-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/q-set.log" 2>&1
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/$TAG.open" 2>&1
"$NODE" "$CLI" wait 4500 >"$TMP/q-wait.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-lit.js")" >"$OUT/$TAG.init" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-sel.js")" >"$OUT/$TAG.init2" 2>&1

# ---------- ① 浅色档 ----------
"$NODE" "$CLI" eval "window.__setLight()" >"$TMP/q-l.log" 2>&1
"$NODE" "$CLI" wait 500 >"$TMP/q-w2.log" 2>&1
"$NODE" "$CLI" eval "window.__vars()" >"$OUT/$TAG.light.vars" 2>&1

"$NODE" "$CLI" eval "window.__selview($IDX)" >"$OUT/$TAG.trig" 2>&1
read -r TX TY <<<"$(jxy "$OUT/$TAG.trig" 0)"
echo "触发器 $PG#$IDX = $TX,$TY"

"$NODE" "$CLI" mouse move "$TX" "$TY" >"$TMP/q-m1.log" 2>&1
"$NODE" "$CLI" mouse down >"$TMP/q-m2.log" 2>&1
"$NODE" "$CLI" mouse up >"$TMP/q-m3.log" 2>&1
"$NODE" "$CLI" wait 700 >"$TMP/q-w3.log" 2>&1
"$NODE" "$CLI" eval "window.__selprobe()" >"$OUT/$TAG.probe_light" 2>&1

"$NODE" "$CLI" eval "window.__selopts()" >"$OUT/$TAG.opts_light" 2>&1
read -r OX OY <<<"$(jxy "$OUT/$TAG.opts_light" 1)"
echo "浅色选项点 = $OX,$OY"
if [ "$OX" != "0" ]; then
  "$NODE" "$CLI" mouse move "$OX" "$OY" >"$TMP/q-m4.log" 2>&1
  "$NODE" "$CLI" wait 400 >"$TMP/q-w4.log" 2>&1
  "$NODE" "$CLI" eval "window.__hovered('.giencoder-select-option')" >"$OUT/$TAG.light.bg" 2>&1
  # 面板底：浮层在触发器下方（top = 触发器底 + 4px）⇒ 从中心下移约 26px 落在面板内
  "$NODE" "$CLI" eval "window.__bgAt($TX, $((TY + 26)), 'giencoder-select-popup')" >"$OUT/$TAG.light.panel" 2>&1
fi

# ---------- ② 暗色档（浮层保持打开）----------
"$NODE" "$CLI" eval "window.__setDark()" >"$TMP/q-d.log" 2>&1
"$NODE" "$CLI" wait 800 >"$TMP/q-w5.log" 2>&1
"$NODE" "$CLI" eval "window.__vars()" >"$OUT/$TAG.dark.vars" 2>&1
"$NODE" "$CLI" eval "window.__selprobe()" >"$OUT/$TAG.probe_dark" 2>&1
"$NODE" "$CLI" eval "window.__selopts()" >"$OUT/$TAG.opts_dark" 2>&1
read -r DX DY <<<"$(jxy "$OUT/$TAG.opts_dark" 1)"
echo "暗色选项点 = $DX,$DY"
if [ "$DX" != "0" ]; then
  "$NODE" "$CLI" mouse move 5 5 >"$TMP/q-m5.log" 2>&1
  "$NODE" "$CLI" wait 180 >"$TMP/q-w6.log" 2>&1
  "$NODE" "$CLI" mouse move "$DX" "$DY" >"$TMP/q-m6.log" 2>&1
  "$NODE" "$CLI" wait 400 >"$TMP/q-w7.log" 2>&1
  "$NODE" "$CLI" eval "window.__hovered('.giencoder-select-option')" >"$OUT/$TAG.dark.bg" 2>&1
  "$NODE" "$CLI" eval "window.__bgAt($TX, $((TY + 26)), 'giencoder-select-popup')" >"$OUT/$TAG.dark.panel" 2>&1
fi
"$NODE" "$CLI" close --all >"$TMP/q-close2.log" 2>&1
echo "=== done $TAG ==="
