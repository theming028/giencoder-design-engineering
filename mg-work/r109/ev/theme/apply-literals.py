# -*- coding: utf-8 -*-
r"""r109 第八拍 · 指令 B 收口：**编译包内 + React bundle 内**剩余字面色值 → DS 色彩系统变量。

邵先生 2026-10-02 指令（第 2 条铁律 + 「打断」升级版）：
  「全站不允许硬编码，若有统一替换为设计系统里最相近的色彩系统。」
  「全局所有界面的色值一律要使用 giencoder 设计系统里已有的色彩系统变量。」

★ 为什么必须在 `apply-tokens.py` **之外**单开一层（而不是并进去）：
  `apply-tokens.py` 的作用域是「**我们自己的** `<style>` 块」，它**刻意跳过**两块：
    · 每页 1 块的 **93.7KB 编译包**（`style/(anon)`，指纹 `:root{--giencoderblue-1:`）
      —— 里面混着两类东西：DS 本体（`:root` / `[giencoder-theme=dark]`）**和**
      **页面级规则**（`.perm-menu-item:hover` 之类）。前者绝不能碰，后者必须收敛；
    · `<script>`（React 编译产物）—— 里面的色值可能是字符串拼接 / 模板 / 状态机，
      通用改写语义不可控。
  本层因此**只做「整条精确配对」**（不做通用改值）：
    每一条都写死「原文 → 新文」并**断言全站出现次数**，多一处少一处都报错拒写。
  ⇒ 新链序：`make109.py → apply109.py → apply-theme.py → apply-dark.py
              → apply-tokens.py → **本脚本**`

★★ 三类改动（全部可核、全部幂等）：
  A. **编译包内的页面级规则**（6 组 × 10 页）：下拉 / hover 的底色与描边
     `.ws-item-hover:hover` / `.model-dropdown-menu-item:hover` / `.workdir-menu-item:hover` /
     `.perm-menu-item:hover,.session-action-item:hover` / `.ws-trigger-hover:hover` /
     `.ws-dropdown-hover:hover`。→ 换成 `--color-fill-*` / `--color-border-*`，
     **浅色档 Δ ≤ 5**，暗色档**自动翻转**（原先靠 apply-dark.py 一条条定向覆盖）。
  B. **已死的尾风任意值类规则**（12 条 × 10 页）：`apply-tokens.py` 第七拍·D 已把
     这些类的**用法**全换成 `var()` 版类名 ⇒ 原规则**零引用**（实测：非 `<style>` 区
     出现 0 次）。规则体里的 `rgb(233 236 238/…)` 与选择器里的 `\#E9ECEE` 都是**死字面**，
     整条删除。⚠ **交通灯 3 条（`#FF5F57`/`#FEBC2E`/`#28C840`）仍被 JS 引用 ⇒ 保留**。
  C. **React bundle 里的内联样式 / 规格字段**（10 组 × 10 页）：
     面板描边 `1px solid #E5E5E5` / `#F2F2F2` / `#E4E6EA`（**下拉浮层的外描边**）、
     模型下拉的 `textColor`（数据里自带 `textToken:'文本/@color-text-1'` 标注）、
     工作空间下拉的选中态 `#ECF2FF` / `#D3E2FF` / `#3570FB`、分段控件激活底 `#E2E3E4`。

★ 刻意**不动**的（各有硬理由，逐条列在 --check 的输出里）：
  · 属性含 `mask` / 值为 `#0000`（透明）—— 非颜色（alpha 通道 / 透明关键字）；
  · `box-shadow` / `filter` 里的黑白色（`rgba(0,0,0,.08)` / `#FFFFFF` / `#0000001a`）
    —— 邵先生裁决：「几何可对齐的才整条换」，这些几何与 DS 的 `--shadowN-*` 对不上；
  · `rgba(0,0,0,.12)` 等浮层投影 —— 同上；
  · **品牌 logo**：`logoColor:` 五色（工作空间徽标）、`fill:` 的厂商标识矢量
    —— 邵先生裁决：「维持豁免」；
  · **深浅两档同处一个三元表达式的冷灰外壳**：`l = c ? '#F4F5F6' : '#E5EDF5'`
    —— 二者是**有意的双色调**（基础工作台偏中性 / 研发工作台偏冷），
    只收敛其一会**抹掉这个区分**；且 `#E5EDF5`(229,237,245) 与最近灰阶
    `--gray-2`(242,242,242) **Δ13**、**掉色相**，超出本工程既定的「同族就近」阈值
    （`apply-tokens.py` 的 `TOL=12`）⇒ 浅色档原样保留，暗色档由 `apply-dark.py`
    的 `[style*="background: rgb(229, 237, 245)"]` 定向覆盖（早已覆盖，实测有效）。

用法：
  python mg-work/r109/ev/theme/apply-literals.py            # 落盘（先快照到 ev/bak-lit2/）
  python mg-work/r109/ev/theme/apply-literals.py --check    # 只报会改什么
  python mg-work/r109/ev/theme/apply-literals.py --revert   # 从 ev/bak-lit2/ 回滚
"""
import argparse
import collections
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PAGES = os.path.join(REPO, 'pages')
BAK = os.path.join(HERE, 'bak-lit2')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

# ---------------------------------------------------------------------------
# A. 编译包内「页面级规则」：整条精确替换（原文 → 新文, 浅色 Δ, 说明）
# ---------------------------------------------------------------------------
PAIRS_CSS = [
    (u'.ws-item-hover:hover{background-color:#f7f7f7!important}',
     u'.ws-item-hover:hover{background-color:var(--color-fill-1)!important}',
     0, u'#f7f7f7 ≡ --gray-1 精确（工作空间下拉项 hover）'),
    (u'.model-dropdown-menu-item:hover{background-color:#f3f4f5!important}',
     u'.model-dropdown-menu-item:hover{background-color:var(--color-fill-2)!important}',
     3, u'#f3f4f5 ≈ --gray-2（大模型下拉项 hover）'),
    (u'.workdir-menu-item:hover{background-color:#f3f4f5!important}',
     u'.workdir-menu-item:hover{background-color:var(--color-fill-2)!important}',
     3, u'同上（工作目录下拉项 hover）'),
    (u'.perm-menu-item:hover,.session-action-item:hover{background-color:#f3f4f5!important}',
     u'.perm-menu-item:hover,.session-action-item:hover{background-color:var(--color-fill-2)!important}',
     3, u'同上（权限下拉 = 邵先生指定的**基准**、会话操作项）'),
    (u'.ws-trigger-hover:hover{background-color:#e4e6ea!important}',
     u'.ws-trigger-hover:hover{background-color:var(--color-border-2)!important}',
     5, u'#e4e6ea ≈ --gray-3（工作空间触发器 hover）'),
    (u'.ws-dropdown-hover:hover{background:#e4e6ea!important}',
     u'.ws-dropdown-hover:hover{background:var(--color-border-2)!important}',
     5, u'同上（工作空间下拉项 hover）'),
    # ── 第八拍·补：占位符色（第二遍审计揪出的漏网）────────────────────────
    (u'.ws-search-input::placeholder{color:#a9a9a9}',
     u'.ws-search-input::placeholder{color:rgb(var(--gray-5))}',
     0, u'#a9a9a9 ≡ --gray-5 精确（工作空间搜索框占位符）'),
    (u'input::-moz-placeholder{opacity:1;color:#9ca3af}',
     u'input::-moz-placeholder{opacity:1;color:rgb(var(--gray-5))}',
     13, u'#9ca3af ≈ --gray-5（Tailwind preflight 占位符；Δ13 略超 TOL=12，'
         u'收它只为消除与上式「双占位符色」——DS 里 gray-5 是最近一级）'),
    (u'textarea::-moz-placeholder{opacity:1;color:#9ca3af}',
     u'textarea::-moz-placeholder{opacity:1;color:rgb(var(--gray-5))}',
     13, u'同上'),
    (u'input::placeholder,textarea::placeholder{opacity:1;color:#9ca3af}',
     u'input::placeholder,textarea::placeholder{opacity:1;color:rgb(var(--gray-5))}',
     13, u'同上'),
]

# ---------------------------------------------------------------------------
# B. 已死的尾风任意值类规则：整条删除（选择器原文，转义形式）
#    ⚠ 交通灯 3 条保留（JS 仍在用）：bg-\[\#FF5F57\] / bg-\[\#FEBC2E\] / bg-\[\#28C840\]
# ---------------------------------------------------------------------------
KILL_SEL = [
    r'.bg-\[\#E9ECEE\]',
    r'.hover\:bg-\[\#E9ECEE\]:hover',
    r'.hover\:\!bg-\[\#E9ECEE\]:hover',
    r'.bg-\[\#F4F5F6\]',
    r'.bg-\[\#E5EDF5\]',
    r'.bg-\[\#E4E6EA\]',
    r'.bg-\[\#DAE3ED\]',
    r'.bg-\[\#C9CDD3\]',
    r'.border-\[\#DAE3ED\]',
    r'.border-\[\#E4E6EA\]',
    r'.border-\[\#ECEEF2\]',
    r'.text-\[\#3770F7\]',
]

# ---------------------------------------------------------------------------
# C. React bundle：内联样式 / 规格字段（原文 → 新文, 浅色 Δ, 说明）
#    用**反引号整体**做锚（确保命中 JS 模板串，不误伤注释 / 样式表）
#    ⚠ `.inset` 那条原为 `inset 0 0 0 1px #E5E5E5`，但该串**同时出现在
#      r109-dark-css 的注释里**（「原文 inset 0 0 0 1px #E5E5E5」）⇒ 加 `, ` 前缀
#      限定到代码上下文（实测：仅 base / conversation 各 1 处，其余页 0 处）。
# ---------------------------------------------------------------------------
PAIRS_JS = [
    (u'`1px solid #E5E5E5`', u'`1px solid var(--color-border-2)`',
     0, u'#E5E5E5 ≡ --gray-3 精确（下拉浮层外描边）'),
    (u', inset 0 0 0 1px #E5E5E5', u', inset 0 0 0 1px var(--color-border-2)',
     0, u'同上（用 inset 环冒充的 1px 描边）'),
    (u'`1px solid #F2F2F2`', u'`1px solid var(--color-border-1)`',
     0, u'#F2F2F2 ≡ --gray-2 精确（卡片/输入框描边）'),
    (u'`1px solid #E4E6EA`', u'`1px solid var(--color-border-2)`',
     5, u'#E4E6EA ≈ --gray-3（面板描边）'),
    (u'`#ECF2FF`', u'`var(--color-primary-1)`',
     9, u'#ECF2FF ≈ --giencoderblue-1（工作空间下拉选中态底）'),
    (u'`1px solid #D3E2FF`', u'`1px solid var(--color-primary-2)`',
     7, u'#D3E2FF ≈ --giencoderblue-2（同上，选中态描边）'),
    (u'`#3570FB`', u'`var(--color-primary-6)`',
     4, u'#3570FB ≈ --giencoderblue-6（选中项标题色）'),
    (u'`#1E1E1E`', u'`var(--color-text-1)`',
     1, u'#1E1E1E ≈ --gray-10；数据自带 textToken:`文本/@color-text-1` 标注'),
    (u'`#BEBEBE`', u'`var(--color-text-4)`',
     11, u'#BEBEBE ≈ --gray-4；数据自带 textToken:`文本/@color-text-4` 标注'),
    (u'`#E2E3E4`', u'`var(--color-fill-3)`',
     3, u'#E2E3E4 ≈ --gray-3（分段控件激活底；暗色档原先**无覆盖**）'),
    # ── 第八拍·补：task-detail 里「数字分身」按钮的**静态**内联样式 ──────────
    #    （JS 字符串里写死的一整套浅蓝 chip：底 / 字 / 描边）
    (r'style=\"background: rgb(236, 242, 255); color: rgb(55, 112, 247); '
     r'border: 1px solid rgb(211, 226, 255);\"',
     r'style=\"background: var(--color-primary-1); color: var(--color-primary-6); '
     r'border: 1px solid var(--color-primary-2);\"',
     0, u'rgb(236,242,255)/rgb(55,112,247)/rgb(211,226,255) ≈ giencoderblue 1/6/2'
        u'（task-detail 工作空间切换按钮；暗色档原先靠 [style*=] 兜）'),
]

# 全站期望总量（= 10 页合计；对不上即判为「页面被别的层动过」⇒ 拒绝落盘）
EXPECT = {
    u'.ws-item-hover:hover{background-color:#f7f7f7!important}': 10,
    u'.model-dropdown-menu-item:hover{background-color:#f3f4f5!important}': 10,
    u'.workdir-menu-item:hover{background-color:#f3f4f5!important}': 10,
    u'.perm-menu-item:hover,.session-action-item:hover{background-color:#f3f4f5!important}': 10,
    u'.ws-trigger-hover:hover{background-color:#e4e6ea!important}': 10,
    u'.ws-dropdown-hover:hover{background:#e4e6ea!important}': 10,
    u'`1px solid #E5E5E5`': 24,
    u', inset 0 0 0 1px #E5E5E5': 2,
    u'`1px solid #F2F2F2`': 10,
    u'`1px solid #E4E6EA`': 2,
    u'`#ECF2FF`': 12,
    u'`1px solid #D3E2FF`': 12,
    u'`#3570FB`': 10,
    u'`#1E1E1E`': 24,
    u'`#BEBEBE`': 4,
    u'`#E2E3E4`': 4,
    u'.ws-search-input::placeholder{color:#a9a9a9}': 10,
    u'input::-moz-placeholder{opacity:1;color:#9ca3af}': 10,
    u'textarea::-moz-placeholder{opacity:1;color:#9ca3af}': 10,
    u'input::placeholder,textarea::placeholder{opacity:1;color:#9ca3af}': 10,
    r'style=\"background: rgb(236, 242, 255); color: rgb(55, 112, 247); '
    r'border: 1px solid rgb(211, 226, 255);\"': 1,
}
KILL_EXPECT = 120          # 12 条 × 10 页

# 刻意保留的（写出来供 --check 报告；键 = 字面，值 = 理由）
KEEP = [
    (u'#0000 / #fff / #000（DS `:root` 内）', u'DS 本体：`--color-white/black/bg-*/menu-*-bg` 的**定义处**'),
    (u'#000（mask-image 内）', u'mask 的 alpha 通道，不是颜色（.scroll-fade / .r74-ripple / .dot-bg）'),
    (u'#0000001a / rgba(0,0,0,.1) 等', u'Tailwind 阴影工具类与脚本内阴影——几何对不上 DS 的 --shadowN-*'),
    (u'rgba(255,255,255,.5/.9) / #FFFFFF', u'inset 高光（主题中性的 scrim）'),
    (u'logoColor: 五色 + 厂商标识 fill:', u'品牌 logo（邵先生：「维持豁免」）'),
    (u"l = c ? '#F4F5F6' : '#E5EDF5'", u'冷灰外壳双色调；后者 Δ13 掉色相 ⇒ 超阈值 + 免抹区分'),
    (u'#FF5F57 / #FEBC2E / #28C840', u'macOS 交通灯系统色（三枚圆点仍由 JS 用该类名）'),
]

RE_DS_BUNDLE = re.compile(r':root\{--giencoderblue-1:')


def rd(p):
    return io.open(p, 'rb').read().decode(u'utf-8').replace(u'\r\n', u'\n')


def wr(p, t):
    io.open(p, 'wb').write(t.replace(u'\n', u'\r\n').encode(u'utf-8'))


def snapshot():
    if os.path.isdir(BAK):
        shutil.rmtree(BAK)
    os.makedirs(BAK)
    for pg in ALL:
        shutil.copy2(os.path.join(PAGES, pg + u'.html'), os.path.join(BAK, pg + u'.html'))


def revert():
    if not os.path.isdir(BAK):
        print(u'✗ 没有快照 %s，无法回滚' % BAK)
        return 1
    n = 0
    for pg in ALL:
        s = os.path.join(BAK, pg + u'.html')
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(PAGES, pg + u'.html'))
            n += 1
    print(u'✓ 已从 %s 回滚 %d 页' % (BAK, n))
    return 0


def comment_spans(t):
    u"""HTML `<!-- -->` 与 CSS `/* */` 的区间（只用来**告警**，不改写）。"""
    sp = []
    for m in re.finditer(r'<!--.*?-->', t, re.S):
        sp.append((m.start(), m.end()))
    for m in re.finditer(r'/\*.*?\*/', t, re.S):
        sp.append((m.start(), m.end()))
    return sp


def apply_page(t, sink, warn):
    u"""返回 (新文本, 改动数)。

    ★ 护栏：任何一条 `old` 若**有命中落在注释里** ⇒ 记入 warn（调用方拒写）。
      理由：注释里的字面是**文档**（例如「原文 inset 0 0 0 1px #E5E5E5」），
            改写它会让注释自相矛盾；这正是本拍第一次 --check 踩到的坑。
    """
    n = 0
    sp = comment_spans(t)
    for old, new, _d, _note in PAIRS_CSS + PAIRS_JS:
        hits = [m.start() for m in re.finditer(re.escape(old), t)]
        inc = [i for i in hits if any(a <= i < b for a, b in sp)]
        if inc:
            warn.append(u'命中注释（拒绝改写）：%s ×%d' % (old, len(inc)))
            continue
        if hits:
            t = t.replace(old, new)
            n += len(hits)
            sink[(u'PAIR', old, new)] += len(hits)
    for sel in KILL_SEL:
        pat = re.compile(re.escape(sel) + r'\{[^}]*\}')
        ms = list(pat.finditer(t))
        inc = [m for m in ms if any(a <= m.start() < b for a, b in sp)]
        if inc:
            warn.append(u'规则命中注释（拒绝删除）：%s ×%d' % (sel, len(inc)))
            continue
        if ms:
            t = pat.sub(u'', t)
            n += len(ms)
            sink[(u'KILL', sel, u'')] += len(ms)
    return t, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--revert', action='store_true')
    args = ap.parse_args()

    if args.revert:
        return revert()

    total_pairs = collections.Counter()
    total_kills = collections.Counter()
    per_page = collections.OrderedDict()
    warn = []
    problems = []
    staged = []          # (路径, 新文本)

    for pg in ALL:
        p = os.path.join(PAGES, pg + u'.html')
        t = rd(p)
        if not RE_DS_BUNDLE.search(t):
            problems.append(u'%s：找不到 DS 编译包指纹' % pg)
        sink = collections.defaultdict(int)
        t2, n = apply_page(t, sink, warn)
        for (kind, old, new), c in sink.items():
            if kind == u'PAIR':
                total_pairs[(old, new)] += c
            else:
                total_kills[old] += c
        per_page[pg] = n
        if n:
            staged.append((p, t2))

    if warn:
        problems.append(u'／'.join(warn))

    # 总量断言：对不上 ⇒ 页面被别的层动过，拒绝静默改写
    for old, new, _d, _note in PAIRS_CSS + PAIRS_JS:
        got = total_pairs.get((old, new), 0)
        if got and got != EXPECT[old]:
            problems.append(u'总量不符：%s 期望 %d 实得 %d' % (old, EXPECT[old], got))
    kg = sum(total_kills.values())
    if kg and kg != KILL_EXPECT:
        problems.append(u'删除总量不符：期望 %d 实得 %d' % (KILL_EXPECT, kg))

    if problems:
        print(u'✗ 前置校验失败，拒绝落盘：')
        for x in problems:
            print(u'   ' + x)
        return 2

    # ★ 先快照、再落盘（本工程惯例：「先快照再落盘」救过场）
    if staged and not args.check:
        snapshot()
        for p, t2 in staged:
            wr(p, t2)

    print(u'=== r109 第八拍 · 编译包 + React bundle 字面色值 → DS 变量（%s）==='
          % (u'检查' if args.check else u'落盘'))
    print()
    print(u'── A. 编译包内页面级规则（整条替换）──')
    any_a = False
    for old, new, d, note in PAIRS_CSS:
        c = total_pairs.get((old, new), 0)
        if c:
            any_a = True
            print(u'   ×%-3d Δ%-3d %s' % (c, d, note))
            print(u'        %s' % old)
            print(u'     →  %s' % new)
    if not any_a:
        print(u'   （已是目标态：0 处）')
    print()
    print(u'── C. React bundle 内联样式 / 规格字段（整条替换）──')
    any_c = False
    for old, new, d, note in PAIRS_JS:
        c = total_pairs.get((old, new), 0)
        if c:
            any_c = True
            print(u'   ×%-3d Δ%-3d %s' % (c, d, note))
            print(u'        %s   →   %s' % (old, new))
    if not any_c:
        print(u'   （已是目标态：0 处）')
    print()
    print(u'── B. 已死尾风任意值类规则（整条删除）──')
    any_b = False
    for sel in KILL_SEL:
        c = total_kills.get(sel, 0)
        if c:
            any_b = True
            print(u'   ×%-3d 删除规则 %s{…}' % (c, sel))
    if not any_b:
        print(u'   （已是目标态：0 处）')
    print()
    print(u'── 刻意保留（豁免）──')
    for k, why in KEEP:
        print(u'   %-44s %s' % (k, why))
    print()
    print(u'按页改动数：' + u'  '.join(u'%s=%d' % (k, v) for k, v in per_page.items()))
    print(u'合计 %d 处' % sum(per_page.values()))
    if args.check:
        print(u'（--check：未落盘）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
