#!/usr/bin/env bash
# r109 第八拍 · 真机验收：下拉菜单「浅色 Δ 复核 + 暗色翻转」（真鼠标）
#   对每页：① 浅色 hover 读底色/描边 → ② 切暗色同一件再 hover 读 → ③ 变量表 + 静态 chip
#   ★ 读值一律走 __bgAt（按坐标几何命中后**沿祖先链**读 computed style）
#     —— 不用 elementFromPoint：浮层背景是铺满面板的 SVG，会挡住菜单项（已踩）。
# ★ 铁律：agent-browser stdout 一律重定向（不接管道）；同一时刻只跑一个实测进程。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"
OUT="mg-work/r109/raw/lit8"
mkdir -p "$OUT" "$EV/tmp"

PAGES="${*:-base dev kanban conversation}"
# ★ 菜单项候选类名（按优先级试；不同下拉用不同类）
#   · 基础/研发工作台侧栏项 —— `hover:bg-[var(--color-fill-2)]`（尾风 var 类，第 7 拍换的）
#   · r81 工作空间浮层项 —— `r81-ws-item`（独立面板，不走尾风）
SUBS='hover:bg-[var(--color-fill-2)]|r81-ws-item|menu-item|giencoder-select-option'

find_item () {   # $1 = 候选串（| 分隔）；输出 "x y sub"
  local s
  IFS='|' read -r -a ARR <<<"$1"
  for s in "${ARR[@]}"; do
    local r
    r=$("$NODE" "$CLI" eval "(function(){var d=JSON.parse(window.__find('$s',460,64));return d.length?(d[0].x+' '+d[0].y):'0 0';})()" 2>/dev/null | tr -d '"' | head -1)
    if [ "${r%% *}" != "0" ]; then echo "$r"; return; fi
  done
  echo "0 0"
}

for PG in $PAGES; do
  TS=$(date +%s%N)
  echo "===== $PG ====="
  "$NODE" "$CLI" close --all >"$EV/tmp/l-close.log" 2>&1
  "$NODE" "$CLI" set viewport 1440 900 >"$EV/tmp/l-set.log" 2>&1
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/$PG.open" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/tmp/l-wait.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-lit.js")" >"$OUT/$PG.init" 2>&1

  # ---------- ① 浅色档 ----------
  "$NODE" "$CLI" eval "window.__setLight()" >"$OUT/$PG.light.set" 2>&1
  "$NODE" "$CLI" wait 500 >"$EV/tmp/l-w2.log" 2>&1
  "$NODE" "$CLI" eval "window.__vars()" >"$OUT/$PG.light.vars" 2>&1
  "$NODE" "$CLI" eval "window.__css('[aria-pressed=\"true\"]', ['backgroundColor','color','borderTopColor'])" >"$OUT/$PG.light.chip" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-lit.js")" >"$OUT/$PG.init2" 2>&1

  # ★ 先「不点任何东西」直接找菜单项 —— 实测教训：**一旦点开浮层，浮层就盖住侧栏**
  #   ⇒ 真鼠标落到侧栏项上时指针事件被浮层吃走，`:hover` 永不生效（bg 读成 transparent）。
  #   ⇒ 只有在「不点找不到项」时才去点触发器（那种页面的菜单项确实在浮层里）。
  IX=$(find_item "$SUBS")
  if [ "${IX%% *}" = "0" ]; then
    TR=$("$NODE" "$CLI" eval "(function(){var d=JSON.parse(window.__trig());return d.length?(d[0].x+' '+d[0].y+' via='+d[0].via):'0 0 none';})()" 2>/dev/null | tr -d '"' | head -1)
    echo "  触发器 = $TR（需点开）"
    TX=${TR%% *}; REST=${TR#* }; TY=${REST%% *}
    if [ "$TX" != "0" ]; then
      "$NODE" "$CLI" mouse move "$TX" "$TY" >"$EV/tmp/l-m1.log" 2>&1
      "$NODE" "$CLI" mouse down >"$EV/tmp/l-m2.log" 2>&1
      "$NODE" "$CLI" mouse up >"$EV/tmp/l-m3.log" 2>&1
      "$NODE" "$CLI" wait 700 >"$EV/tmp/l-w3.log" 2>&1
      IX=$(find_item "$SUBS")
    fi
  else
    echo "  触发器 = （无需点开：菜单项在侧栏，直接可 hover）"
  fi
  echo "  菜单项   = $IX"
  HX=${IX%% *}; HY=${IX#* }
  if [ "$HX" != "0" ]; then
    "$NODE" "$CLI" mouse move "$HX" "$HY" >"$EV/tmp/l-h1.log" 2>&1
    "$NODE" "$CLI" wait 400 >"$EV/tmp/l-w4.log" 2>&1
    "$NODE" "$CLI" eval "window.__bgAt($HX, $HY, '')" >"$OUT/$PG.light.bg" 2>&1
  fi

  # ---------- ② 暗色档（同一坐标再 hover，不重新点开）----------
  "$NODE" "$CLI" eval "window.__setDark()" >"$OUT/$PG.dark.set" 2>&1
  "$NODE" "$CLI" wait 800 >"$EV/tmp/l-w5.log" 2>&1
  if [ "$HX" != "0" ]; then
    # 先把指针移开再移回，确保 :hover 重新进入（改档后浏览器可能复用旧 hover）
    "$NODE" "$CLI" mouse move 5 5 >"$EV/tmp/l-m4.log" 2>&1
    "$NODE" "$CLI" wait 160 >"$EV/tmp/l-w5b.log" 2>&1
    "$NODE" "$CLI" mouse move "$HX" "$HY" >"$EV/tmp/l-m5.log" 2>&1
    "$NODE" "$CLI" wait 400 >"$EV/tmp/l-w6.log" 2>&1
    "$NODE" "$CLI" eval "window.__bgAt($HX, $HY, '')" >"$OUT/$PG.dark.bg" 2>&1
  fi
  "$NODE" "$CLI" eval "window.__vars()" >"$OUT/$PG.dark.vars" 2>&1
  "$NODE" "$CLI" eval "window.__css('[aria-pressed=\"true\"]', ['backgroundColor','color','borderTopColor'])" >"$OUT/$PG.dark.chip" 2>&1
done

"$NODE" "$CLI" close --all >"$EV/tmp/l-close2.log" 2>&1
echo
echo "=== 产物：$OUT ==="
ls "$OUT" | head -80
