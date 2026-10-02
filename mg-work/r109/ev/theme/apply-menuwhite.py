# -*- coding: utf-8 -*-
r"""r109 第十一拍 · 下拉菜单面板「浅色档 = 白色」+ 暗色档保持基准。

★ 邵先生原话（第十一拍 #1，标注「重要」）：
    「全站所有的下拉菜单的容器背景色在浅色模式下都应该是白色」

★ 现状（真机取证 raw/dd9-light/panel-{0..5}.json）：
  base 页 6 类下拉面板（添加 / 技能 / 标准模式 / 大模型 / 工作目录 / 默认权限）
  浅色档底 **全是**  rgba(247,247,247,0.88)  —— 第九拍为对齐暗色基准改的，
  连「基准」自己（默认权限）也是这个值 ⇒ 与「浅色应为白色」冲突。

★ 修法（最小、可逆、不碰 DS 编译包）：
  1) 浅色档：把 28 处 `rgba(var(--gray-1),0.88)` 换成 `var(--color-bg-1)`
     —— 浅色档 `--color-bg-1 = #fff`（纯白，DS 变量，满足铁律 #2「禁硬编码」）
     —— 暗色档该写法会变 `#17171a`（不透明深黑），不是基准 ⇒ 必须由第 2 步压回
  2) 暗色档：在 </head> 前追加覆盖块 `r109-menuwhite-css`，把同一批选择器
     压回 `rgba(var(--gray-1),0.88)`（暗色 = rgba(31,31,31,.88)，第九拍基准）
     —— 选择器与第 1 步逐字相同、位置更靠后 ⇒ 暗色档必然胜出

★ 覆盖面（28 处，全部经真机确认属「下拉菜单容器」）：
  CSS   .giencoder-select-popup              ×10 页
        .skills-popup-bg                     ×10 页
        avatar/task-detail 内联样式           ×2
  JS    base/conversation 添加菜单面板        ×3 each（6）
        —— 该 6 处自带 `background` inline style（优先级最高），
           故暗色档不给它们加覆盖块也仍会变深黑 ⇒ 这两页的暗色档
           额外补 3 条 inline 面板选择器覆盖（见 DARK_SELECTORS 末段）

★ 幂等判据：旧串计数 = 0 且覆盖块内容逐字符（规范化换行后）相同。
★ 回滚：python apply-menuwhite.py --revert
"""
import argparse
import collections
import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')
BAK = os.path.join(ROOT, 'mg-work', 'r109', 'ev', 'bak-menuwhite')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

RE_DS_BUNDLE = re.compile(re.escape(u':root{--giencoderblue-1:245, 248, 255'))

BLOCK_ID = u'r109-menuwhite-css'

# ── 第 1 步：浅色档 → 纯白（var(--color-bg-1) 浅 = #fff）──────────────────
# ⚠ 实际存在**四种**写法变体（真机核实，缺一不可）：
OLD_LIST = [
    u'background:rgba(var(--gray-1),0.88)',       # ① .giencoder-select-popup（紧凑）
    u'background:rgba(var(--gray-1), 0.88)',      # ② .skills-popup-bg（冒号后无空格、逗号后有）
    u'background: rgba(var(--gray-1), 0.88)',     # ③ .td-skill-pop 内联（两边都有空格）
    u'background:`rgba(var(--gray-1), 0.88)`',    # ④ JS 添加菜单面板（模板字符串）
]
NEW_FOR = {
    OLD_LIST[0]: u'background:var(--color-bg-1)',
    OLD_LIST[1]: u'background:var(--color-bg-1)',
    OLD_LIST[2]: u'background: var(--color-bg-1)',
    OLD_LIST[3]: u'background:`var(--color-bg-1)`',
}
EXPECT = {OLD_LIST[0]: 10, OLD_LIST[1]: 10, OLD_LIST[2]: 2, OLD_LIST[3]: 2}

# 幂等护栏：改完之后，这四种「旧写法」在**本层块之外**必须为 0
def old_survey(t):
    u"""统计四种旧写法在（去掉本层块的）文本里的残留数"""
    own = RE_BLOCK.search(t)
    body = (t[:own.start()] + t[own.end():]) if own else t
    return {o: body.count(o) for o in OLD_LIST}

# ── 第 1b 步：既有暗色覆盖的 0.9 → 0.88（邵先生裁决「统一到 0.88 基准」）──
#   真机取证：html[giencoder-theme='dark'] .skills-popup-bg
#   { background: rgba(var(--gray-1), 0.9) !important; ... }  —— 比基准亮 1.5 级
#
# ★★ 关键陷阱（本层实测踩过，务必保留此注释）：
#   step1b 的产物若写成「冒号后有空格 + 逗号后无空格」以外的第三种变体③
#   （即 `rgba(var(--gray-1), 0.88)`，两边都有空格），它会与 step1 的 OLD_LIST[2]
#   **逐字相同** ⇒ 下一遍重跑时（stage1 在 stage1b 之前）
#   step1 会把这 20 处暗色覆盖**再改成 `var(--color-bg-1)`**
#   （暗色档 = #17171a 纯黑 ⇒ 技能面板变全黑；实测第 2 遍落盘后
#    `td-skill-pop` / `skills-popup-bg` 的 dark 规则真的变成了 var(--color-bg-1)）。
#   ⇒ 修法：step1b 的产物**刻意使用「冒号后有空格、逗号后无空格」这一
#     step1 三种变体都匹配不到的空格组合**（`rgba(var(--gray-1),0.88)`），
#     既满足「统一到 0.88」的语义，又保证跨遍幂等（步 1b 自身 old 是 `, 0.9)`
#     ⇒ 也不会自撞）。
D_OLD_LIST = [
    u"html[giencoder-theme='dark'] .td-skill-pop { background: rgba(var(--gray-1), 0.9) !important; }",
    u"html[giencoder-theme='dark'] .skills-popup-bg { background: rgba(var(--gray-1), 0.9) !important;",
]
D_NEW_FOR = {
    # 注意：产物用「冒号后有空格、逗号后无空格」——见上方 ★★ 注释
    D_OLD_LIST[0]: u"html[giencoder-theme='dark'] .td-skill-pop { background: rgba(var(--gray-1),0.88) !important; }",
    D_OLD_LIST[1]: u"html[giencoder-theme='dark'] .skills-popup-bg { background: rgba(var(--gray-1),0.88) !important;",
}
D_EXPECT = {D_OLD_LIST[0]: 1, D_OLD_LIST[1]: 1}

# ── 第 2 步：暗色档覆盖块 ────────────────────────────────────────────────
# 说明：第 1b 步那两条自带 !important，本块必须也带 !important 才能胜出；
#       位置在它们之后（锚 </head> 前）且 !important 同行级 ⇒ 靠文档顺序取胜。
DARK_BLOCK = u'''<style id="r109-menuwhite-css">
  /* ★ r109 第十一拍 ①：下拉菜单面板 —— 浅色档为纯白（第 1 步把底改成 var(--color-bg-1)，
     浅色档 --color-bg-1 = #fff）；暗色档统一压回第九拍基准 rgba(var(--gray-1),0.88)
     （= rgba(31,31,31,.88)，即邵先生 A 指令「以『默认权限』下拉的暗色配色为准」的基准），
     并统一原先 0.9 的偏差。
     本块锚在 </head> 前、且与既有暗色规则同为 !important ⇒ 文档顺序更靠后者胜出。
     ★ 本块内刻意使用「带空格」的 rgba(...) 写法：step1 的三种 old 串都匹配不到它，
       从而保证本层重跑时**不会改到自己的产物**（幂等必需）。
     摘掉本块即回滚暗色档。

     ★★ 补充（第十一拍落地后真机取证 raw/dd9-dark/ 发现的覆盖缺口）：
       第 1 步把「默认权限 / 添加菜单 / 技能面板」这 3 类**内联样式面板**的底也改成了
       var(--color-bg-1)（暗色 = #17171a 不透明深黑），但它们**不是** .giencoder-select-popup
       —— 其载体是 role=menu / role=listbox 的**内联 style** 元素，
       单纯靠 .giencoder-select-popup 选择器压不回来（真机实测这三类停在 rgb(23,23,26)，
       与其它三类 rgba(31,31,31,.88) 不统一）。
       ⇒ 本块再补 3 条 aria-label 精确选择器（内联样式优先级最高 ⇒ 必须 !important），
         使 6 类下拉面板的暗色档全部 = rgba(var(--gray-1),0.88)。 */
  html[giencoder-theme='dark'] .giencoder-select-popup,
  [giencoder-theme=dark] .giencoder-select-popup,
  html[giencoder-theme='dark'] .skills-popup-bg,
  [giencoder-theme=dark] .skills-popup-bg,
  html[giencoder-theme='dark'] .td-skill-pop,
  /* 内联样式面板三兄弟：添加菜单 / 默认权限 / 技能面板 */
  html[giencoder-theme='dark'] [role="menu"][aria-label="添加内容"],
  html[giencoder-theme='dark'] [role="listbox"][aria-label="权限选择"],
  html[giencoder-theme='dark'] [role="listbox"][aria-label="技能选择"],
  [giencoder-theme=dark] [role="menu"][aria-label="添加内容"],
  [giencoder-theme=dark] [role="listbox"][aria-label="权限选择"],
  [giencoder-theme=dark] [role="listbox"][aria-label="技能选择"]{
    background: rgba(var(--gray-1), 0.88) !important;
  }
</style>
'''

# 每页额外需要压回的「内联样式面板」选择器 —— 经查无（avatar/task-detail 的内联面板
# 就是 .td-skill-pop，已由 step1b + 本块统一处理）⇒ 留空，保持逻辑单一。
PER_PAGE_DARK = {}

RE_BLOCK = re.compile(u'<style id="%s">.*?</style>\\n?' % BLOCK_ID, re.S)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def norm(t):
    return t.replace(u'\r\n', u'\n')


def comment_spans(t):
    u"""注释区间。

    ⚠ 关键：必须**顺序扫描**（找到 `/*` 后跳到 `*/` 之后继续），
       不能对每个 `/*` 独立 `find('*/')` —— 否则一个未闭合/交叉的
       `/*` 会把后面所有活代码都罩进区间（本层实测踩过：
       规则被误判「在注释里」而拒改）。
    """
    out = []
    i = 0
    n = len(t)
    while i < n:
        a = t.find(u'/*', i)
        if a < 0:
            break
        e = t.find(u'*/', a + 2)
        if e < 0:
            out.append((a, n))
            break
        out.append((a, e + 2))
        i = e + 2          # ★ 从注释之后继续，不再回头看
    # HTML 注释 <!-- -->
    i = 0
    while i < n:
        a = t.find(u'<!--', i)
        if a < 0:
            break
        e = t.find(u'-->', a + 4)
        if e < 0:
            out.append((a, n))
            break
        out.append((a, e + 3))
        i = e + 3
    return out


def real_head(t):
    u"""真正的 </head> 下标（排除注释区里的同名行文）；不唯一返回 None"""
    spans = comment_spans(t)
    hits = []
    i = 0
    while True:
        k = t.find(u'</head>', i)
        if k < 0:
            break
        if not any(a <= k < b for a, b in spans):
            hits.append(k)
        i = k + 7
    return hits[0] if len(hits) == 1 else None


def dark_block_for(pg):
    u"""按页生成暗色覆盖块（含该页特有的内联面板选择器）"""
    extra = u''
    if pg in PER_PAGE_DARK:
        sels = PER_PAGE_DARK[pg]
        extra = u'\n  ' + u'  /* 该页下拉面板为内联样式（优先级更高），单独压回 */\n  ' + \
                u',\n  '.join(
                    u'body[giencoder-theme=dark] %s,\n  [giencoder-theme=dark] %s' % (s, s)
                    for s in sels) + u'{\n    background:rgba(var(--gray-1),0.88) !important;\n  }\n'
    return DARK_BLOCK.replace(u'</style>\n', extra + u'</style>\n')


def apply_page(t, pg, sink, warn):
    u"""逐步改写。

    ⚠ 关键：**每改一次都必须重算注释区间**。
       否则第 1 条改写会让文本长度/偏移全部错位，
       而后续条目仍拿**旧 spans** 判定 ⇒ 活代码被误判「落在注释里」而拒改
       （本层实测踩过：D_OLD_LIST[1] 被 D_OLD_LIST[0] 的改写带偏）。
    """
    # ★★ 顺序至关重要，分两阶段（不可合并成一个循环，也不可颠倒）：
    #   阶段 1 = step1（四种旧写法 → var(--color-bg-1)）
    #   阶段 2 = step1b（0.9 → 0.88）
    #   为什么阶段 1 必须在先：阶段 2 的产物正是 `background: rgba(var(--gray-1), 0.88)`
    #   ⇒ 若阶段 1 在后跑，它会把这 20 处**暗色覆盖**也改成 var(--color-bg-1)
    #     （暗色档 --color-bg-1 = #17171a 深黑 ⇒ 面板变纯黑，实测踩过）。
    #   而阶段 2 在最后，不再被任何后续阶段重扫 ⇒ 收敛。
    for old in OLD_LIST:
        new = NEW_FOR[old]
        i = 0
        while True:
            spans = comment_spans(t)          # ★ 每次查找前重算
            own = RE_BLOCK.search(t)
            own_span = (own.start(), own.end()) if own else None
            k = t.find(old, i)
            if k < 0:
                break
            if own_span and own_span[0] <= k < own_span[1]:
                i = k + len(old)
                continue
            if any(a <= k < b for a, b in spans):
                warn.append(u'%s：命中落在注释里，拒绝改写：%s…' % (pg, old[:40]))
                i = k + len(old)
                continue
            t = t[:k] + new + t[k + len(old):]
            sink[old] += 1
            i = k + len(new)

    for old in D_OLD_LIST:
        new = D_NEW_FOR[old]
        i = 0
        while True:
            spans = comment_spans(t)
            own = RE_BLOCK.search(t)
            own_span = (own.start(), own.end()) if own else None
            k = t.find(old, i)
            if k < 0:
                break
            if own_span and own_span[0] <= k < own_span[1]:
                i = k + len(old)
                continue
            if any(a <= k < b for a, b in spans):
                warn.append(u'%s：命中落在注释里，拒绝改写：%s…' % (pg, old[:40]))
                i = k + len(old)
                continue
            t = t[:k] + new + t[k + len(old):]
            sink[old] += 1
            i = k + len(new)
    # step 2：追加/更新暗色覆盖块
    blk = dark_block_for(pg)
    m = RE_BLOCK.search(t)
    if m:
        if norm(m.group(0)) == norm(blk):
            sink[u'(dark-block-already)'] += 1
        else:
            t = t[:m.start()] + blk + t[m.end():]
            sink[u'(dark-block-refresh)'] += 1
    else:
        h = real_head(t)
        if h is None:
            warn.append(u'%s：</head> 不唯一，拒绝注入覆盖块' % pg)
        else:
            t = t[:h] + blk + t[h:]
            sink[u'(dark-block-insert)'] += 1
    return t


def snapshot(force=False):
    u"""拍快照。

    ★ 教训（本层实测踩过）：第 2/3 遍重跑时 snapshot() **覆盖了干净快照**
      ⇒ --revert 再也回不到干净态，只能靠 undo-menuwhite.py 逆运算补救。
      ⇒ 现在：已存在快照时**默认拒绝覆盖**（须显式 --force）。
    """
    if os.path.isdir(BAK) and not force:
        n = len([f for f in os.listdir(BAK) if f.endswith(u'.html')])
        print(u'  ⚠ 快照已存在（%d 页），跳过（避免覆盖干净基线；需覆盖请加 --force）' % n)
        return
    if os.path.isdir(BAK):
        shutil.rmtree(BAK)
    os.makedirs(BAK)
    for pg in ALL:
        src = os.path.join(PAGES, pg + u'.html')
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(BAK, pg + u'.html'))
    print(u'  快照 → mg-work/r109/ev/bak-menuwhite/（%d 页）' % len(ALL))


def revert():
    if not os.path.isdir(BAK):
        print(u'✗ 无快照：%s' % BAK)
        return 2
    n = 0
    for pg in ALL:
        src = os.path.join(BAK, pg + u'.html')
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(PAGES, pg + u'.html'))
            n += 1
    print(u'✓ 已从快照还原 %d 页' % n)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--revert', action='store_true')
    args = ap.parse_args()

    if args.revert:
        return revert()

    sink = collections.Counter()
    per_page = collections.OrderedDict()
    warn, problems, staged = [], [], []

    for pg in ALL:
        p = os.path.join(PAGES, pg + u'.html')
        t = rd(p)
        if not RE_DS_BUNDLE.search(t):
            problems.append(u'%s：找不到 DS 编译包指纹' % pg)
        before = len(norm(t))
        t2 = apply_page(t, pg, sink, warn)
        after = len(norm(t2))
        per_page[pg] = after - before
        if t2 != t:
            staged.append((p, t2))

    if warn:
        problems.append(u'／'.join(warn))

    if problems:
        print(u'✗ 前置校验失败，拒绝落盘：')
        for x in problems:
            print(u'   ' + x)
        return 2

    if staged and not args.check:
        snapshot()
        for p, t2 in staged:
            wr(p, t2)

    print(u'=== r109 第十一拍 · 下拉菜单面板浅色档 → 白色（%s）==='
          % (u'检查' if args.check else u'落盘'))
    print()
    for old in OLD_LIST:
        print(u'  [step1 ] ×%-3d %s' % (sink[old], old))
    print(u'          → %s' % NEW_FOR[OLD_LIST[0]])
    print()
    for old in D_OLD_LIST:
        print(u'  [step1b] ×%-3d 0.9 → 0.88  %s…' % (sink[old], old[:58]))
    print()
    print(u'  [step2 ] 暗色覆盖块：注入 %d 页 / 刷新 %d 页 / 已就绪 %d 页'
          % (sink[u'(dark-block-insert)'], sink[u'(dark-block-refresh)'],
             sink[u'(dark-block-already)']))
    print()
    print(u'── 每页字符数变化（规范化 \\r\\n→\\n 后）──')
    for pg, d in per_page.items():
        print(u'   %-12s %+d' % (pg, d))
    return 0


if __name__ == '__main__':
    sys.exit(main())
