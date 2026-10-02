#!/usr/bin/env bash
# r109 · base 页「下拉菜单配色」横向取证：切暗色 → 枚举所有下拉触发器 → 逐个点开
#   → 读可见浮层面板的底色/描边/模糊 + 截图
# ★ 用页面自带的 window.__giTheme.set('dark')（比探针的 __setDark 更贴近真实交互）
# ★ 铁律：stdout 一律重定向；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
PG="${1:-base}"; MAX="${2:-10}"; THEME="${3:-dark}"
OUT="mg-work/r109/raw/dd9-$THEME"
mkdir -p "$OUT" "$TMP"
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
jlen () {
  "$PY" -c "
import json,sys
raw=open(sys.argv[1],encoding='utf-8').read().strip()
try: d=json.loads(raw)
except Exception: d=[]
if isinstance(d,str):
    try: d=json.loads(d)
    except Exception: d=[]
print(len(d) if isinstance(d,list) else 0)
" "$1" 2>/dev/null
}
jt () {   # 取第 i 件的 t/cls 文本
  "$PY" -c "
import json,sys
raw=open(sys.argv[1],encoding='utf-8').read().strip()
try: d=json.loads(raw)
except Exception: d=[]
if isinstance(d,str):
    try: d=json.loads(d)
    except Exception: d=[]
i=int(sys.argv[2])
if not isinstance(d,list) or not d or i>=len(d): print('?'); raise SystemExit
print('%s | %s' % (d[i].get('t',''), d[i].get('cls','')))
" "$1" "$2" 2>/dev/null
}

"$NODE" "$CLI" close --all >"$TMP/d-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/d-set.log" 2>&1
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/open.log" 2>&1
"$NODE" "$CLI" wait 4500 >"$TMP/d-wait.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-lit.js")" >"$OUT/init1.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-sel.js")" >"$OUT/init2.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-trigs.js")" >"$OUT/init3.log" 2>&1

# 暗色档（页面自带 API）
"$NODE" "$CLI" eval "window.__giTheme.set('$THEME'); 'T'" >"$TMP/d-dark.log" 2>&1
"$NODE" "$CLI" wait 1400 >"$TMP/d-w2.log" 2>&1
"$NODE" "$CLI" screenshot "$OUT/$PG-dark-closed.png" >"$TMP/d-shot0.log" 2>&1
"$NODE" "$CLI" eval "window.__vars()" >"$OUT/dark.vars" 2>&1

"$NODE" "$CLI" eval "window.__alltrig()" >"$OUT/trigs.json" 2>&1
N=$(jlen "$OUT/trigs.json")
echo "触发器总数 = $N（取前 $MAX 个）"
[ "$N" -gt "$MAX" ] && N=$MAX

i=0
while [ "$i" -lt "$N" ]; do
  read -r X Y <<<"$(jxy "$OUT/trigs.json" "$i")"
  LBL=$(jt "$OUT/trigs.json" "$i")
  echo "--- #$i  ($X,$Y)  $LBL"
  if [ "$X" != "0" ]; then
    "$NODE" "$CLI" mouse move "$X" "$Y" >"$TMP/d-m1-$i.log" 2>&1
    "$NODE" "$CLI" mouse down >"$TMP/d-m2-$i.log" 2>&1
    "$NODE" "$CLI" mouse up >"$TMP/d-m3-$i.log" 2>&1
    "$NODE" "$CLI" wait 800 >"$TMP/d-w3-$i.log" 2>&1
    "$NODE" "$CLI" eval "window.__panels()" >"$OUT/panel-$i.json" 2>&1
    "$NODE" "$CLI" screenshot "$OUT/$PG-dd-$i.png" >"$TMP/d-shot-$i.log" 2>&1
    # 关浮层：点左上角空白处
    "$NODE" "$CLI" mouse move 8 8 >"$TMP/d-m4-$i.log" 2>&1
    "$NODE" "$CLI" mouse down >"$TMP/d-m5-$i.log" 2>&1
    "$NODE" "$CLI" mouse up >"$TMP/d-m6-$i.log" 2>&1
    "$NODE" "$CLI" wait 350 >"$TMP/d-w4-$i.log" 2>&1
  fi
  i=$((i + 1))
done
"$NODE" "$CLI" close --all >"$TMP/d-close2.log" 2>&1
echo "=== done · 产物 $OUT ==="
