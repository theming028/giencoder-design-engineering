#!/usr/bin/env bash
# r109 第七拍 · 下拉菜单「暗色统一」实测（真鼠标）
#  ① 变量翻转（暗色档下 DS 阶梯与语义 token 的计算值）
#  ② 打开一个下拉 ⇒ 真鼠标 hover 到菜单项 ⇒ 读实际底色
#  ★ 铁律：agent-browser stdout 一律重定向；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/drop4"
mkdir -p "$OUT" "$EV/tmp"

PG="${1:-base}"
TS=$(date +%s%N)

"$NODE" "$CLI" close --all >"$EV/tmp/d-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/tmp/d-set.log" 2>&1
echo "===== $PG ====="
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/$PG.open" 2>&1
"$NODE" "$CLI" wait 4200 >"$OUT/$PG.wait" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-drop.js")" >"$OUT/$PG.init" 2>&1

# ① 切暗色 ⇒ 读变量表
"$NODE" "$CLI" eval "window.__setDark()" >"$OUT/$PG.setdark" 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" eval "window.__vars()" >"$OUT/$PG.vars.raw" 2>&1

# ② 找触发器：优先 r81-ws-trigger，其次 aria-haspopup
"$NODE" "$CLI" eval "window.__find('r81-ws-trigger', 420, 60)" >"$OUT/$PG.trig.raw" 2>&1

# 解出第一个触发点坐标
read -r TX TY <<<"$("$PY" - "$OUT/$PG.trig.raw" <<'PYEOF'
import io, json, sys
raw = io.open(sys.argv[1], encoding='utf-8').read().strip()
s = json.loads(raw) if raw.startswith('"') else raw
d = json.loads(s)
if d:
    print(d[0]['x'], d[0]['y'])
else:
    print('0 0')
PYEOF
)"
echo "  触发器坐标 = $TX $TY"

if [ "$TX" != "0" ]; then
  "$NODE" "$CLI" mouse move "$TX" "$TY" >/dev/null 2>&1
  "$NODE" "$CLI" mouse down >/dev/null 2>&1
  "$NODE" "$CLI" mouse up >/dev/null 2>&1
  "$NODE" "$CLI" wait 700 >/dev/null 2>&1
fi

# ③ 列出浮层里的候选菜单项
"$NODE" "$CLI" eval "window.__find('hover:bg-[var(--color-fill-2)]', 460, 60)" >"$OUT/$PG.items.raw" 2>&1

# ④ 取第一个候选 ⇒ 真鼠标 hover ⇒ peek
read -r HX HY <<<"$("$PY" - "$OUT/$PG.items.raw" <<'PYEOF'
import io, json, sys
raw = io.open(sys.argv[1], encoding='utf-8').read().strip()
s = json.loads(raw) if raw.startswith('"') else raw
d = json.loads(s)
if d:
    print(d[0]['x'], d[0]['y'])
else:
    print('0 0')
PYEOF
)"
echo "  菜单项坐标 = $HX $HY"

if [ "$HX" != "0" ]; then
  "$NODE" "$CLI" mouse move "$HX" "$HY" >/dev/null 2>&1
  "$NODE" "$CLI" wait 260 >/dev/null 2>&1
  "$NODE" "$CLI" eval "window.__peek($HX, $HY)" >"$OUT/$PG.hover.raw" 2>&1
fi

"$NODE" "$CLI" close --all >"$EV/tmp/d-close2.log" 2>&1
echo "=== 产物 ==="
for f in "$OUT/$PG.vars.raw" "$OUT/$PG.trig.raw" "$OUT/$PG.items.raw" "$OUT/$PG.hover.raw"; do
  echo "--- $f ---"
  cat "$f" 2>/dev/null
  echo
done
