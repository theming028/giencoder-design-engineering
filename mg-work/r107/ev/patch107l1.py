# -*- coding: utf-8 -*-
"""r107 第十一拍（①②③）—— 仍是未提交期的**就地返工**，不另起代数。

改序（只能下→上）：
    1. `mg-work/r107/apply107.py`        wire() 里骨架屏两条计时 1100 → 380（③ 的一半）
    2. `mg-work/r107/part107/panel.css`  第 15 / 16 / 17 节（① 浮条正文黑 · ② 地址栏激活态 · ③ 数字动效提速）
    3. 重跑 `mg-work/r107/apply107.py` 落页面

幂等判据：每处都带 `mark`（**只有改完之后才存在**的串）⇒ 复跑「应用 0 项 / 跳过 N 项」。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
APPLY = os.path.join(REPO, 'mg-work', 'r107', 'apply107.py')
PCS = os.path.join(REPO, 'mg-work', 'r107', 'part107', 'panel.css')

APPLIED = []
SKIPPED = []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark):
    t, nl = rd(p)
    if mark and mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）' % (label, n))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


def tail(p, mark, new, label):
    t, nl = rd(p)
    if mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    if not t.endswith('\n'):
        t += '\n'
    wr(p, t + new, nl)
    APPLIED.append(label)
    print('   应用  %s（追加 %d 字符）' % (label, len(new)))


# ================================================================================
# 1. apply107.py · wire() 骨架屏计时 1100 → 380
#    原文**从文件里现取**（不手抄），避免转义/空白漂移。
# ================================================================================
B_START = '  function wire(host) {\n'
B_END = '}, 1100);\n'

MARK_L1 = 'r107-l1'

NEW_NOTE = """    /* ★ r101 ⑪：骨架屏退场。**第十一拍 ③：1100ms → 380ms**（邵先生：「这种数字动效实在是太慢，
       还以为没有数字呢」）。为什么非改不可 —— 数字的滑入动效**不可能早于骨架屏退场被看到**
       （`.r93-sk` 是 `position:absolute; inset:0` + 不透明 `--color-bg-2` 底，它盖着的那段时间里
       任何动效都白做）。旧值真机实测时间线（`performance.now()`）：骨架屏 2012ms 开始淡出 →
       2326ms 从 DOM 移除 → 数字 **2493ms** 才首次可见（整整 2.5 秒）。改后：380ms 起淡出 →
       700ms 移除，数字配合在 440~740ms 滑入（见 panel.css 第 17 节）⇒ 空窗由 167ms 降到 0。
       —— `320ms` 保留：CSS 那条 `transition: opacity 0.3s ease` 走完正好 300ms，再早移除会跳一下。 */
"""


def patch_apply107():
    t, nl = rd(APPLY)
    if MARK_L1 in t:
        SKIPPED.append('apply107.py · wire() 骨架屏计时 1100 → 380')
        print('   跳过  apply107.py · wire() 骨架屏计时（已应用）')
        return
    i = t.find(B_START)
    if i < 0:
        sys.exit('!! apply107.py：找不到 wire() 起点')
    if t.count(B_START) != 1:
        sys.exit('!! apply107.py：wire() 起点命中 %d 次（应 1）' % t.count(B_START))
    # 端点取**第二处** `}, 1100);`（第一处是骨架屏那条，第二处是 data-r93-app 那条）
    j1 = t.find(B_END, i)
    if j1 < 0:
        sys.exit('!! apply107.py：找不到第一处 `}, 1100);`')
    j2 = t.find(B_END, j1 + 1)
    if j2 < 0:
        sys.exit('!! apply107.py：找不到第二处 `}, 1100);`')
    j = j2 + len(B_END)
    block = t[i:j]
    if block.count('}, 1100);') != 2 or block.count('}, 320);') != 1:
        sys.exit('!! apply107.py：块内计数异常（1100=%d / 320=%d）'
                 % (block.count('}, 1100);'), block.count('}, 320);')))
    # ① 两条计时
    new = block.replace('}, 1100);', '}, 380);')
    # ② 旧注释里那两处数字
    for a, b in (('1100ms 后淡出（CSS', '380ms 后淡出（CSS'),
                 ('数值与骨架屏的 1100ms 一致', '数值与骨架屏的 380ms 一致')):
        if new.count(a) != 1:
            sys.exit('!! apply107.py：注释锚点 %r 命中 %d 次' % (a, new.count(a)))
        new = new.replace(a, b)
    # ③ 在骨架屏那段旧注释**之后**插入第十一拍的说明
    a = '       在后面持续参与合成。 */\n'
    if new.count(a) != 1:
        sys.exit('!! apply107.py：骨架屏注释尾锚点命中 %d 次' % new.count(a))
    new = new.replace(a, a + NEW_NOTE, 1)
    # ④ 幂等标记（写在 data-r93-app 那句之前）
    b = '    setTimeout(function () {\n      document.documentElement.setAttribute'
    if new.count(b) != 1:
        sys.exit('!! apply107.py：标记插入点命中 %d 次' % new.count(b))
    new = new.replace(b, '    /* %s */\n' % MARK_L1 + b, 1)
    wr(APPLY, t[:i] + new + t[j:], nl)
    APPLIED.append('apply107.py · wire() 骨架屏计时 1100 → 380')
    print('   应用  apply107.py · wire() 骨架屏计时（块 %d → %d 字符）' % (len(block), len(new)))


# ================================================================================
# 2. panel.css · 第 15/16/17 节
# ================================================================================
CSS_NEW = """
/* ================================================================================
   ★ 第十一拍（2026-10-01 13:4x 邵先生四条）—— 仍是 r107 **未提交期的就地返工**。
     ①②③ 全部落在本适配层（本文件）+ `apply107.py` 的 `wire()` 计时；
     ④（对照 Codex 官方补缺）落在下方第 18 节与 `part107/{browse.html,panel.js}`。
     ⚠ 体位与 R106_CSS / PANEL_CSS 一致：源件与历代遗产块逐字不动，
       只在本块用「同特异性 + 文档序在后」压过去（`build_css()` 把 PANEL_CSS 排在最后）。
   ================================================================================ */

/* ---------------------------------------------------------------- 15. 划词浮条：图标与文字默认正文黑（第十一拍 ①）
   实测（1440 / 真机 `getComputedStyle`）：两枚按钮的 `color` 都是 `rgb(55, 112, 247)`
   —— 因为 DS 的 `.giencoder-btn-text` 基类把文字色定成 `--color-primary-6`（主色蓝），
   而浮条这两枚是**普通工具动作**、不是主操作 ⇒ 邵先生要的「默认正文黑」
   = `--color-text-1`（gray-10 = `#1F1F1F`）。图标走 `stroke="currentColor"` ⇒ 改 `color` 即同时改图标。
   特异性 (0,2,0) > `.giencoder-btn-text` (0,1,0)，且本块文档序在后 ⇒ 必胜。
   ⚠ 只改基态色：`:hover` / `:active` 只换背景，`color` 不会被抢走。 */
.td-selbar .giencoder-btn { color: var(--color-text-1); }

/* ---------------------------------------------------------------- 16. 浏览器地址栏「输入中激活态」（第十一拍 ②）
   实测改前：`.td-url-pill` 只有 `background: --color-fill-2` + `input:focus { outline:none }`
   ⇒ **聚焦后零视觉变化**（`box-shadow` 恒为 `none`、底色恒为 `rgb(242,242,242)`）。
   口径照 DS 自己的输入框聚焦样式 `.giencoder-input-wrapper:focus-within`
   （`border-color: --color-primary-6` + `box-shadow: 0 0 0 2px --color-primary-light-2`）：
   本 Pill 是**无边框胶囊**（`border-radius: 999px`）⇒ 用「内描边 1px 主色 + 外 2px 浅主色环」
   复刻同一组视觉；同时把灰底 `--color-fill-2` 提成白底 `--color-bg-2`（= DS 输入框聚焦后变白）。
   ⚠ 用 `inset` 描边而不是 `border`（写 `border` 会让整颗胶囊高 2px、地址栏跟着抖）；
   ⚠ 外环 2px：`.td-url` 有 `padding: 6px 12px` ⇒ 四边都有余量，不会被裁。 */
.td-url-pill { transition: background-color 120ms ease, box-shadow 120ms ease; }
.td-url-pill:focus-within {
  background: var(--color-bg-2);
  box-shadow: inset 0 0 0 1px var(--color-primary-6), 0 0 0 2px var(--color-primary-light-2);
}
/* 锁定图标（`.td-url-pill > svg`）跟随：聚焦时由 text-3 提到 text-2（与输入文字同族）。 */
.td-url-pill:focus-within > svg { color: var(--color-text-2); }

/* ---------------------------------------------------------------- 17. 「调用 N 个工具」数字动效提速（第十一拍 ③）
   实测改前时间线（1440 / 真机 `performance.now()`，相对 timeOrigin）：
     骨架屏开始淡出 2012ms → 从 DOM 移除 2326ms → **数字首次可见 2493ms**
   ⇒ 从导航到看见数字要 **2.5 秒**，邵先生的观感是「还以为没有数字呢」。根因两层：
     ① 数字的 `animation-delay: calc(1.5s + ni*55ms)` + `fill: both`
        ⇒ 延迟期内停在 keyframes 的 `from`（`opacity:0` + 下移）＝**窗口里是空的**
        （`.r93-num` 是 inline-block，宽度由内部 `<i>` 撑 ⇒ 空位一直占着，看着就是个缺口）；
     ② 那 1.5s 的基础延迟是**为了等骨架屏退场**（骨架屏 1100ms 起淡出、+320ms 移除），
        而骨架屏是**不透明**的（`background: --color-bg-2` + `inset:0`）⇒ 早于它退场的动效全白做。
   ⇒ 提速必须**两边一起动**：骨架屏生命周期由 1100/320 收到 **380/320**（`apply107.py` 的
     `wire()`，标记 `r107-l1`），数字延迟由 1.5s 收到 **0.44s**、时长 0.46s→**0.30s**、
     错开 55ms→**26ms**。改后：骨架屏 380ms 起淡出、700ms 移除；数字 440~740ms 滑入
     ⇒ 数字**紧贴骨架屏退场滑进来**，空窗由 167ms 降到 0，整体由 2.49s 压到 **~1.66s**。
   ⚠ 只覆盖 `animation-duration` / `animation-delay` 两条长属性（不动 `animation-name` / `fill-mode`）
     ⇒ 与 `CSS` 里那条 `animation:` 简写同特异性、文档序在后，必胜；
     且 `both` 语义沿用（延迟期仍停在 `from`，不会先闪一下原位置）。
   ⚠ 时长 0.30s 仍在舒适区（DS 弹层入场就是 0.2s 档）。 */
.r93-num > .r93-num-i {
  animation-duration: 0.30s;
  animation-delay: calc(0.44s + var(--r93-ni, 0) * 26ms);
}
/* r107-l1 */
"""


def main():
    print('== 1. apply107.py ==')
    patch_apply107()
    print('== 2. part107/panel.css ==')
    tail(PCS, '/* r107-l1 */', CSS_NEW, 'panel.css · 第 15/16/17 节')
    print('\n应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))


if __name__ == '__main__':
    main()
