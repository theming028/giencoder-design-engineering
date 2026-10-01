# -*- coding: utf-8 -*-
"""r107 第七拍 · 刷新 `.workbuddy/memory/PAGES.md`（P3.11i 拍次 + 固定事实 + 必看）与 `PLAYBOOK.md`（P3.43）。
用法： python mg-work/r107/ev/doc107h3.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PAGES = os.path.join(REPO, '.workbuddy', 'memory', 'PAGES.md')
PLAY = os.path.join(REPO, '.workbuddy', 'memory', 'PLAYBOOK.md')

# ---------------- PAGES.md ----------------
PAGES_TABLE = [
    (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 · 复刻 Codex 右栏 · 2026-10-01 · **共六拍**）',
     u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 · 复刻 Codex 右栏 · 2026-10-01 · **共七拍**）', 1),

    (u'> **⑥ 底部统计行「框选不到」实为 CSS 生成内容 → 换真 DOM / `.r93-pre` 去字体族 / 内容列变窄时技能浮窗与 `.r93-alert` 自适应**\n'
     u'> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一节）。',
     u'> **⑥ 底部统计行「框选不到」实为 CSS 生成内容 → 换真 DOM / `.r93-pre` 去字体族 / 内容列变窄时技能浮窗与 `.r93-alert` 自适应** ·\n'
     u'> **⑦ 右栏里的竞品名全换 GienCoder / 去掉下拉菜单的标题行与快捷键提示 / 选中项补底色 / 提交卡输入框拉通 / 右栏字体统一 / 全屏按钮随右栏联动**\n'
     u'> （详见 `acceptance.md` 第七 / 八 / 九 / 十 / 十一 / 十二节）。', 1),

    # 固定事实表尾追加四行
    (u'| **内容列变窄时自适应** | ★ **第六拍 ⑱**：技能选择浮窗 `html[data-r93-page=\'conversation\'] .giencoder-select[role=\'listbox\'][aria-label=\'技能选择\'] { width: min(760px, 100%) !important }`（React **行内**写死 760 ⇒ 必须 `!important`；包含块 = 输入卡）；`.r93-alert` 由定高',
     u'| **内容列变窄时自适应** | ★ **第六拍 ⑱**：技能选择浮窗 `html[data-r93-page=\'conversation\'] .giencoder-select[role=\'listbox\'][aria-label=\'技能选择\'] { width: min(760px, 100%) !important }`（React **行内**写死 760 ⇒ 必须 `!important`；包含块 = 输入卡）；`.r93-alert` 由定高', 1),
]

PAGES_APPEND_ROW = u"""| **下拉菜单的「标题行 / 快捷键」** | ★ **第七拍 ⑲⑳**：两者都**隐藏** —— `.td-browse .td-mm-cap, .td-browse .td-ctx-head { display:none }` 与 `.td-browse .td-mm-key, .td-browse .td-ctx-key { display:none }`。⚠ 各自都有**两类来源**（静态 HTML + `panel.js` 现场生成）⇒ 只改 HTML 治不全，一律用 CSS 关 |
| **选中项底色** | ★ **第七拍 ㉑**：`.td-…menu .giencoder-dropdown-item.is-checked { background: var(--color-primary-light-1) }` —— 原来只有主色文字 + ✓（实测 `rgba(0,0,0,0)`）；规则写在 `:hover` **之后** ⇒ 悬停选中项不翻成 hover 灰；**不补** 3px 左缘条（那是 Menu 族的表达） |
| **提交卡「目标分支」输入框** | ★ **第七拍 ㉑**：`.giencoder-input-wrapper.td-commit-in { display: flex }` —— DS 编译样式是 `inline-flex; width:auto; min-width:120px` ⇒ 原来只有 207（同卡 `.td-commit-h/-lb/-msg/-f` 都是 308） |
| **右栏字体族** | ★ **第七拍 ㉒**：`panel.css` 自己那 8 条写死的等宽族就地换 `var(--font-family)`（`.td-diff-path` / `.td-diff-stat` / `.td-dr` / `.td-dsc-c` / `.td-diff-more` / `.td-commit-num` / `.td-term` / `.td-url-pill input`）；「文件」模块代码区那条在 **r102 代已交付的 `part105/browse.css`** 里 ⇒ 用 `.td-browse .td-browse-pre { font-family: var(--font-family) }` 覆盖（153 个 `.td-code*` 靠继承） |
| **全屏按钮联动** | ★ **第七拍 ㉓**：`.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }` —— 右栏展开时隐藏、收起复现。**纯 CSS 即可**（实测 `.av-browse-on` 挂在 shell flex 行 = `main` 与预览栏的共同父级上，按钮在其内）；⚠ 只针对这一枚，别用 `.r93-baracts` 整组 |
| **右栏竞品名** | ★ **第七拍 ⑲**：右栏里**渲染成文字**的 8 处 + 两处悬停 `title` 全部换成 GienCoder；**三条 `td-sum-src` 外链 `href` 与历代设计来源注释有意保留**（URL 替换即 404、且不渲染） |
"""

PAGES_APPEND2 = u"""7. ★★ **「不该出现在右栏里的词 / 字体」三查**（第七拍）—— 改这一块之后跑一遍：
   · `TreeWalker(SHOW_TEXT)` 走 `.td-browse`，正则 `/codex|chat\\s?gpt/i` ⇒ 渲染文字应为 **0**；
   · `panel.css` 里 `ui-monospace` 应只剩 **1 处**（第 11 节的说明注释，不是声明）；
   · `.td-browse *` 里 `getComputedStyle(el).fontFamily !== bodyFont` 的元素数应为 **0**。
   ⚠ 同名前缀的还有**别的页**：`grep -i codex pages/*.html` 扫一遍再决定（第七拍就在 `avatar.html` 挖到 1 处）。
8. ★★ **下拉菜单的「标题行 / 快捷键提示」各有两类来源**（静态 HTML + `panel.js` 现场生成）⇒
   只改 HTML 治不全 —— 一律用 CSS 的 `display:none` 关（column flex 里塌行不占位，与删节点视觉等价）。
   ★ 同理：**联动显隐（第七拍 ⑦）先量状态类挂在哪一级**，能 CSS 就别写 JS（见 PLAYBOOK P3.43④⑤）。
"""

# ---------------- PLAYBOOK.md ----------------
PLAY_TABLE = [
    (u'⇒ `apply107.py` 仍是「apply106 + **11 处替换**」的干净产物，`_head.html` / `_mods.html` 未动',
     u'⇒ `apply107.py` 是「apply106 + **11 处替换**」（第七拍增至 **13 处**）的干净产物，`_head.html` / `_mods.html` 未动', 1),
]

P343 = u"""
### P3.43 r107 第七拍（竞品名清除 / 菜单标题与快捷键 / 选中底色 / 输入框拉通 / 字体统一 / 全屏联动 · 2026-10-01 12:1x）—— ★ 六条新教训

#### ① ★★ 「渲染出来的字」与「渲染不出来的字」要分开判

用户说「全局去掉 X 这个词」时，先把页面里 X 的出现**分类**，再决定动不动：

| 类别 | 动不动 | 为什么 |
|---|---|---|
| 渲染成页面文字（文本节点 / `title`） | **必改** | 用户看得见 |
| 外链 `href` / `src` 里的同名词 | **不改** | 替换域名段直接 404；且不渲染成页面文字 |
| 历史上写下的**设计来源注释** | **保留** | 是后续维护者判断「照谁做的」的唯一线索 |

**判据配方**：

```js
var w = document.createTreeWalker(document.querySelector('.td-browse'), NodeFilter.SHOW_TEXT), n, c = 0;
while ((n = w.nextNode())) if (/codex|chat\\s?gpt/i.test(n.nodeValue)) c++;      // 渲染文字
document.querySelectorAll('.td-browse *').forEach(function (e) {               // 属性（排除 href/src）
  for (var i = 0; i < e.attributes.length; i++) {
    var a = e.attributes[i];
    if (a.name !== 'href' && a.name !== 'src' && /codex|chat\\s?gpt/i.test(a.value)) c++;
  }
});
```

★ **顺手反查别的页**：本拍在 `avatar.html`（历史会话列表）里还挖出一处 ——
`re.findall('codex', io.open(p).read(), re.I)` 扫一遍 `pages/*.html` 就能列全，别只盯着用户当前看的那一页。
★ **自己新增的注释一律避开被清理的词**，否则「清理这件事」的文档本身又把它引入了。

#### ② ★★ 同一处改动要先判「节点从哪来」：静态 HTML vs JS 现场生成

本拍的下拉菜单标题行有**两类来源**：

- 静态 HTML：`.td-mm-cap`（写死在 `_head.html` / `_mods.html` 里）
- **JS 现场生成**：`.td-ctx-head`（`ctxBuild()` 里 `createElement`）

⇒ **只删 HTML 治不了后者**。正解 = 一段 CSS 把两类一起关：

```css
.td-browse .td-mm-cap,
.td-browse .td-ctx-head { display: none; }
```

**为什么 `display:none` 而不是删节点**：① 两类来源一处管；② 菜单是 `flex-direction: column`，
塌掉的行**不参与布局** ⇒ 与真删节点**视觉完全等价**；③ 幂等友好（不依赖 HTML 片段的内容，跨代复用更安全）。

#### ③ ★ DS 组件「宽度不拉通」先查它自己的 `display`

本拍那条输入框挂 `.giencoder-input-wrapper`，**编译样式本身就是 `display: inline-flex; width: auto; min-width: 120px`**
⇒ 宽度只吃内容自然宽（实测同卡别的行都是 **308**、它只有 **207**）。

**修法要点**：
- 一行 `display: flex` 就够（内部 `prefix + input` 的排布一字不用动）。
- **写双类**（`.giencoder-input-wrapper.td-commit-in`，(0,2,0)）⇒ 不依赖「panel.css 在文档序最后」这条约定。
- 判据读**同级兄弟的宽度** ⇒ 一眼看出谁短了（这比读自己的 `getComputedStyle().width` 更直观）。

#### ④ ★★ 「统一字体族」要分清「本代自己的样式」与「跨代沿用的移植件」

本拍要把整个右栏的字体统一成全局默认族，落到两处：

1. `panel.css` 自己那 **8 条**写死的等宽族 ⇒ **就地改**（本拍：8 处 `ui-monospace, …` → `var(--font-family)`）。
2. 「文件」模块代码区那条在 **r102 代已交付的 `mg-work/r102/part105/browse.css`** 里
   （跨代沿用，**不回改已交付的代**）⇒ 只能在本页**多一级类数覆盖**：`.td-browse .td-browse-pre { font-family: var(--font-family) }`。

★ **这条是「改完第一遍、量出来才补的」**：首轮只改了 panel.css 里那 8 条，量到
「`.td-browse *` 里还有 **153 个**元素落等宽」⇒ 再往下查才定位到移植件。
**教训：判据要覆盖「整棵子树」，不能只验「我改过的那些选择器」。**

```js
var bf = getComputedStyle(document.body).fontFamily, c = 0, g = {};
document.querySelectorAll('.td-browse *').forEach(function (e) {
  if (getComputedStyle(e).fontFamily !== bf) { c++; var k = e.tagName + '.' + e.className.split(' ')[0]; g[k] = (g[k] || 0) + 1; }
});
// c 应为 0；不为 0 时**按 tagName + className 分组** ⇒ 一眼看出剩下的都挂在哪个父级上（本拍：153 全在 .td-browse-pre 下）
```

#### ⑤ ★★ 联动显隐先找「状态类挂在哪一级」—— 能 CSS 就别 JS

本拍要「右栏展开时隐藏页头那枚全屏按钮」。**先量状态类挂在哪**：

```js
document.getElementById('av-browse-slot').parentElement.className
// ⇒ "flex min-h-0 flex-1 pb-2 pl-3 pr-2 av-browse-on"
```

它挂在 **shell 的 flex 行**上，而按钮在 `main` 里 ⇒ 是它的**后代** ⇒ **纯 CSS 可判**：

```css
.av-browse-on .r93-baract[data-r93-fullscreen] { display: none; }
```

⇒ **省掉一整个 MutationObserver / 事件联动**。
⚠ **只写你要的那一枚**（`[data-r93-fullscreen]`），别用 `.r93-baracts` 整组 —— 组里有几枚就先数一遍
（本拍是 2 枚：全屏 + 开关侧栏，只隐藏前者）。

#### ⑥ 本拍门禁 / 体位

幂等 ✓（第二遍「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 与 `vd-r107c.txt` **逐字节相同**
（md5 `3dbf654337559509110899e48bef1b1c`）⇒ 零新增｜改动面 = `M pages/conversation.html`（`+2244 / −3`）
+ `M pages/avatar.html`（`+1 / −1`）+ `?? mg-work/r107/`；`base.html` 472150 字符**逐字节不变**。
产物 **925776 → 927464 字符（+1688）**。

★ **体位小改**：与前六拍「源件一字未动」不同，本拍**动了 `_mods.html` 的文案** ⇒
`browse.html` 由 71538 → 71578（+40）⇒ `apply107.py` 的 EDITS 由 **11 处增至 13 处**
（新增 `2d)` 正向 + 逆操作，改 `avatar.html` 那一处 —— 先例见 `apply106.py` 的 `2b)`）。
⚠ **跨页文案替换的锚点用「带引号的整串」**（`'…自定义大模型方法'`）⇒ 不碰同名注释、天然幂等。
⚠ **写回时必须 `newline=''` / 走二进制**：本仓页面是 **CRLF**，用默认 `'w'` 打开会把读到已归一化的
`\\n` 全部按平台默认写回 —— 内容没变、整页却全变 `M`（这坑与 P3.38 的「口径」是一对）。

★ **一次性文档脚本也属「动手记录」**：`patch107h*.py` / `doc107h*.py` 放 `ev/`，
并与探针、裁片一起列进 HANDOFF（下次返工顺着它们就能看清「这拍到底改了什么」）。
"""


def apply(path, table, label):
    b = io.open(path, 'rb').read()
    t = b.decode('utf-8')
    for old, new, want in table:
        n = t.count(old)
        if n != want:
            sys.exit(u'!! %s 锚点命中 %d 次（应 %d 次）：%r' % (label, n, want, old[:70]))
        t = t.replace(old, new)
    io.open(path, 'wb').write(t.encode('utf-8'))
    return len(b.decode('utf-8').replace('\r\n', '\n')), len(t.replace('\r\n', '\n'))


def main():
    a, b = apply(PAGES, PAGES_TABLE, 'PAGES')
    # 固定事实表尾：插在「内容列变窄时自适应」那一行的行尾之后
    t = io.open(PAGES, 'rb').read().decode('utf-8')
    lines = t.split('\n')
    hit = None
    for i, l in enumerate(lines):
        if l.startswith(u'| **内容列变窄时自适应**'):
            hit = i
    if hit is None:
        sys.exit(u'!! PAGES 找不到「内容列变窄时自适应」行')
    lines.insert(hit + 1, PAGES_APPEND_ROW.rstrip('\n'))
    t = '\n'.join(lines)
    # 必看段：追加在「6. ★★ `+` 菜单只有五项」那一条之后（该条是最后一条）
    anchor = u'   第三拍已把它全链路删除 ⇒ 页面里 `td-side` / `AV_SVG` / 「侧边聊天」四个字**应全为 0**。\n'
    if t.count(anchor) != 1:
        sys.exit(u'!! PAGES 必看段锚点命中 %d 次' % t.count(anchor))
    t = t.replace(anchor, anchor + PAGES_APPEND2, 1)
    io.open(PAGES, 'wb').write(t.encode('utf-8'))
    c, d = a, len(t.replace('\r\n', '\n'))
    print(u'   PAGES.md %d → %d 字符' % (c, d))
    for k in [u'共七拍', u'第七拍 ⑲', u'第七拍 ㉓', u'不该出现在右栏里的词']:
        print(u'     %s x %d' % (k, t.count(k)))

    a2, b2 = apply(PLAY, PLAY_TABLE, 'PLAYBOOK')
    t2 = io.open(PLAY, 'rb').read().decode('utf-8')
    if u'### P3.43 ' in t2:
        print(u'   PLAYBOOK.md P3.43 已存在，跳过')
    else:
        t2 = t2.rstrip('\n') + u'\n' + P343
        io.open(PLAY, 'wb').write(t2.encode('utf-8'))
    print(u'   PLAYBOOK.md %d → %d 字符' % (a2, len(t2.replace('\r\n', '\n'))))
    for k in [u'P3.43 ', u'13 处']:
        print(u'     %s x %d' % (k, t2.count(k)))


if __name__ == '__main__':
    main()
