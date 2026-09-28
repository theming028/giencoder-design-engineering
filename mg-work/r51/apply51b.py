# -*- coding: utf-8 -*-
"""r51 补丁 b：精修 .td-browse-tab 的「摘要」图标
设计稿（容器-178 / 1350:18310，device 1.5×）逐像素回推，viewBox 24 记为：
  · 文档盒 device x40..56.5 / y19.5..39.5  → viewBox x2.5..19 / y2..22
  · 右上角是**直斜切**：device (53,20)→(56.5,25) → viewBox (15.5,2)→(19,7.5)
    （不是小圆角；此前用 3.5 圆弧，视觉上"开口"不够）
  · 圆徽标：外径 device x47..58 → viewBox 外缘 9.5..20.5，圆心 (15,17.5)、r=4.5
    —— 圆心到描边中线 = 4.5，外缘 5.5；它把文档右边(19)与下边(22)在
    x≈11.8 之后全部挖空，与设计稿「底边只剩到 device x49」完全吻合。
"""
import io, sys, os

P = 'pages/task-detail.html'
s = io.open(P, encoding='utf-8').read()

OLD = ('<path d=\\"M4 2h11.5a3.5 3.5 0 0 1 3.5 3.5v15a1.5 1.5 0 0 1-1.5 1.5H4a1.5 1.5 0 0 1-1.5-1.5v-17A1.5 1.5 0 0 1 4 2Z\\"/>'
       '<path d=\\"M7.5 9.5h6.5\\"/>'
       '<path d=\\"M6.5 13h3.5\\"/>'
       '<path d=\\"M7 16.5h3.5\\"/>'
       '<circle cx=\\"15.5\\" cy=\\"18\\" r=\\"4\\" style=\\"fill:var(--color-bg-1)\\"/>')
NEW = ('<path d=\\"M4 2h11.5l3.5 5.5v13a1.5 1.5 0 0 1-1.5 1.5H4a1.5 1.5 0 0 1-1.5-1.5v-17A1.5 1.5 0 0 1 4 2Z\\"/>'
       '<path d=\\"M7.5 9.5h6.5\\"/>'
       '<path d=\\"M6.5 13h3.5\\"/>'
       '<path d=\\"M7 16.5h3.5\\"/>'
       '<circle cx=\\"15\\" cy=\\"17.5\\" r=\\"4.5\\" style=\\"fill:var(--color-bg-1)\\"/>')

if NEW in s and OLD not in s:
    print('= 已是目标态，跳过')
    sys.exit(0)
c = s.count(OLD)
if c != 1:
    raise SystemExit(f'!! 锚点命中 {c} 次，期望 1 -> 中止')
s = s.replace(OLD, NEW, 1)

print('=== 自检 ===')
checks = [
    ('<style> 仍 2', s.count('<style>'), 2),
    ('</style> 仍 3', s.count('</style>'), 3),
    ('<script> 仍 8', s.count('<script>'), 8),
    ('</script> 仍 8', s.count('</script>'), 8),
    ('斜切路径 1 处', s.count('h11.5l3.5 5.5v13a1.5'), 1),
    ('圆 r=4.5 1 处', s.count('r=\\"4.5\\" style=\\"fill:var(--color-bg-1)\\"'), 1),
    ('旧圆弧 0 处', s.count('a3.5 3.5 0 0 1 3.5 3.5v15'), 0),
    ('树行 is-dir 仍 10', s.count('class=\\"td-bf is-dir'), 10),
    ('data-td-split 仍 5', s.count('data-td-split'), 5),
]
fail = 0
for name, got, want in checks:
    ok = got == want
    fail += 0 if ok else 1
    print(f'  {"OK " if ok else "!! "}{name}: got={got} want={want}')
if fail:
    print(f'!! {fail} 条失败，未写盘'); sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print(f'✅ 已写盘 {len(s)} 字节')
