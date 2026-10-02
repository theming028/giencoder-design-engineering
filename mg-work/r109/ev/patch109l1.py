# -*- coding: utf-8 -*-
"""r109 第一拍（第一层补丁）—— 邵先生四条：

  ① **删掉 `td-page-blank` 容器**（浏览器模式下那条 26px 演示灰带）。
     DOM 侧已在 `part109/_mods.html` 删净；这里删掉 `panel.css` 里配套的那条规则，不留死规则。

  ② **`td-annot-bar` 从底部挪到顶部**（「不容易被注意到」）。
     ⚠ 只把 `bottom: 0` 改成 `top: 0` **不够**：`position: sticky` 的 `top` 只在元素位于
       「滚动容器里首个可滚动子件」之前才追得上 —— 它原来是 `.td-view` 的**末位子件**。
       DOM 侧已同步把它挪成 `.td-view` 的**首位子件**（`_mods.html`），两处一起才生效。

  ③ **`td-url-annot` 进入批注模式后变红色系的「退出批注」**。
     「浅底红 + 红字」= 底 `--color-danger-light-1`（red-1 `#FFECE8`）+ 字 `--color-danger-6`
     （red-6 `#F53F3F`）；文案「标注 ⇄ 退出批注」的切换在 `panel.js` 的 `setAnnot()`。

  ④ **`td-elnote` 按邵先生自己的三张 MasterGo 稿重做**（`file=193158744355579` /
     `page_id=1119:15374`，导出 PNG 均按 scale=2 逐像素量过）：
       稿1 `1409:18319` 初始态 356×48 —— pin 24×24 + 12 缝 + 卡 320×48
       稿2 `1204:18467` 输入态 356×108 —— 卡 = 输入区 296×44 + 12 缝 + 底行 296×28
       稿3 `1409:18332` 已批注锚点 24×24 —— 与 pin 同形，实心主色 + 白数字 12/16/500
     ★ 卡的内距是 **12 = 1px 描边 + 11px padding**：稿2 的底行写的是 `left:12 width:296`，
       从**描边外沿**起算；全局 `box-sizing: border-box` 下只有 padding 11 才对得上。
     ★ 高度公式（邵先生：「按行数算，1 行=86」）= 12 + 22n + 12 + 28 + 12：
       空态 48、1 行 86、2 行（稿2）108；封顶 200 之后输入区自己滚。

★ 体位与硬规则：
  · r108 已交付并封板（`172e580`）⇒ 本拍是**新代数 r109**，不是就地返工。
  · 硬规则 22「双层产物只能下→上改」⇒ 改序：
      1. `mg-work/r109/part109/_head.html`   （本拍无改动 —— 一字未动）
      2. `mg-work/r109/part109/_mods.html`   （①② 已在上一段落好：删灰带 + 标注条置首）
      3. `mg-work/r109/part109/panel.css`    ← 本补丁
      4. `mg-work/r109/part109/panel.js`     ← 本补丁
      5. `python mg-work/r109/ev/splice109.py`  → 重建 `part109/browse.html`
      6. `python mg-work/r109/apply109.py`      → 落 `pages/conversation.html`

★ 各层的 `mark` 是「后一层必须替前一层保住」的契约：本层是新代数的第一层，
  只往 `panel.css` / `panel.js` 里插 `r109-l1` 标记，r93~r108 的标记一个不碰
  （收尾有跨层兜底断言）。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P109 = os.path.join(REPO, 'mg-work', 'r109', 'part109')
PCS = os.path.join(P109, 'panel.css')
PJS = os.path.join(P109, 'panel.js')
MODS = os.path.join(P109, '_mods.html')

APPLIED = []
SKIPPED = []
STRICT = True
CHECK = False      # --check：只验锚点，不落盘


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    if CHECK:
        return
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
    print('   %s  %s（%d → %d 字符）'
          % ('校验' if CHECK else '应用', label, len(t), len(t) - len(old) + len(new)))


# ================================================================================
# ① ② ③ ④  panel.css
# ================================================================================
CSS_BLANK_OLD = '''.td-page-blank {
  height: 26px; margin: -12px -12px 12px;
  background: var(--color-fill-2);
}
'''

CSS_BLANK_NEW = '''/* r109-l1 · ① td-page-blank 已删 */
/* ★ r109-l1 ①（邵先生：「右栏浏览器模式下，`td-page-blank` 这个容器要删除」）：
   这里原有那条 26px 高的演示用灰带 —— `.td-page` 的负外边距 `-12px -12px 12px`
   就是专门为它通栏写的。DOM 侧（`_mods.html`）与规则一起删，不留死规则。 */
'''

CSS_BAR_OLD = '''.td-annot-bar {
  position: sticky; bottom: 0; z-index: 2;
'''

CSS_BAR_NEW = '''/* r109-l1 · ② 标注条改贴顶 */
/* ★ r109-l1 ②（邵先生：「`td-annot-bar` 这个容器要显示到上面去，不要显示在下面，
   不容易被注意到」）：`bottom: 0` → `top: 0`。
   ⚠ 只改这一行**不够** —— `position: sticky` 的 `top` 只在元素位于「滚动容器里首个
     可滚动子件」之前才追得上；它原来是 `.td-view` 的**末位子件**（贴在末尾时 sticky 的
     `top` 永远追不上滚动）。DOM 侧已同步把它挪成 `.td-view` 的**首位子件**，
     两处一起才生效（真机取证见 acceptance 第二节）。 */
.td-annot-bar {
  position: sticky; top: 0; z-index: 2;
'''

CSS_ANNOT_OLD = '''.td-url-annot[aria-pressed='true'] {
  border-color: transparent;
  background: var(--color-primary-1); color: var(--color-primary-6);
}
'''

CSS_ANNOT_NEW = '''/* r109-l1 · ③ 批注态按钮转红 */
/* ★ r109-l1 ③（邵先生：「`td-url-annot` 这个批注按钮，在进入批注模式后，按钮就变成
   红色系的『退出批注』按钮」；追问后定色 = **浅底红 + 红字**）：
     底 `--color-danger-light-1`（red-1 = `#FFECE8`）+ 字 `--color-danger-6`（red-6 = `#F53F3F`）。
   文案「标注 ⇄ 退出批注」的切换在 `panel.js` 的 `setAnnot()`。
   ⚠ 这条与上面的 `.td-url-annot:hover` **特异性打平**（都是 (0,2,0)），靠文档序取胜
     ⇒ 批注态下 hover 也保持红 —— 「退出」是当前态，不该在 hover 时退回中性色。
   ⚠ 只改 `.td-url-annot`：标注条里那枚「完成」按钮也带 `data-td-annot`，但它是条内的
     动作、不是「批注开关」，按「不得改动不必涉及的模块」不动。 */
.td-url-annot[aria-pressed='true'] {
  border-color: transparent;
  background: var(--color-danger-light-1); color: var(--color-danger-6);
}
'''

# ---- ④ 元素评论气泡：整块替换 ----------------------------------------------------
CSS_ELNOTE_OLD = '''/* 元素评论气泡 */
.td-elnote {
  position: absolute; z-index: 3; left: 12px; right: 12px;
  padding: 10px 12px;
  background: var(--color-bg-popup);
  border: 1px solid var(--color-primary-6);
  border-radius: 8px;
  box-shadow: var(--shadow3-down);
}
.td-elnote[hidden] { display: none; }
.td-elnote-t { margin-bottom: 6px; font-size: var(--font-size-body-1); color: var(--color-text-3); }
.td-elnote-t b { color: var(--color-primary-6); font-weight: 500; }
.td-elnote textarea {
  display: block; width: 100%; box-sizing: border-box; resize: none;
  padding: 6px 8px; border: 1px solid var(--color-border-2); border-radius: 6px;
  background: var(--color-bg-2); color: var(--color-text-1);
  font-family: inherit; font-size: var(--font-size-body-1); line-height: 1.5;
}
.td-elnote textarea:focus { outline: none; border-color: var(--color-primary-6); }
.td-elnote-f { display: flex; justify-content: flex-end; gap: 6px; margin-top: 8px; }
.td-elnote-f button {
  height: calc(26px * var(--ui-fs-ratio)); padding: 0 12px;
  border: 1px solid var(--color-border-2); border-radius: 6px;
  background: transparent; color: var(--color-text-1);
  font-size: var(--font-size-body-1); cursor: pointer;
}
.td-elnote-f button.is-primary { background: var(--color-primary-6); border-color: transparent; color: var(--color-white); }
'''

CSS_ELNOTE_NEW = '''/* r109-l1 · ④ 元素评论气泡 + 已批注锚点（邵先生三稿重做） */
/* ★ r109-l1 ④（邵先生：「这个发起批注 `td-elnote` 的设计请使用我自己的设计方案……
   请精确的像素级还原」）。三张稿：`file=193158744355579`、`page_id=1119:15374`，
   导出 PNG 都是 scale=2，下面每个数都是从 PNG 上逐像素量出来的：
     稿1 `1409:18319` 初始态 356×48 —— pin 24×24 + 12 缝 + 卡 320×48
     稿2 `1204:18467` 输入态 356×108 —— 卡 = 输入区 296×44 + 12 缝 + 底行 296×28
     稿3 `1409:18332` 已批注锚点 24×24 —— 与 pin 同形，实心主色 + 白数字 12/16/500
   ★ 卡的内距是 **12 = 1px 描边 + 11px padding**：稿2 的底行写的是 `left:12 width:296`，
     从**描边外沿**起算；全局 `box-sizing: border-box` 下只有 padding 11 才对得上
     （量到的正文墨迹左沿也正是卡左 + 13 = 描边 1 + 内距 12）。
   ★ 高度公式（邵先生：「按行数算，1 行=86」）= 12 + 22n + 12 + 28 + 12：
     空态 48、1 行 86、2 行（稿2）108；封顶 200 之后输入区自己滚。
   ⚠ 唯一已知偏差：稿1 的「添加」停在卡右缘内 **10px**、稿2 的「添加」停在 **12px** ——
     同一枚按钮在手放的两稿里差 2px，本层统一取 12（稿2 那侧是自动布局值），
     见 acceptance 第四节的逐像素对照。 */
.td-elnote {
  position: absolute; z-index: 3; left: 12px;
  width: 356px; max-width: calc(100% - 24px);
  display: flex; align-items: flex-start; gap: 12px;
}
.td-elnote[hidden] { display: none; }

/* ① pin（未批注）：白底 + 2px 主色描边 + 中心 6px 实心点；**左下角纯直角**、其余三向
   12 圆角（稿子的元图就是这个形：`border-radius: 12px 12px 12px 0`）。
   稿1 / 稿2 的 pin 都在 `top: 12` —— 正对卡片内容区上沿（也就是正文首行）。 */
.td-elnote-pin {
  flex: none; position: relative; box-sizing: border-box;
  width: calc(24px * var(--ui-fs-ratio));
  height: calc(24px * var(--ui-fs-ratio));
  margin-top: calc(12px * var(--ui-fs-ratio));
  border: 2px solid var(--color-primary-6);
  border-radius: calc(12px * var(--ui-fs-ratio)) calc(12px * var(--ui-fs-ratio)) calc(12px * var(--ui-fs-ratio)) 0;
  background: var(--color-bg-2);
  font-size: var(--font-size-body-1);
}
.td-elnote-pin::after {
  content: ''; position: absolute; left: 50%; top: 50%;
  width: calc(6px * var(--ui-fs-ratio)); height: calc(6px * var(--ui-fs-ratio));
  margin: calc(-3px * var(--ui-fs-ratio)) 0 0 calc(-3px * var(--ui-fs-ratio));
  border-radius: 50%; background: var(--color-primary-6);
  /* ⚠ 本规则体含 `height: calc(...)` ⇒ 必须同时声明字号 token（同上；`scan-flatten.py`
     会数这一条，基线是 2 条 —— 别把 `.td-elnote-pin::after` 变成第 3 条）。 */
  font-size: var(--font-size-body-1);
}
/* ③ 已批注：与稿3 同一枚 —— 整块实心主色 + 白数字。
   稿3 把数字写成 `left:9px top:4px` 的绝对定位，那是「24 盒里居中一个单字」的产物
   ⇒ 这里直接用 flex 居中表达同一件事，两位数也不会跑偏。 */
.td-elnote-pin.is-done {
  display: flex; align-items: center; justify-content: center;
  background: var(--color-primary-6); color: var(--color-white);
  font-size: var(--font-size-body-1); font-weight: 500;
  line-height: calc(16px * var(--ui-fs-ratio));
}
.td-elnote-pin.is-done::after { content: none; }
/* 已批注落在被标注元素右上角的那一枚（与稿3 同形同色）。
   ⚠ 本规则体含 `height: calc(...)` ⇒ **必须**同时声明字号 token，否则收尾的
     `apply88b.converge()` 会把 calc 压平成裸 px（`scan-flatten.py` 会抓这条）。 */
.td-anchor {
  position: absolute; z-index: 2; box-sizing: border-box;
  width: calc(24px * var(--ui-fs-ratio));
  height: calc(24px * var(--ui-fs-ratio));
  border: 2px solid var(--color-primary-6);
  border-radius: calc(12px * var(--ui-fs-ratio)) calc(12px * var(--ui-fs-ratio)) calc(12px * var(--ui-fs-ratio)) 0;
  display: flex; align-items: center; justify-content: center;
  background: var(--color-primary-6); color: var(--color-white);
  font-size: var(--font-size-body-1); font-weight: 500;
  line-height: calc(16px * var(--ui-fs-ratio));
}

/* ② 卡片：320 宽 / 白底 / 1px `--color-border-2` / 8 圆角 / `0 4px 12px rgba(0,0,0,.08)`。
   ⚠ 影子走 DS 的 `--shadow2-down`（`0 4px 10px #0000001a`）：**偏移与稿子同为 4px**，
     模糊 10 vs 12、透明度 10% vs 8% —— 8% 那一档本页没有对应 token，不为它新造 hex。 */
.td-elnote-card {
  flex: 1 1 auto; min-width: 0; box-sizing: border-box;
  display: flex; flex-direction: row; align-items: center; gap: 12px;
  height: calc(48px * var(--ui-fs-ratio));            /* 稿1：空态卡高 48 */
  max-height: calc(200px * var(--ui-fs-ratio));       /* 邵先生：最高撑到 200，溢出内滚 */
  overflow: hidden;
  padding: 11px;                                      /* + 1px 描边 = 12，对齐稿子的内距 */
  border: 1px solid var(--color-border-2); border-radius: 8px;
  background: var(--color-bg-2); box-shadow: var(--shadow2-down);
  font-size: var(--font-size-body-3);
}
/* 有内容（稿2）：改成纵列，高度交给输入区撑 —— 1 行 86、2 行 108… */
.td-elnote-card.has-text {
  flex-direction: column; align-items: stretch;
  height: auto;
}
.td-elnote-input {
  display: block; flex: 1 1 auto; min-width: 0; min-height: 0; box-sizing: border-box;
  width: 100%; margin: 0; padding: 0; border: 0; outline: none;
  background: transparent; resize: none; overflow-y: auto;
  font-family: inherit; font-size: var(--font-size-body-3);
  line-height: calc(22px * var(--ui-fs-ratio));
  color: var(--color-text-1);
}
/* 纵列里输入区不抢空间（`0 1 auto`：按内容高，触顶时才收缩给自滚让路）。 */
.td-elnote-card.has-text .td-elnote-input { flex: 0 1 auto; }
/* 稿1 / 稿2 的占位与提示都是 `#A9A9A9` = `--color-neutral-5`（gray-5）。
   ⚠ 页面全局有一条 `input::placeholder, textarea::placeholder` 的灰色硬编码（尾风那档
     `gray-400`），本规则按特异性 (0,2,0) > (0,1,0) 把它压过 —— 顺带把那一处 token 缺口
     收进本页的 token 化口径（`gaps.log` 里那条历史记录因此不再需要本页承担）。 */
.td-elnote-input::placeholder { opacity: 1; color: var(--color-neutral-5); }
.td-elnote-foot {
  flex: none; box-sizing: border-box;
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
}
/* 空态（稿1）：卡里只有「占位 + 一枚禁用的添加」—— 没有提示、没有取消。 */
.td-elnote-card:not(.has-text) .td-elnote-hint,
.td-elnote-card:not(.has-text) .td-elnote-cancel { display: none; }
.td-elnote-hint {
  flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  font-size: var(--font-size-body-1);
  line-height: calc(22px * var(--ui-fs-ratio));
  color: var(--color-neutral-5);
}
.td-elnote-hint em { font-style: normal; }
/* Ctrl 按住：邵先生「按钮 + 提示都变」+「字不变，只高亮后半句」
   ⇒ 只给后半句 `<em>` 上主色，前半句的 `--color-neutral-5` 不动。 */
.td-elnote-card.is-ctrl .td-elnote-hint em { color: var(--color-primary-6); }
.td-elnote-acts { flex: none; display: flex; align-items: center; gap: 8px; }
/* 两枚按钮走 DS 组件（`giencoder-btn` + `giencoder-btn-size-small` = 28 高）。
   几何上按稿子纠三处，三处都是「DS 默认值 vs 稿子」的差：
     · 内距 12 → **11**：DS 的 `.giencoder-btn` 自带 1px 透明描边
       （`border: 1px solid #0000`）⇒ 11 + 1 = 12 才等于稿子的「2 字宽 24 + 左右各 12」= 48；
     · 字号 14（`--font-size-body-3`）→ **12**：稿子两枚都是 12px（墨迹宽 22.5 ≈ 24 − 字侧边距）；
     · 去掉 DS 给填充按钮补的那圈 1px 同色 ring（`box-shadow: 0 0 0 1px`）：
       稿子的按钮是 48×28 净尺寸，ring 会把可见范围顶成 50×30。
       `:not(:focus-visible)` 是为了**留住** `.giencoder-btn:focus-visible` 的 2px 焦点环
       —— 可访问性不能一起干掉。 */
.td-elnote-acts .giencoder-btn { padding: 0 11px; font-size: var(--font-size-body-1); }
.td-elnote-acts .giencoder-btn:not(:focus-visible) { box-shadow: none; }
/* 稿1 的「添加」是**禁用**：底 `--color-primary-2`（`#DAE4FE`）+ 白字。
   ⚠ 不是 DS 那套禁用（`.giencoder-btn[disabled]{opacity:.4}` —— 主色 40% 叠白会得到
     `#AFC6FA`，与稿子的 `#DAE4FE` 差得远）。这里换 `--btn-bg`：DS 的 primary 用
     `--btn-ring: var(--btn-bg)` + `box-shadow` 描了一圈同色，换 `--btn-bg` 会把
     底色和那圈 ring 一起换掉（自定义属性在使用时才解析）。 */
.td-elnote-ok[disabled] { --btn-bg: var(--color-primary-2); opacity: 1; cursor: default; pointer-events: none; }
/* r109-l1 */
'''

# ---- ④b 第 14 节那条「省略号」选择器组里，`.td-elnote-t` 已成死选择器 ------------------
CSS_ELLIPSIS_OLD = '''（跨代资产一律不回头改）。 */
.td-browse :is(.td-browse-tree-title, .td-diff-more, .td-diff-btn, .td-commit-btn,
               .td-commit-t, .td-commit-lb, .td-note-who, .td-note-time,
               .td-sum-tag, .td-sum-srct i, .td-sum-artt i,
               .td-elnote-t, .td-url-annot, .td-page-cta, .td-page-foot,
'''

CSS_ELLIPSIS_NEW = '''（跨代资产一律不回头改）。 */
/* ★ r109-l1 ④：选择器组里原有的 `.td-elnote-t`（旧版气泡那行「评论元素 xx」标题）
   随气泡重做一并退役 —— 留着是**死选择器**（DOM 里再没有这个类，永远匹配不到），
   按「不留死规则」摘掉。本组其余 12 条一律不动。 */
.td-browse :is(.td-browse-tree-title, .td-diff-more, .td-diff-btn, .td-commit-btn,
               .td-commit-t, .td-commit-lb, .td-note-who, .td-note-time,
               .td-sum-tag, .td-sum-srct i, .td-sum-artt i,
               .td-url-annot, .td-page-cta, .td-page-foot,
'''


def do_css():
    print('=== 1/2  panel.css（① 删灰带 · ② 标注条贴顶 · ③ 批注态转红 · ④ 评论气泡重做）===')
    edit(PCS, CSS_BLANK_OLD, CSS_BLANK_NEW, '① 删 .td-page-blank', 'r109-l1 · ① td-page-blank 已删')
    edit(PCS, CSS_BAR_OLD, CSS_BAR_NEW, '② .td-annot-bar bottom:0 → top:0', 'r109-l1 · ② 标注条改贴顶')
    edit(PCS, CSS_ANNOT_OLD, CSS_ANNOT_NEW, '③ .td-url-annot 批注态转红', 'r109-l1 · ③ 批注态按钮转红')
    edit(PCS, CSS_ELNOTE_OLD, CSS_ELNOTE_NEW, '④ .td-elnote 三稿重做', 'r109-l1 · ④ 元素评论气泡')
    edit(PCS, CSS_ELLIPSIS_OLD, CSS_ELLIPSIS_NEW, '④b 摘掉死选择器 .td-elnote-t',
         '★ r109-l1 ④：选择器组里原有的')


# ================================================================================
# ③ 文案切换 + ④ 全新交互   panel.js
# ================================================================================
JS_OLD = '''    elnote = document.createElement('div');
    elnote.className = 'td-elnote';
    elnote.setAttribute('hidden', '');
    elnote.innerHTML = '<div class="td-elnote-t">评论元素 <b></b></div>'
      + '<textarea rows="2" aria-label="元素评论" placeholder="这个元素想怎么改？"></textarea>'
      + '<div class="td-elnote-f">'
      + '<button type="button" data-td-elnote-cancel="1">取消</button>'
      + '<button type="button" class="is-primary" data-td-elnote-ok="1">添加评论</button>'
      + '</div>';
    if (view) view.appendChild(elnote);
    function setAnnot(on) {
      brw.classList.toggle('is-annotating', on);
      if (annotBar) { if (on) annotBar.removeAttribute('hidden'); else annotBar.setAttribute('hidden', ''); }
      for (var i = 0; i < annotBtns.length; i++) {
        annotBtns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
      }
      if (!on) elnote.setAttribute('hidden', '');
    }
    for (var ab = 0; ab < annotBtns.length; ab++) {
      annotBtns[ab].addEventListener('click', function () {
        setAnnot(!brw.classList.contains('is-annotating'));
      });
    }
    if (view) {
      view.addEventListener('click', function (e) {
        if (!brw.classList.contains('is-annotating')) return;
        var el = e.target && e.target.closest ? e.target.closest('[data-td-el]') : null;
        if (!el) return;
        var er = el.getBoundingClientRect(), vr = view.getBoundingClientRect();
        elnote.style.top = (er.bottom - vr.top + view.scrollTop + 8) + 'px';
        var b = elnote.querySelector('.td-elnote-t b');
        if (b) b.textContent = el.className.replace('td-page-card', '卡片').replace('td-page-cta', '主按钮') || '元素';
        elnote.removeAttribute('hidden');
      });
    }
    var noteCancel = elnote.querySelector('[data-td-elnote-cancel]');
    var noteOk = elnote.querySelector('[data-td-elnote-ok]');
    if (noteCancel) noteCancel.addEventListener('click', function () { elnote.setAttribute('hidden', ''); });
    if (noteOk) {
      noteOk.addEventListener('click', function () {
        elnote.setAttribute('hidden', '');
        setAnnot(false);
        say('评论已带入对话（视觉演示）');
      });
    }
'''

JS_NEW = '''    elnote = document.createElement('div');
    elnote.className = 'td-elnote';
    elnote.setAttribute('hidden', '');
    /* ★ r109-l1 ④（邵先生的三张 MasterGo 稿，`file=193158744355579` / `page_id=1119:15374`）：
         稿1 `1409:18319` 初始态 356×48 —— pin 24×24 + 12 缝 + 卡 320×48（占位 + 禁用「添加」）
         稿2 `1204:18467` 输入态 356×108 —— 卡 = 输入区 + 12 缝 + 底行（提示 + 取消 + 添加）
         稿3 `1409:18332` 已批注锚点 24×24 —— 与 pin 同形，实心主色 + 白数字
       结构 = `pin` 与 `card` **两个兄弟**（pin 要能独立切「已批注」实心态），几何全在 panel.css。
       ⚠ 旧版的 `.td-elnote-t`（「评论元素 xx」标题）/ `.td-elnote-f`（26 高、圆角 6、透明底）
         整套退役：稿子里没有标题行，两枚按钮也换成了 DS 组件。 */
    elnote.innerHTML =
      '<span class="td-elnote-pin" aria-hidden="true"></span>'
      + '<div class="td-elnote-card">'
      + '<textarea class="td-elnote-input" rows="1" aria-label="元素评论" placeholder="输入你的注释"></textarea>'
      + '<div class="td-elnote-foot">'
      + '<span class="td-elnote-hint">Enter添加，<em>Ctrl+Enter发送</em></span>'
      + '<span class="td-elnote-acts">'
      + '<button type="button" class="td-elnote-cancel giencoder-btn giencoder-btn-size-small '
      + 'giencoder-btn-secondary" data-td-elnote-cancel="1">取消</button>'
      + '<button type="button" class="td-elnote-ok giencoder-btn giencoder-btn-size-small '
      + 'giencoder-btn-primary" data-td-elnote-ok="1" disabled>添加</button>'
      + '</span></div></div>';
    if (view) view.appendChild(elnote);
    var noteCard = elnote.querySelector('.td-elnote-card');
    var notePin = elnote.querySelector('.td-elnote-pin');
    var noteTa = elnote.querySelector('.td-elnote-input');
    var noteOk = elnote.querySelector('[data-td-elnote-ok]');
    var noteCancel = elnote.querySelector('[data-td-elnote-cancel]');
    var noteList = [];        /* 已批注：`{ el, n, text, anchor }`，n = 下标 + 1 */
    var noteCur = null;       /* 气泡此刻挂在哪个 `[data-td-el]` 上 */
    var noteCtrlOn = false;

    function noteFind(el) {
      for (var i = 0; i < noteList.length; i++) if (noteList[i].el === el) return noteList[i];
      return null;
    }
    /* 卡高 = 12 + 输入区 + 12 + 底行 28 + 12（空态锁 48）。
       邵先生「按行数算，1 行=86」⇒ 输入区高 = 行数 × 行高；行高从 computed 取，
       `--ui-fs` 换档时自动跟着走。超过 200 的部分由卡片 `max-height` + 输入区自滚兜住
       （卡片是纵列 + 输入区 `min-height:0`，触顶时它才是那个被收缩的件）。 */
    function noteGrow() {
      var has = noteTa.value.replace(/\\s+/g, '') !== '';
      noteCard.classList.toggle('has-text', has);
      if (noteOk) noteOk.disabled = !has;
      if (!has) { noteTa.style.height = ''; return; }
      noteTa.style.height = 'auto';
      noteTa.style.height = noteTa.scrollHeight + 'px';
    }
    /* ★ r109-l1 ④：Ctrl 联动 —— 邵先生「按钮 + 提示都变」+「字不变，只高亮后半句」。
       按钮 添加 ⇄ 发送 在这里，提示后半句的高亮交给 `.is-ctrl`（panel.css）。 */
    function noteCtrl(on) {
      noteCtrlOn = on;
      noteCard.classList.toggle('is-ctrl', on);
      if (noteOk) noteOk.textContent = on ? '发送' : '添加';
    }
    function setAnnot(on) {
      brw.classList.toggle('is-annotating', on);
      if (annotBar) { if (on) annotBar.removeAttribute('hidden'); else annotBar.setAttribute('hidden', ''); }
      for (var i = 0; i < annotBtns.length; i++) {
        annotBtns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
        /* ★ r109-l1 ③：工具条那枚「标注」进入批注态后改文案为「退出批注」。
           ⚠ 只认 `.td-url-annot` —— 标注条里那枚「完成」也带 `data-td-annot`，不动它。 */
        if (annotBtns[i].classList.contains('td-url-annot')) {
          var lb = annotBtns[i].querySelector('span');
          if (lb) lb.textContent = on ? '退出批注' : '标注';
        }
      }
      if (!on) { elnote.setAttribute('hidden', ''); noteCur = null; }
    }
    for (var ab = 0; ab < annotBtns.length; ab++) {
      annotBtns[ab].addEventListener('click', function () {
        setAnnot(!brw.classList.contains('is-annotating'));
      });
    }
    /* 打开气泡：该元素**已有**批注 ⇒ pin 直接是稿3 的实心态、输入框回填原文；
       没有 ⇒ 稿1 的初始态（占位 + 禁用「添加」）。
       ★★ 顺序是硬的：**先摘 `[hidden]` 再 `noteGrow()`**。
       真机踩过（本拍第一版）：`noteGrow()` 里用 `ta.scrollHeight` 定高，而气泡此刻还在
       `display: none` 下 ⇒ `scrollHeight` **恒为 0** ⇒ 回填的长文本被压成 0 高，
       重开气泡只剩底行（卡片 48 而不是 86+）。与硬规则「摘 `[hidden]` + 挂开态类必须在
       同一 tick 之外留一次重排」同族 —— 隐藏元素量不出几何。 */
    function noteEdit(el) {
      var prev = noteFind(el);
      noteCur = el;
      noteTa.value = prev ? prev.text : '';
      notePin.textContent = prev ? String(prev.n) : '';
      notePin.classList.toggle('is-done', !!prev);
      noteCtrl(noteCtrlOn);
      var er = el.getBoundingClientRect(), vr = view.getBoundingClientRect();
      elnote.style.top = (er.bottom - vr.top + view.scrollTop + 8) + 'px';
      elnote.removeAttribute('hidden');
      noteGrow();
    }
    /* 锚点（稿3）：落在被标注元素的**右上角**（−12 = 让 24×24 的锚点中心咬住那个角）。
       ⚠ 稿子只给了锚点长相、没给落点 ⇒ 取「右上角」这个通行读法（Figma 批注同款），
         若有偏差请邵先生指定。 */
    function noteDrop(el, n) {
      var a = document.createElement('span');
      a.className = 'td-anchor';
      a.textContent = String(n);
      a.setAttribute('aria-hidden', 'true');
      var er = el.getBoundingClientRect(), vr = view.getBoundingClientRect();
      a.style.left = (er.right - vr.left + view.scrollLeft - 12) + 'px';
      a.style.top = (er.top - vr.top + view.scrollTop - 12) + 'px';
      view.appendChild(a);
      return a;
    }
    function noteCommit() {
      if (!noteCur) return;
      var text = noteTa.value.replace(/\\s+/g, '');
      if (!text) return;
      var rec = noteFind(noteCur);
      if (rec) { rec.text = text; }
      else {
        rec = { el: noteCur, n: noteList.length + 1, text: text, anchor: null };
        rec.anchor = noteDrop(noteCur, rec.n);
        noteList.push(rec);
      }
      elnote.setAttribute('hidden', '');
      noteCur = null;
      /* ★ r109-l1 ④：**不再** `setAnnot(false)`。稿3 的存在说明「加完一条留在批注模式」
         才是原意 —— 加完就退出的话，锚点根本来不及被看到。锚点常驻：它跟 Figma 批注
         一样是「页面上已经存在的意见」，不随批注模式开合。 */
      say('评论已带入对话（视觉演示）');
    }
    if (view) {
      view.addEventListener('click', function (e) {
        if (!brw.classList.contains('is-annotating')) return;
        var el = e.target && e.target.closest ? e.target.closest('[data-td-el]') : null;
        if (!el) return;
        noteEdit(el);
      });
    }
    /* ⚠ 气泡挂在 `.td-view` 里 ⇒ 它自己的点击会冒到上面那条 view 监听上，
       点「取消」会顺手把气泡重新打开。断在气泡这一层。 */
    elnote.addEventListener('click', function (e) { e.stopPropagation(); });
    noteTa.addEventListener('input', noteGrow);
    /* 稿2 的提示写的是「Enter添加，Ctrl+Enter发送」⇒ 两种回车都落到同一枚提交上
       （本页是静态演示，两者的差别只在文案）。顺手拦掉换行，免得输入框里长出一行。 */
    noteTa.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); noteCommit(); }
    });
    if (noteCancel) noteCancel.addEventListener('click', function () {
      elnote.setAttribute('hidden', ''); noteCur = null;
    });
    if (noteOk) noteOk.addEventListener('click', noteCommit);
    /* ★ r109-l1 ④：Ctrl 按住 / 松开。挂在 `document` 上 —— 邵先生的演示说的是「按下
       ctrl 键」即可，不该限定焦点在输入框里。`blur` 兜底（切走窗口时归位，免得卡在
       「发送」态）。 */
    document.addEventListener('keydown', function (e) { if (e.key === 'Control') noteCtrl(true); });
    document.addEventListener('keyup', function (e) { if (e.key === 'Control') noteCtrl(false); });
    window.addEventListener('blur', function () { noteCtrl(false); });
'''


def do_js():
    print('=== 2/2  panel.js（③ 文案切换 · ④ 气泡交互重做）===')
    edit(PJS, JS_OLD, JS_NEW, '③④ 浏览器模块重做', '★ r109-l1 ④')


# ================================================================================
# 跨层自检
# ================================================================================
def verify():
    print()
    print('=== 跨层自检 ===')
    c = rd(PCS)[0]
    j = rd(PJS)[0]
    m = rd(MODS)[0]
    bad = []
    # ★★ 断言判据不能拿「裸词」直接查 —— 说明注释里往往逐字写着被删掉的东西，
    #    一查就假报（本代在 `splice109.py` 上已踩过一模一样的坑）。统一先剥注释。
    c_bare = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
    j_bare = re.sub(r'/\*.*?\*/', '', j, flags=re.S)
    j_bare = re.sub(r'^\s*//.*$', '', j_bare, flags=re.M)

    # ① 灰带：CSS 规则与 DOM 都必须归零
    if '.td-page-blank' in c_bare:
        bad.append('panel.css：① 的 `.td-page-blank` 规则没删干净')
    if 'td-page-blank' in re.sub(r'<!--.*?-->', '', m, flags=re.S):
        bad.append('_mods.html：① 的 `<div class="td-page-blank">` 没删干净')
    if 'r109-l1 · ① td-page-blank 已删' not in c:
        bad.append('panel.css：① 的留痕注释丢了')

    # ② 标注条：CSS 贴顶 + DOM 首个子件
    if 'position: sticky; top: 0; z-index: 2;' not in c:
        bad.append('panel.css：② 的 `.td-annot-bar` 没改成 `top: 0`')
    if 'position: sticky; bottom: 0' in c_bare:
        bad.append('panel.css：② 仍有 `bottom: 0` 的 sticky')
    bare = re.sub(r'<!--.*?-->', '', m, flags=re.S)
    if 'data-td-annot-bar' not in bare:
        bad.append('_mods.html：② 的标注条不见了')
    iv, ib, ip = bare.find('class="td-view"'), bare.find('data-td-annot-bar'), bare.find('class="td-page"')
    if not (0 <= iv < ib < ip):
        bad.append('_mods.html：② 的标注条不是 `.td-view` 的首个子件（view=%d bar=%d page=%d）'
                   % (iv, ib, ip))

    # ③ 批注态转红
    sec3 = c_bare.split('.td-url-annot[aria-pressed=\'true\']')
    if len(sec3) != 2:
        bad.append('panel.css：③ 的 `.td-url-annot[aria-pressed=\'true\']` 命中 %d 次'
                   % (len(sec3) - 1))
    else:
        body3 = sec3[1].split('}')[0]
        for s in ('--color-danger-light-1', '--color-danger-6'):
            if s not in body3:
                bad.append('panel.css：③ 的红态少 `%s`' % s)
        if '--color-primary-1' in body3 or '--color-primary-6' in body3:
            bad.append('panel.css：③ 的红态里还留着旧的主色底/字')
    if '退出批注' not in j or "'标注'" not in j:
        bad.append('panel.js：③ 的「标注 ⇄ 退出批注」文案切换不在')

    # ④ 气泡
    for s in ('.td-elnote-pin {', '.td-elnote-pin.is-done {', '.td-anchor {',
              '.td-elnote-card {', '.td-elnote-card.has-text {', '.td-elnote-input {',
              '.td-elnote-foot {', '.td-elnote-hint {', '.td-elnote-acts {',
              '.td-elnote-ok[disabled] {'):
        if s not in c_bare:
            bad.append('panel.css：④ 少 `%s`' % s)
    for s in ('padding: 11px;', 'height: calc(48px * var(--ui-fs-ratio));',
              'max-height: calc(200px * var(--ui-fs-ratio));',
              'line-height: calc(22px * var(--ui-fs-ratio));',
              'width: 356px; max-width: calc(100% - 24px);'):
        if s not in c_bare:
            bad.append('panel.css：④ 少几何声明 `%s`' % s)
    for s in ('td-elnote-pin', 'td-elnote-card', 'td-elnote-foot', 'td-elnote-hint',
              'td-elnote-acts', 'td-elnote-ok', 'td-elnote-cancel', 'td-anchor',
              'noteGrow', 'noteCtrl', 'noteEdit', 'noteDrop', 'noteCommit'):
        if s not in j_bare:
            bad.append('panel.js：④ 少 `%s`' % s)
    # 旧结构必须归零（注释已剥 ⇒ 这里查到的就是真代码/真规则）。
    # ⚠ 用**词边界**查，不能用裸前缀：`.td-elnote-foot` 里含着 `.td-elnote-f`
    #   —— 第一版就是这么假报的（与「判据不能写裸词」同族，只是换成「裸前缀」）。
    for pat, label in ((r'\.td-elnote-t(?![-\w])', '.td-elnote-t'),
                       (r'\.td-elnote-f(?![-\w])', '.td-elnote-f')):
        if re.search(pat, c_bare) or re.search(pat, j_bare):
            bad.append('④ 旧结构残留 `%s`' % label)
    for s in ('<div class="td-elnote-t">评论元素', '这个元素想怎么改', '添加评论</button>'):
        if s in c_bare or s in j_bare:
            bad.append('④ 旧结构残留 `%s`' % s)
    # ⚠ `添加评论` 是**裸词**，页面上本来就有三处无关的右鍵菜单项（「在此行添加评论」等）
    #   ⇒ 只能查带上下文的那一整串（上面那条），不能查词本身。
    # ⚠ 分割锚点要用**代码**（注释已被剥掉；原来拿注释里的「浏览器模块」当锚点 ⇒ IndexError）
    seg_js = j_bare.split("var brw = pane.querySelector('.td-brw')")[-1].split('var BRW_TEXT')[0]
    if 'setAnnot(false);' in seg_js:
        bad.append('panel.js：④ noteCommit() 里还留着 `setAnnot(false);`')
    if 'noteCommit' not in seg_js:
        bad.append('panel.js：④ 浏览器模块里找不到 noteCommit（分割锚点可能失效）')

    # 命名冲突：`noteOpen` 是同文件里既有的局部变量（Esc 裁决链），本层不能用同名函数
    if 'function noteOpen' in j_bare:
        bad.append('panel.js：④ 函数名 `noteOpen` 与既有局部变量撞名（Esc 链里那处）')

    # ★★ 真机踩过的顺序坑：`noteEdit()` 里 `noteGrow()` 必须在**摘掉 `[hidden]` 之后**。
    #    隐藏态（`display:none`）下 `ta.scrollHeight` 恒为 0 ⇒ 回填的长文本被压成 0 高。
    # ⚠ r109-l2 ④ 把形参改成 `(el, at)` ⇒ 这里按**前缀**分割，两种签名都命中
    #   （后一层必须替前一层保住判据；见 patch109l2.py 顶部说明）。
    seg_edit = j_bare.split('function noteEdit(el')
    if len(seg_edit) != 2:
        bad.append('panel.js：④ `noteEdit()` 命中 %d 次' % (len(seg_edit) - 1))
    else:
        body_edit = seg_edit[1].split('\n    }')[0]
        i_unhide = body_edit.find("removeAttribute('hidden')")
        i_grow = body_edit.find('noteGrow()')
        if i_unhide < 0 or i_grow < 0 or i_grow < i_unhide:
            bad.append('panel.js：④ `noteEdit()` 里 `noteGrow()` 不在摘 `[hidden]` 之后'
                       '（隐藏时 scrollHeight 恒 0 ⇒ 回填的文本高度为 0）'
                       '（unhide=%d grow=%d）' % (i_unhide, i_grow))

    # 字号机制：凡用 calc(Npx * ratio) 声明 line-height / height / min-height 的规则体，
    # 必须同时出现 `var(--font-size-*)` token，否则 apply88b.converge() 会压平它。
    RATIO = r'var\(--ui-fs-ratio\)'
    rx_lh = re.compile(r'line-height:\s*calc\(\d+(?:\.\d+)?px \* ' + RATIO + r'\)')
    rx_h = re.compile(r'(?<![-\w])(height|min-height):\s*calc\(\d+(?:\.\d+)?px \* ' + RATIO + r'\)')
    rx_fs = re.compile(r'var\(--font-size-[a-z0-9-]+\)')
    for one in re.finditer(r'([^{}]*)\{([^{}]*)\}', c_bare):
        sel, body = one.group(1).strip(), one.group(2)
        if not (rx_lh.search(body) or rx_h.search(body)):
            continue
        if rx_fs.search(body):
            continue
        if any(k in sel for k in ('td-elnote', 'td-anchor')):
            bad.append('panel.css：④ `%s` 会被 converge 压平（有 calc 高度但缺字号 token）'
                       % sel.splitlines()[-1].strip()[:60])

    # 注释括号配平（本仓踩过：注释正文里出现 `*/` 会提前闭合块注释）
    for p, label in ((PJS, 'panel.js'), (PCS, 'panel.css')):
        s = rd(p)[0]
        if s.count('/*') != s.count('*/'):
            bad.append('%s：注释括号不配平（`/*` %d / `*/` %d）' % (label, s.count('/*'), s.count('*/')))

    # 跨代标记存活：panel.css 的 `/* rNN-lM */` 尾巴一家人，本层一个不碰
    for mk in ('/* r107-l1 */', '/* r107-l2 */', '/* r108-l1 */', '/* r108-l2 */',
               '/* r108-l3 */', '/* r108-l4 */', '/* r108-l5 */', '/* r108-l6 */',
               '/* r108-l7 */', '/* r109-l1 */'):
        if mk not in c:
            bad.append('panel.css：跨代标记 `%s` 丢了' % mk)
    for mk in ('★ r108-l7 ②：这里原有', 'r108-l6', 'r107-l2'):
        if mk not in j:
            bad.append('panel.js：跨代标记 `%s` 丢了' % mk)

    if bad:
        sys.exit('!! 跨层自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')
    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print('   跳过  %s' % s)


def main():
    global CHECK
    if '--check' in sys.argv:
        CHECK = True
        print('== --check：只验锚点，不落盘 ==')
        do_css()
        do_js()
        print()
        print('锚点全部命中 ✓（%d 项待改；本模式未写入）' % len(APPLIED))
        return
    do_css()
    do_js()
    verify()


if __name__ == '__main__':
    main()
