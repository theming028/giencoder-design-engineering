# -*- coding: utf-8 -*-
"""第22轮 b 补丁：修正 td-main : td-side 的 8:2 实现方式。

实测（容器 1366，折叠态）：
  flex: 8 1 0 / 2 1 0 + min-width  -> main 1060 / side 306  (side 22.4%)  ✗
  flex: 1 1 80% / 1 1 20% + min   -> main 1086 / side 280  (side 20.5%)  ✓
原因：两栏都是滚动容器，flex-basis:0 时被内容尺寸兜底，比例不可控。
"""
import io

SRC = "mg-work/r21/build-detail.py"
s = io.open(SRC, encoding="utf-8").read()

EDITS = [
    ("main-ratio",
     "        flex: 8 1 0; min-width: 0; overflow: auto; padding: 0 0 32px;  /* 主体 : 信息列 = 8 : 2 */\n",
     "        flex: 1 1 80%; min-width: 0; overflow: auto; padding: 0 0 32px;  /* 主体 : 信息列 = 8 : 2 */\n"),
    ("side-ratio",
     "        flex: 2 1 0; min-width: var(--td-side-min); box-sizing: border-box; overflow: auto;\n",
     "        flex: 1 1 20%; min-width: var(--td-side-min); box-sizing: border-box; overflow: auto;\n"),
]

for name, old, new in EDITS:
    n = s.count(old)
    if n != 1:
        raise SystemExit("PATCH FAIL [%s] count=%d" % (name, n))
    s = s.replace(old, new)
    print("OK  %s" % name)

io.open(SRC, "w", encoding="utf-8").write(s)
print("PATCHED", len(s))
