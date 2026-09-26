# -*- coding: utf-8 -*-
"""
第 10 轮修复
1) header tab：未选中时只显示前两个字（基础 / 研发）
2) settings 分组小标题（通用/关于）颜色再浅一级 -> var(--color-text-3)
3) settings 的 main 容器补波点背景（dot-bg）
4) settings 的 main 内容容器默认宽度 860px
"""
import glob
import os
import sys

PAGES = sorted(glob.glob('pages/*.html'))
LOG = []


def rep(s, old, new, tag, expect=1):
    n = s.count(old)
    if n != expect:
        LOG.append('MISS  %-46s (found %d, expect %d)' % (tag, n, expect))
        return s, False
    LOG.append('OK    %-46s (x%d)' % (tag, n))
    return s.replace(old, new), True


# ---------------------------------------------------------------- 1) tab 文案
TAB_OLD = r"""shrink-0`}),t.label]"""
TAB_NEW = r"""shrink-0`}),r?t.label:t.label.slice(0,2)]"""

for f in PAGES:
    s = open(f, encoding='utf-8').read()
    orig = s
    s, _ = rep(s, TAB_OLD, TAB_NEW, '%s tab 未选中取前两字' % os.path.basename(f))
    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- settings 专属
SP = 'pages/settings.html'
s = open(SP, encoding='utf-8').read()

# 2) 分组小标题浅一级
s, _ = rep(
    s,
    r"""[color:color-mix(in_srgb,var(--color-text-1)_80%_transparent)]`""",
    r"""[color:var(--color-text-3)]`""",
    'settings 分组小标题 -> text-3')

# 3) main 补 dot-bg
s, _ = rep(
    s,
    r"""className:A(`min-w-0 flex-1 h-full overflow-hidden rounded-lg border bg-white`""",
    r"""className:A(`min-w-0 flex-1 h-full overflow-hidden rounded-lg border bg-white dot-bg`""",
    'settings main 加 dot-bg')

# 3b) 注入 .dot-bg 规则（settings 里原本没有）
DOT = ('.dot-bg{background-image:radial-gradient(circle, rgba(55, 112, 247, 0.1) 1.5px, '
       'transparent 1.5px);background-size:20px 20px;}\n')
k = s.rfind('<style>')
j = s.find('</style>', k)
if '.dot-bg{' in s:
    LOG.append('SKIP  settings .dot-bg 规则已存在')
elif k != -1 and j != -1:
    s = s[:j] + DOT + s[j:]
    LOG.append('OK    settings 注入 .dot-bg 规则')
else:
    LOG.append('MISS  settings 注入 .dot-bg 规则')

# 4) 内容容器默认宽度 860px
s, _ = rep(
    s,
    r"""{className:`mx-auto mt-3 flex w-full max-w-3xl flex-col gap-4`,children:[""",
    r"""{className:`mx-auto mt-3 flex w-full flex-col gap-4`,style:{maxWidth:860},children:[""",
    'settings 内容容器 maxWidth 860')

open(SP, 'w', encoding='utf-8').write(s)

print('\n'.join(LOG))
bad = [l for l in LOG if l.startswith('MISS')]
print('\n%s' % ('FAILED' if bad else 'ALL DONE'))
sys.exit(1 if bad else 0)
