# -*- coding: utf-8 -*-
"""r107 第七拍 · 改 `part107/panel.css`：
   A) ⑥ 右栏字体统一 —— 8 处写死等宽族就地换成 `var(--font-family)`
   B) 追加第 13 节：② 菜单标题 / ③ 选中态底色 / ④ 快捷键 / ⑤ 提交卡输入框拉通 / ⑦ 全屏按钮联动
用法： python mg-work/r107/ev/patch107h.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = os.path.join(REPO, 'mg-work', 'r107', 'part107', 'panel.css')

OLD = b'font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;'
NEW = b'font-family: var(--font-family);'
WANT = 8

SEC13 = u'''

/* ================================================================ 13. 第七拍（2026-10-01 12:1x 邵先生七条）
   本节承担 ② 菜单标题 / ③ 选中态底色 / ④ 快捷键提示 / ⑤ 提交卡输入框拉通 / ⑦ 全屏按钮联动；
   ⑥「右栏字体统一」不在这里做覆盖，而是**回到第 1~5 节各自那条规则就地改**
     （把写死的等宽族换成 `var(--font-family)`）—— 那些选择器都是具体类（`.td-diff-path` / `.td-dr` …），
     堆一条通配既压不住、又容易误伤。
   ①「Codex / ChatGPT → GienCoder」是文案替换，落在 `_mods.html` 与 `apply107.py`，不在本文件。 */

/* ② 去掉下拉菜单顶部的标题行。两类来源：静态 HTML 里的 `td-mm-cap`
   （`+` 菜单的「在侧栏打开」、审查范围菜单的「对比范围」），以及右键菜单里由 panel.js
   现场生成的「目标名」行 —— 本段一并关掉。
   用 `display: none` 而非删节点：① 两种来源一处管；② 菜单是 `flex-direction: column`，
   塌掉的行不参与布局 ⇒ 与真删节点视觉等价。 */
.td-browse .td-mm-cap,
.td-browse .td-ctx-head { display: none; }

/* ④ 去掉下拉菜单里的快捷键提示 —— 同样两类：静态的、与右键菜单动态生成的。 */
.td-browse .td-mm-key,
.td-browse .td-ctx-key { display: none; }

/* ③ 选中项「常显底色」。改前只有主色文字 + 右侧 ✓（实测 `background-color` 为 `rgba(0,0,0,0)`），
   邵先生要求补底色。取 DS 里用于选中项的浅主色 `--color-primary-light-1`；
   ⚠ 不补那枚 3px 左缘条 —— 本页第五拍已认定它属于 Menu 族的表达，不是 Dropdown。
   写在 `:hover` 规则之后 ⇒ 悬停选中项时底色不翻成 hover 灰（「常显」）。 */
.td-mod-menu .giencoder-dropdown-item.is-checked,
.td-rv-menu .giencoder-dropdown-item.is-checked,
.td-ctxmenu .giencoder-dropdown-item.is-checked { background: var(--color-primary-light-1); }

/* ⑤ 提交卡里的「目标分支」输入框要拉通。它挂的是 DS 的 `.giencoder-input-wrapper`，
   该编译样式为 `display: inline-flex; width: auto; min-width: 120px` ⇒ 宽度只吃内容自然宽。
   实测：卡片内容宽 308，它只有 207（同卡片的说明文字 / 输入区 / 按钮行都是 308）。
   block 级 flex ⇒ 一处 `display` 撑满，内部排布一字不变。 */
.giencoder-input-wrapper.td-commit-in { display: flex; }

/* ⑦ 右栏展开时页头那枚「全屏」按钮隐藏，收起后复现。
   判据用 `.av-browse-on` —— 实测它加在 shell 的 flex 行上（`main` 与预览栏的共同父级），
   而那枚按钮在 `main` 里 ⇒ 纯 CSS 可判，不需要 JS 联动。
   ⚠ 只针对「全屏」那一枚；旁边那枚开关侧栏的不动。 */
.av-browse-on .r93-baract[data-r93-fullscreen] { display: none; }
'''


def main():
    b = io.open(P, 'rb').read()
    n = b.count(OLD)
    # 幂等：第一遍命中 8、复跑命中 0（已是目标态）都合法；其它数为异常。
    if n not in (0, WANT):
        sys.exit('!! 字体锚点命中 %d 次（应 %d 或 0 次）' % (n, WANT))
    b2 = b.replace(OLD, NEW)
    if b'13. \xe7\xac\xac\xe4\xb8\x83\xe6\x8b\x8d' in b2:
        print('   第 13 节已存在，跳过追加')
    else:
        eol = b'\r\n' if b2.count(b'\r\n') > 100 else b'\n'
        seg = SEC13.replace('\r\n', '\n').replace('\n', eol.decode('ascii')).encode('utf-8')
        if not b2.endswith(eol):
            b2 += eol
        b2 += seg.lstrip(b'\r\n')
    io.open(P, 'wb').write(b2)
    t1 = b.decode('utf-8').replace('\r\n', '\n')
    t2 = b2.decode('utf-8').replace('\r\n', '\n')
    print('   panel.css %d → %d 字符（%+d）；字体替换 %d 处' % (len(t1), len(t2), len(t2) - len(t1), n))
    print('   ui-monospace 残留 %d 处（应 1 = 第 11 节注释）' % (t2.count('ui-monospace')))


if __name__ == '__main__':
    main()
