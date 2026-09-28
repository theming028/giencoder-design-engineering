# -*- coding: utf-8 -*-
"""第 51 轮（r51）task-detail.html 补丁：7 项
1) .td-ai-foot 图标与文字 → 12px
2) .td-right-acts 内图标按钮 → 28×28
3) .td-browse-tab 左侧图标按设计稿还原（文档 + 右下角圆形徽标）
4) .td-browse 的 box-shadow 去掉
5) 顶栏 .td-browse-add / 收起侧栏 按钮 24 → 32（加大两号），图标 14 → 16
6) .td-right-acts 内按钮去掉投影；.td-round-btn → 28px
7) .td-browse-files 的 item hover 指针 → pointer

幂等：每个替换先判「新串是否已存在」，已存在则跳过。
自检只允许：① 标签级计数不变 ② 针对被改对象的精确增减量。
"""
import io, sys, shutil, os

P = 'pages/task-detail.html'
BK = '/tmp/r51-backup/task-detail.html'

if not os.path.exists(BK):
    os.makedirs('/tmp/r51-backup', exist_ok=True)
    shutil.copy(P, BK)
    print('已备份 ->', BK)

s = io.open(P, encoding='utf-8').read()
n0 = len(s)
log = []


def rep(old, new, tag, expect_count=1):
    """替换：old 出现 expect_count 次；若 new 已存在则视为已完成。"""
    global s
    if new in s and old not in s:
        log.append(f'  = {tag}（已是目标态，跳过）')
        return
    c = s.count(old)
    if c != expect_count:
        raise SystemExit(f'!! {tag}: 锚点命中 {c} 次，期望 {expect_count} 次 -> 中止')
    s = s.replace(old, new, expect_count)
    log.append(f'  + {tag}（替换 {expect_count} 处）')


# ---------------------------------------------------------------- 1) ai-foot 12px
rep(
    '.td-ai-foot { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta); }',
    '/* ★ 第 51 轮第 1 项：底行「输出完成 / Token 速率」图标与文字统一 12px\n'
    '         （--font-size-body-1 = 12px；图标本就 12px，只调字号）。 */\n'
    '      .td-ai-foot { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-1); color: var(--td-meta); }',
    '① .td-ai-foot 字号 → 12px')

# ------------------------------------------------- 2)+6) round-btn 28px + 去投影
rep(
    '.td-round-btn { box-sizing: border-box; width: 32px; padding: 0; border-color: transparent; line-height: 0; }',
    '/* ★ 第 51 轮第 2/6 项：标题栏图标按钮 32×32 → 28×28；\n'
    '         并去掉 DS .giencoder-btn-secondary 自带的投影（0 1px 2px #0f172a0a）——\n'
    '         图标按钮不需要浮起感。:hover/:active 一并覆盖（特指度 ≥ 基础规则，且本页样式表\n'
    '         位于 DS 组件 CSS 之后，同权重后者胜）；\n'
    '         但**保留** :focus-visible 的键盘焦点环（a11y，不在此列）。 */\n'
    '      .td-round-btn,\n'
    '      .td-round-btn:hover,\n'
    '      .td-round-btn:active {\n'
    '        box-sizing: border-box; width: 28px; height: 28px; padding: 0;\n'
    '        border-color: transparent; box-shadow: none; line-height: 0;\n'
    '      }',
    '②⑥ .td-round-btn → 28×28 且 shadow:none')

# ------------------------------------------------------- 4) .td-browse 去投影
rep(
    'border-radius: 0 8px 8px 0; box-shadow: var(--td-panel-shadow);',
    'border-radius: 0 8px 8px 0;\n        /* ★ 第 51 轮第 4 项：去掉浮起投影（--td-panel-shadow）——\n'
    '           文件预览栏与 AI 会话栏是同一块面板的两栏，不应有层级感。 */',
    '④ .td-browse 去掉 box-shadow')

# --------------------------------------------------- 5) 顶栏按钮 24 → 32 + 图标 16
rep(
    '      .td-browse-add, .td-browse-ico {\n'
    '        display: inline-flex; align-items: center; justify-content: center; flex: none;\n'
    '        width: 24px; height: 24px; padding: 0; border: 0; border-radius: 4px;\n'
    '        background: transparent; color: var(--color-text-2); cursor: pointer;\n'
    '      }',
    '      .td-browse-add, .td-browse-ico {\n'
    '        display: inline-flex; align-items: center; justify-content: center; flex: none;\n'
    '        width: 24px; height: 24px; padding: 0; border: 0; border-radius: 4px;\n'
    '        background: transparent; color: var(--color-text-2); cursor: pointer;\n'
    '      }\n'
    '      /* ★ 第 51 轮第 5 项：顶栏「新建标签(+)」与「收起侧栏(X)」加大两号 —— 24 → 32，\n'
    '         恰等于 .td-browse-bar 的内容盒高（40 − 4×2）；图标同步 14 → 16\n'
    '         （设计稿实测加号/叉号墨迹 10.7 逻辑 px，对应 16 viewBox-盒）。\n'
    '         ⚠ 必须限定在 .td-browse-bar 内：.td-browse-ico 同时被 crumb 的两个按钮复用\n'
    '         （那里是 16px 图标 + 24px 盒），不能连带放大。 */\n'
    '      .td-browse-bar .td-browse-add,\n'
    '      .td-browse-bar .td-browse-ico { width: 32px; height: 32px; }\n'
    '      .td-browse-bar .td-browse-add svg,\n'
    '      .td-browse-bar .td-browse-ico svg { width: 16px; height: 16px; }',
    '⑤ 顶栏 +/X 按钮 → 32×32，图标 16px')

# ----------------------------------------------------------- 7) tree item pointer
rep(
    'white-space: nowrap; overflow: hidden; cursor: default;',
    'white-space: nowrap; overflow: hidden; cursor: pointer;',
    '⑦ .td-bf hover 指针 → pointer')

# ------------------------------------------------------------ 3) tab 图标颜色
rep(
    '.td-browse-tab svg { color: var(--color-text-2); }',
    '/* ★ 第 51 轮第 3 项：设计稿实测该图标墨迹核心 RGB(31,31,31) = --color-text-1，\n'
    '         比原 text-2(#4E4E4E) 深一档（同行「摘要」文字亦为 text-1）。 */\n'
    '      .td-browse-tab svg { color: var(--color-text-1); }',
    '③ tab 图标色 → text-1')

# ------------------------------------------------ 3) tab 图标本体（HTML，JS 串内）
OLD_ICON = ('<span class=\\"td-browse-tab\\">'
            '<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"14\\" height=\\"14\\" '
            'fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" '
            'stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">'
            '<path d=\\"M3 5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z\\"/>'
            '<path d=\\"M15 3v18\\"/></svg>摘要</span>')
NEW_ICON = ('<span class=\\"td-browse-tab\\">'
            '<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"16\\" height=\\"16\\" '
            'fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" '
            'stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">'
            '<path d=\\"M4 2h11.5a3.5 3.5 0 0 1 3.5 3.5v15a1.5 1.5 0 0 1-1.5 1.5H4a1.5 1.5 0 0 1-1.5-1.5v-17A1.5 1.5 0 0 1 4 2Z\\"/>'
            '<path d=\\"M7.5 9.5h6.5\\"/>'
            '<path d=\\"M6.5 13h3.5\\"/>'
            '<path d=\\"M7 16.5h3.5\\"/>'
            '<circle cx=\\"15.5\\" cy=\\"18\\" r=\\"4\\" style=\\"fill:var(--color-bg-1)\\"/>'
            '</svg>摘要</span>')
rep(OLD_ICON, NEW_ICON, '③ tab 图标 → 文档+圆形徽标（16px）')

# --------------------------------------------- 5) 顶栏两个按钮的 svg 属性 14 → 16
rep('aria-label=\\"新建标签\\"><svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"14\\" height=\\"14\\"',
    'aria-label=\\"新建标签\\"><svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"16\\" height=\\"16\\"',
    '⑤「新建标签」图标 attr → 16')
rep('data-td-browse-close=\\"1\\"><svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"14\\" height=\\"14\\"',
    'data-td-browse-close=\\"1\\"><svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"16\\" height=\\"16\\"',
    '⑤「收起侧栏」图标 attr → 16')

# -------------------------------------------------------------------- 自检
print('\n'.join(log))
print('\n=== 结构自检 ===')
checks = [
    ('<style> 仍 2', s.count('<style>'), 2),
    ('</style> 仍 3', s.count('</style>'), 3),
    ('<script> 仍 8', s.count('<script>'), 8),
    ('</script> 仍 8', s.count('</script>'), 8),
    ('树行 is-dir 仍 10', s.count('class=\\"td-bf is-dir'), 10),
    ('树行 is-file 仍 18', s.count('class=\\"td-bf is-file'), 18),
    ('data-td-split 仍 5', s.count('data-td-split'), 5),
    ('ai-foot 字号已改 1 处', s.count('font-size: var(--font-size-body-1); color: var(--td-meta)'), 1),
    ('ai-foot 旧字号 2→1 处', s.count('gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta)'), 1),
    ('round-btn 28px 且无影 1 处', s.count('border-color: transparent; box-shadow: none; line-height: 0;'), 1),
    ('panel-shadow 用法 4→3', s.count('box-shadow: var(--td-panel-shadow);'), 3),
    ('browse 规则不再含 shadow', s.count('border-radius: 0 8px 8px 0; box-shadow:'), 0),
    ('bar 按钮 32 两条选择器', s.count('.td-browse-bar .td-browse-add'), 2),
    ('bar 按钮 svg 16 两条选择器', s.count('.td-browse-bar .td-browse-add svg'), 1),
    ('td-bf cursor pointer', s.count('overflow: hidden; cursor: pointer;'), 1),
    ('tab svg color text-1', s.count('.td-browse-tab svg { color: var(--color-text-1); }'), 1),
    ('新 tab 图标存在', s.count('M7.5 9.5h6.5'), 1),
    ('旧 panel-right 图标 2→1', s.count('M15 3v18'), 1),
]
fail = 0
for name, got, want in checks:
    ok = got == want
    if not ok:
        fail += 1
    print(f'  {"OK " if ok else "!! "}{name}: got={got} want={want}')

if fail:
    print(f'\n!! {fail} 条自检失败，未写盘')
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print(f'\n✅ 已写盘 {P}: {n0} → {len(s)} 字节（{"+" if len(s)>=n0 else ""}{len(s)-n0}）')
