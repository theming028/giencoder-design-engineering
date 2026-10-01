# -*- coding: utf-8 -*-
"""r107 第七拍 · 刷新 `.workbuddy/memory/HANDOFF.md`（读数 + 七拍段 + 门禁）。
用法： python mg-work/r107/ev/doc107h.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = os.path.join(REPO, '.workbuddy', 'memory', 'HANDOFF.md')

SEG7 = u"""> ★★ **第七拍返工（邵先生 12:1x 反馈七条，见 `acceptance.md` 第十二节 / PLAYBOOK **P3.43**）**：
>   ⑲ ★★ **「渲染出来的字」与「渲染不出来的字」要分开判** —— 右栏里**可见**的竞品名共 8 处
>     （diff 文件名 / 三行代码 / 摘要描述段 / 三条来源标题）+ 两处悬停 `title`，全部换成 GienCoder；
>     **三条 `td-sum-src` 的外链 `href` 有意保留**（真实地址，替换域名段即 404，且不渲染成页面文字）；
>     前六拍写下的 7 处**设计来源注释**（CSS 5 / JS 2）同样保留。
>     ★ 本轮新增的注释一律避开被清理的词（我自己的第 13 节注释已改成「竞品名」中性表述）。
>     另补一处真·全局：`pages/avatar.html` 历史会话列表里那条示例标题（含竞品名的那条）
>     ⇒ 做法照 `apply106.py` 的 `2b)` 先例，`apply107.py` 新增 `2d)` 正 + 逆，EDITS **11 → 13 处**。
>   ⑳ ★★ **同一处改动要先判「节点从哪来」** —— 下拉菜单的标题行有两类来源：
>     静态 HTML（`.td-mm-cap`）与 **JS 现场生成**（`.td-ctx-head`，`ctxBuild()` 里建）⇒
>     删 HTML 治不了后者 ⇒ **一段 `display:none` 把两类一起关**（菜单是 column flex，塌行不占位 ⇒ 与删节点视觉等价）。
>     快捷键提示同理（静态 `.td-mm-key` ×10 + JS 的 `.td-ctx-key`）。
>   ㉑ ★ **DS 组件「宽度不拉通」先查它自己的 display** —— 提交卡的「目标分支」输入框挂
>     `.giencoder-input-wrapper`（编译样式 `display:inline-flex; width:auto; min-width:120px`）
>     ⇒ 实测**同卡其它行都是 308、它只有 207**；修法 = 双类
>     `.giencoder-input-wrapper.td-commit-in { display:flex }`（提高特异性，不赌文档序）。
>   ㉒ ★★ **「统一字体族」要分清「本代自己的样式」与「跨代沿用的移植件」** ——
>     `panel.css` 自己那 8 条**就地改**；「文件」模块代码区那条在 **r102 代已交付的 `part105/browse.css`** 里
>     （不回改历史代）⇒ 只能在本页**多一级类数覆盖**（`.td-browse .td-browse-pre`），
>     153 个 `.td-code*` 子树靠继承。⚠ 这条是**改完第一遍量出来才补的**。
>   ㉓ ★★ **联动显隐先找「状态类挂在哪一级」** —— 右栏的 `.av-browse-on` 实测加在
>     **shell 的 flex 行**上（`main` 与预览栏的共同父级），页头那枚按钮在 `main` 里 ⇒ 是它的后代
>     ⇒ **纯 CSS 可判，不必写 JS**：`.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }`。
> ★★ **第七拍体位**：仍是 r107 **就地返工**（`apply107.py` / `GENS` / 注入块 id / `NAV_TAG` 全不动）；
>   六条落在 `part107/panel.css`（新增第 13 节 + 第 1~5 节各自的 `font-family` 就地改），
>   一条落在 `part107/_mods.html` 文案 + `apply107.py` 的 `2d)`。改序照旧（下→上）。
>   `base.html` 仍**逐字节不变**（472150 字符）。第七拍产物 **925776 → 927464 字符（+1688；相对 HEAD +128233）**。
"""

DETAIL7 = u"""**★ 第七拍七条（邵先生 12:1x）**：
- ① **竞品名 → GienCoder**：右栏里**渲染成文字**的 8 处（`.td-diff-path` 文件名 / `.td-dr-t` ×3 /
  `.td-sum-p` 描述段 / `.td-sum-src b` ×3）+ 两处悬停 `title`。判据 = `TreeWalker(SHOW_TEXT)` 走 `.td-browse`，
  `/codex|chat\\s?gpt/i` **8 → 0**（四档一致）；属性扫描（排除 `href`）**2 → 0**。
  **有意保留**：三条 `td-sum-src` 外链 `href` + 前六拍的 7 处设计来源注释。
  **另清一处（真·全局）**：`pages/avatar.html` 历史会话列表那条示例标题 ⇒ `git diff --numstat` = `+1 / −1`；
  `make107.py` 的 EDITS **11 → 13 处**（E12 正向 / E13 逆向，锚点用带引号的整串 ⇒ 不碰同名注释）。
- ② **去掉下拉菜单的标题行** ⇒ `.td-browse .td-mm-cap, .td-browse .td-ctx-head { display:none }`
  （静态 + JS 现场生成两类一并关）。实测 `capDisp:"none"`、`getBoundingClientRect()` 归零。
- ③ **选中项常显底色** ⇒ 改前 `rgba(0,0,0,0)`、改后 `rgb(245,248,255)`（= `--color-primary-light-1`，
  口径取自 DS Menu 的 `.giencoder-menu-item-selected`；**不补**那枚 3px 左缘条 —— 第五拍已认定那是 Menu 族的表达）。
  规则写在 `:hover` 之后 ⇒ 悬停选中项不翻成 hover 灰。
- ④ **去掉快捷键** ⇒ `.td-browse .td-mm-key, .td-browse .td-ctx-key { display:none }`
  （静态实测 10 处：⇧⌘G / ⌃` / ⌘T / ⌘P / ⌘I / ⌥⌘C / ⌥⌘P / ⌘1 / ⌘2 / ⌘R）。
- ⑤ **提交卡输入框拉通** ⇒ 改前 `207 / 可用 308`（同卡 `.td-commit-h/-lb/-msg/-f` 都是 308）⇒
  `.giencoder-input-wrapper.td-commit-in { display:flex }` ⇒ 改后 `308 / 308`、`gap:0`。
- ⑥ **右栏字体统一** ⇒ `panel.css` 自己那 8 条就地换 `var(--font-family)`
  （`.td-diff-path` / `.td-diff-stat` / `.td-dr` / `.td-dsc-c` / `.td-diff-more` / `.td-commit-num` /
  `.td-term` / `.td-url-pill input`）；「文件」模块代码区那条在 r102 代已交付的 `part105/browse.css` 里
  ⇒ 末尾用 `.td-browse .td-browse-pre { font-family: var(--font-family) }` 覆盖（153 个 `.td-code*` 靠继承）。
  判据：`.td-browse *`（1137→1149 个元素）里 `fontFamily !== bodyFont` 的**计数 153 → 0**。
- ⑦ **全屏按钮联动** ⇒ `.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }`（**纯 CSS**）。
  实测右栏关 `display:flex`（`rect [1359,57,28,28]`）/ 开 `display:none`（rect 归零）。
- 第七拍门禁：幂等 ✓（第二遍「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107c.txt`
  **逐字节相同**（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜改动面 = `M conversation.html`（`+2244 / −3`）
  + `M avatar.html`（`+1 / −1`）；`base.html` **472150 字符逐字节不变**。
  产物 **925776 → 927464 字符（+1688；相对 HEAD +128233）**；
  资产 `_mods.html 35916 · browse.html 71578 · panel.css 39686`（`panel.js 48583` / `_head.html 5270` 未动）。
  裁片：改前 `raw/h2-{add-menu,opts-menu,commit}`、改后 `raw/h3-{add-menu,opts-menu,commit,ctxmenu}`；
  探针 `ev/p107h1~h3.js` + `probe107h{,2,3}.sh`；动手前备份 `ev/bak7/`。

"""

TABLE = [
    (u'r107 侧栏模块标签化已落地（六拍累积）',
     u'r107 侧栏模块标签化已落地（七拍累积）', 1),

    # 第六拍产物行之后，插入第七拍段
    (u">   `base.html` 仍**逐字节不变**（472150 字符）。第六拍产物 **921730 → 925776 字符（+4046；相对 HEAD +126545）**。\n"
     u"> ★★ **第五拍体位**",
     u">   `base.html` 仍**逐字节不变**（472150 字符）。第六拍产物 **921730 → 925776 字符（+4046；相对 HEAD +126545）**。\n"
     + SEG7 +
     u"> ★★ **第五拍体位**", 1),

    # 累计链
    (u">   → **920259**（第四拍 +25343）→ **921730**（第五拍 +1471）→ **925776 Unicode 字符**（第六拍 +4046）；\n"
     u">   **相对 HEAD 合计 +126545**。UTF-8 字节（LF 归一）870627 → 952672 → 976078 → 1004420 → 1006094 → **1012253**；工作区字节（CRLF）947490 → 958664 → 979610 → 1011192 → 1012899 → **1019153**；LF `sha1 6655f13a1afd`。",
     u">   → **920259**（第四拍 +25343）→ **921730**（第五拍 +1471）→ **925776**（第六拍 +4046）→ **927464 Unicode 字符**（第七拍 +1688）；\n"
     u">   **相对 HEAD 合计 +128233**。UTF-8 字节（LF 归一）870627 → 952672 → 976078 → 1004420 → 1006094 → 1012253 → **1015265**；工作区字节（CRLF）947490 → 958664 → 979610 → 1011192 → 1012899 → 1019153 → **1022207**；LF `sha1 79aa4533761b`。", 1),

    (u"> 工作区（未提交）：**只有 `M pages/conversation.html`（925776 字符）+ `?? mg-work/r107/`**\n"
     u">   —— **`base.html` 与 8 个外壳页逐字节不变**（因为 nav 块沿用 `r106-nav-js`；`apply107` 跑完打印「base.html 已是目标态」）。",
     u"> 工作区（未提交）：**`M pages/conversation.html`（927464 字符）+ `M pages/avatar.html`（`+1 / −1`，第七拍文案）+ `?? mg-work/r107/`**\n"
     u">   —— **`base.html` 逐字节不变**；8 个外壳页里**只有 `avatar.html` 因第七拍文案动了 1 处**，其余 7 页不动\n"
     u">   （nav 块沿用 `r106-nav-js`；`apply107` 跑完打印「base.html 已是目标态」）。", 1),

    (u"**只有 `M pages/conversation.html`（925776 字符）+ `?? mg-work/r107/`** —— **base.html 与 8 个外壳页逐字节不变**。",
     u"**`M pages/conversation.html`（927464 字符）+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`** —— **base.html 逐字节不变**（8 个外壳页里只有 avatar.html 因文案动 1 处，其余 7 页不动）。", 1),

    (u"**2026-10-01.md 续记 r106 + r107（六拍）**", u"**2026-10-01.md 续记 r106 + r107（七拍）**", 1),

    (u"共**六拍**）—— **新一代（r106 已交付 `4d081ba`），🚫 未提交**",
     u"共**七拍**）—— **新一代（r106 已交付 `4d081ba`），🚫 未提交**", 1),

    (u"> 完整版见 `mg-work/r107/acceptance.md`（**十一节**，含第二 ~ 六拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.42**；",
     u"> 完整版见 `mg-work/r107/acceptance.md`（**十二节**，含第二 ~ 七拍返工）；机制级教训见 PLAYBOOK **P3.39 ~ P3.43**；", 1),

    (u"→ 921730（第五拍 +1471）→ 925776（第六拍 +4046，合计 +126545）**；",
     u"→ 921730（第五拍 +1471）→ 925776（第六拍 +4046）→ 927464（第七拍 +1688，合计 +128233）**；", 1),

    (u"UTF-8 字节（LF 归一）870627 → 952672 → 976078 → 1004420 → 1006094 → **1012253**；工作区字节（CRLF）958664 → 979610 → 1011192 → 1012899 → **1019153**。**另 9 页逐字节不变。**",
     u"UTF-8 字节（LF 归一）870627 → 952672 → 976078 → 1004420 → 1006094 → 1012253 → **1015265**；工作区字节（CRLF）958664 → 979610 → 1011192 → 1012899 → 1019153 → **1022207**。**另 8 页逐字节不变**（仅 avatar.html 文案动了 1 处）。", 1),

    # 第七拍详情段 + 七查
    (u"**⑤ 六查（全绿 · 六拍各跑一遍）**：幂等 ✓（**每拍连跑两遍**，第二遍「已是目标态」）｜\n"
     u"`check-syntax.py pages/*.html` **10/10 通过**（conversation `script=9 style=16`，六拍不变）｜",
     DETAIL7 +
     u"**⑤ 七查（全绿 · 七拍各跑一遍）**：幂等 ✓（**每拍连跑两遍**，第二遍「已是目标态」）｜\n"
     u"`check-syntax.py pages/*.html` **10/10 通过**（conversation `script=9 style=16`，七拍不变）｜", 1),
]


def main():
    b = io.open(P, 'rb').read()
    t = b.decode('utf-8')
    for old, new, want in TABLE:
        n = t.count(old)
        if n != want:
            sys.exit(u'!! 锚点命中 %d 次（应 %d 次）：%r' % (n, want, old[:70]))
        t = t.replace(old, new)
    io.open(P, 'wb').write(t.encode('utf-8'))
    t2 = t.replace('\r\n', '\n')
    print(u'   HANDOFF.md %d 字符 → %d 字符' % (len(b.decode('utf-8').replace('\r\n', '\n')), len(t2)))
    for k in [u'七拍', u'第七拍', u'927464', u'1022207', u'1015265', u'79aa4533761b', u'128233', u'七查', u'P3.43']:
        print(u'   %s x %d' % (k, t2.count(k)))
    for k in [u'925776 字符）+ `?? mg-work/r107/`', u'六拍**', u'六查']:
        c = t2.count(k)
        print(u'   残留 %r x %d' % (k, c))


if __name__ == '__main__':
    main()
