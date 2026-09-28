# -*- coding: utf-8 -*-
"""第 50 轮：task-detail 打开侧栏文件预览栏的 7 项修正。

1. 「收起侧栏」按钮图标：chevron-right → 关闭(X)
2. 浏览态（右栏展示）下禁用「按住标题栏左右拖动互换两栏位置」
3. .td-bf 行高 34 → 28px；内部 chevron/图标 16 → 13px、字号 body-3(14) → body-2(13)；
   同时按 13px 盒宽重算左内距/间距，保持 chevron 中心仍在引导线 x=14、名称列左缘不变
4. .td-right 与 .td-browse 衔接线：--td-hairline(#F2F2F2) → --color-border-2(#E5E5E5)
5. .td-browse-bar 底线：同上
6. .td-browse-tree 与 .td-browse-code 衔接线：--color-border-1 → --color-border-2
7. .td-browse-search 换用 DS 标准 Input 组件（default 变体 + prefix 搜索图标 + medium 32px）

幂等：所有替换都先断言「旧串恰好存在 1 次」，已改过的串直接跳过。
"""
import io, os, re, shutil, sys

PAGE = 'pages/task-detail.html'
BAK = '/tmp/r50-backup/task-detail.html'

s = io.open(PAGE, encoding='utf-8').read()
orig = s
os.makedirs(os.path.dirname(BAK), exist_ok=True)
if not os.path.exists(BAK):
    shutil.copy2(PAGE, BAK)
    print('[backup]', BAK)

before_tags = (s.count('<style>'), s.count('</style>'), s.count('<script'), s.count('</script>'))
print('[before tags] style/close/script/close =', before_tags)
print('[before] --td-hairline =', s.count('--td-hairline'),
      '| color-border-1 =', s.count('var(--color-border-1)'),
      '| height: 34px =', s.count('height: 34px'),
      '| m9 18 6-6-6-6 =', s.count(r'm9 18 6-6-6-6'))

changed = []


def sub_once(old, new, label, must=True):
    """全局恰好替换一次；已替换过则跳过（幂等）。"""
    global s
    n = s.count(old)
    if n == 0 and new in s:
        print('  [skip]%s（已是新值）' % label)
        return False
    if n != 1:
        print('  [FAIL]%s 期望旧串 1 次，实际 %d 次' % (label, n))
        if must:
            raise SystemExit('替换前置断言失败: ' + label)
        return False
    s = s.replace(old, new, 1)
    changed.append(label)
    print('  [ok]  %s' % label)
    return True


# ---------------------------------------------------------------- 4/5/6 分隔线加深一级
sub_once(
    'background: var(--color-bg-1); border-left: 1px solid var(--td-hairline);',
    'background: var(--color-bg-1); border-left: 1px solid var(--color-border-2);',
    '4. .td-browse 左衔接线 border-1 → border-2')

sub_once(
    '        display: flex; align-items: center; gap: 8px; padding: 4px 16px;\n'
    '        border-bottom: 1px solid var(--td-hairline);\n',
    '        display: flex; align-items: center; gap: 8px; padding: 4px 16px;\n'
    '        border-bottom: 1px solid var(--color-border-2);\n',
    '5. .td-browse-bar 底线 → border-2')

sub_once(
    '        display: flex; flex-direction: column; gap: 8px; overflow: auto;\n'
    '        border-right: 1px solid var(--color-border-1);\n',
    '        display: flex; flex-direction: column; gap: 8px; overflow: auto;\n'
    '        border-right: 1px solid var(--color-border-2);\n',
    '6. .td-browse-tree 右衔接线 border-1 → border-2')

# ---------------------------------------------------------------- 3 树行 28px / 图标·字号 13px
sub_once(
    '      .td-bf {\n'
    '        position: relative; display: flex; align-items: center; height: 34px; box-sizing: border-box;\n'
    '        font-size: var(--font-size-body-3); color: var(--color-text-1);\n',
    '      .td-bf {\n'
    '        position: relative; display: flex; align-items: center; height: 28px; box-sizing: border-box;\n'
    '        font-size: var(--font-size-body-2); color: var(--color-text-1);\n',
    '3a. .td-bf 行高 34 → 28px、字号 body-3(14) → body-2(13)')

# chevron 盒 16 → 13px：中心要保持在引导线 x=14 ⇒ 左内距 6 → 7.5
sub_once(
    '      .td-bf.is-dir { padding-left: calc(6px + var(--d, 0) * 20px); }',
    '      /* 行内盒 13px（与设计稿实测一致）：chevron 中心仍须落在引导线 x=14 ⇒ 左内距 14−13/2=7.5 */\n'
    '      .td-bf.is-dir { padding-left: calc(7.5px + var(--d, 0) * 20px); }',
    '3b. .td-bf.is-dir 左内距 6 → 7.5px')

sub_once(
    '      .td-bf-arrow {\n'
    '        flex: none; width: 16px; height: 16px; padding: 0; border: 0; background: transparent;',
    '      .td-bf-arrow {\n'
    '        flex: none; width: 13px; height: 13px; padding: 0; border: 0; background: transparent;',
    '3c. .td-bf-arrow 16 → 13px')

sub_once('.td-bf.is-dir > .td-bf-arrow { margin-right: 6px; }',
         '.td-bf.is-dir > .td-bf-arrow { margin-right: 7.5px; }',
         '3d. chevron 右间距 6 → 7.5px（文件夹图标列左缘仍为 28）')

sub_once('.td-bf-ico { flex: none; width: 16px; height: 16px; color: var(--color-text-2); }',
         '.td-bf-ico { flex: none; width: 13px; height: 13px; color: var(--color-text-2); }',
         '3e. .td-bf-ico 16 → 13px')

sub_once('.td-bf.is-dir > .td-bf-ico { margin-right: 8px; }',
         '.td-bf.is-dir > .td-bf-ico { margin-right: 7.5px; }',
         '3f. 目录图标右间距 8 → 7.5px（名称列左缘 28+13+7.5 不变）')

sub_once('.td-bf.is-file > .td-bf-ico { margin-right: 7px; }',
         '.td-bf.is-file > .td-bf-ico { margin-right: 10px; }',
         '3g. 文件图标右间距 7 → 10px（名称列左缘仍为 31）')

# ---------------------------------------------------------------- 7 搜索框换 DS Input
OLD_SEARCH = (
    '<div class=\\"td-browse-search\\">'
    '<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"14\\" height=\\"14\\" '
    'fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" '
    'stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">'
    '<circle cx=\\"11\\" cy=\\"11\\" r=\\"8\\"/><path d=\\"m21 21-4.3-4.3\\"/></svg>'
    '<span>搜索文件</span></div>'
)
NEW_SEARCH = (
    '<div class=\\"giencoder-input-wrapper td-browse-search\\" data-component=\\"input\\" '
    'data-variant=\\"prefix\\" data-size=\\"medium\\" data-state=\\"default\\">'
    '<span class=\\"giencoder-input-prefix\\">'
    '<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"14\\" height=\\"14\\" '
    'fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" '
    'stroke-linejoin=\\"round\\" aria-hidden=\\"true\\">'
    '<circle cx=\\"11\\" cy=\\"11\\" r=\\"8\\"/><path d=\\"m21 21-4.3-4.3\\"/></svg></span>'
    '<input class=\\"giencoder-input\\" type=\\"text\\" placeholder=\\"搜索文件\\" aria-label=\\"搜索文件\\">'
    '</div>'
)
sub_once(OLD_SEARCH, NEW_SEARCH, '7. .td-browse-search → DS Input(default+prefix, medium 32px)')

# 自绘盒子的视觉样式删除，只留 flex:none
sub_once(
    '      .td-browse-search {\n'
    '        margin: 0; height: 32px; flex: none; box-sizing: border-box;\n'
    '        display: flex; align-items: center; gap: 8px; padding: 0 8px; border-radius: 4px;\n'
    '        background: var(--color-fill-1); color: var(--color-text-3); font-size: var(--font-size-body-3);\n'
    '      }\n',
    '      /* ★ 第 50 轮第 7 项：搜索框改用 DS 标准 Input 组件（default 变体 + prefix 搜索图标）。\n'
    '         设计稿实测：白底 + 1px 浅边框 + 32px 高（= DS sizes.medium）、左侧放大镜 13px；\n'
    '         原先自绘的 fill-1 扁平盒子（无边/8px 内距）与设计稿不符，已删除，\n'
    '         这里只保留 flex: none，避免在树容器（flex column）里被拉伸或压缩。 */\n'
    '      .td-browse-search { flex: none; }\n',
    '7b. 删除自绘搜索框视觉样式（保留 flex: none）')

# ---------------------------------------------------------------- 2 浏览态禁止标题栏拖动换位
sub_once(
    '      .td-root.is-browse .td-browse { display: flex; }\n',
    '      .td-root.is-browse .td-browse { display: flex; }\n'
    '      /* ★ 第 50 轮第 2 项：浏览态（文件预览栏展示时）AI 对话框固定为「会话在左、预览在右」，\n'
    '         因此其标题栏不再承担「左右拖动互换两栏位置」的手势 —— 光标也不再是 grab。 */\n'
    '      .td-root.is-browse .td-right-bar { cursor: default; }\n',
    '2a. CSS：浏览态标题栏光标 grab → default')

sub_once(
    "        if (root.classList.contains('is-fullscreen') || root.classList.contains('is-collapsed')) return;\n",
    "        if (root.classList.contains('is-fullscreen') || root.classList.contains('is-collapsed')\n"
    "            || root.classList.contains('is-browse')) return;\n",
    '2b. JS：bindSwapBar 增加 is-browse 守卫（不进入拖动态、不落盘）')

# ---------------------------------------------------------------- 1 「收起侧栏」→ 关闭图标
key = 'data-td-browse-close=\\"1\\"'
i = s.find(key)
if i < 0:
    raise SystemExit('找不到关闭按钮锚点')
seg = s[i:i + 600]
OLD_CHEV = '<path d=\\"m9 18 6-6-6-6\\"/>'
NEW_X = '<path d=\\"M18 6 6 18\\"/><path d=\\"m6 6 12 12\\"/>'
if OLD_CHEV in seg:
    s = s[:i] + s[i:i + 600].replace(OLD_CHEV, NEW_X, 1) + s[i + 600:]
    changed.append('1. 「收起侧栏」chevron-right → 关闭(X) 图标')
    print('  [ok]  1. 「收起侧栏」chevron-right → 关闭(X) 图标')
elif NEW_X in seg:
    print('  [skip]1.（已是 X 图标）')
else:
    raise SystemExit('关闭按钮内找不到旧 chevron')

# ---------------------------------------------------------------- 注释同步（说明 28/13）
s = s.replace(
    '      /* ★ 第 49 轮第 6 项：.td-browse-files 按设计稿还原为 tree\n'
    '         实测（节点 1350:18310）：行距 34px、缩进 20px/级、',
    '      /* ★ 第 49 轮第 6 项：.td-browse-files 按设计稿还原为 tree\n'
    '         ★ 第 50 轮第 3 项：行高改 28px（比设计稿 34px 更紧凑）、行内图标与字号统一 13px。\n'
    '         设计稿实测（节点 1350:18310）：行距 34px、缩进 20px/级、')

# ---------------------------------------------------------------- 结构自检
after_tags = (s.count('<style>'), s.count('</style>'), s.count('<script'), s.count('</script>'))
print('\n[after tags]', after_tags)
assert after_tags == before_tags, '标签级计数被破坏: %s -> %s' % (before_tags, after_tags)

checks = [
    ('--td-hairline 减少 2 处',              s.count('--td-hairline'), 4),
    ('var(--color-border-1) 减少 1 处',      s.count('var(--color-border-1)'), 15),
    ('height: 34px 归零',                    s.count('height: 34px'), 0),
    ('旧 chevron 路径归零',                  s.count(r'm9 18 6-6-6-6'), 0),
    ('X 图标路径恰 1 处',                    s.count('<path d=\\"M18 6 6 18\\"/>'), 1),
    ('giencoder-input-wrapper 26',           s.count('giencoder-input-wrapper'), 26),
    ('giencoder-input-prefix 7',             s.count('giencoder-input-prefix'), 7),
    ('td-browse-search 仍 2 处',             s.count('td-browse-search'), 2),
    ('is-browse)) return 恰 1 处',           s.count("|| root.classList.contains('is-browse')) return;"), 1),
    ('is-browse .td-right-bar 规则 1 处',    s.count('.td-root.is-browse .td-right-bar { cursor: default; }'), 1),
    ('data-td-browse-close 仍 2 处',         s.count('data-td-browse-close'), 2),
    ('data-td-split 仍 5 处(H+F)',           s.count('data-td-split'), 5),
    ('树行 .td-bf is-dir/is-file 计数',      s.count('class=\\"td-bf is-dir') + s.count('class=\\"td-bf is-file'), 28),
]
print('\n=== 结构自检 ===')
bad = 0
for label, got, want in checks:
    ok = got == want
    bad += 0 if ok else 1
    print(('  OK  ' if ok else '  BAD ') + label + ' → %s (期望 %s)' % (got, want))

if bad:
    raise SystemExit('自检失败 %d 项，未写入文件' % bad)

if s == orig:
    print('\n无变化（幂等重跑）')
else:
    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('\n已写入 %s：%d → %d 字节' % (PAGE, len(orig), len(s)))
print('改动项：\n  - ' + '\n  - '.join(changed))
