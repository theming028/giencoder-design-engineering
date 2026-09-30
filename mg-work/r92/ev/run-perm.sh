#!/bin/bash
# r92 ④ 实测：base.html 权限触发器在「默认权限」/「完全访问」两态下的文字与图标色
# ⚠ .ws-dropdown-hover 有两个（工作目录 / 默认权限）⇒ 一律用 :has(.lucide-lock) 精确定位
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
O=mg-work/r92/ev
TRIG='.ws-dropdown-hover:has(svg.lucide-lock)'

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/base.html?v=$(date +%s%N)" >/dev/null 2>&1
"$NODE" "$AB" wait 2200 >/dev/null 2>&1

# T0：默认态（应为「默认权限」）
"$NODE" "$AB" eval "$(cat $O/p92-perm.js)" > "$O/p92-perm-t0.txt" 2>&1
"$NODE" "$AB" screenshot "$TRIG" "$O/../raw/web-perm-def-r92.png" >/dev/null 2>&1

# T1：展开菜单（真鼠标点触发器）
"$NODE" "$AB" click "$TRIG" >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat $O/p92-perm.js)" > "$O/p92-perm-t1.txt" 2>&1
"$NODE" "$AB" screenshot "[role=\"listbox\"][aria-label=\"权限选择\"]" "$O/../raw/web-perm-menu-r92.png" >/dev/null 2>&1

# T2：点第 2 个选项「完全访问」→ 菜单收起
"$NODE" "$AB" click "[aria-label=\"权限选择\"] .perm-menu-item:nth-of-type(2)" >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat $O/p92-perm.js)" > "$O/p92-perm-t2.txt" 2>&1
"$NODE" "$AB" screenshot "$TRIG" "$O/../raw/web-perm-full-r92.png" >/dev/null 2>&1

# T3：再点开菜单 → 触发器在展开态也应是红色
"$NODE" "$AB" click "$TRIG" >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat $O/p92-perm.js)" > "$O/p92-perm-t3.txt" 2>&1
"$NODE" "$AB" screenshot "$TRIG" "$O/../raw/web-perm-full-open-r92.png" >/dev/null 2>&1

# T4：切回「默认权限」→ 应恢复 text-2
"$NODE" "$AB" click "[aria-label=\"权限选择\"] .perm-menu-item:nth-of-type(1)" >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat $O/p92-perm.js)" > "$O/p92-perm-t4.txt" 2>&1
"$NODE" "$AB" screenshot "$TRIG" "$O/../raw/web-perm-back-r92.png" >/dev/null 2>&1
echo DONE
