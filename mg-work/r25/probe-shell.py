# -*- coding: utf-8 -*-
"""对比各页面外壳的「路由映射 / 导航函数 / file: 判断」，确认 tab 失效范围。"""
import io
import re

FILES = ["base.html", "dev.html", "kanban.html", "settings.html", "avatar.html",
         "automation.html", "skills.html", "req-kanban.html", "task-detail.html"]

NAV_RE = re.compile(r"function (\w+)\(e\)\{if\(typeof e===.number.\)\{window\.history\.go\(e\);return\}.{0,240}", re.S)
MAP_RE = re.compile(r"var (\w+)=\{.{0,400}?\.html.?[^}]{0,300}\}")

for f in FILES:
    h = io.open("pages/" + f, encoding="utf-8", errors="replace").read()
    nav = NAV_RE.search(h)
    print("=== %s ===" % f)
    if nav:
        print("  nav fn %s: %s" % (nav.group(1), nav.group(0)[:250].replace("\n", " ")))
    else:
        print("  nav fn: NOT FOUND")
    print("  has `protocol===`file:` : %s" % ("protocol===`file:`" in h))
    m = MAP_RE.search(h)
    if m:
        seg = m.group(0)
        for k in ("base.html", "dev.html", "kanban.html"):
            if k in seg:
                print("  map %s: 含 %s" % (m.group(1), k))
                break
    print("  含 工作台切换: %s" % ("工作台切换" in h))
