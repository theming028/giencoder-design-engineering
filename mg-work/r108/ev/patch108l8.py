# -*- coding: utf-8 -*-
"""r108 第十九拍（第八层补丁）—— 邵先生两条：

  ① **整个右栏 `.td-browse` 的文本（含代码）划词后都要弹浮动工具条（添加到对话 / 复制）**。
     原判据把划词浮条**只放行主对话口** `.r93-scroll` ⇒ 右栏里划词浮条**根本不弹**
     （真机实测：真鼠标拖选能选中审查 diff 的代码行、也能选中摘要那行小字，但 `.td-selbar`
     **从未被创建**，`selbarExists = false`）。⇒ 放行根扩成「`.r93-scroll` ∪ `.td-browse`」。

  ② **`.td-mod-menu` 出现的瞬间会闪烁 / 跳动 / 位移，不够自然**。
     根因 = **「摘 `[hidden]`」与「挂开态类」挤在同一个 tick**：`[hidden]` 生效时元素是
     `display:none`，浏览器拿不到「改前样式」⇒ 紧随其后的那些属性过渡被**静默跳过**。
     真机逐帧采样（rAF）证实：`menu.getAnimations()` **恒为 `[]`**，`opacity / translate /
     scale` 在**同一帧内**直接落到终态 —— 契约里那条 0.2s spring 入场**从未运行过**，
     观感就是「硬切弹出来」。
     ⇒ 开的那一侧拆两步：先摘 `[hidden]` → `void menu.offsetWidth` 强制重排（记账「改前样式」）
       → 再挂 `.giencoder-popup-open`；并把 `placeRv()` 挪到挂类**之前** ⇒ 位置在第一帧可见前
       就定好，**零位移**。

★ 体位与硬规则：
  · r108 **仍未提交**（判据 `git status` 里 `conversation.html` 仍是 ` M`）⇒ **就地返工、不另起代数**，
    本拍作为 r108 的**第八层补丁**（l1~l7 之后）。
  · 本层**只改 `part108/panel.js` 一件**（不改 CSS、不改 HTML）⇒ 不必重跑 `splice108.py`
    （`browse.html` 里没有 panel.js 的内容），直接重跑 `apply108.py` 即可落盘。
  · `mark` 是「后一层必须替前一层保住」的契约：本层不新增 CSS 标记，只加两条 JS 留痕注释
    （`★ r108-l8 ①` / `★★ r108-l8 ②`），l1~l7 的标记一个不碰（收尾有跨层兜底断言）。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P107 = os.path.join(REPO, 'mg-work', 'r107', 'part107')
P108 = os.path.join(REPO, 'mg-work', 'r108', 'part108')
HEAD = os.path.join(P108, '_head.html')
MODS = os.path.join(P108, '_mods.html')
PCS = os.path.join(P108, 'panel.css')
PJS = os.path.join(P108, 'panel.js')

APPLIED = []
SKIPPED = []
STRICT = True


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark, strict=None):
    t, nl = rd(p)
    strict = STRICT if strict is None else strict
    if mark and mark in t:
        if strict and old in t:
            sys.exit('!! %s：mark 歧义 —— `old` 与 `mark` 同时存在 ⇒ mark 不是「改完才出现」的串\n'
                     '   mark=%r\n   old=%r' % (label, mark, old[:200]))
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）\n   old=%r' % (label, n, old[:240]))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


# ================================================================================
# ① + ②  `panel.js`
# ================================================================================
def do_js():
    print('=== 1/1  panel.js（① 划词范围扩到整个右栏 · ② 入场过渡修活）===')

    # ---- ① 划词浮条的放行根：`.r93-scroll` → `.r93-scroll ∪ .td-browse` ----------
    J1_OLD = ("    if (!e.target || !e.target.closest || !e.target.closest('.r93-scroll')) "
              "{ selHide(); return; }\n")
    J1_NEW = (
        "    /* ★ r108-l8 ①（邵先生：「整个右栏 `td-browse` 所有的文本（含代码）被鼠标框选后，\n"
        "       都要在上方显示浮动工具条（添加到对话、复制）」）：\n"
        "       原判据只放行主对话口 `.r93-scroll` ⇒ 右栏里划词**浮条根本不弹**。\n"
        "       真机实测（1440×900，真实鼠标拖选，非合成事件）：审查 diff 的代码行能选中\n"
        "       （`Selection.toString()` 拿到 `'   <aside class=\"td-browse\" …>\\n89\\n− …'` 这类多行内容）、\n"
        "       摘要那行小字也能选中，但 `.td-selbar` **从未被创建**（`selbarExists = false`）。\n"
        "       ⇒ 放行根扩成「`.r93-scroll` ∪ `.td-browse`」，覆盖右栏全部模块\n"
        "         （摘要 / 审查 diff 代码 / 终端 / 浏览器 / 文件树与代码区 / 预览）。\n"
        "       ⚠ 两者是**并列的 flex 兄弟**、互不包含（1440 实测：`.r93-scroll` [13,49,778,604] 与\n"
        "         `.td-browse` [791,48,641,844]）⇒ 不会互相误判；主对话口原有划词能力一字未动。\n"
        "       ⚠ 页签名（`.td-browse-tab`）与文件树行名（`.td-bf`）本来就带 `user-select: none`\n"
        "         （它们是「控件」不是「内容」）⇒ 那两处仍拖不出选区，属既有口径、本拍不动。 */\n"
        "    var selHost = (e.target && e.target.closest)\n"
        "      ? e.target.closest('.r93-scroll, .td-browse') : null;\n"
        "    if (!selHost) { selHide(); return; }\n"
    )
    edit(PJS, J1_OLD, J1_NEW, '① 划词浮条放行根扩到整个右栏',
         '★ r108-l8 ①（邵先生：')

    # ---- ① 段落头注释同步（原写「选区限定在 .r93-scroll 内」已不成立） ----------
    J1B_OLD = "     ★ 选区限定在 `.r93-scroll`（主对话口）内 ⇒ 不干扰右栏、也不干扰顶栏 / aside。 */\n"
    J1B_NEW = (
        "     ★ 选区范围（★ r108-l8 ① 扩容）：`.r93-scroll`（主对话口）**∪** `.td-browse`\n"
        "       （整个右栏 —— 摘要 / 审查 diff 代码 / 终端 / 浏览器 / 文件树与代码区 / 预览）。\n"
        "       顶栏与左侧导航 aside 仍不在范围内。 */\n"
    )
    edit(PJS, J1B_OLD, J1B_NEW, '① 段落头注释同步', '★ r108-l8 ① 扩容')

    # ---- ① 文件头职责清单补一行 ------------------------------------------------
    J1C_OLD = "     ⑥ 摘要：会话摘要 / 计划 / 来源 / 产物（静态展示 + 复制反馈）\n"
    J1C_NEW = ("     ⑥ 摘要：会话摘要 / 计划 / 来源 / 产物（静态展示 + 复制反馈）\n"
               "     ⑦ 通用：划词浮条（★ r108-l8 ① 起覆盖**整个右栏**，不再只限主对话口）\n")
    # ⚠ strict=False：本步的 `new` = `old`（第 ⑥ 条那一行）**原样接回** + 追加第 ⑦ 条
    #   ⇒ 复跑时 `old` 必然仍在，与 mark 同时命中会被误判「mark 不唯一」
    #   （与 l5 / l6 / l7 的同类豁免一致 —— 这是**第四次**踩「原样接回」了）。
    edit(PJS, J1C_OLD, J1C_NEW, '① 文件头职责清单补第 ⑦ 条', '⑦ 通用：划词浮条', strict=False)

    # ---- ② 开的那一侧拆两步（强制重排 + 位置先行） ------------------------------
    J2_OLD = (
        "    if (willOpen) {\n"
        "      menu.removeAttribute('hidden');\n"
        "      menu.classList.add(POP_OPEN);\n"
        "      if (trigger) trigger.setAttribute('aria-expanded', 'true');\n"
        "      placeRv(menu, trigger);                         /* r107-k2 */\n"
        "    } else {\n"
    )
    J2_NEW = (
        "    if (willOpen) {\n"
        "      /* ★★ r108-l8 ②（邵先生：「菜单出现的瞬间会有闪烁或跳动或位移现象，不够自然」）：\n"
        "         根因 = **「摘 `[hidden]`」与「挂开态类」挤在同一个 tick**。\n"
        "         `[hidden]` 生效时元素是 `display:none`，浏览器**拿不到「改前样式」** ⇒ 紧随其后的\n"
        "         `display:none → flex` 那次样式变更里，`opacity / translate / scale` 的过渡被\n"
        "         **静默跳过**。真机 rAF 逐帧采样（关态采 4 帧 → 第 5 帧点开 → 再采 30 帧）证实：\n"
        "           · `menu.getAnimations()` **恒为 `[]`**；\n"
        "           · `opacity / translate / scale` 在**同一帧内**直接从基态落到终态。\n"
        "         ⇒ 契约里那条 0.2s spring 入场**从未运行过**，观感就是「硬切弹出来」。\n"
        "         ⇒ 下面四行拆两步：① 摘 `[hidden]`（元素进入 `display:flex` + 基态\n"
        "            `opacity:0 / visibility:hidden / translate:0 4px / scale:.96`，仍然不可见）；\n"
        "            ② `void menu.offsetWidth` **强制重排** —— 逼浏览器把上面那份「改前样式」记账；\n"
        "            ③ `placeRv()` 摆位（在「第一帧可见」之前定好 ⇒ **零位移**）；\n"
        "            ④ 最后才挂 `.giencoder-popup-open` ⇒ 过渡正常起跑。\n"
        "         同机同页对照实测（两例写法只差一行强制重排）：\n"
        "           · 旧写法：anims = `[]`，首帧即 `opacity:1 / translate:0px / scale:1`；\n"
        "           · 新写法：anims = `opacity:running|scale:running|translate:running`，逐帧\n"
        "             `opacity` 0 → .189 → .428 → .676 → .821 → .894 → … → 1（约 12 帧 ≈ 0.2s），\n"
        "             且 `scale` 过冲到 `1.0039` 再回落 = 契约那条 spring 的回弹。\n"
        "         ⚠ 只改「开」这一侧。关的一侧仍是摘类 + `[hidden]`（立即 `display:none`）——\n"
        "           本拍**不引入退场延迟**，免得与 Esc 分层、连点重开这些既有路径抢时序\n"
        "           （那些路径都把 `[hidden]` 当**唯一状态位**在用）。\n"
        "         ⚠ 本修法对共用本函数的四枚下拉（`.td-mod-menu` / `.td-rv-scope-menu` /\n"
        "           `.td-commit-menu` / `.td-rv-opts`）一并生效 —— 它们本来就是**同一条代码路径**、\n"
        "           共享同一段 CSS 过渡，属于同一个修复面。\n"
        "         ⚠ 另有两处**同型缺陷但走别的函数**，本拍按「不改不必涉及的模块」**不动**：\n"
        "           右键菜单 `ctxShow()` 与 `.zd-menu` 的 `placeZdMenu()`（同样是「摘 `[hidden]` +\n"
        "           挂类」同一 tick）⇒ 它们的入场也仍是硬切。要一并对齐说一声。 */\n"
        "      menu.removeAttribute('hidden');\n"
        "      void menu.offsetWidth;\n"
        "      placeRv(menu, trigger);                         /* r107-k2 */\n"
        "      menu.classList.add(POP_OPEN);\n"
        "      if (trigger) trigger.setAttribute('aria-expanded', 'true');\n"
        "    } else {\n"
    )
    edit(PJS, J2_OLD, J2_NEW, '② 开态拆两步（强制重排 + 位置先行）', '★★ r108-l8 ②（邵先生：')


# ================================================================================
# 跨层兜底断言
# ================================================================================
def verify():
    print()
    print('=== 跨层兜底断言 ===')
    j = rd(PJS)[0]
    jcode = re.sub(r'/\*.*?\*/', '', j, flags=re.S)
    jcode = re.sub(r'(?m)^\s*//.*$', '', jcode)
    bad = []

    # ① 判据（⚠ 一律写成 count == 1：只查「存在」抓不到「重复应用」）
    if jcode.count(".closest('.r93-scroll, .td-browse')") != 1:
        bad.append('panel.js：划词放行根应恰好 1 处（实 %d）'
                   % jcode.count(".closest('.r93-scroll, .td-browse')"))
    if jcode.count(".closest('.r93-scroll')") != 0:
        bad.append('panel.js：旧的「只放行 .r93-scroll」判据仍有残留（代码里）')
    if jcode.count('var selHost') != 1:
        bad.append('panel.js：`var selHost` 应恰好 1 处（实 %d）' % jcode.count('var selHost'))
    if j.count('★ r108-l8 ①（邵先生：') != 1:
        bad.append('panel.js：① 的留痕注释应恰好 1 处（实 %d）' % j.count('★ r108-l8 ①（邵先生：'))
    if j.count('★ r108-l8 ① 扩容') != 1:
        bad.append('panel.js：① 的段落头同步注释应恰好 1 处')
    if j.count('⑦ 通用：划词浮条') != 1:
        bad.append('panel.js：文件头第 ⑦ 条应恰好 1 处')

    # ② 判据：开的那一侧必须「摘 hidden → 强制重排 → 摆位 → 挂开态类」四步齐备且有序
    WANT = ("      menu.removeAttribute('hidden');\n"
            "      void menu.offsetWidth;\n"
            "      placeRv(menu, trigger);                         /* r107-k2 */\n"
            "      menu.classList.add(POP_OPEN);\n"
            "      if (trigger) trigger.setAttribute('aria-expanded', 'true');\n")
    if j.count(WANT) != 1:
        bad.append('panel.js：② 的「摘 hidden → 强制重排 → 摆位 → 挂开态类」四步序列应恰好 1 处'
                   '（实 %d）' % j.count(WANT))
    if jcode.count('void menu.offsetWidth;') != 1:
        bad.append('panel.js：`void menu.offsetWidth;` 应恰好 1 处（实 %d）'
                   % jcode.count('void menu.offsetWidth;'))
    if j.count('★★ r108-l8 ②（邵先生：') != 1:
        bad.append('panel.js：② 的留痕注释应恰好 1 处（实 %d）' % j.count('★★ r108-l8 ②（邵先生：'))
    # ② 反向判据：旧的三行顺序（挂类在 placeRv 之前）必须已消失
    # ⚠★ 判据全部**限定在 `toggleMenu` 函数体内**：下面两个「形状」在文件里都各出现
    #    2 次（另一处是 `.zd-menu` 的 `placeZdMenu()` —— 同型缺陷但本拍不动）
    #    ⇒ 拿全文计数会被误判（第一版就是这么误报的）。
    t0 = j.index('function toggleMenu(menu, trigger) {')
    t1 = j.index('\n  }\n', t0)
    tbody = j[t0:t1]
    OLDSEQ = ("      menu.removeAttribute('hidden');\n"
              "      menu.classList.add(POP_OPEN);\n")
    if OLDSEQ in tbody:
        bad.append('panel.js：旧的「摘 hidden 后立刻挂开态类」顺序仍留在 `toggleMenu` 里 —— '
                   '过渡仍会被静默跳过')
    CLOSE_SEQ = ("      menu.setAttribute('hidden', '');\n"
                 "      menu.classList.remove(POP_OPEN);\n")
    if tbody.count(CLOSE_SEQ) != 1:
        bad.append('panel.js：`toggleMenu` 关的分支结构被改动（应仍是「置 hidden → 摘类」，实 %d）'
                   % tbody.count(CLOSE_SEQ))
    # 另两处同型缺陷本拍**有意保留**（留痕，别被后来的「顺手清理」误删）
    if j.count(OLDSEQ) != 1:
        bad.append('panel.js：`.zd-menu`（`placeZdMenu`）那处同型写法应原样保留（实 %d 处）'
                   % j.count(OLDSEQ))

    # 跨层标记存活（本层不新增 CSS 标记，只保证历代标记一个不少）
    marks = [
        (PCS, '/* r108-l7 */', 'l7'), (PCS, '/* r108-l6 */', 'l6'), (PCS, '/* r108-l5 */', 'l5'),
        (PCS, '/* r108-l4 */', 'l4'), (PCS, '/* r108-l3 */', 'l3'), (PCS, '/* r108-l2 */', 'l2'),
        (PCS, '.td-rv-body > .td-diff { flex: none; }', 'l7 · 卡片不收缩'),
        (PJS, "var PLACE_ABS = ['td-mod-menu', 'td-rv-menu'];", 'l6 · 定位白名单'),
        (PJS, '★ r108-l7 ②：这里原有', 'l7 · 删最大化整段'),
        (MODS, 'data-td-prev-save="1"', 'l7 · 另存为'),
        (HEAD, 'data-td-open-mod="summary"', 'l7 · 摘要置首'),
    ]
    for p, mk, label in marks:
        if mk not in rd(p)[0]:
            bad.append('%s：%s（在 %s 里找不到）' % (label, mk, os.path.basename(p)))

    # ★★★ 注释括号配平（第七拍真踩：注释正文里写 `*/` 会提前闭合块注释 ⇒ check-syntax FAIL）
    for p, label in ((PJS, 'panel.js'), (PCS, 'panel.css')):
        s = rd(p)[0]
        if s.count('/*') != s.count('*/'):
            bad.append('%s：注释括号不配平（`/*` %d 个 / `*/` %d 个）—— 多半是注释正文里'
                       '出现了 `*/`' % (label, s.count('/*'), s.count('*/')))

    if bad:
        sys.exit('!! 跨层自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')
    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print('   跳过  %s' % s)


def main():
    do_js()
    verify()


if __name__ == '__main__':
    main()
