#!/usr/bin/env bash
# r109 第八拍补测 · 通用 hover 取证：真鼠标 hover 任意选择器 → 浅/暗两档读「谁在 :hover」
# 用法：bash hover-read.sh <页> <目标选择器> <标签> [触发器选择器] [触发器索引] [目标索引]
#   例：bash hover-read.sh base '.ws-item-hover' ws-item
#       bash hover-read.sh base '.perm-menu-item' perm '.perm-trigger' 0 1
# ★ 读数走 __hovered（:hover 命中判定），不用面积法 —— 避免浮层重叠时读成下层元素。
# ★ 铁律：agent-browser stdout 一律重定向；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
EV="mg-work/r109/ev/theme"; OUT="mg-work/r109/raw/lit8"; TMP="$EV/tmp"
mkdir -p "$OUT" "$TMP"

PG="$1"; SEL="$2"; TAG="$3"; TRIG="${4:-}"; TIDX="${5:-0}"; IDX="${6:-0}"
TS=$(date +%s%N)

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
if not isinstance(d,list) or not d: print('0 0'); raise SystemExit
i=min(int(sys.argv[2]),len(d)-1)
print('%d %d' % (d[i]['x'],d[i]['y']))
" "$1" "$2" 2>/dev/null
}

hr () {  # $1 = 选择器（作为 eval 内 JS 单引号串）
  "$NODE" "$CLI" eval "window.__hovered('$1')" 2>/dev/null
}

"$NODE" "$CLI" close --all >"$TMP/h-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/h-set.log" 2>&1
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/$TAG.open" 2>&1
"$NODE" "$CLI" wait 4500 >"$TMP/h-wait.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-lit.js")" >"$OUT/$TAG.init" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-sel.js")" >"$OUT/$TAG.init2" 2>&1

"$NODE" "$CLI" eval "window.__setLight()" >"$TMP/h-l.log" 2>&1
"$NODE" "$CLI" wait 500 >"$TMP/h-w2.log" 2>&1
"$NODE" "$CLI" eval "window.__vars()" >"$OUT/$TAG.light.vars" 2>&1

# 需要时先点开触发器（目标在浮层里）
if [ -n "$TRIG" ]; then
  "$NODE" "$CLI" eval "window.__center('$TRIG', $TIDX)" >"$OUT/$TAG.trig" 2>&1
  read -r TX TY <<<"$(jxy "$OUT/$TAG.trig" 0)"
  echo "触发器 $TRIG#$TIDX = $TX,$TY"
  if [ "$TX" != "0" ]; then
    "$NODE" "$CLI" mouse move "$TX" "$TY" >"$TMP/h-m1.log" 2>&1
    "$NODE" "$CLI" mouse down >"$TMP/h-m2.log" 2>&1
    "$NODE" "$CLI" mouse up >"$TMP/h-m3.log" 2>&1
    "$NODE" "$CLI" wait 700 >"$TMP/h-w3.log" 2>&1
  fi
fi

"$NODE" "$CLI" eval "window.__center('$SEL', $IDX)" >"$OUT/$TAG.cent" 2>&1
read -r X Y <<<"$(jxy "$OUT/$TAG.cent" 0)"
echo "目标 $SEL#$IDX = $X,$Y"
if [ "$X" != "0" ]; then
  "$NODE" "$CLI" mouse move "$X" "$Y" >"$TMP/h-m4.log" 2>&1
  "$NODE" "$CLI" wait 420 >"$TMP/h-w4.log" 2>&1
  hr "$SEL" >"$OUT/$TAG.light.bg"
fi

"$NODE" "$CLI" eval "window.__setDark()" >"$TMP/h-d.log" 2>&1
"$NODE" "$CLI" wait 800 >"$TMP/h-w5.log" 2>&1
"$NODE" "$CLI" eval "window.__vars()" >"$OUT/$TAG.dark.vars" 2>&1
if [ "$X" != "0" ]; then
  "$NODE" "$CLI" mouse move 5 5 >"$TMP/h-m5.log" 2>&1
  "$NODE" "$CLI" wait 180 >"$TMP/h-w6.log" 2>&1
  "$NODE" "$CLI" mouse move "$X" "$Y" >"$TMP/h-m7.log" 2>&1
  "$NODE" "$CLI" wait 420 >"$TMP/h-w7.log" 2>&1
  hr "$SEL" >"$OUT/$TAG.dark.bg"
fi
"$NODE" "$CLI" close --all >"$TMP/h-close2.log" 2>&1
echo "=== done $TAG ==="
