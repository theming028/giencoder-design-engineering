# -*- coding: utf-8 -*-
"""
第 73 轮 · 补丁 c（需求 5：下拉菜单 / 浮窗「显隐」通用微动效，9 页）

【口径 —— 用户拍板】
  ① 进场：覆盖**全部**浮窗；
  ② 退场：只做**页面自定义浮窗**（有 JS 状态机的），DS 组件库浮层保持原开合机制不动。

【取证方式】agent-browser 实机逐页扫（`mg-work/r73/ev/enum-popups.js`），
读的是 **computed** `transitionProperty / transitionDuration / animationName`，
而不是正则搜压缩产物（后者会把 `giencoder-popup-open` 之类误算进来）：见 ev/enum-result.md。

【实测结论：真正缺动效的只有 3 处】
  · `.td-add-pop`      添加菜单（task-detail / avatar）—— hidden 属性开关，transition=all/0s，无任何动效
  · `.td-skill-pop`    技能面板（task-detail / avatar）—— 同上
  · `.giencoder-tooltip-popup`  DS Tooltip（全 9 页共享样式表）—— 只有 box-shadow，无进场
  · `.avatar-tooltip`  头像悬停提示（task-detail / avatar / base 有 DOM）—— 只有 opacity 淡入，缺位移，且退场秒隐

【已自带开合动效、本轮**不动**的】
  组件库：.giencoder-select-popup / .giencoder-dropdown-popup / .giencoder-popover /
          .giencoder-date-picker-popup / .giencoder-modal（模态不属于「下拉浮窗」）
  页面自定义：.td-ctx（右键菜单）/ .td-more（更多操作）—— r54/r59 已按契约做全开合过渡

【实现要点】
  ② 组用「display 离散过渡（allow-discrete）+ @starting-style」同时拿到进场与退场，
     **不需要改一行 JS**（原先 `pop.hidden = true/false` 保持原样）。
     只用 translate / scale 独立属性、不用 transform —— `.td-skill-pop` 靠
     `transform:translateX(-50%)` 做水平居中，独立属性与其天然复合、互不覆盖。
  ③ `.avatar-tooltip` 把 visibility 的隐藏延后到过渡结束 ⇒ 顺带补上退场淡出（原来是秒隐）。

【落点】`</body>` 之前 —— 层叠最晚。
  必须晚于页面里既有的 `.td-add-pop[hidden]{display:none!important}` 与
  `.avatar-wrap:hover .avatar-tooltip{...}`：同特异性时后置者胜。

幂等三要素：MARK 命中即 SKIP；锚点 `</body>` 必须恰好 1 次；跑完立刻复跑验幂等。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r73c-backup'
PAGES = 'pages'

MARK = '<style id="r73-popup-css">'
ANCHOR = '</body>'

NEW = (
    '<style id="r73-popup-css">\n'
    '  /* ★ 第 73 轮 · 需求 5：下拉菜单 / 浮窗「显隐」通用微动效。\n'
    '     口径（用户拍板）：进场覆盖全部浮窗；退场只做「页面自定义浮窗」。\n'
    '     实机逐页实测（computed transition / animation）后，真正缺动效的只有本块这 3 处；\n'
    '     组件库的 Select / Dropdown / Popover / DatePicker 弹层、以及 .td-ctx / .td-more\n'
    '     早已自带开合过渡，本块不重复定义、不覆盖。 */\n'
    '\n'
    '  /* ① 通用进场微动效：淡入 + 4px 上移 + 缩放 0.97（与组件库弹层同一套参数） */\n'
    '  @keyframes r73-pop-in {\n'
    '    from {\n'
    '      opacity: 0;\n'
    '      translate: 0 4px;\n'
    '      scale: 0.97;\n'
    '    }\n'
    '  }\n'
    '\n'
    '  /* ② 组件库 Tooltip：挂载即显示、原本没有任何动效 ⇒ 只补进场 */\n'
    '  .giencoder-tooltip-popup {\n'
    '    animation: r73-pop-in 160ms cubic-bezier(0.34, 0.69, 0.1, 1) both;\n'
    '  }\n'
    '\n'
    '  /* ③ 页面自定义浮窗（对话框上方的「添加」菜单 / 技能面板）：由 hidden 属性开关。\n'
    '     用「display 离散过渡 + @starting-style」同时拿到进场与退场，**无需改 JS**：\n'
    '       · allow-discrete ⇒ 关闭时先把动效播完，再真正落到 display:none\n'
    '       · @starting-style ⇒ 打开时先给出 from 值，opacity / translate / scale 才有起跑点\n'
    '     ⚠️ 这里只用 translate / scale 独立属性、不用 transform ——\n'
    '        技能面板靠 transform:translateX(-50%) 做水平居中，独立属性与其天然复合、互不覆盖。 */\n'
    '  .td-add-pop,\n'
    '  .td-skill-pop {\n'
    '    transition: opacity 160ms cubic-bezier(0.34, 0.69, 0.1, 1),\n'
    '                translate 160ms cubic-bezier(0.34, 0.69, 0.1, 1),\n'
    '                scale 160ms cubic-bezier(0.34, 0.69, 0.1, 1),\n'
    '                display 160ms allow-discrete;\n'
    '  }\n'
    '  .td-add-pop[hidden],\n'
    '  .td-skill-pop[hidden] {\n'
    '    opacity: 0;\n'
    '    translate: 0 4px;\n'
    '    scale: 0.97;\n'
    '  }\n'
    '  @starting-style {\n'
    '    .td-add-pop:not([hidden]),\n'
    '    .td-skill-pop:not([hidden]) {\n'
    '      opacity: 0;\n'
    '      translate: 0 4px;\n'
    '      scale: 0.97;\n'
    '    }\n'
    '  }\n'
    '\n'
    '  /* ④ 悬停型提示（头像「停用数字分身」）：保留原有淡入、补 2px 上移；\n'
    '     并把 visibility 的隐藏延后到过渡结束 ⇒ 顺带补上退场淡出（原本是秒隐）。 */\n'
    '  .avatar-tooltip {\n'
    '    translate: 0 2px;\n'
    '    transition: opacity 150ms ease, translate 150ms ease, visibility 0s 150ms;\n'
    '  }\n'
    '  .avatar-wrap:hover .avatar-tooltip {\n'
    '    translate: 0 0;\n'
    '  }\n'
    '</style>\n'
)

# 自检用的唯一多行片段（都不与注释重复）
U1 = '@keyframes r73-pop-in {\n    from {'
U2 = '.giencoder-tooltip-popup {\n    animation: r73-pop-in 160ms'
U3 = 'display 160ms allow-discrete;'
U4 = '@starting-style {'
U5 = '.avatar-wrap:hover .avatar-tooltip {\n    translate: 0 0;'
U6 = '.td-skill-pop[hidden] {\n    opacity: 0;'


def files():
    return [f for f in sorted(os.listdir(os.path.join(ROOT, PAGES))) if f.endswith('.html')]


def load(name):
    with io.open(os.path.join(ROOT, PAGES, name), encoding='utf-8') as f:
        return f.read()


def save(name, s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    src = os.path.join(ROOT, PAGES, name)
    dst = os.path.join(BACKUP, name)
    if not os.path.exists(dst):
        with io.open(src, encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(src, 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    for bad in ('</body', '</html'):
        if bad in payload:
            sys.exit('!! 元守卫失败：%s 载荷含 %s' % (label, bad))


def main():
    guard('浮窗浮层块', NEW)

    applied, skipped, failed = [], [], []
    for name in files():
        s = load(name)
        if MARK in s:
            skipped.append(name)
            continue
        n = s.count(ANCHOR)
        if n != 1:
            failed.append('%s: %s 命中 %d 次' % (name, ANCHOR, n))
            continue
        before = s
        s = s.replace(ANCHOR, NEW + ANCHOR)
        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            expect = 1 if tag in ('<style', '</style>') else 0
            if d != expect:
                failed.append('%s: 标签计数 %s Δ%d（期望 Δ%d）' % (name, tag, d, expect))
                break
        else:
            save(name, s)
            applied.append(name)

    print('应用: %d 页 | 跳过: %d 页 | 失败: %d 页' % (len(applied), len(skipped), len(failed)))
    if applied:
        print('  已改: ' + ', '.join(applied))
    if skipped:
        print('  已就位: ' + ', '.join(skipped))
    for f in failed:
        print('  ✗ ' + f)
    if failed:
        sys.exit(1)

    # ================= 自检 =================
    print('\n--- 自检 ---')
    checks = []
    for name in files():
        t = load(name)
        checks.append(('%s: 本块恰好 1 个' % name, t.count(MARK) == 1))
        checks.append(('%s: 通用进场关键帧在位' % name, t.count(U1) == 1))
        checks.append(('%s: 组件库 Tooltip 进场规则在位' % name, t.count(U2) == 1))
        checks.append(('%s: display 离散过渡在位' % name, t.count(U3) == 1))
        checks.append(('%s: @starting-style 块在位' % name, t.count(U4) == 1))
        checks.append(('%s: 隐藏态起始值在位' % name, t.count(U6) == 1))
        checks.append(('%s: 悬停提示位移规则在位' % name, t.count(U5) == 1))
        checks.append(('%s: 锚点仍唯一' % name, t.count(ANCHOR) == 1))
        checks.append(('%s: 未引入旧玻璃块 r71-glass-css' % name, t.count('r71-glass-css') == 0))
    ok = 0
    for nm, cond in checks:
        if cond:
            ok += 1
        else:
            print('  ✗ %s' % nm)
    print('自检：%d/%d 通过' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
