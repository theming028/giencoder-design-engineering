#!/usr/bin/env bash
# r109 第四拍（裁决③）· 逐状态亮面审计 · **真鼠标驱动**（10 页）
#
# 为什么不用 JS 合成 click：实测打不开这些浮层（`aria-expanded` 仍 false）⇒ 假阴性。
# 见 `p-state.js` 文件头。这里用 `mouse move / down / up` 发**真事件**。
#
# ★★ 铁律：agent-browser 的 stdout 绝不能接管道（守护进程持有写端 ⇒ 管道永不 EOF）。一律重定向。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/state4"
mkdir -p "$OUT" "$EV/tmp"

PAGES="${*:-base avatar automation skills settings conversation dev kanban req-kanban task-detail}"

"$NODE" "$CLI" close --all >"$EV/st-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/st-set.log" 2>&1

for pg in $PAGES; do
  TS=$(date +%s%N)
  echo "===== $pg ====="
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/st-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/st-wait-$pg.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-state.js")" >"$EV/st-init-$pg.log" 2>&1
  "$NODE" "$CLI" eval "window.__reset()" >/dev/null 2>&1      # ★ 台账按页清空，防串账
  "$NODE" "$CLI" eval "window.__one('默认态')" >/dev/null 2>&1
  "$NODE" "$CLI" eval "window.__pts()" >"$OUT/$pg.pts.raw" 2>&1

  # 解出触发点（agent-browser 的 eval 输出是 JSON 套 JSON ⇒ 逐层 json.loads）
  "$PY" - "$OUT/$pg.pts.raw" "$OUT/$pg.pts.txt" <<'PYEOF'
import io, json, sys
raw = io.open(sys.argv[1], encoding='utf-8').read().strip()
s = json.loads(raw) if raw.startswith('"') else raw
d = json.loads(s)
lines = ['%d %d %s' % (p['x'], p['y'], p['sel'].replace(' ', '_')) for p in d['pts']]
io.open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('  theme=%s 触发点 %d' % (d['theme'], len(lines)))
PYEOF

  n=0; skip=0
  : > "$OUT/$pg.map.txt"
  while read -r x y sel; do
    [ -z "${x:-}" ] && continue
    echo "t$n $x $y $sel" >> "$OUT/$pg.map.txt"
    # ① 真鼠标点开（move → down → up；★ 用合成的 `el.click()` 打不开，见 p-state.js 文件头）
    "$NODE" "$CLI" mouse move "$x" "$y" >/dev/null 2>&1
    "$NODE" "$CLI" mouse down >/dev/null 2>&1
    "$NODE" "$CLI" mouse up >/dev/null 2>&1
    # ② 移开鼠标（避免 :hover 干扰），落点选内容区空白处
    "$NODE" "$CLI" mouse move 905 320 >/dev/null 2>&1
    # ③ 扫描
    # ★★ 标签里**只放序号**，不放选择器（本拍真踩：把 `path()` 拼进 JS 字面量后
    #    `eval` 报 `SyntaxError: Invalid or unexpected token`，整轮 22 次点击全废、
    #    台账只剩默认态那 2 条 —— 而错误只落在被覆盖的日志里，不看你根本发现不了）。
    #    序号 ↔ 选择器的对应写在 `$pg.map.txt`。
    "$NODE" "$CLI" eval "window.__one('t$n')" >"$EV/tmp/st-one.txt" 2>&1
    if grep -q 'not a function' "$EV/tmp/st-one.txt" 2>/dev/null; then
      # 页面里混着**会跳路由**的可点件（`安装技能` → skills.html、顶栏「研发工作台」→ dev.html）
      # ⇒ 一跳转探针全局全没；把页面拉回来重新注入。台账在 localStorage 里，不怕导航。
      skip=$((skip + 1))
      "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$(date +%s%N)" >/dev/null 2>&1
      "$NODE" "$CLI" wait 3800 >/dev/null 2>&1
      "$NODE" "$CLI" eval "$(cat "$EV/p-state.js")" >/dev/null 2>&1
    fi
    # ④ 在**空白处再点一下**把浮层收掉。
    #    ★★ 不这么做的话，下一个触发件的第一次点击只会「关掉上一个浮层」而**不开新的**
    #      ⇒ 权限浮层 / 技能浮层永远打不开（本拍真踩第二次假阴性的直接成因）。
    "$NODE" "$CLI" mouse down >/dev/null 2>&1
    "$NODE" "$CLI" mouse up >/dev/null 2>&1
    "$NODE" "$CLI" eval "window.__close()" >/dev/null 2>&1
    n=$((n + 1))
    [ "$n" -ge 26 ] && break
  done < "$OUT/$pg.pts.txt"

  "$NODE" "$CLI" eval "window.__dump()" >"$OUT/$pg.json" 2>&1
  # ★ 兜底：若最后一次点击把页面带走了（探针全局随导航消失），拉回页面重新注入再取台账
  #   —— 台账在 localStorage 里，不怕导航。
  if grep -q 'not a function' "$OUT/$pg.json" 2>/dev/null; then
    "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$(date +%s%N)" >/dev/null 2>&1
    "$NODE" "$CLI" wait 3800 >/dev/null 2>&1
    "$NODE" "$CLI" eval "$(cat "$EV/p-state.js")" >/dev/null 2>&1
    "$NODE" "$CLI" eval "window.__dump()" >"$OUT/$pg.json" 2>&1
  fi
  echo "  真鼠标点击 $n 次（其中跳路由重载 $skip 次）"
done

"$NODE" "$CLI" close --all >"$EV/st-close2.log" 2>&1
echo "=== 产物 ==="
ls -la "$OUT"
