# -*- coding: utf-8 -*-
"""第33轮第 6 项配套：把 DS 的 --color-warning-1..10 全档同步进各页内联 :root。

背景：页面内联 :root 是 DS 导出时的「裁剪档」（success/warning/danger 只有 5/6）。
本页 `.kb-card-dash rect { stroke: var(--color-warning-4) }` 因此拿到空值
→ stroke 变成 invalid at computed-value time → 落到初始值 none（虚线整条消失）。
DS 源 giencoder-design-system/colors_and_type.css 已补全 warning-1..10（亮/暗两处），
这里按铁律「页面内联 :root 必须与 colors_and_type.css 逐一对齐」把同档写回页面。
幂等：已存在 --color-warning-4 则跳过。
"""
import os

OLD = ("--color-warning-6:rgb(var(--orange-6));"
       "--color-warning-5:rgb(var(--orange-5));")
NEW = "".join(
    "--color-warning-%d:rgb(var(--orange-%d));" % (n, n)
    for n in (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
)

PAGES = "pages"
changed = []
skipped = []

for fn in sorted(os.listdir(PAGES)):
    if not fn.endswith(".html"):
        continue
    p = os.path.join(PAGES, fn)
    with open(p, "rb") as f:
        raw = f.read()
    s = raw.decode("utf-8")
    # 判据必须带冒号：页面里 `stroke: var(--color-warning-4)` 这类「使用处」也会命中裸名
    if "--color-warning-4:" in s:
        skipped.append(fn)
        continue
    n = s.count(OLD)
    if n == 0:
        skipped.append(fn + "(no-match)")
        continue
    s = s.replace(OLD, NEW)
    with open(p, "wb") as f:
        f.write(s.encode("utf-8"))
    changed.append("%s (x%d)" % (fn, n))

print("changed:", ", ".join(changed) if changed else "-")
print("skipped:", ", ".join(skipped) if skipped else "-")
