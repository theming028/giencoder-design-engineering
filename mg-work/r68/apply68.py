#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 68 轮：把「研发工作台 > 任务看板 > 任务详情页」(pages/task-detail.html) 右栏 AI 对话框的
全部要素，替换到「数字分身」右栏 (pages/avatar.html)。

用户已拍板的 4 个口径：
  ① 容器外观      → 保留投影（不动 .td-right 的 box-shadow）
  ② 顶栏按钮      → 加上第 4 个「打开侧栏」（视觉对齐；本页无浏览面板，点击无响应）
  ③ 标题栏留白    → 保留第 45 轮的 gap:48px（不跟详情页回 8px）
  ④ AI 消息元信息 → 照搬详情页（耗时链接 + 发丝线 + 上下文注入）

替换项（共 11 条）：
  DOM: D1 顶栏第 4 按钮 / D2 meta 段 / D3 附件图标 svg
  CSS: C1 .td-file-ico 尺寸 / C2 .td-file-ico svg + 大卡覆盖 / C3 .td-ai-meta margin /
       C4 .td-ai-meta a / C5 新增 .td-ai-rule + .td-ai-ctx / C6 .td-ai-foot 字号 /
       C7 .td-round-btn 尺寸 + svg / C8 composer 收缩链

铁律：
  · 幂等：每条替换先判 newmark，命中即 SKIP；复跑必须 Δ0 字节
  · 新增注释**不复述**被删/被改的标识符（否则污染词频断言）
  · 新增注释**不写字面量** </script> / <style> / </body>（否则污染标签计数）
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)

P_AV = 'pages/avatar.html'
TD_DOM = 'mg-work/r68/td-right.dom.html'

applied, skipped, fails = [], [], []

cur = open(P_AV, encoding='utf-8').read()
before = cur
td_dom = open(TD_DOM, encoding='utf-8').read()


def sub(label, old, new, newmark, expect=1):
    global cur
    if newmark and newmark in cur:
        skipped.append(label)
        return False
    n = cur.count(old)
    if n != expect:
        sys.exit('✗ [%s] 锚点命中 %d 次（期望 %d）\n   OLD[:160]=%r' % (label, n, expect, old[:160]))
    cur = cur.replace(old, new, 1)
    applied.append((label, len(new) - len(old)))
    return True


def seg(text, start, end, label):
    """从 text 中截取 [start, end] 片段，返回 (片段, 起点)"""
    a = text.find(start)
    if a < 0:
        sys.exit('✗ [%s] 起点未找到: %r' % (label, start[:80]))
    b = text.find(end, a)
    if b < 0:
        sys.exit('✗ [%s] 终点未找到: %r' % (label, end[:80]))
    return text[a:b + len(end)], a


# ============================ D1 顶栏第 4 个按钮 ============================
# 从详情页提取「打开侧栏」按钮原文
btn_td, _ = seg(td_dom, '<button class="giencoder-btn', '</button>', 'D1-td')
# 定位到正确的那个（含 aria-label="打开侧栏"）
a = td_dom.find('aria-label="打开侧栏"')
a = td_dom.rfind('<button', 0, a)
b = td_dom.find('</button>', a) + len('</button>')
btn_td = td_dom[a:b]

D1_OLD = ('<path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg></button>\n'
          '        </div>\n'
          '      </header>')
D1_NEW = ('<path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg></button>\n'
          '          ' + btn_td + '\n'
          '        </div>\n'
          '      </header>')
sub('D1 顶栏「打开侧栏」按钮', D1_OLD, D1_NEW, 'data-td-browse-toggle="1"')

# ============================ D2 AI 消息 meta 段 ============================
meta_old, _ = seg(cur, '<div class="td-ai-meta">', '</div>', 'D2-av')
# 精确定位：从 <div class="td-ai-meta"> 到其后第一个 </div>
m = re.search(r'<div class="td-ai-meta">.*?</div>', cur, re.S)
if not m:
    sys.exit('✗ [D2] 未匹配到 meta 段')
meta_old = m.group(0)
meta_new = td_dom[td_dom.find('<div class="td-ai-meta">'):]
meta_new = meta_new[meta_new.find('<div class="td-ai-meta">'):]
meta_new = meta_new[:meta_new.find('</a>', meta_new.find('上下文注入')) + 4]
sub('D2 AI 消息 meta 段', meta_old, meta_new, 'class="td-ai-ctx"')

# ============================ D3 附件文档图标 ============================
ico_old, _ = seg(cur, '<span class="td-file-ico">', '</span>', 'D3-av')
ico_new, _ = seg(td_dom, '<span class="td-file-ico">', '</span>', 'D3-td')
sub('D3 附件文档图标 svg', ico_old, ico_new, 'd="M6.375,1.875')

# ============================ C1 .td-file-ico 尺寸 ============================
C1_OLD = '.td-file-ico { width: 16px; height: 16px; flex: none; color: var(--td-ico-gray); line-height: 0; }'
C1_NEW = '.td-file-ico { width: 14px; height: 14px; flex: none; color: var(--td-ico-gray); line-height: 0; }'
sub('C1 .td-file-ico 16→14', C1_OLD, C1_NEW, C1_NEW)

# ============================ C2 .td-file-ico svg + 大卡覆盖 ============================
C2_OLD = '.td-file-ico svg { display: block; width: 100%; height: 100%; }'
C2_NEW = ('.td-file-ico svg { display: block; width: 14px; height: 14px; }\n'
          '/* ★ 第 68 轮：图标尺寸改为固定值后，24px 图标的大卡需要显式覆盖（与任务详情页同口径）。 */\n'
          '      .td-file--lg .td-file-ico svg { width: 24px; height: 24px; }')
sub('C2 .td-file-ico svg 定尺寸 + 大卡覆盖', C2_OLD, C2_NEW, '.td-file--lg .td-file-ico svg { width: 24px; height: 24px; }')

# ============================ C3 .td-ai-meta margin ============================
C3_OLD = '.td-ai-meta { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta); }'
C3_NEW = '.td-ai-meta { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta); margin-top: 8px; }'
sub('C3 .td-ai-meta +margin-top', C3_OLD, C3_NEW, C3_NEW)

# ============================ C4 .td-ai-meta a ============================
C4_OLD = '.td-ai-meta a { display: inline-flex; align-items: center; gap: 4px; color: var(--td-meta); text-decoration: none; }'
C4_NEW = '.td-ai-meta a { display: inline-flex; align-items: center; gap: 2px; color: var(--td-meta); text-decoration: none; line-height: 22px; }'
sub('C4 .td-ai-meta a gap/line-height', C4_OLD, C4_NEW, C4_NEW)

# ============================ C5 新增 .td-ai-rule + .td-ai-ctx ============================
C5_OLD = '.td-ai-meta svg { width: 14px; height: 14px; flex: none; }'
C5_NEW = ('.td-ai-meta svg { width: 14px; height: 14px; flex: none; }\n'
          '/* ★ 第 68 轮：AI 消息头元信息区与任务详情页对齐 —— 耗时链接下方一条整宽发丝线，\n'
          '         其下再一行是与详情页同款的上下文入口链接（同 #868686 色 + 14px 图标）。 */\n'
          '      .td-ai-rule { flex: none; height: 1px; background: var(--color-border-1); margin: 4px 0; }\n'
          '      .td-ai-ctx {\n'
          '        display: inline-flex; align-items: center; gap: 4px; align-self: flex-start;\n'
          '        height: 22px; margin-bottom: 4px;\n'
          '        font-size: var(--font-size-body-3); line-height: 22px; color: var(--td-meta); text-decoration: none;\n'
          '      }\n'
          '      .td-ai-ctx svg { width: 14px; height: 14px; flex: none; }\n'
          '      .td-ai-ctx:hover, .td-ai-ctx:focus-visible { color: var(--color-primary-6); }')
sub('C5 新增 .td-ai-rule / .td-ai-ctx', C5_OLD, C5_NEW, '.td-ai-ctx {')

# ============================ C6 .td-ai-foot 字号 ============================
C6_OLD = '.td-ai-foot { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta); }'
C6_NEW = '.td-ai-foot { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-1); color: var(--td-meta); }'
sub('C6 .td-ai-foot 字号 body-3→body-1', C6_OLD, C6_NEW, C6_NEW)

# ============================ C7 .td-round-btn 尺寸 + svg ============================
C7_OLD = '      .td-round-btn { box-sizing: border-box; width: 32px; padding: 0; border-color: transparent; line-height: 0; }'
C7_NEW = ('      .td-round-btn,\n'
          '      .td-round-btn:hover,\n'
          '      .td-round-btn:active {\n'
          '        box-sizing: border-box; width: 28px; height: 28px; padding: 0;\n'
          '        border-color: transparent; box-shadow: none; line-height: 0;\n'
          '      }\n'
          '/* ★ 第 68 轮：标题栏图标本体 16 → 14px（按钮盒仍是 28×28）。 */\n'
          '      .td-right-acts .td-round-btn svg { width: 14px; height: 14px; }')
sub('C7 .td-round-btn 32→28 + svg', C7_OLD, C7_NEW, '.td-right-acts .td-round-btn svg { width: 14px; height: 14px; }')

# ============================ C8 composer 收缩链 ============================
C8_OLD = '/* 补齐 base 页使用、本页 Tailwind 产物未包含的 3 个任意值类 */'
C8_NEW = ('/* ★ 第 68 轮：AI 对话框横向空间不足时，大模型选择器文字自动截断省略（与任务详情页同口径）。\n'
          '         病因：模型选择器带内联 flex-shrink:0，DS 的 .giencoder-select-view-text 省略号\n'
          '         永远触发不到 —— 右栏 ≤ 400px 时整条工具条会被顶出对话框框外。\n'
          '         修法：放开整条收缩链（逐级 min-width:0），图标按钮不参与收缩。 */\n'
          '      .td-composer .mt-auto,\n'
          '      .td-composer .mt-auto > .flex,\n'
          '      .td-composer .mt-auto .flex.items-center.gap-2 { min-width: 0; }\n'
          '      .td-composer .giencoder-select { min-width: 0 !important; flex-shrink: 1 !important; }\n'
          '      .td-composer .giencoder-select-view { min-width: 0; }\n'
          '      .td-composer .giencoder-select-selection { min-width: 0; overflow: hidden; }\n'
          '      .td-composer .giencoder-select-view-text { min-width: 0; }\n'
          '      .td-composer .mt-auto button { flex: none; }\n'
          '      /* 大模型选择器贴对话框右缘：弹层改为右对齐、向内展开，否则会伸出白框。 */\n'
          '      .td-composer .mt-auto .flex.items-center.gap-2 > .giencoder-select > .giencoder-select-popup { left: auto; right: 0; }\n'
          '/* 补齐 base 页使用、本页 Tailwind 产物未包含的 3 个任意值类 */')
sub('C8 composer 收缩链', C8_OLD, C8_NEW, '.td-composer .giencoder-select { min-width: 0 !important')

# ============================ 写盘 ============================
open(P_AV, 'w', encoding='utf-8').write(cur)

print('=' * 74)
print('应用 %d 项 | 跳过 %d 项（幂等命中）| 字节 %+d' % (len(applied), len(skipped), len(cur) - len(before)))
print('=' * 74)
for lbl, d in applied:
    print('  ✓ %-42s %+5d B' % (lbl, d))
for lbl in skipped:
    print('  · %-42s SKIP' % lbl)

# ============================ 自检 ============================
print()
print('---------- 自检 ----------')

# (1) 元守卫：新增片段里不得复述「应消失」的 token
GUARD = ['思考过程']   # 只放「应消失」的 token；新增文案（如上下文入口）不属此列
for name, txt in (('D2-new', meta_new), ('D1-new', D1_NEW), ('C2-new', C2_NEW),
                  ('C5-new', C5_NEW), ('C7-new', C7_NEW), ('C8-new', C8_NEW)):
    bad = [g for g in GUARD if g in txt]
    if bad:
        fails.append('%s 新增片段含应消失的 token: %s' % (name, bad))

# (2) 标签级计数（改前 vs 改后 差值）
for t in ('<style>', '</style>', '<script>', '</script>', '<div', '</div>', '</aside>'):
    a, b = before.count(t), cur.count(t)
    ok = a == b
    print('  %-12s %-5d → %-5d %s' % (t, a, b, '✓ 无变化' if ok else '✗ %+d' % (b - a)))
    if not ok:
        fails.append('标签计数变化 ' + t)

# (3) 被改对象的精确计数
def chk(name, got, want):
    ok = got == want
    print('  %-46s %-3s %s' % (name, got, '✓' if ok else '✗ 期望 %s' % want))
    if not ok:
        fails.append(name)

print()
chk('data-td-browse-toggle（新增按钮）', cur.count('data-td-browse-toggle="1"'), 1)
chk('td-sep 在 DOM 中的剩余处数', cur.count('<span class="td-sep"></span>'), 1)
chk('td-ai-rule（新增 DOM 元素）', cur.count('<span class="td-ai-rule"'), 1)
chk('td-ai-ctx 元素', cur.count('<a class="td-ai-ctx"'), 1)
chk('上下文注入（DOM 链接文本）', cur.count('>上下文注入</a>'), 1)
print()
chk('旧 meta 链接文案已消失', cur.count('任务完成，耗时 28m12s'), 0)
chk('新 meta 链接文案已就位', cur.count('任务完成，耗时28m12s'), 1)
print()
chk('.td-ai-rule 规则', cur.count('.td-ai-rule {'), 1)
chk('.td-ai-ctx 规则', cur.count('.td-ai-ctx {'), 1)
chk('.td-ai-ctx svg 规则', cur.count('.td-ai-ctx svg {'), 1)
chk('.td-right-acts .td-round-btn svg 规则', cur.count('.td-right-acts .td-round-btn svg'), 1)
chk('.td-file--lg .td-file-ico svg 规则', cur.count('.td-file--lg .td-file-ico svg'), 1)
chk('composer 收缩链锚点', cur.count('.td-composer .giencoder-select { min-width: 0 !important'), 1)
print()
chk('旧 32px 按钮盒已消失', cur.count('width: 32px; padding: 0; border-color: transparent'), 0)
chk('旧 .td-file-ico svg 100% 已消失', cur.count('.td-file-ico svg { display: block; width: 100%'), 0)

# (4) 关键 CSS 值就位
for name, pat, want in (
    ('.td-file-ico 14px', '.td-file-ico { width: 14px; height: 14px;', 1),
    ('.td-ai-meta margin-top', 'color: var(--td-meta); margin-top: 8px; }', 1),
    ('.td-ai-meta a gap:2px', 'gap: 2px; color: var(--td-meta); text-decoration: none; line-height: 22px;', 1),
    ('.td-ai-foot body-1', '.td-ai-foot { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-1);', 1),
    ('round-btn 28x28', 'box-sizing: border-box; width: 28px; height: 28px; padding: 0', 1),
):
    chk(name, cur.count(pat), want)

# (5) 保留项（用户口径）不得被动到
print()
chk('.td-right 仍为投影（保留）', cur.count('background: var(--color-bg-1); border-radius: 8px;\n        box-shadow: var(--td-panel-shadow);'), 1)
chk('.td-right-bar gap:48px 保留', cur.count('.td-right-bar { gap: 48px; }'), 1)

print()
if fails:
    print('✗✗✗ FAILED %d 项：' % len(fails))
    for f in fails:
        print('   -', f)
    sys.exit(1)
print('✓✓✓ ALL PASS')
