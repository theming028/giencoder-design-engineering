# -*- coding: utf-8 -*-
"""r52 补丁：task-detail.html 五项
1) td-ai-meta 对齐设计稿节点 836:27829（组 10471）：单条「任务完成，耗时28m12s ⌄」+ 发丝线 + 「上下文注入」
2) AI 对话框横向压缩时，大模型选择器文字自动省略，不再把工具条顶出框外
3) td-left / td-right / td-browse 面板：投影 → 1px #DAE3ED 描边
4) td-browse-add / td-browse-ico 容器 32 → 28px（图标保持 16px ★r52b 修正：设计稿实测加号墨迹 10.7 逻辑px，Lucide plus ink 占 16/24 ⇒ 图标盒 16px；用户原话只要求「容器 28px」）
5) td-right-acts 内图标本体 16 → 14px
幂等：脚本可重复执行；已应用则跳过。
"""
import io
import os
import re
import sys

P = 'pages/task-detail.html'
BLOB = ('/Users/shaoyuming/.mgmcp/artifacts/blobs/sha256/6e/'
        '6eedce6629c090ae071d8c580690b5a02c5510b029dc427d80154a5acf7e710c')

s = io.open(P, encoding='utf-8').read()
before = s
applied, skipped = [], []


def grab_ctx_path():
    """从设计稿 blob 里取「上下文注入」图标（节点 836:27785）的 path data。"""
    svg = io.open(BLOB, encoding='utf-8').read()
    m = re.search(r'<path d="([^"]+)"', svg)
    if not m:
        sys.exit('!! 未能从 blob 解析上下文图标 path')
    d = m.group(1)
    assert 'master_svg0' not in d
    return d


CTX_D = grab_ctx_path()

# ---------------------------------------------------------------- 替换对
# 1) AI 消息头元信息区 HTML（JS 字符串数组，属性引号是 \" ）
OLD_META_HTML = (
    r'<div class=\"td-ai-meta\">",' + '\n'
    r'        "              <a href=\"#\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" '
    r'stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\">'
    r'<path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/>'
    r'<path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg>思考过程</a>",' + '\n'
    r'        "              <span class=\"td-sep\"></span>",' + '\n'
    r'        "              <a href=\"#\">任务完成，耗时 28m12s</a>",' + '\n'
    r'        "            </div>",'
)

NEW_META_HTML = (
    r'<div class=\"td-ai-meta\">",' + '\n'
    r'        "              <a href=\"#\">任务完成，耗时28m12s'
    r'<svg viewBox=\"0 0 14 14\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" '
    r'stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\">'
    r'<path d=\"M3.4 5.2L7 9l3.6-3.8\"/></svg></a>",' + '\n'
    r'        "            </div>",' + '\n'
    r'        "            <span class=\"td-ai-rule\" aria-hidden=\"true\"></span>",' + '\n'
    r'        "            <a class=\"td-ai-ctx\" href=\"#\">'
    r'<svg viewBox=\"0 0 14 14\" width=\"14\" height=\"14\" fill=\"currentColor\" fill-rule=\"evenodd\" '
    r'aria-hidden=\"true\"><path d=\"' + CTX_D + r'\"/></svg>上下文注入</a>",'
)

# 2) 元信息区 CSS
OLD_META_CSS = (
    '.td-ai-meta { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); '
    'color: var(--td-meta); }\n'
    '      .td-ai-meta a { display: inline-flex; align-items: center; gap: 4px; color: var(--td-meta); '
    'text-decoration: none; }\n'
    '      .td-ai-meta a:hover { color: var(--color-primary-6); }\n'
    '      .td-ai-meta svg { width: 14px; height: 14px; flex: none; }'
)
NEW_META_CSS = (
    '/* ★ 第 52 轮第 1 项：按设计稿节点 836:27829（组 10471）重写 AI 消息头元信息区。\n'
    '         设计稿实测：只有一条「任务完成，耗时28m12s」链接（14px 文字，文字后 gap 2px 接 14px 下箭头，\n'
    '         整体 164×22，色 #868686 = --td-meta）；其下 12px 一条 520 全长的 #F2F2F2 发丝线；\n'
    '         再 12px 是「上下文注入」链接（同 #868686 色 + 14px 图标，88×22，gap 4px）。\n'
    '         原实现把「思考过程」链接错放在这一行（且带竖分隔线），与设计稿不符，本轮一并纠正。 */\n'
    '      .td-ai-meta { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); '
    'color: var(--td-meta); margin-top: 8px; }\n'
    '      .td-ai-meta a { display: inline-flex; align-items: center; gap: 2px; color: var(--td-meta); '
    'text-decoration: none; line-height: 22px; }\n'
    '      .td-ai-meta a:hover { color: var(--color-primary-6); }\n'
    '      .td-ai-meta svg { width: 14px; height: 14px; flex: none; }\n'
    '      .td-ai-rule { flex: none; height: 1px; background: var(--color-border-1); margin: 4px 0; }\n'
    '      .td-ai-ctx {\n'
    '        display: inline-flex; align-items: center; gap: 4px; align-self: flex-start;\n'
    '        height: 22px; margin-bottom: 4px;\n'
    '        font-size: var(--font-size-body-3); line-height: 22px; color: var(--td-meta); text-decoration: none;\n'
    '      }\n'
    '      .td-ai-ctx svg { width: 14px; height: 14px; flex: none; }\n'
    '      .td-ai-ctx:hover, .td-ai-ctx:focus-visible { color: var(--color-primary-6); }'
)

# 3) 面板描边 token
OLD_TOKEN = '        --td-panel-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);'
NEW_TOKEN = (
    '        --td-panel-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);\n'
    '        /* ★ 第 52 轮第 3 项：面板描边色。设计稿根帧 836:26404 实测：白面板四周有一圈 1px 线，\n'
    '           在 #E5EDF5 底上按 0.5x 合成读数 #DFE8F1 ⇒ 反解原色 (223.5,232,241)*2-(229,237,245)\n'
    '           = #DAE3ED。DS 无常量，故沿用本页既有惯例（--td-crumb-line）落成本页 token。 */\n'
    '        --td-panel-line: #DAE3ED;'
)

# 4) 左栏
OLD_LEFT = (
    '      .td-left {\n'
    '        flex: 1 1 auto; min-width: var(--td-left-min); box-sizing: border-box;\n'
    '        display: flex; flex-direction: column; overflow: hidden;\n'
    '        background: var(--color-bg-1); border-radius: 8px;\n'
    '        box-shadow: var(--td-panel-shadow);\n'
    '      }'
)
NEW_LEFT = (
    '      .td-left {\n'
    '        flex: 1 1 auto; min-width: var(--td-left-min); box-sizing: border-box;\n'
    '        display: flex; flex-direction: column; overflow: hidden;\n'
    '        background: var(--color-bg-1); border-radius: 8px;\n'
    '        /* ★ 第 52 轮第 3 项：设计稿容器边缘是 1px #DAE3ED 描边，不是投影 */\n'
    '        border: 1px solid var(--td-panel-line);\n'
    '      }'
)

# 5) 右栏
OLD_RIGHT = ('        box-shadow: var(--td-panel-shadow);   '
             '/* 同左栏：设计稿无描边，只有柔和投影 */')
NEW_RIGHT = ('        /* ★ 第 52 轮第 3 项：同左栏 —— 投影改为 1px #DAE3ED 描边 */\n'
             '        border: 1px solid var(--td-panel-line);')

# 6) 文件预览栏
OLD_BROWSE = ('        background: var(--color-bg-1); border-left: 1px solid var(--color-border-2);\n'
              '        border-radius: 0 8px 8px 0;')
NEW_BROWSE = ('        background: var(--color-bg-1);\n'
              '        /* ★ 第 52 轮第 3 项：外缘 1px #DAE3ED；左边线与 AI 会话栏接缝另取档（第 50 轮第 4 项） */\n'
              '        border: 1px solid var(--td-panel-line);\n'
              '        border-left: 1px solid var(--color-border-2);\n'
              '        border-radius: 0 8px 8px 0;')

# 7) 浏览态右栏右缘
OLD_BR_RIGHT = ('      .td-root.is-browse .td-right { border-top-right-radius: 0; border-bottom-right-radius: 0; }')
NEW_BR_RIGHT = ('      .td-root.is-browse .td-right {\n'
                '        border-top-right-radius: 0; border-bottom-right-radius: 0;\n'
                '        /* ★ 第 52 轮第 3 项：右缘交给 .td-browse 的左边线，避免接缝变 2px */\n'
                '        border-right: 0;\n'
                '      }')

# 8) 浏览栏按钮尺寸
OLD_BARBTN = ('      .td-browse-bar .td-browse-add,\n'
              '      .td-browse-bar .td-browse-ico { width: 32px; height: 32px; }\n'
              '      .td-browse-bar .td-browse-add svg,\n'
              '      .td-browse-bar .td-browse-ico svg { width: 16px; height: 16px; }')
NEW_BARBTN = ('      .td-browse-bar .td-browse-add,\n'
              '      .td-browse-bar .td-browse-ico { width: 28px; height: 28px; }\n'
              '      .td-browse-bar .td-browse-add svg,\n'
              '      .td-browse-bar .td-browse-ico svg { width: 16px; height: 16px; }')

# 9) AI 标题栏图标本体
OLD_ROUND = ('      .td-round-btn,\n'
             '      .td-round-btn:hover,\n'
             '      .td-round-btn:active {\n'
             '        box-sizing: border-box; width: 28px; height: 28px; padding: 0;\n'
             '        border-color: transparent; box-shadow: none; line-height: 0;\n'
             '      }')
NEW_ROUND = OLD_ROUND + (
    '\n      /* ★ 第 52 轮第 5 项：标题栏图标本体 16 → 14px（设计稿 icon-wrapper 尺寸=14）。\n'
    '         按钮盒仍是 28×28（第 51 轮第 2 项）。 */\n'
    '      .td-right-acts .td-round-btn svg { width: 14px; height: 14px; }')

# 10) 对话框横向收缩链
OLD_COMPOSER = '      .td-composer { flex: none; margin: 8px 20px 20px; }'
NEW_COMPOSER = (
    '      .td-composer { flex: none; margin: 8px 20px 20px; }\n'
    '      /* ★ 第 52 轮第 2 项：AI 对话框横向空间不足时，大模型选择器文字自动截断省略。\n'
    '         病因：模型选择器带内联 `flex-shrink: 0`，DS 的\n'
    '         `.giencoder-select-view-text{overflow:hidden;text-overflow:ellipsis;flex:1}` 永远触发不到 ——\n'
    '         实测 --td-right-w ≤ 400px（对话框内容盒 360）时整条工具条就被顶出对话框框外。\n'
    '         修法：放开整条收缩链（select → selection → view-text 逐级 min-width:0），\n'
    '         并让图标按钮不参与收缩（保持 32px 正圆，只会让选择器文字先让位）。 */\n'
    '      .td-composer .mt-auto,\n'
    '      .td-composer .mt-auto > .flex,\n'
    '      .td-composer .mt-auto .flex.items-center.gap-2 { min-width: 0; }\n'
    '      .td-composer .giencoder-select { min-width: 0 !important; flex-shrink: 1 !important; }\n'
    '      .td-composer .giencoder-select-view { min-width: 0; }\n'
    '      .td-composer .giencoder-select-selection { min-width: 0; overflow: hidden; }\n'
    '      .td-composer .giencoder-select-view-text { min-width: 0; }\n'
    '      .td-composer .mt-auto button { flex: none; }')

# 11) 模型选择器弹层右对齐（独立成对：NEW_COMPOSER 已写盘，不能挂靠第 10 项）
OLD_POPUP = '      .td-composer .mt-auto button { flex: none; }'
NEW_POPUP = (
    '      .td-composer .mt-auto button { flex: none; }\n'
    '      /* 配套：大模型选择器贴在对话框右缘，弹层改为**右对齐、向内展开** ——\n'
    '         否则打开时弹层右缘会伸出对话框白框（实测 320px 宽时超出 28px）。 */\n'
    '      .td-composer .mt-auto .flex.items-center.gap-2 > .giencoder-select > .giencoder-select-popup '
    '{ left: auto; right: 0; }')

PAIRS = [
    ('1 元信息区 HTML', OLD_META_HTML, NEW_META_HTML, r'class=\\"td-ai-ctx\\"'),
    ('2 元信息区 CSS', OLD_META_CSS, NEW_META_CSS, r'\.td-ai-rule \{ flex: none'),
    ('3 面板描边 token', OLD_TOKEN, NEW_TOKEN, r'--td-panel-line: #DAE3ED;'),
    ('4 左栏描边', OLD_LEFT, NEW_LEFT,
     r'min-width: var\(--td-left-min\)[\s\S]*?border: 1px solid var\(--td-panel-line\);'),
    ('5 右栏描边', OLD_RIGHT, NEW_RIGHT, r'同左栏 —— 投影改为 1px #DAE3ED 描边'),
    ('6 预览栏描边', OLD_BROWSE, NEW_BROWSE, r'外缘 1px #DAE3ED；左边线与 AI 会话栏接缝'),
    ('7 浏览态右缘', OLD_BR_RIGHT, NEW_BR_RIGHT, r'右缘交给 \.td-browse 的左边线'),
    ('8 浏览栏按钮 28px', OLD_BARBTN, NEW_BARBTN, r'\.td-browse-ico \{ width: 28px; height: 28px; \}'),
    ('9 标题栏图标 14px', OLD_ROUND, NEW_ROUND,
     r'\.td-right-acts \.td-round-btn svg \{ width: 14px; height: 14px; \}'),
    ('10 对话框收缩链', OLD_COMPOSER, NEW_COMPOSER, r'\.td-composer \.mt-auto button \{ flex: none; \}'),
    ('11 弹层右对齐', OLD_POPUP, NEW_POPUP, r'\.giencoder-select > \.giencoder-select-popup'),
]

# ⚠️ 幂等性坑：第 3/9/10 项的 NEW 串是 OLD 串的**超集**（OLD 是 NEW 的前缀），
#    若先判 count(OLD) 会永远命中、重复追加。故**先判 NEW 标记**，再判 OLD。
for label, old, new, newmark in PAIRS:
    if re.search(newmark, s):
        skipped.append(label)
    elif s.count(old) == 1:
        s = s.replace(old, new, 1)
        applied.append(label)
    else:
        sys.exit('!! 【%s】锚点匹配数 = %d（应为 1，且 NEW 标记也不存在）' % (label, s.count(old)))

if s != before:
    io.open(P, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- 自检
def cnt(k):
    return s.count(k)


CHECKS = [
    # 标签级计数（必须与改前一致）
    ('<style> 仍 2', cnt('<style>'), 2),
    ('</style> 仍 3', cnt('</style>'), 3),
    ('<script> 仍 8', cnt('<script>'), 8),
    ('</script> 仍 8', cnt('</script>'), 8),
    # 1) 元信息区：精确增减（按 HTML 专属串判定，避免注释里的同名文字干扰）
    ('思考过程链接 1→0', cnt('思考过程</a>'), 0),
    ('上下文注入链接 0→1', cnt('上下文注入</a>'), 1),
    ('「耗时 28」带空格 1→0', cnt('任务完成，耗时 28m12s'), 0),
    ('「耗时28」无空格 0→1', cnt('>任务完成，耗时28m12s<'), 1),
    ('td-ai-meta 容器仍 1', cnt(r'class=\"td-ai-meta\"'), 1),
    ('td-ai-head 容器仍 1', cnt(r'class=\"td-ai-head\"'), 1),
    ('元信息行里的旧竖线 1→0', cnt(r'\"td-ai-meta\">",\n        \"              <span class=\\\"td-sep\\\">'), 0),
    ('td-ai-ctx 5 处(CSS4+HTML1)', cnt('td-ai-ctx'), 5),
    ('td-ai-rule 2 处(CSS1+HTML1)', cnt('td-ai-rule'), 2),
    # 2) 收缩链（CSS 4 条新规则 + 既有 3 处引用 = 7）
    ('composer 收缩链 7 处', cnt('.td-composer .giencoder-select'), 7),
    # 3) 面板描边
    ('--td-panel-line 4 处(定义1+用法3)', cnt('--td-panel-line'), 4),
    ('panel-shadow 用法 5→3', cnt('box-shadow: var(--td-panel-shadow)'), 3),
    ('#DAE3ED 10 处(定义1+用法3+注释6)', cnt('#DAE3ED'), 10),
    # 4) 浏览栏按钮
    ('.td-browse-ico 32px 1→0', cnt('.td-browse-bar .td-browse-ico { width: 32px; height: 32px; }'), 0),
    ('.td-browse-ico 28px 0→1', cnt('.td-browse-bar .td-browse-ico { width: 28px; height: 28px; }'), 1),
    ('浏览栏 svg 16px 保持 1', cnt('.td-browse-bar .td-browse-ico svg { width: 16px; height: 16px; }'), 1),
    # 5) 标题栏图标
    ('td-right-acts svg 规则 0→1', cnt('.td-right-acts .td-round-btn svg { width: 14px; height: 14px; }'), 1),
    ('td-round-btn 28px 仍 1', cnt('box-sizing: border-box; width: 28px; height: 28px; padding: 0;'), 1),
    # 其余不得受伤
    ('td-browse 树行仍 10', cnt(r'class=\"td-bf is-dir'), 10),
    ('data-td-split 仍 5', cnt('data-td-split'), 5),
    ('context 图标 path 入页', cnt(CTX_D[:48]), 1),
]

bad = 0
print('=== r52 自检 ===')
for label, got, want in CHECKS:
    ok = (got == want)
    if not ok:
        bad += 1
    print(('  OK  ' if ok else '  !!  ') + '%-38s %s/%s' % (label, got, want))

print('\n应用: %d 项 | 跳过(已应用): %d 项' % (len(applied), len(skipped)))
if skipped:
    print('   跳过:', '、'.join(skipped))
if bad:
    sys.exit('!! 自检失败 %d 条（文件已写盘，请检查上面的 !! 行）' % bad)
print('✅ 全部自检通过，文件大小 %d 字节' % len(s))
