#!/usr/bin/env bash
# r109 第四拍（裁决③ 补漏）· **悬停态**亮面审计（10 页）
#
# 为什么单开一趟：点击态扫描（`scan-state.sh`）扫不到 **悬停才挂载的浮层**——
#   DS Tooltip 是 `createPortal` 到 `body` 的 portal，**只在该触发件 hover 时才进 DOM**；
#   默认态、点击展开态里它都不存在 ⇒ 前三轮一条都没扫到（`p-state.js` 的判据本身没问题，
#   是「取样时它不在）」。这一趟专治这一类：**只 hover、不点击**。
#
# ★★ 铁律：agent-browser 的 stdout 绝不能接管道（守护进程持有写端 ⇒ 管道永不 EOF）。一律重定向。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/hover4"
mkdir -p "$OUT" "$EV/tmp"

PAGES="${*:-base avatar automation skills settings conversation dev kanban req-kanban task-detail}"

"$NODE" "$CLI" close --all >"$EV/hv-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/hv-set.log" 2>&1

for pg in $PAGES; do
  TS=$(date +%s%N)
  echo "===== $pg ====="
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/hv-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/hv-wait-$pg.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-state.js")" >"$EV/hv-init-$pg.log" 2>&1
  "$NODE" "$CLI" eval "window.__reset()" >/dev/null 2>&1
  "$NODE" "$CLI" eval "window.__one('默认态')" >/dev/null 2>&1
  "$NODE" "$CLI" eval "window.__pts()" >"$OUT/$pg.pts.raw" 2>&1

  "$PY" - "$OUT/$pg.pts.raw" "$OUT/$pg.pts.txt" <<'PYEOF'
import io, json, sys
raw = io.open(sys.argv[1], encoding='utf-8').read().strip()
s = json.loads(raw) if raw.startswith('"') else raw
d = json.loads(s)
lines = ['%d %d %s' % (p['x'], p['y'], p['sel'].replace(' ', '_')) for p in d['pts']]
io.open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('  theme=%s 触发点 %d' % (d['theme'], len(lines)))
PYEOF

  n=0
  : > "$OUT/$pg.map.txt"
  while read -r x y sel; do
    [ -z "${x:-}" ] && continue
    echo "t$n $x $y $sel" >> "$OUT/$pg.map.txt"
    # ① 只 hover（真鼠标 move 到位），**不按任何键**
    "$NODE" "$CLI" mouse move "$x" "$y" >/dev/null 2>&1
    "$NODE" "$CLI" wait 700 >/dev/null 2>&1        # 等 portal 挂载 + 过渡走完
    # ② 扫描（标签只放序号，选择器写在 map.txt；见 scan-state.sh 的教训）
    "$NODE" "$CLI" eval "window.__one('h$n')" >"$EV/tmp/hv-one.txt" 2>&1
    if grep -q 'not a function' "$EV/tmp/hv-one.txt" 2>/dev/null; then
      # 页面里混着**会跳路由**的可点件（`安装技能` → skills.html）——纯 hover 一般不会跳，
      # 但兜一层：拉回页面重新注入（台账在 localStorage 里，不怕导航）。
      "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$(date +%s%N)" >/dev/null 2>&1
      "$NODE" "$CLI" wait 3800 >/dev/null 2>&1
      "$NODE" "$CLI" eval "$(cat "$EV/p-state.js")" >/dev/null 2>&1
    fi
    # ③ 移开鼠标（让 tooltip 卸载），再进下一个触发点
    "$NODE" "$CLI" mouse move 905 320 >/dev/null 2>&1
    n=$((n + 1))
    [ "$n" -ge 26 ] && break
  done < "$OUT/$pg.pts.txt"

  # ④ 收尾：鼠标停在页面正中，等 tooltip 卸载后再取台账（避免把「残留 tooltip」算进结果）
  "$NODE" "$CLI" mouse move 720 700 >/dev/null 2>&1
  "$NODE" "$CLI" wait 300 >/dev/null 2>&1
  "$NODE" "$CLI" eval "window.__dump()" >"$OUT/$pg.json" 2>&1
  if grep -q 'not a function' "$OUT/$pg.json" 2>/dev/null; then
    "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$(date +%s%N)" >/dev/null 2>&1
    "$NODE" "$CLI" wait 3800 >/dev/null 2>&1
    "$NODE" "$CLI" eval "$(cat "$EV/p-state.js")" >/dev/null 2>&1
    "$NODE" "$CLI" eval "window.__dump()" >"$OUT/$pg.json" 2>&1
  fi
  echo "  悬停扫描 $n 个触发点"
done

"$NODE" "$CLI" close --all >"$EV/hv-close2.log" 2>&1
echo "=== 产物 ==="
ls -la "$OUT"
