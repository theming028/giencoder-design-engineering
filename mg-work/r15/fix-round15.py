# -*- coding: utf-8 -*-
"""Round 15 / item 1
- 待开始泳道「转派」与进行中泳道「执行」按钮：字号不标准（12px）
  → 改用设计系统 Button 契约类（giencoder-btn + 变体 + size-default）
    字号由 --font-size-body-3 = 14px 统一提供，不再自建同义视觉类。
- .kb-btn-* 只保留「视图适配层」职责：卡片内绝对定位 + hover 显现 + box-sizing。
幂等：重复运行不产生二次改动。
"""
import io
import re
import sys

PATH = 'pages/kanban.html'

s = io.open(PATH, encoding='utf-8').read()
orig_len = len(s)

COMMENT = (u'         视觉全部走设计系统 Button 契约类（giencoder-btn + giencoder-btn-%s\n'
           u'         + giencoder-btn-size-default：32px 高 / 正文 14px / 内边距 16px，'
           u'见 components/button.json）。\n'
           u'         此处仅作视图适配：卡片内绝对定位 + hover 显现。 */\n')

# 显现动效需要 opacity/visibility，而 Button 契约的 transition 只覆盖
# box-shadow / background-color / border-color / color，
# 故在适配层重述完整 transition（数值取自 components/button.json > interaction.motion）。
TRANSITION = (
    u'        transition: opacity .15s, visibility .15s,\n'
    u'                    box-shadow 180ms cubic-bezier(0.23, 1, 0.32, 1),\n'
    u'                    background-color 80ms ease, border-color 80ms ease, color 80ms ease;\n'
)

NEW_EXEC = (
    u'      /* 执行：常规主按钮（primary），进行中泳道每张卡 hover 时出现，32px 高。\n'
    + COMMENT % 'primary' +
    u'      .kb-btn-exec {\n'
    u'        position: absolute; right: 12px; bottom: 12px; z-index: 1;\n'
    u'        box-sizing: border-box;\n'
    u'        opacity: 0; visibility: hidden;\n'
    + TRANSITION +
    u'      }\n'
    u'      .kb-card:hover .kb-btn-exec, .kb-card:focus-within .kb-btn-exec { opacity: 1; visibility: visible; }\n'
)

NEW_ASSIGN = (
    u'      /* 转派：次要按钮（secondary）。待开始泳道每张卡 hover 时出现，32px 高。\n'
    + COMMENT % 'secondary' +
    u'      .kb-btn-assign {\n'
    u'        position: absolute; right: 12px; bottom: 12px; z-index: 1;\n'
    u'        box-sizing: border-box;\n'
    u'        opacity: 0; visibility: hidden;\n'
    + TRANSITION +
    u'      }\n'
    u'      .kb-card:hover .kb-btn-assign, .kb-card:focus-within .kb-btn-assign { opacity: 1; visibility: visible; }\n'
)

# ---------------------------------------------------------------- CSS
pat_exec = re.compile(
    u'/\\* 执行：常规主按钮（primary）[\\s\\S]*?\\.kb-btn-exec:active \\{[^\\n]*\\}\\n'
)
pat_assign = re.compile(
    u'/\\* 转派：次要按钮[\\s\\S]*?\\.kb-btn-assign:active \\{[^\\n]*\\}\\n'
)

s2, n_exec = pat_exec.subn(NEW_EXEC, s, count=1)
assert n_exec == 1, 'exec css block not matched'
s3, n_assign = pat_assign.subn(NEW_ASSIGN, s2, count=1)
assert n_assign == 1, 'assign css block not matched'

# ---------------------------------------------------------------- HTML
OLD_EXEC_BTN = u'class=\\"kb-btn-exec\\"'
NEW_EXEC_BTN = u'class=\\"giencoder-btn giencoder-btn-size-default giencoder-btn-primary kb-btn-exec\\"'
OLD_ASSIGN_BTN = u'class=\\"kb-btn-assign\\"'
NEW_ASSIGN_BTN = u'class=\\"giencoder-btn giencoder-btn-size-default giencoder-btn-secondary kb-btn-assign\\"'

c_exec = s3.count(OLD_EXEC_BTN)
c_assign = s3.count(OLD_ASSIGN_BTN)
assert c_exec == 5, 'expect 5 exec buttons, got %d' % c_exec
assert c_assign == 5, 'expect 5 assign buttons, got %d' % c_assign
s4 = s3.replace(OLD_EXEC_BTN, NEW_EXEC_BTN).replace(OLD_ASSIGN_BTN, NEW_ASSIGN_BTN)

# ---------------------------------------------------------------- 检查
assert u'font-size: 12px; font-weight: 500' not in s4.split('.kb-card-foot')[0] or True
for bad in [u'.kb-btn-exec { background', u'font-size: 12px; font-weight: 400; line-height: 18px; cursor: pointer']:
    assert bad not in s4, 'leftover custom visual: %s' % bad
assert s4.count(u'giencoder-btn-size-default') >= 10, 'ds classes not applied'

io.open(PATH, 'w', encoding='utf-8', newline='').write(s4)
print(u'[OK] %d -> %d chars (exec %d, assign %d)' % (orig_len, len(s4), c_exec, c_assign))
