# -*- coding: utf-8 -*-
"""r17：创建任务弹窗 (kb-crt) 5 项调整。

1) footer 按钮垂直居中：.kb-crt-foot 高度 56，flex 默认 align-items:stretch/start，
   按钮会贴顶 → 补 align-items:center。
2) 任务类型宽度自适应：.kb-crt-type 由固定 168px 改为 max-content（min 168 / max 360）。
3) aside 五个字段（状态/优先级/关联需求/前置任务/责任人）的 label 由「内嵌在
   .giencoder-select-view 内」改为「与 .kb-crt-row 同级、排在控件之前」，
   与「预期完成」的左右排列一致。
4) .kb-crt-editor-body 内改为真正的 <textarea> 多行文本框。
5) 弹窗宽高与展开动效对齐「待协作任务」弹窗 (.kb-coop)：80% 宽、top:0 贴 main 顶、
   bottom:48px 纵向拉伸、顶角直角 0 0 12px 12px、基准点 top center + translateX(-50%)。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, 'pages', 'kanban.html')
s = open(P, 'rb').read().decode('utf-8')
before = len(s)


def sub(old, new, why, expect=1):
    global s
    n = s.count(old)
    if n != expect:
        print('[ABORT] 命中 %d 次（应为 %d）：%s' % (n, expect, why))
        sys.exit(1)
    s = s.replace(old, new)
    print('  [OK] %s' % why)


print('### 1. footer 按钮垂直居中')
sub(
    ".kb-crt-foot { height: 56px; flex: none; padding: 0 24px; border-top-color: var(--kb-crt-divider); }",
    ".kb-crt-foot { height: 56px; flex: none; padding: 0 24px; border-top-color: var(--kb-crt-divider); align-items: center; }",
    'kb-crt-foot 补 align-items:center',
)

print('### 2. 任务类型宽度自适应')
sub(
    ".kb-crt-type { width: 168px; flex: none; }",
    ".kb-crt-type { width: max-content; min-width: 168px; max-width: 360px; flex: none; }",
    'kb-crt-type 168px -> max-content(min168/max360)',
)

print('### 3. aside 五个字段的 label 移到 row 层级（左右排列）')
pat = re.compile(
    r'<div class=\\"kb-crt-row\\">'
    r'<div class=\\"(giencoder-select kb-crt-fld[a-z0-9 -]*)\\"[^>]*>'
    r'<div class=\\"giencoder-select-view\\"([^>]*)>'
    r'<span class=\\"kb-crt-lbl\\">([^<]+)</span>'
)
new_s, cnt = pat.subn(
    r'<div class=\\"kb-crt-row\\"><span class=\\"kb-crt-lbl\\">\3</span>'
    r'<div class=\\"\1\\"><div class=\\"giencoder-select-view\\"\2>',
    s,
)
if cnt != 5:
    print('[ABORT] label 搬移命中 %d 处（应为 5：状态/优先级/关联需求/前置任务/责任人）' % cnt)
    sys.exit(1)
s = new_s
print('  [OK] 5 个字段的 label 已移到 .kb-crt-row 内、控件之前（与「预期完成」一致）')
# 自检：row 内不应再残留内嵌 label
left = re.findall(r'kb-crt-row\\"><div class=\\"giencoder-select[^>]*><div class=\\"giencoder-select-view\\"[^>]*><span class=\\"kb-crt-lbl\\"', s)
print('  [check] 仍内嵌 label 的 row 数：%d（应为 0）' % len(left))

print('### 4. 编辑器正文改为 <textarea>')
sub(
    '.kb-crt-editor-ph { display: flex; flex-direction: column; font-size: var(--font-size-body-3); line-height: 24px; color: rgb(var(--gray-5)); }',
    '.kb-crt-textarea {\n'
    '        display: block; width: 100%; height: 100%; box-sizing: border-box;\n'
    '        margin: 0; padding: 0; border: none; outline: none; resize: none;\n'
    '        background: transparent; overflow: auto;\n'
    '        font-family: var(--font-family); font-size: var(--font-size-body-3);\n'
    '        line-height: 24px; color: var(--color-text-1);\n'
    '      }\n'
    '      .kb-crt-textarea::placeholder { color: rgb(var(--gray-5)); }',
    'CSS：.kb-crt-editor-ph -> .kb-crt-textarea',
)
sub(
    '.kb-crt-editor-body { flex: 1; min-height: 0; padding: 16px; overflow: auto; }',
    '.kb-crt-editor-body { flex: 1; min-height: 0; padding: 16px; overflow: hidden; }',
    'CSS：editor-body 外层改 overflow:hidden（滚动交给 textarea 自己）',
)
sub(
    r'''"            <div class=\"kb-crt-editor-ph\"><span>你可以通过用户故事的形式描述任务。</span><span>基本格式：作为某个角色，我需要做某些事情，以便实现什么目标。</span></div>",''',
    r'''"            <textarea class=\"kb-crt-textarea\" aria-label=\"任务描述\" placeholder=\"你可以通过用户故事的形式描述任务。&#10;基本格式：作为某个角色，我需要做某些事情，以便实现什么目标。\"></textarea>",''',
    'HTML：editor-body 内容改为 textarea（两行占位用 &#10;）',
)

print('### 5. 宽高与展开动效对齐 kb-coop')
sub(
    """        --kb-crt-mask: rgba(0, 0, 0, 0.32);   /* 遮罩：svg_8e860390（#000 32% + backdrop blur 5px） */
        position: absolute; inset: 0; z-index: 60;
        display: flex; align-items: center; justify-content: center;
      }""",
    """        --kb-crt-mask: rgba(0, 0, 0, 0.32);   /* 遮罩：svg_8e860390（#000 32% + backdrop blur 5px） */
        /* r17：宽高与展开动效对齐「待协作任务」弹窗 .kb-coop（同 80% / 底距 48px） */
        --kb-crt-width: 80%;
        --kb-crt-gap-bottom: 48px;
        position: absolute; inset: 0; z-index: 60;
      }""",
    'CSS：.kb-crt 加 --kb-crt-width/--kb-crt-gap-bottom，去掉 flex 居中',
)
sub(
    """      .kb-crt-dialog {
        position: relative; z-index: 1;
        width: min(1280px, calc(100% - 64px)); height: min(820px, calc(100% - 24px));
        display: flex; flex-direction: column;
        background: var(--color-bg-1); border-radius: var(--border-radius-xl);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
        opacity: 0; transform-origin: top center;
        transform: translateY(-12px) scaleY(0.97);
        transition: opacity 130ms var(--transition-timing-function-standard),
                    transform 160ms var(--transition-timing-function-standard);
        will-change: transform, opacity;
      }
      .kb-crt.is-open .kb-crt-dialog { opacity: 1; transform: translateY(0) scaleY(1); }""",
    """      .kb-crt-dialog {
        position: absolute; left: 50%; top: 0; bottom: var(--kb-crt-gap-bottom);
        width: var(--kb-crt-width);
        height: auto; max-height: none; z-index: 1;
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--color-bg-1); border-radius: 0 0 12px 12px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
        opacity: 0; transform-origin: top center;
        transform: translateX(-50%) translateY(-12px) scaleY(0.97);
        transition: opacity 130ms var(--transition-timing-function-standard),
                    transform 160ms var(--transition-timing-function-standard);
        will-change: transform, opacity;
      }
      .kb-crt.is-open .kb-crt-dialog { opacity: 1; transform: translateX(-50%) translateY(0) scaleY(1); }""",
    'CSS：.kb-crt-dialog 改 80% 宽 + 顶部吸附 + 顶角直角 + translateX(-50%) 动效',
)

open(P, 'wb').write(s.encode('utf-8'))
print('\n%s  %d -> %d chars' % (os.path.basename(P), before, len(s)))
