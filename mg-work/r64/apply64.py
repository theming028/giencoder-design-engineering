# -*- coding: utf-8 -*-
"""
r64 —— pages/task-detail.html
 第 61 轮把「更多操作」下拉菜单图标缩到 12px，观感偏小 → 回调为 14px。
 图标框（.td-more-ico）仍保持 16px，因此文字起始 x 恒为 37px 不变（r59 逐像素对齐结论继续成立）。

幂等 + 自检：
  ① 标签级计数不变（<style>/</style>/<script>/</script>）
  ② 被改对象精确增减（新串 ==1、旧串 ==0）
  ③ 未触碰的既有 token 计数与改前**相等**（不写死数值，按改前快照比对）
"""
import sys

P = 'pages/task-detail.html'
s = open(P, encoding='utf-8').read()
s0 = s                                  # 改前快照，供「未触碰 token 计数相等」比对
before_bytes = len(s.encode('utf-8'))

TAGS = ['<style>', '</style>', '<script>', '</script>']
tag_before = {t: s.count(t) for t in TAGS}

OLD = ('      /* ★ 第 61 轮：图标墨迹「小两号」—— 16px → 12px（墨迹 14px → 10.5px）。\n'
       '         只缩 svg，图标框仍 16px：文字起始 x 保持 37px 不变（r59 的逐像素对齐结论继续成立），\n'
       '         且 flex 居中会自动吸收两侧各 2px 余量。 */\n'
       '      .td-more-ico svg { display: block; width: 12px; height: 12px; }\n')

NEW = ('      /* ★ 第 61 轮：图标墨迹「小两号」—— 16px → 12px（墨迹 14px → 10.5px）。\n'
       '         ★ 第 64 轮：12px 观感偏小，回调为 14px（即设计稿原始口径 16px 框内 ≈14px 墨迹）。\n'
       '         始终只缩 svg、图标框保持 16px：文字起始 x 恒为 37px 不变（r59 逐像素对齐结论继续成立），\n'
       '         且 flex 居中会自动吸收两侧余量 (16−14)/2 = 1px。 */\n'
       '      .td-more-ico svg { display: block; width: 14px; height: 14px; }\n')

MARK = '.td-more-ico svg { display: block; width: 14px; height: 14px; }'

if MARK in s:
    print('  SKIP  （已应用）')
else:
    n = s.count(OLD)
    if n != 1:
        print('  !!FAIL 锚点命中 %d 次，期望 1' % n)
        sys.exit(1)
    s = s.replace(OLD, NEW, 1)
    print('  OK    图标 12px -> 14px')

print('\n--- 自检 ---')
ok = True

for t in TAGS:
    a, b = s.count(t), tag_before[t]
    if a != b:
        ok = False
    print('  %-4s 标签 %-10s %d -> %d' % ('OK' if a == b else 'FAIL', t, b, a))

for needle, want in [(MARK, 1),
                     ('.td-more-ico svg { display: block; width: 12px; height: 12px; }', 0)]:
    a = s.count(needle)
    if a != want:
        ok = False
    print('  %-4s 计数 %-62s = %d（期望 %d）' % ('OK' if a == want else 'FAIL', needle, a, want))

# 未触碰的既有 token：计数必须与改前相等
for t in ['.td-more-ico', '--color-danger-6', '--color-text-1', 'is-danger']:
    a, b = s.count(t), s0.count(t)
    if a != b:
        ok = False
    print('  %-4s 未触碰 %-16s %d -> %d（应相等）' % ('OK' if a == b else 'FAIL', t, b, a))

after_bytes = len(s.encode('utf-8'))
print('  字节 %d -> %d（%+d）' % (before_bytes, after_bytes, after_bytes - before_bytes))

if not ok:
    print('\n!! 自检未通过，未写盘')
    sys.exit(1)

open(P, 'w', encoding='utf-8').write(s)
print('\n已写入 %s' % P)
