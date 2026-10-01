# -*- coding: utf-8 -*-
"""r107 第八拍（2026-10-01 12:4x 邵先生六条）—— **就地返工，不另起代数**。

体位：改序 part107/* → （不需 splice / make107）→ apply107.py。
      ⚠ apply107.py 是**运行时** `_read_part()` 读 panel.css / panel.js / browse.html，
        本轮六条全部落在这两个源件里，`_mods.html` 未动 ⇒ **不必重跑 splice107/make107**。

六条 → 改动落点：
  ① 全局自适应省略        → panel.css 新增第 14 节（三类分治，见节内注释）
  ② 去掉「折叠此文件」项   → panel.js  ctxForFile() 删该菜单项 + 顺手删失去引用的 isOpen
  ③ .td-sum-h = 15px      → panel.css 第 6 节就地改（无 15px token ⇒ 用 calc(Npx * ratio)）
  ④ .td-diff-path 展开中粗 → panel.css 第 3 节，` .td-diff.is-open .td-diff-path`
  ⑤ path / rows 一律 13px  → panel.css 第 3 节（容器）+ 第 14 节（三处写死 12px 的子规则覆盖）
  ⑥ .r107-stats 文字居中   → panel.css 第 10 节：靠**盒子居中**（fit-content + margin auto）
                             实现，不用 `text-align:center`（见节内注释的两条理由）

幂等：每处 `edit()` 先查「新串特征子串」是否已在 ⇒ 在就跳过；否则断言锚点唯一再替换。
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(os.path.dirname(HERE), 'part107')
CSS = os.path.join(PART, 'panel.css')
JS = os.path.join(PART, 'panel.js')

APPLIED = []
SKIPPED = []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark):
    """幂等单点替换：mark 已在 ⇒ 跳过；否则要求 old 唯一。"""
    t, nl = rd(p)
    if mark in t:
        SKIPPED.append(label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1）' % (label, n))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)


def tail(t, mark, new, label):
    if mark in t:
        SKIPPED.append(label)
        return t
    APPLIED.append(label)
    return t + new


# ==================================================================== panel.css
# ---- ① ⑤ 第 3 节：diff 头路径（13px + 展开中粗） -------------------
edit(
    CSS,
    """.td-diff-path {
  flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  font-family: var(--font-family);
  color: var(--color-text-1);
}
""",
    """.td-diff-path {
  flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  font-family: var(--font-family);
  font-size: var(--font-size-body-2);
  color: var(--color-text-1);
}
/* ★ 第八拍 ④：**展开后转中粗**。折叠态保持常规粗细 ⇒ 一眼就能看出哪几份改动是打开着的。
   （与 `.td-diff.is-reverted .td-diff-path` 只差属性、不冲突：那条改的是划线/颜色。） */
.td-diff.is-open .td-diff-path { font-weight: 500; }
""",
    'CSS-④⑤ .td-diff-path 13px + 展开 500',
    '.td-diff.is-open .td-diff-path { font-weight: 500; }',
)

# ---- ⑤ 第 3 节：rows 容器字号 13px（子节点靠继承） ------------------
edit(
    CSS,
    ".td-diff-rows { padding: 2px 0 6px; }",
    ".td-diff-rows { padding: 2px 0 6px; font-size: var(--font-size-body-2); }",
    'CSS-⑤ .td-diff-rows 容器 13px',
    'padding: 2px 0 6px; font-size: var(--font-size-body-2);',
)

# ---- ③ 第 6 节：摘要区块标题 15px -----------------------------------
edit(
    CSS,
    "  margin: 0; font-size: var(--font-size-body-1); font-weight: 500; color: var(--color-text-1);",
    "  margin: 0; font-size: calc(15px * var(--ui-fs-ratio)); font-weight: 500; color: var(--color-text-1);",
    'CSS-③ .td-sum-h = 15px',
    'margin: 0; font-size: calc(15px * var(--ui-fs-ratio));',
)

# ---- ⑥ ① 第 10 节：统计行居中 + 省略号（三态幂等） -------------------
OLD_STATS = """.r107-stats {
  font-size: var(--font-size-body-1);
  line-height: calc(16px * var(--ui-fs-ratio));
  color: var(--r93-meta);
  white-space: nowrap;
}
"""
MID_STATS = """.r107-stats {
  font-size: var(--font-size-body-1);
  line-height: calc(16px * var(--ui-fs-ratio));
  color: var(--r93-meta);
  white-space: nowrap;
  /* ★ 第八拍 ⑥「文字居中」：靠**盒子居中**（宽度贴合文字 + `margin: 0 auto`）实现，
     不用 `text-align: center` —— 理由有两条，都不能省：
       ① 宿主里这一行是兜满整行宽的（实测 1440 下盒宽 714 = 输入卡内容宽），
          盒子贴合后视觉位置**与 `text-align: center` 逐像素相同**；
       ② 一旦文字长过盒宽（1024 下内容 630 > 盒 315），`text-align: center` 会让它
          **两端同时被裁且不出省略号**，与本拍 ① 正面冲突。
     ★ 第八拍 ①「宽度不够出省略号」：`min-width:0`(无) + `overflow:hidden` + `ellipsis` 三件套，
       本行 `white-space` 本来就是 `nowrap` ⇒ 窄档自动变省略号。 */
  width: fit-content; max-width: 100%; margin: 0 auto;
  overflow: hidden; text-overflow: ellipsis;
}
"""
NEW_STATS = """.r107-stats {
  font-size: var(--font-size-body-1);
  line-height: calc(16px * var(--ui-fs-ratio));
  color: var(--r93-meta);
  white-space: nowrap;
  /* ★ 第八拍 ⑥「文字居中」。这一行是**真节点**（第六拍把 `::after` 换来的），
     与输入卡共用同一条盒宽规则（`main > … > div.mt-8 > div`，r95 ② / r106 ④ 两版，
     **都带 `!important`**）⇒ 盒宽恒等于输入卡：860 / 714 / 315（实测三档全等）。
     ⚠ 所以「盒子贴合 + `margin: 0 auto`」这条路走不通（本拍第一版走过，被 `!important` 压死、
       是死代码）：`width` / `min-width` / `max-width` 全被那两条钉住，改不动；真节点也不像
       当年的 `::after` 那样自动 shrink-wrap ⇒ 满宽盒里文字默认靠左；而宿主的 `items-center`
       对这个满宽子项不生效（实测输入卡自己就是齐左的），靠 `margin: auto` 会比输入卡**偏 32px**。
     ⇒ 居中只能写 `text-align`（它没有任何 `!important` 竞争者）。
     实测判据 = **文字盒中心 − 输入卡中心 = 0**（1440 / 右栏开）。 */
  text-align: center;
  /* ★ 第八拍 ①「宽度不够出省略号」：`white-space: nowrap` 本来就有，这里补 `overflow: hidden`，
     让窄档**不再越过输入卡右边界外溢**（改前 1024 实测外溢 315px）。
     ★ ① 与 ⑥ 在本元素上**可以共存**：Chromium 在「居中 + 溢出」时对齐行为退化为 `start`
       （文字盒仍自盒左缘起算），省略号**照常落在行尾** —— 实测 1024 截图尾部为「首 token 平…」。 */
  overflow: hidden; text-overflow: ellipsis;
}
"""
# 多版本自愈：**按选择器整块替换**（不锚定历史版本正文）——
# 本拍这条规则改过三稿（fit-content → text-align → 更正注释），逐版字符串匹配会一直追不上。
# `.r107-stats` 的规则体里没有嵌套花括号 ⇒ 取选择器之后第一个 `\n}\n` 即块尾。
def replace_block(t, sel, new_block, label):
    global _APPLIED_N
    i = t.find(sel)
    if i < 0:
        SKIPPED.append(label + '（未找到选择器）')
        return t
    j = t.find('\n}\n', i)
    if j < 0:
        sys.exit('!! %s：找不到块尾' % label)
    cur = t[i:j + 3]
    if cur == new_block:
        SKIPPED.append(label)
        return t
    APPLIED.append(label + '（整块替换 %d → %d 字符）' % (len(cur), len(new_block)))
    return t[:i] + new_block + t[j + 3:]


_t, _nl = rd(CSS)
wr(CSS, replace_block(_t, '.r107-stats {\n', NEW_STATS, 'CSS-⑥① .r107-stats'), _nl)

# ---- ① ⑤ 新增第 14 节 ------------------------------------------------
SECTION14 = """
/* ---------------------------------------------------------------- 14. 全局自适应省略（第八拍 ①）
   ▸ 需求：「全局所有的对象元素或容器，当自适应宽度的横向宽度不够时，内部的文字会自动呈现省略号」。
   ▸ 落地口径（三类分治，写死在这儿免得下轮再逐条讨论）：
       ① 单行文本容器（名称 / 路径 / 域名 / 标题 / 计数）⇒ **省略号** —— 本节处理；
       ② 代码与终端（`.td-dr-t` / `.td-dsc-c` / `.td-code-*` / `.td-term-*`）⇒ 保持 `pre` + 按需折行，
          **不截断**：截断代码会丢信息，而且它们本来就是「窄了就换行」的语义；
       ③ 多行正文（`.td-sum-p` / `.td-note-b` / `.td-sum-plan li` / `.td-page-h1`）⇒ 保持折行，
          **不截断**：截断段落等于丢内容。
   ▸ 三件套缺一不可：`min-width:0`（flex 子项的收缩下限默认是 min-content，不解除就永远把兄弟顶出去）
     + `overflow:hidden` + `text-overflow:ellipsis` + `white-space:nowrap`（不换行才谈得上省略）。
   ▸ 本节排在文档序最末 ⇒ 与移植件 browse.css 同特异性时**必胜**（跨代资产一律不回头改）。 */
.td-browse :is(.td-browse-tree-title, .td-diff-more, .td-diff-btn, .td-commit-btn,
               .td-commit-t, .td-commit-lb, .td-note-who, .td-note-time,
               .td-sum-tag, .td-sum-srct i, .td-sum-artt i,
               .td-elnote-t, .td-url-annot, .td-page-cta, .td-page-foot,
               .td-rv-commit, .td-rv-pr) {
  min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
/* 容器自带 `display:flex / inline-flex` 时，裸文本会变成**匿名 flex 项**，容器上的
   `text-overflow` 对它无效 ⇒ 文字落在子 `<span>` 里的这几处要单独点。（`.td-mm-name`
   那条已经在第 1 节覆盖了四枚下拉与右键菜单的条目文字，这里不重复。） */
.td-browse :is(.td-rv-commit, .td-rv-pr) > span,
.td-browse .td-commit-row > span,
.td-browse .td-commit-ck > span {
  min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
/* 行内评论头：让「评论人」先让位、「时间」保持原宽（时间只有几个字，被截断就读不懂了）。 */
.td-browse .td-note-who { flex: 1 1 auto; }
.td-browse .td-note-time { flex: none; }

/* ★ 第八拍 ⑤：`.td-diff-rows` 内一律 13px。
   `.td-dr`(12) / `.td-dsc-c`(12) / `.td-diff-more`(12) 三处各自写死了字号 ⇒ 只改容器无效，
   逐条同值覆盖。⚠ 只**换 token 档位**（仍旧写成 `var(--font-size-*)`）⇒
   `apply88b.converge()` 的「含 token 才重派生行高」判据不受影响，`.td-dr` 的 20px 行高照旧。 */
.td-diff-rows .td-dr,
.td-diff-rows .td-dsc-c,
.td-diff-rows .td-diff-more { font-size: var(--font-size-body-2); }
"""
_t, _nl = rd(CSS)
wr(CSS, tail(_t, '14. 全局自适应省略', SECTION14, 'CSS-①⑤ 新增第 14 节'), _nl)

# ==================================================================== panel.js
# ---- ② 删掉「折叠此文件 / 展开此文件」这一整项 ------------------------
edit(
    JS,
    """      '-',
      { label: isOpen ? '折叠此文件' : '展开此文件', ico: isOpen ? 'close' : 'plus', act: function () { setDiffOpen(art, !isOpen); syncFoldBtn(); } },
      { label: toExpand ? '展开全部文件' : '折叠全部文件', ico: toExpand ? 'plus' : 'close', act: function () { if (foldBtn) foldBtn.click(); } }
""",
    """      '-',
      { label: toExpand ? '展开全部文件' : '折叠全部文件', ico: toExpand ? 'plus' : 'close', act: function () { if (foldBtn) foldBtn.click(); } }
""",
    'JS-② 删除「折叠/展开此文件」菜单项',
    # ⚠ mark 必须**只在改后**存在：原来这里写的是 fold-all 那一行 —— 它在改前也在，
    #    于是第一遍就被误判成「已应用」而静默跳过（isOpen 却已删 ⇒ 变成未定义变量）。
    #    改成用「`'-',` 紧跟 fold-all 项」这个只有删掉中间那项才成立的邻接关系。
    "'-',\n      { label: toExpand ? '展开全部文件'",
)

# ---- ② 顺手删掉因此失去引用的 isOpen（同一函数里只剩这一处引用） ------
edit(
    JS,
    """    var path = ctxTxt(art.querySelector('.td-diff-path')) || '文件';
    var isOpen = art.classList.contains('is-open');
    var staged""",
    """    var path = ctxTxt(art.querySelector('.td-diff-path')) || '文件';
    var staged""",
    'JS-② 删除失去引用的 isOpen',
    "var path = ctxTxt(art.querySelector('.td-diff-path')) || '文件';\n    var staged",
)

# ---- ② 头部职责注释同步（原文写的是「单个 / 全部⇄展开全部」） ---------
edit(
    JS,
    "     ③ 审查：文件折叠（单个 / 全部⇄展开全部）/ 统一⇄并排 / 对比范围 / 显示选项八项",
    "     ③ 审查：文件折叠（点头部 = 单个 / 菜单 = 全部⇄展开全部）/ 统一⇄并排 / 对比范围 / 显示选项八项",
    'JS-② 职责注释同步',
    "文件折叠（点头部 = 单个 / 菜单 = 全部⇄展开全部）",
)

# ==================================================================== 汇报
print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
for x in APPLIED:
    print('  + %s' % x)
for x in SKIPPED:
    print('  = %s（已存在）' % x)
for p in (CSS, JS):
    t, nl = rd(p)
    print('%-34s %d 字符 / %d 行 / 行尾=%s' % (os.path.basename(p), len(t), t.count('\n') + 1, 'CRLF' if nl == '\r\n' else 'LF'))
