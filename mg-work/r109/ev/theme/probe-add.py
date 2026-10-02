# -*- coding: utf-8 -*-
"""r109 · 统计「添加菜单面板」inline 规格在全站的出现次数，供整条替换做断言。"""
import io, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

OLD = (u"background:`var(--color-bg-2)`,borderRadius:8,"
       u"boxShadow:`0px 8px 20px 0px rgba(0, 0, 0, 0.1), "
       u"inset 0 0 0 1px var(--color-border-2)`,"
       u"backdropFilter:`blur(20px)`,WebkitBackdropFilter:`blur(20px)`")

tot = 0
for p in sorted(glob.glob(os.path.join(ROOT, 'pages', '*.html'))):
    s = io.open(p, encoding='utf-8', newline='').read()
    n = s.count(OLD)
    if n:
        print('%-22s x%d' % (os.path.basename(p), n))
        tot += n
print('合计 =', tot)

# 顺带：还有没有别的 blur(20px) 面板（可能也要统一）
print()
print('=== 全站 backdropFilter 取值汇总 ===')
cnt = {}
for p in sorted(glob.glob(os.path.join(ROOT, 'pages', '*.html'))):
    s = io.open(p, encoding='utf-8', newline='').read()
    for m in re.finditer(r'backdropFilter:\s*`([^`]{1,50})`', s):
        cnt[m.group(1)] = cnt.get(m.group(1), 0) + 1
for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
    print('  %-46s x%d' % (k, v))
