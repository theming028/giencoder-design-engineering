#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 67 轮补丁 A：移除「执行中」卡片标题的文字流光（Text Shimmer）

背景：r62 引入、r63 改配色。用户本轮要求「去掉」。
      删掉后 .kb-card-title 回到基础规则：color: var(--color-text-1) / font-weight: 400
      （hover → 500、.kb-col--doing 常驻 500 这两条独立规则保留）。

删除范围（3 处，全在 pages/kanban.html）：
  ① CSS：`/* ★ 第 62 轮：「执行中」卡片标题文字流光 …` → `</style>` 之前
         （含 @keyframes kb-title-shimmer、.kb-card:has(.kb-running) .kb-card-title、
           prefers-reduced-motion 兜底块）
  ② JS ：SHIMMER_SPREAD 常量 + bindShimmer() 函数（至 `  function inject() {` 之前）
  ③ JS ：inject() 里的 `bindShimmer(wrap);` 调用

⚠️ 不动的同名词：压缩 bundle（Tailwind 层）里的 `@keyframes shimmer{…}` / `@keyframes shimmer-mask{…}`
   —— 属 motion-primitives 的其它组件，与标题流光无关；`.kb-running`（状态标签）本身保留。

★★ 本轮踩到的坑（写进 MEMORY）：**新增的注释里不能出现被自检断言的 token**。
   首版我在 JS 注释里写了「SHIMMER_SPREAD / bindShimmer 已移除」，三个残留断言当场失败
   —— 与「禁止全文件关键词总数不变」同类陷阱。注释只用来描述，不要复述被删标识符。

幂等：三处均留 `/* ★ 第 67 轮 */` 注释锚点（调用点用「OLD 不存在 = 已应用」判定）。
"""
import os
import sys

PAGE = 'pages/kanban.html'

MARK_CSS = '/* ★ 第 67 轮：已移除「执行中」卡片标题的文字流光'
MARK_JS = '/* ★ 第 67 轮：标题文字流光的脚本部分已移除'

# ⚠️ 两个 NEW 注释都刻意避开 kb-shimmer / kb-title-shimmer / --kb-shimmer-spread /
#    SHIMMER_SPREAD / bindShimmer 这些会被下方断言扫到的标识符。
CSS_NEW = ('/* ★ 第 67 轮：已移除「执行中」卡片标题的文字流光。\n'
           '         标题恢复为静态色 —— 基础规则已给 color: var(--color-text-1)，无需额外声明。\n'
           '         （.kb-col--doing 常驻 500 / .kb-card:hover 500 两条独立规则不受影响。） */\n'
           '      ')
JS_NEW = ('  /* ★ 第 67 轮：标题文字流光的脚本部分已移除，\n'
          '     标题不再需要按字数写高光带宽变量。 */\n')

applied = []
skipped = []

s = open(PAGE, encoding='utf-8').read()
n0 = len(s)

# ---------------------------------------------------------------- ① CSS 块
if MARK_CSS in s:
    skipped.append(('CSS', '已移除（命中第 67 轮标记）'))
else:
    a = s.find('/* ★ 第 62 轮：「执行中」卡片标题文字流光（Text Shimmer）')
    if a < 0:
        sys.exit('✗ [CSS] 找不到起点锚点')
    b = s.find('</style>', a)
    if b < 0 or (b - a) > 4000:
        sys.exit('✗ [CSS] 结束锚点异常：a=%d b=%d' % (a, b))
    core = s[a:b]
    for need, cnt in (('@keyframes kb-title-shimmer', 1),
                      ('.kb-card:has(.kb-running) .kb-card-title', 2),   # 主规则 + reduced-motion 兜底
                      ('@media (prefers-reduced-motion', 1),
                      ('var(--kb-shimmer-spread)', 2)):                  # calc 里两处
        got = core.count(need)
        if got != cnt:
            sys.exit('✗ [CSS] 待删块内 %r 出现 %d 次（期望 %d）' % (need, got, cnt))
    s = s[:a] + CSS_NEW + s[b:]
    applied.append(('CSS', '删除流光样式块', len(CSS_NEW) - (b - a)))

# ---------------------------------------------------------------- ② JS 常量 + 函数
if MARK_JS in s:
    skipped.append(('JS', '已移除（命中第 67 轮标记）'))
else:
    a = s.find('  /* ★ 第 62 轮：「执行中」卡片标题文字流光（Text Shimmer）\n     —— 复刻')
    if a < 0:
        sys.exit('✗ [JS] 找不到起点锚点')
    b = s.find('\n  function inject() {', a)
    if b < 0:
        sys.exit('✗ [JS] 找不到终点锚点（function inject）')
    core = s[a:b]
    for need in ('var SHIMMER_SPREAD = 2;', 'function bindShimmer(wrap)',
                 "setProperty('--kb-shimmer-spread'"):
        if core.count(need) != 1:
            sys.exit('✗ [JS] 待删块内 %r 出现 %d 次（期望 1）' % (need, core.count(need)))
    if 'function inject' in core:
        sys.exit('✗ [JS] 待删块越界吞进了 inject()')
    s = s[:a] + JS_NEW + s[b:]
    applied.append(('JS', '删除 SHIMMER_SPREAD + bindShimmer', len(JS_NEW) - len(core)))

# ---------------------------------------------------------------- ③ JS 调用点
CALL_OLD = '    bindShimmer(wrap);\n'
if CALL_OLD not in s:
    skipped.append(('JS-CALL', '已移除（OLD 不存在）'))
else:
    if s.count(CALL_OLD) != 1:
        sys.exit('✗ [JS-CALL] %r 出现 %d 次（期望 1）' % (CALL_OLD.strip(), s.count(CALL_OLD)))
    s = s.replace(CALL_OLD, '', 1)
    applied.append(('JS-CALL', '删除 bindShimmer(wrap) 调用', -len(CALL_OLD)))

# ---------------------------------------------------------------- 写回
if applied:
    assert len(s) < n0, '净字节数未减少（%d → %d）' % (n0, len(s))   # ⚠️ 仅在实际应用时断言
    open(PAGE, 'w', encoding='utf-8').write(s)

s2 = open(PAGE, encoding='utf-8').read()
print('=' * 68)
for p, lbl, d in applied:
    print('  应用 [%s] %s  %+d B' % (p, lbl, d))
for p, lbl in skipped:
    print('  跳过 [%s] %s' % (p, lbl))
print('=' * 68)

fail = 0


def chk(desc, got, want):
    global fail
    ok = got == want
    if not ok:
        fail += 1
    print('  %s %-44s = %s（期望 %s）' % ('✓' if ok else '✗', desc, got, want))


print('残留检查（被删对象必须归零）：')
chk('kb-shimmer', s2.count('kb-shimmer'), 0)
chk('kb-title-shimmer', s2.count('kb-title-shimmer'), 0)
chk('--kb-shimmer-spread', s2.count('--kb-shimmer-spread'), 0)
chk('bindShimmer', s2.count('bindShimmer'), 0)
chk('SHIMMER_SPREAD', s2.count('SHIMMER_SPREAD'), 0)
print('必须保留的无关项：')
chk('@keyframes shimmer{（Tailwind 层）', s2.count('@keyframes shimmer{'), 1)
chk('@keyframes shimmer-mask{', s2.count('@keyframes shimmer-mask{'), 1)
chk('@keyframes kb-spin（.kb-running 用）', s2.count('@keyframes kb-spin'), 1)
chk('.kb-col--doing .kb-card-title', s2.count('.kb-col--doing .kb-card-title'), 1)
chk('.kb-card:hover .kb-card-title', s2.count('.kb-card:hover .kb-card-title'), 1)
chk('.kb-running {（状态标签本体）', s2.count('.kb-running {'), 1)
print('标签级计数（改前 vs 改后应为原值）：')
for t in ('<style>', '</style>', '<script>', '</script>'):
    print('    %-12s = %d' % (t, s2.count(t)))
print('自检：')
chk('净字节未增加（改前=%d 改后=%d）' % (n0, len(s2)), len(s2) <= n0, True)
print('=' * 68)
print('总字节 %d → %d（%+d）' % (n0, len(s2), len(s2) - n0))
print('ALL PASS' if fail == 0 else 'FAILED: %d 项' % fail)
sys.exit(0 if fail == 0 else 1)
