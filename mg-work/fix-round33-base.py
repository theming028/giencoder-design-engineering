# -*- coding: utf-8 -*-
"""round33 第 5 项：base.html 的 .dot-bg 去掉彩色弥散层，只保留波点。

背景：`pages/kanban|task-detail|settings|dev|req-kanban.html` 的 `.dot-bg` 早已是「纯波点」
（`.dot-bg{background-image:radial-gradient(circle, rgba(55,112,247,.1) 1.5px, transparent 1.5px);background-size:20px 20px;}`），
只有 `pages/base.html` 还留着 5 层（1 层波点 + 4 层彩色弥散：giencoderblue / purple / cyan / pinkpurple）。
本次把 base.html 的两处规则（亮色 + 深色主题各一条）统一成与其它页一致的单层波点。

幂等：已是单层则跳过。
"""
import io
import re

P = r'E:\GienCoder\giencoder-design-engineering\pages\base.html'
CANON = (".dot-bg{background-image:radial-gradient(circle, rgba(55, 112, 247, 0.1) 1.5px, "
         "transparent 1.5px);background-size:20px 20px;}")

s = io.open(P, encoding='utf-8').read()
before = len(s)

pat = re.compile(r"\.dot-bg\{background-image:radial-gradient\(circle[^}]*\}")
hits = pat.findall(s)
print("匹配到 .dot-bg 规则 %d 条" % len(hits))
for i, h in enumerate(hits):
    print("  [%d] %d chars: %s" % (i, len(h), h[:110]))

if not hits:
    print("RESULT: NO_MATCH（可能已处理）")
else:
    s2, n = pat.subn(CANON, s)
    io.open(P, 'w', encoding='utf-8', newline='').write(s2)
    print("已替换 %d 条；文件 %d → %d chars" % (n, before, len(s2)))
    left = pat.findall(s2)
    print("替换后残留多层规则 %d 条" % len(left))
    print("RESULT: OK")
