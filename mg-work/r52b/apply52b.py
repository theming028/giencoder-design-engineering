# -*- coding: utf-8 -*-
"""
第 52 轮 b：修正「浏览栏按钮图标尺寸」的过度修改（幂等 + 自检）

背景 / 依据
----------
r52 第 4 项用户原话：
  「其实"td-browse-ico" 和"td-browse-add"把容器尺寸调整为28px即可」

对照 r52 第 5 项原话：
  「"td-right-acts"容器内的几个图标**本身**的尺寸调整14px」

两句刻意区分 **容器** / **图标本身**：
  · 第 4 项 = 只动 **容器** → 28px
  · 第 5 项 = 只动 **图标** → 14px

r52 实现时把浏览栏的 svg 也一并 16px→14px，属**过度修改**。

设计稿取证（节点 1350:18310，1.5× device）
------------------------------------------
顶栏行 device y[10,50) 墨迹簇：
  x[39,59)   20×22 dev → 13.3×14.7 逻辑px  ⇒ 「摘要」左侧文档图标（16px 盒，r51 已测）
  x[67,107)  40×20 dev → 26.7×13.3 逻辑px  ⇒ 文字「摘要」
  x[160,176) 16×16 dev → 10.7×10.7 逻辑px  ⇒ 加号「+」
Lucide plus 路径 `M5 12h14` + `M12 5v14`，stroke-width 2 ⇒ 墨迹占 16/24 盒宽。
  ⇒ 设计稿加号图标盒 = 10.7 × 24/16 = **16.05 ≈ 16px**
故：容器 28px + 图标 16px。

改动
----
.td-browse-bar .td-browse-add svg,
.td-browse-bar .td-browse-ico svg { width: 14px; height: 14px; }   →  16px
（`.td-right-acts .td-round-btn svg` 的 14px 属于第 5 项，**不得误伤**）
"""
import re
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE = os.path.join(ROOT, 'pages', 'task-detail.html')

OLD = ('      .td-browse-bar .td-browse-add svg,\n'
       '      .td-browse-bar .td-browse-ico svg { width: 14px; height: 14px; }')
NEW = ('      .td-browse-bar .td-browse-add svg,\n'
       '      .td-browse-bar .td-browse-ico svg { width: 16px; height: 16px; }')
NEWMARK = r'\.td-browse-bar \.td-browse-ico svg \{ width: 16px; height: 16px; \}'

s = open(PAGE, encoding='utf-8').read()
bef = s


def raw_cnt(text, p):
    return len(re.findall(p, text))


# 改动前的标签级基线 —— 用于「精确增减量」断言（铁律：只断言被改对象的增量 / 标签级计数不变）
BASE = {p: raw_cnt(bef, p) for p in (r'<style', r'</style>', r'<script', r'</script>')}

applied, skipped = [], []
# ⚠️ 先判 NEW 标记（NEW 是 OLD 的近似串，且顺序无关；这里 NEW 与 OLD 互斥，仍按惯例先判 NEW）
if re.search(NEWMARK, s):
    skipped.append('浏览栏图标回 16px')
elif s.count(OLD) == 1:
    s = s.replace(OLD, NEW, 1)
    applied.append('浏览栏图标回 16px')
else:
    sys.exit('!! 锚点匹配数 = %d（应为 1，且 NEW 标记不存在）' % s.count(OLD))

if s != bef:
    open(PAGE, 'w', encoding='utf-8').write(s)

s = open(PAGE, encoding='utf-8').read()


def cnt(p):
    return len(re.findall(p, s))


CHECKS = [
    # 1) 本次目标
    ('浏览栏 svg 14px 已清零', cnt(r'\.td-browse-bar \.td-browse-ico svg \{ width: 14px; height: 14px; \}'), 0),
    ('浏览栏 svg 16px 现为 1', cnt(NEWMARK), 1),
    # 2) 容器仍 28px（第 4 项本体，不得回退）
    ('.td-browse-ico 容器 28px 仍 1', cnt(r'\.td-browse-bar \.td-browse-ico \{ width: 28px; height: 28px; \}'), 1),
    ('.td-browse-ico 容器 32px 已清零', cnt(r'\.td-browse-bar \.td-browse-ico \{ width: 32px; height: 32px; \}'), 0),
    # 3) 第 5 项不得误伤：td-right-acts 图标仍 14px
    ('td-right-acts svg 仍 14px', cnt(r'\.td-right-acts \.td-round-btn svg \{ width: 14px; height: 14px; \}'), 1),
    # 4) crumb 的两个同名 .td-browse-ico 未被波及（它们在 .td-browse-bar 之外）
    ('crumb 按钮仍 2 个', cnt(r'class=\\"td-browse-ico\\" type=\\"button\\" aria-label=\\"隐藏文件目录\\"'), 1),
    ('浏览器打开按钮仍 1 个', cnt(r'class=\\"td-browse-ico\\" type=\\"button\\" aria-label=\\"在浏览器中打开当前文件\\"'), 1),
    # 5) 页面结构不得受伤（标签级计数「精确增减量 = 0」）
    ('<style> 增量 0', cnt(r'<style') - BASE[r'<style'], 0),
    ('</style> 增量 0', cnt(r'</style>') - BASE[r'</style>'], 0),
    ('<script 增量 0', cnt(r'<script') - BASE[r'<script'], 0),
    ('</script> 增量 0', cnt(r'</script>') - BASE[r'</script>'], 0),
]

bad = []
for label, got, want in CHECKS:
    flag = 'OK ' if got == want else '!! '
    if got != want:
        bad.append(label)
    print('  %s %-34s %s/%s' % (flag, label, got, want))

print('\n应用: %d 项 | 跳过(已应用): %d 项' % (len(applied), len(skipped)))
for x in applied:
    print('   应用:', x)
for x in skipped:
    print('   跳过:', x)

if bad:
    sys.exit('!! 自检失败: %s' % '; '.join(bad))
print('✅ 全部自检通过，文件大小 %d 字符' % len(s))
