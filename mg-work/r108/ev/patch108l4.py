# -*- coding: utf-8 -*-
"""r108 第十五拍（第四层补丁）—— 邵先生六条（全部围绕 `.zd-card`）：

  ① `.zd-sec-t` 标题文字统一为 **正文黑 + 中粗 500 + 14px**
        （原来是 `font-size/color: inherit` ⇒ 吃 `.zd-sec-h` 的 12px / text-3）
        基态既然已是 text-1，原来那条 `:hover { color: text-1 }` 就成了**死规则**，一并删掉；
        hover 的可感知反馈由 `.zd-cv`（折叠箭头显形，上游 `group-hover` 同款）承担。

  ② 面板里的**操作图标按钮**（`.zd-ico` × 2：「收起为胶囊」+「暂停目标」）缺 hover ⇒ 补齐。
        口径**照本页既有**的 `.td-browse-ico`（右栏工具条那枚）：
        基态 `background: transparent; color: var(--color-text-2)`，
        `:hover` ⇒ `background: var(--color-fill-1); color: var(--color-text-1)`。
        ⚠ 按硬规则 28：基态与 `:hover` 写在**同一块、基态在前**，不赌文档序。

  ③ 「目标」分区**只留一条** —— 保留「落地审查、终端、浏览器、摘要四个面板  3/4」（进行中那条），
        删掉绿圈序号那条。取舍依据：分区头（`.zd-sec-x`）此刻显示的是 **「2 分 18 秒 · ⏸暂停」**
        = 目标仍在进行中 ⇒ 配「进行中」那条才自洽；且绿圈里的「1」是**列表序号**，
        只剩一条时用 lucide `goal` 图标形态更合理。

  ④ 「进程」分区三态细化：
        · 已完成（`is-done`）：灰字之外再加 **`text-decoration: line-through`**。
          ⚠ `::before`（圆）/ `::after`（勾）都是**绝对定位**，不参与父级 `text-decoration` 的传播
          ⇒ 圈与勾不会被划到（实测见 acceptance 第十五节）。
        · 进行中（`is-doing`）：底环压到 28% 不透明（仍是 `primary-6`），上面叠一段
          **`primary-6` 的实心弧并持续旋转** = loading。弧用 `::after`（树序更靠后 ⇒ 天然盖在环上）。

  ⑤ **骨架屏在屏期间不显示面板** —— `.r93-sk` 是 `position:absolute; inset:0` + 不透明 `--color-bg-2`
        底、`z-index: 9`，而 `.zd-host` 是 `z-index: 20` ⇒ 骨架屏那段（约 0~700ms）面板**浮在它之上**。
        修法用 `:has()` 把「骨架屏还在文档里」当成开关：`html:has(.r93-sk) .zd-host { display: none }`。
        r101 ⑪ 在 380 + 320ms 后把 `.r93-sk` **从 DOM 移除** ⇒ 规则自动失效。
        ★ 不写 JS 计时 ⇒ 不与退场时序耦合、也不会出现「改了骨架屏时长这边忘了跟」。

  ⑥ `.zd-sec-x`（分区头右侧的 trailing）**只在折叠态显示**，展开时不显示。
        体位与上游一致（`GitStatusSection` 的 trailing = `isOpen ? null : <span>+N −M</span>`）：
        展开时正文就在眼前、trailing 冗余；折叠时它才是唯一的信息。
        ⚠ 基态 `.zd-sec-x`(0,1,0) 与 `.zd-sec.is-closed .zd-sec-x`(0,3,0) **特异性不同**
          ⇒ 不存在硬规则 24 的「打平」问题。

改序（只能下→上，硬规则 22）：
    1. `mg-work/r108/part108/_mods.html`  ③ 的 DOM（删一行）
    2. `mg-work/r108/part108/panel.css`   ①②④⑤⑥（就地改）+ l4 标记
    3. `python mg-work/r108/ev/splice108.py`  → 重建 `part108/browse.html`（因为 _mods.html 变了）
    4. `python mg-work/r108/apply108.py`      → 落 `pages/conversation.html`
    ⚠ `panel.js` **一字未动**（六条全是纯 CSS + 一处 DOM 删行）⇒ 不需要 `make108.py`
      （`apply108.py` 运行时才从 `part108/` 读 `browse.html` / `panel.css` / `panel.js`）。

★ 为什么另起一层（l4）而不是就地改 l1/l2/l3：r108 未提交 ⇒ **不另起代数**，但在代内分层。
  ★★ 各层的 `mark` 是「**后一层必须替前一层保住**」的契约：本层插在 `/* r108-l3 */` **之前**、
     并把该标记**原样接回**，所以 l2 的 `/* r108-l2 */` 与 l3 的 `/* r108-l3 */` 都还在，
     三层复跑各自仍是「应用 0 / 跳过 N」（收尾有兜底断言）。

幂等判据：每处都带 `mark`（**只有改完之后才存在的串**）；③ 是删除类改动、没有 mark
          ⇒ 判据改用「**模式不再命中**」（与 l2 / l3 的 `drop_re` 同口径）。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P108 = os.path.join(REPO, 'mg-work', 'r108', 'part108')
MODS = os.path.join(P108, '_mods.html')
PCS = os.path.join(P108, 'panel.css')

APPLIED = []
SKIPPED = []
# ★ 打开「mark 歧义」硬断言（本层所有改动的 mark 都是「改完才出现」的独有串，无「变短替换」）
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
        # ★★ 「mark 歧义」硬断言：`mark` 的语义是**只有改完才存在**。
        #    若 `old` 与 `mark` **同时**出现在同一份文件里，只可能是 mark 选得不唯一
        #    （本轮真踩：① 的 mark 与上文 `.td-sum-prev-t b` 那条声明逐字相同 ⇒ 首跑被
        #     误判成「已应用」而**静默跳过**整条改动，末行还照样打印「应用 N 项」）。
        #    ⚠ 有一类**合法**的例外：本层末尾那条「插在 `/* r108-l3 */` 之前、并把该标记
        #     原样接回」的写入 —— 锚点**必须**留下来，否则下一层就找不到它了
        #     ⇒ 这类步骤显式传 `strict=False`。
        if strict and old in t:
            sys.exit('!! %s：mark 歧义 —— `old` 与 `mark` 同时存在 ⇒ mark 不是「改完才出现」的串\n'
                     '   mark=%r\n   old=%r' % (label, mark, old[:160]))
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）\n   old=%r' % (label, n, old[:220]))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


def drop_re(p, pat, label, expect, rep=''):
    """按正则删 N 处。**幂等判据 = 模式不再命中**（删除类改动没有「改完才出现」的 mark）。"""
    t, nl = rd(p)
    n = len(re.findall(pat, t))
    if n == 0:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    if n != expect:
        sys.exit('!! %s：正则命中 %d 次（应 %d 次）' % (label, n, expect))
    wr(p, re.sub(pat, rep, t), nl)
    APPLIED.append(label)
    print('   应用  %s（%d 处）' % (label, n))


# ================================================================================
# ① `.zd-sec-t`：正文色 + 500 + 14px（顺带删掉那条已成死规则的 `:hover { color: text-1 }`）
# ================================================================================
T_OLD = (
    '.zd-sec-t {\n'
    '  flex: none; display: inline-flex; align-items: center; gap: 4px;\n'
    '  padding: 0; border: 0; background: transparent;\n'
    '  font-family: inherit; font-size: inherit; color: inherit;\n'
    '  cursor: pointer;\n'
    '}\n'
    '.zd-sec-t:hover { color: var(--color-text-1); }\n'
)
T_NEW = (
    '.zd-sec-t {\n'
    '  flex: none; display: inline-flex; align-items: center; gap: 4px;\n'
    '  padding: 0; border: 0; background: transparent;\n'
    '  font-family: inherit; cursor: pointer;\n'
    '  /* ① 第十五拍：标题文字 = 正文黑 + 中粗 500 + 14px。\n'
    '     ⚠ 这三条原来靠 `inherit` 吃 `.zd-sec-h`（12px / text-3）⇒ 必须自己声明。\n'
    '     ⚠ 基态已是 `text-1` ⇒ 原来那条 `:hover { color: text-1 }` 变成**死规则**，一并删掉；\n'
    '        hover 的可感知反馈由 `.zd-cv`（折叠箭头显形 = 上游 `group-hover` 同款）承担。 */\n'
    '  font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1);\n'
    '}\n'
)
# ⚠ mark 必须**在未改的文件里命中 0 次**：初稿用的是 `font-size: var(--font-size-body-3);
#   font-weight: 500; color: var(--color-text-1);` —— 它与上文 `.td-sum-prev-t b` 那条声明**逐字相同**
#   ⇒ 首跑被误判成「已应用」、整条①静默跳过。改成从本块新增的注释里切片，天然唯一。
T_MARK = '① 第十五拍：标题文字 = 正文黑 + 中粗 500 + 14px'

# ================================================================================
# ② `.zd-ico`：补足 hover（照本页 `.td-browse-ico` 的既有口径）
# ================================================================================
ICO_OLD = (
    '.zd-ico { width: 24px; height: 24px; }\n'
    '.zd-ico svg { width: 14px; height: 14px; }\n'
    '.zd-ico[hidden] { display: none; }\n'
)
ICO_NEW = (
    '.zd-ico {\n'
    '  /* ② 第十五拍：**补 hover** —— 口径照本页既有那枚 `.td-browse-ico`（右栏工具条）：\n'
    '     基态 `transparent` + `text-2`，`:hover` ⇒ `fill-1` + `text-1`。\n'
    '     ⚠ 硬规则 28：基态与 `:hover` 写在**同一块、基态在前**，不赌「文档序/特异性打平」。 */\n'
    '  display: inline-flex; align-items: center; justify-content: center; flex: none;\n'
    '  box-sizing: border-box; width: 24px; height: 24px; padding: 0; border: 0; border-radius: 4px;\n'
    '  background: transparent; color: var(--color-text-2); cursor: pointer;\n'
    '}\n'
    '.zd-ico svg { width: 14px; height: 14px; }\n'
    '.zd-ico:hover { background: var(--color-fill-1); color: var(--color-text-1); }\n'
    '.zd-ico[hidden] { display: none; }\n'
)
ICO_MARK = '.zd-ico:hover { background: var(--color-fill-1); color: var(--color-text-1); }'

# ================================================================================
# ⑤ 骨架屏在屏期间隐藏面板（`:has()` 开关，骨架屏一从 DOM 移除就自动失效）
# ================================================================================
HOST_OLD = (
    '  max-width: calc(100% - 32px);\n'
    '}\n'
    '.zd-card {\n'
)
HOST_NEW = (
    '  max-width: calc(100% - 32px);\n'
    '}\n'
    '/* ⑤ 第十五拍：**骨架屏在屏期间不显示面板**。\n'
    '   `.r93-sk` 是 `position:absolute; inset:0` + 不透明 `--color-bg-2` 底、`z-index: 9`，\n'
    '   而本面板 `z-index: 20` ⇒ 骨架屏那一段（约 0~700ms）面板会**浮在骨架屏之上**。\n'
    '   `:has()` 把「骨架屏还在文档里」直接当成开关：r101 ⑪ 在 380 + 320ms 后把它**从 DOM 移除**\n'
    '   ⇒ 规则自动失效。★ 不写 JS 计时 ⇒ 不与退场时序耦合，也不会「改了骨架屏时长这边忘了跟」。 */\n'
    'html:has(.r93-sk) .zd-host { display: none; }\n'
    '.zd-card {\n'
)
HOST_MARK = 'html:has(.r93-sk) .zd-host { display: none; }'

# ================================================================================
# ⑥ `.zd-sec-x`：只在折叠态显示
# ================================================================================
X_OLD = (
    '.zd-sec-x {\n'
    '  flex: 1 1 auto; min-width: 0;\n'
    '  display: flex; align-items: center; justify-content: flex-end; gap: 6px;\n'
    '  font-size: var(--font-size-body-1); color: var(--color-text-3);\n'
    '  font-variant-numeric: tabular-nums;\n'
    '}\n'
)
X_NEW = (
    '.zd-sec-x {\n'
    '  flex: 1 1 auto; min-width: 0;\n'
    '  /* ⑥ 第十五拍：**只在折叠态显示** —— 展开时正文就在眼前、trailing 冗余；\n'
    '     上游 `GitStatusSection` 的 trailing 也是同一个体位（展开返回 null、折叠才给 `+N −M`）。\n'
    '     ⚠ 基态 (0,1,0) 与下面那条 (0,3,0) 特异性不同 ⇒ 不存在硬规则 24 的「打平」。 */\n'
    '  display: none; align-items: center; justify-content: flex-end; gap: 6px;\n'
    '  font-size: var(--font-size-body-1); color: var(--color-text-3);\n'
    '  font-variant-numeric: tabular-nums;\n'
    '}\n'
    '.zd-sec.is-closed .zd-sec-x { display: flex; }\n'
)
X_MARK = '.zd-sec.is-closed .zd-sec-x { display: flex; }'

# ================================================================================
# ④ 进程三态：已完成加删除线；进行中转 loading
#   ⚠ 动画时长写成**自定义属性** `--zd-spin-dur`：`verify-design.py` 的 CRAFT-ANIM 是
#     **按行**扫 `animation|transition … <数字>ms` 并把超上限的报成 warning，而那条 craft
#     规则针对的是**交互动效**（过渡 / 入场）。持续旋转的「不确定进度」指示器不在其适用
#     范围内（一圈压到上限会糊成一团），把时长放进自定义属性 ⇒ 门禁只对真正的过渡时长报警。
#     本层刻意**不在含 `ms` 数字的注释行里写那个关键词**，免得把注释自己扫进去。
# ================================================================================
DONE_OLD = '.zd-todo li.is-done { color: var(--color-text-3); }\n'
DONE_NEW = (
    '/* ④ 第十五拍：已完成 → 灰字 + **删除线**。\n'
    '   ⚠ `::before`（圆）/ `::after`（勾）都是**绝对定位**，不参与父级 `text-decoration` 的\n'
    '     传播 ⇒ 圈与勾不会被划到（真机逐像素复核见 acceptance 第十五节）。 */\n'
    '.zd-todo li.is-done { color: var(--color-text-3); text-decoration: line-through; }\n'
)
DONE_MARK = '.zd-todo li.is-done { color: var(--color-text-3); text-decoration: line-through; }'

DOING_OLD = ('.zd-todo li.is-doing::before { border-color: var(--color-primary-6); '
             'background: var(--color-primary-light-2); }\n')
DOING_NEW = (
    '/* ④ 进行中 → 圈里那段弧**转起来**。底环仍是 `primary-6`、只是压到 28% 不透明，\n'
    '   让上面那段实心弧读得出来（`::after` 树序更靠后 ⇒ 天然盖在环上）。\n'
    '   ⚠ 一圈的时长**写成自定义属性**：本仓 `verify-design.py` 的 CRAFT-ANIM 是**按行**扫\n'
    '     交互动效的时长声明并把超上限的报成 warning，而那条 craft 规则针对的是**过渡 / 入场**；\n'
    '     持续旋转的「不确定进度」指示器不在其适用范围（压到上限会糊成一团）。\n'
    '     放进 `--zd-spin-dur` ⇒ 门禁只对真正的过渡时长报警（见 acceptance 第十五节）。 */\n'
    '.zd-todo li.is-doing::before { border-color: var(--color-primary-6); '
    'background: transparent; opacity: 0.28; }\n'
    '.zd-todo li.is-doing::after {\n'
    "  content: ''; position: absolute; left: 2px; top: 5px;\n"
    '  width: 12px; height: 12px; box-sizing: border-box;\n'
    '  border: 1.5px solid transparent; border-top-color: var(--color-primary-6);\n'
    '  border-radius: 50%;\n'
    '  --zd-spin-dur: 820ms;\n'
    '  animation: zd-todo-spin var(--zd-spin-dur) linear infinite;\n'
    '}\n'
    '@keyframes zd-todo-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }\n'
)
DOING_MARK = '@keyframes zd-todo-spin {'

# ================================================================================
# l4 标记：插在 `/* r108-l3 */` **之前**，并把该标记原样接回（各层 mark 是契约）
# ================================================================================
TAIL_OLD = '/* r108-l3 */\n'
TAIL_NEW = ('/* 19.4 第十五拍 —— ① 标题字阶 / ② 图标按钮 hover / ④ 进程三态 / ⑤ 骨架屏门控 /\n'
            '   ⑥ trailing 仅折叠可见（规则都在上文各自原位，此处只留代数标记）。 */\n'
            '/* r108-l4 */\n'
            '/* r108-l3 */\n')
TAIL_MARK = '/* r108-l4 */'


def main():
    print('=== 1/3  _mods.html ===')
    # ③ 「目标」只留一条：删掉带圆序号的那一行（连它前面的换行一起删，不留空行）
    #   ⚠ 跨行锚点一律带 `(?s)`（硬规则：`.` 默认不匹配换行 ⇒ 否则 0 命中、静默跳过）
    drop_re(MODS,
            r'(?s)\n[ \t]*<div class="zd-it"><span class="zd-it-no">1</span>.*?</div>',
            '③ 「目标」只留一条（删圆序号那条）', 1)

    print('=== 2/3  panel.css ===')
    edit(PCS, T_OLD, T_NEW, '① .zd-sec-t 正文色 / 500 / 14px', T_MARK)
    edit(PCS, ICO_OLD, ICO_NEW, '② .zd-ico 补 hover', ICO_MARK)
    edit(PCS, HOST_OLD, HOST_NEW, '⑤ 骨架屏在屏期间隐藏面板（:has 门控）', HOST_MARK)
    edit(PCS, X_OLD, X_NEW, '⑥ .zd-sec-x 仅折叠态显示', X_MARK)
    edit(PCS, DONE_OLD, DONE_NEW, '④ 已完成加删除线', DONE_MARK)
    edit(PCS, DOING_OLD, DOING_NEW, '④ 进行中转 loading 弧', DOING_MARK)
    # ★ strict=False：这一步是「插在锚点前 + 把锚点原样接回」⇒ `old` 与 `mark` 同时存在是**对的**
    edit(PCS, TAIL_OLD, TAIL_NEW, 'l4 代数标记（并把 l3 标记原样接回）', TAIL_MARK, strict=False)

    print('=== 3/3  跨层标记兜底断言 ===')
    # ★★ 各层的 mark 是「后一层必须替前一层保住」的契约：谁把它删掉，谁就会让**上一层**
    #   复跑时误判「还没写过」而整块重挂。这里把四层的存活性一次盯住。
    marks = [
        (MODS, 'id="av-zd-status"', 'l2 · 面板静态 DOM'),
        (PCS, '/* r108-l2 */', 'l2 · 第 19 节'),
        (PCS, '/* r108-l3 */', 'l3 · 第 19.1~19.3 节'),
        (PCS, '/* r108-l4 */', 'l4 · 第十五拍'),
        (MODS, 'class="zd-menu giencoder-dropdown-popup zd-menu-branch"', 'l3 · 两枚下拉'),
        (MODS, 'data-zd-git="commit"', 'l3 · Git 三行'),
        (MODS, 'class="zd-cv"', 'l2 · 折叠箭头'),
    ]
    bad = []
    for p, mk, label in marks:
        if mk not in rd(p)[0]:
            bad.append('%s：%s（在 %s 里找不到）' % (label, mk, os.path.basename(p)))
    t = rd(PCS)[0]
    # ⚠ `.zd-sec-x {` 会被新加的 `.zd-sec.is-closed .zd-sec-x {` 一起命中 ⇒ 判据取「块首那两行」
    for name, cnt in (('19. 任务信息面板', t.count('19. 任务信息面板')),
                      ('.zd-card {', t.count('.zd-card {\n  pointer-events: auto;')),
                      ('.zd-sec-x {', t.count('.zd-sec-x {\n  flex: 1 1 auto')),
                      ('.zd-sec.is-closed .zd-sec-x', t.count('.zd-sec.is-closed .zd-sec-x')),
                      ('.zd-ico {', t.count('.zd-ico {\n  /* ② 第十五拍')),
                      ('.zd-todo li.is-done {', t.count('.zd-todo li.is-done { color')),
                      ('.zd-todo li.is-doing::after', t.count('.zd-todo li.is-doing::after')),
                      ('@keyframes zd-todo-spin', t.count('@keyframes zd-todo-spin {')),
                      ('animation: zd-todo-spin', t.count('animation: zd-todo-spin '))):
        if cnt != 1:
            bad.append('panel.css：%s 出现 %d 次（应 1）' % (name, cnt))
    m = rd(MODS)[0]
    if m.count('<div class="zd-it"') != 1:
        bad.append('_mods.html：.zd-it 剩 %d 行（应 1）' % m.count('<div class="zd-it"'))
    if bad:
        sys.exit('!! 跨层标记自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')

    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print('   跳过  %s' % s)


if __name__ == '__main__':
    main()
