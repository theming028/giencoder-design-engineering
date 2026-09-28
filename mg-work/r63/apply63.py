# -*- coding: utf-8 -*-
"""
r63 —— pages/kanban.html
 1) 「进行中」泳道（.kb-col--doing）内所有卡片标题常驻中粗 500，其它泳道不变。
 2) 「执行中」卡片标题流光换配色：灰底+深灰光 → 深底(#1F1F1F)+品牌蓝扫光(--color-primary-6)。

幂等：每处替换先判 mark（新文本特征串），已应用则 SKIP。
自检：① 标签级计数不变（<style>/</style>/<script>/</script>）
      ② 针对被改对象的精确增减（成对渐变串 1→0 / 0→1），不做全文件关键词总数断言。
"""
import sys

P = 'pages/kanban.html'
s = open(P, encoding='utf-8').read()
before_bytes = len(s.encode('utf-8'))


def sub1(s, label, old, new, mark, expect=1):
    if mark in s:
        print('  SKIP  %s（已应用）' % label)
        return s
    n = s.count(old)
    if n != expect:
        print('  !!FAIL %s：命中 %d 次，期望 %d' % (label, n, expect))
        sys.exit(1)
    if new in s:
        print('  !!FAIL %s：新文本已存在（会重复）' % label)
        sys.exit(1)
    s = s.replace(old, new, 1)
    print('  OK    %s' % label)
    return s


# ---------- 基线快照（用于自检） ----------
TAGS = ['<style>', '</style>', '<script>', '</script>']
tag_before = {t: s.count(t) for t in TAGS}

# ---------- ① 注释补记：说明第 63 轮的配色变更 ----------
OLD1 = '静置色 = --color-text-3(#868686) · 高光色 = --color-text-1(#1F1F1F)\n'
NEW1 = ('静置色 = --color-text-3(#868686) · 高光色 = --color-text-1(#1F1F1F)\n'
        '           ★ 第 63 轮改配色：原「灰底 + 深灰光」静置色 #868686 太浅、标题读不清 →\n'
        '             改为「深底 + 品牌蓝扫光」：静置 = --color-text-1(#1F1F1F)（与其它卡标题同色，最清晰），\n'
        '             高光 = --color-primary-6（本页运行时解析 rgb(55,112,247) = #3770F7，与同卡「执行中」蓝标签同源）。\n')
s = sub1(s, '① 注释补记配色变更', OLD1, NEW1, mark='★ 第 63 轮改配色')

# ---------- ② 渐变两处色值：高光→primary-6，静置→text-1 ----------
OLD2 = ('            var(--color-text-1),\n'
        '            #0000 calc(50% + var(--kb-shimmer-spread))),\n'
        '          linear-gradient(var(--color-text-3), var(--color-text-3));')
NEW2 = ('            var(--color-primary-6),\n'
        '            #0000 calc(50% + var(--kb-shimmer-spread))),\n'
        '          linear-gradient(var(--color-text-1), var(--color-text-1));')
s = sub1(s, '② 流光配色 高光→primary-6 / 静置→text-1',
         OLD2, NEW2, mark='linear-gradient(var(--color-text-1), var(--color-text-1));')

# ---------- ③ 「进行中」泳道标题常驻中粗 500 ----------
OLD3 = ('      .kb-card:hover .kb-card-title { font-weight: 500; }\n')
NEW3 = ('      .kb-card:hover .kb-card-title { font-weight: 500; }\n'
        '      /* ★ 第 63 轮：「进行中」泳道内所有卡片标题常驻中粗 500（其它泳道维持 400、hover 才 500）。\n'
        '         该列已常驻 500，hover 时字重不再变化 —— r33 为「hover 变粗」预留的 8px 右内距\n'
        '         在此列不再承担防抖职责，但保留无害（文字盒布局与其它列保持一致）。 */\n'
        '      .kb-col--doing .kb-card-title { font-weight: 500; }\n')
s = sub1(s, '③ 进行中列标题字重 500',
         OLD3, NEW3, mark='.kb-col--doing .kb-card-title { font-weight: 500; }')

# ---------- 自检 ----------
print('\n--- 自检 ---')
ok = True

for t in TAGS:
    a = s.count(t)
    b = tag_before[t]
    flag = 'OK' if a == b else 'FAIL'
    if a != b:
        ok = False
    print('  %-4s 标签 %-10s %d -> %d' % (flag, t, b, a))

checks = [
    ('@keyframes kb-title-shimmer', 1),
    ('kb-title-shimmer 2s linear infinite', 1),
    ('linear-gradient(var(--color-text-1), var(--color-text-1));', 1),
    ('linear-gradient(var(--color-text-3), var(--color-text-3));', 0),
    ('.kb-col--doing .kb-card-title { font-weight: 500; }', 1),
    # 高光层的完整特征串（唯一）：primary-6 位于 spread 渐变的中间停点
    ('var(--color-primary-6),\n            #0000 calc(50% + var(--kb-shimmer-spread))', 1),
]
for needle, want in checks:
    a = s.count(needle)
    flag = 'OK' if a == want else 'FAIL'
    if a != want:
        ok = False
    print('  %-4s 计数 %-58s = %d（期望 %d）' % (flag, needle, a, want))

after_bytes = len(s.encode('utf-8'))
print('  字节 %d -> %d（%+d）' % (before_bytes, after_bytes, after_bytes - before_bytes))

if not ok:
    print('\n!! 自检未通过，未写盘')
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('\n已写入 %s' % P)
