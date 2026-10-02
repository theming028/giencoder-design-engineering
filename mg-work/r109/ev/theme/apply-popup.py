# -*- coding: utf-8 -*-
r"""r109 第九拍 · 「下拉菜单面板」配色统一到**基准**（基础工作台对话框「默认权限」下拉）。

★ 起因（邵先生实测反馈）：base 页「标准模式 / 大模型 / 工作目录 / 添加」等下拉的暗色配色
  与「默认权限」下拉**不一致**。真机取证（raw/dd9/panel-*.json）显示暗色档面板底差 **64 级**：

    默认权限（基准）  rgba(31,31,31,0.88)   blur(10px) saturate(100%)   ← 基准
    技能              rgba(31,31,31,0.88)   blur(10px) saturate(100%)   ✅ 已同基准
    标准模式/大模型/工作目录  rgb(95,95,96)  无磨砂                        ❌ 亮 64 级
    添加              rgb(35,35,36)        blur(20px)                   ❌ 暗一级且无边框

  根因：三种面板用了**三个不同 DS 变量** ——
    基准 = `rgba(var(--gray-1), 0.88)`（半透明 + 磨砂）
    select 浮层 = `var(--color-bg-5)`（暗色 `#5f5f60`，不透明）
    添加菜单   = `var(--color-bg-2)`（暗色 `#232324`，不透明）

★ 统一策略：**只做整条精确配对**（写死原文 → 新文 + 断言全站次数），不做通用改值。
  - 底 / 磨砂 / 描边全部对齐基准规格；`z-index / radius / 尺寸 / 阴影` **一字不动**。
  - 浅色档影响：`#fff` → `rgba(247,247,247,0.88)` + 磨砂 —— 与基准**同款**，属统一的必要结果。

用法：
  python apply-popup.py            # 落盘（先快照到 ev/bak-popup/）
  python apply-popup.py --check    # 只检查（不落盘）
  python apply-popup.py --revert   # 从快照回滚
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
BAK = os.path.join(ROOT, 'mg-work', 'r109', 'ev', 'bak-popup')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

# DS 编译包指纹（每页必须存在，否则拒绝落盘）
RE_DS_BUNDLE = re.compile(re.escape(u':root{--giencoderblue-1:245, 248, 255'))

# ───────────────────────── A. CSS：TDesign select 浮层 → 基准规格 ─────────────────────────
SEL_POPUP_OLD = (
    u'.giencoder-select-popup{z-index:1000;background:var(--color-bg-5);'
    u'border:1px solid var(--color-border-2);border-radius:8px;width:max-content;'
    u'min-width:200px;max-height:280px;padding:6px;position:absolute;'
    u'top:calc(100% + 4px);left:0;overflow-y:auto;box-shadow:0 8px 20px #0000001a}')
SEL_POPUP_NEW = (
    u'.giencoder-select-popup{z-index:1000;background:rgba(var(--gray-1),0.88);'
    u'border:1px solid var(--color-border-2);border-radius:8px;width:max-content;'
    u'min-width:200px;max-height:280px;padding:6px;position:absolute;'
    u'top:calc(100% + 4px);left:0;overflow-y:auto;box-shadow:0 8px 20px #0000001a;'
    u'backdrop-filter:blur(10px) saturate(100%);'
    u'-webkit-backdrop-filter:blur(10px) saturate(100%)}')

# ───────────────────────── B. JS：添加菜单面板 → 基准规格 ─────────────────────────
ADD_OLD = (
    u'background:`var(--color-bg-2)`,borderRadius:8,'
    u'boxShadow:`0px 8px 20px 0px rgba(0, 0, 0, 0.1), '
    u'inset 0 0 0 1px var(--color-border-2)`,'
    u'backdropFilter:`blur(20px)`,WebkitBackdropFilter:`blur(20px)`')
ADD_NEW = (
    u'background:`rgba(var(--gray-1), 0.88)`,borderRadius:8,'
    u'boxShadow:`0px 8px 20px 0px rgba(0, 0, 0, 0.1), '
    u'inset 0 0 0 1px var(--color-border-2)`,'
    u'backdropFilter:`blur(10px) saturate(100%)`,'
    u'WebkitBackdropFilter:`blur(10px) saturate(100%)`')

# ───────────────────────── A2. CSS：ZCode 复刻菜单（conversation）→ 基准 ─────────────────────────
#   真机实测（raw/dd9-dark/panel-{4,5}.json）：暗色档 = color(srgb .3725 ×3 / .82) ≈ rgb(95,95,96)@.82，
#   与基准 rgba(31,31,31,.88) 差 64 级；磨砂是 blur(18px) saturate(160%)。
#   ⚠ 磨砂那条规则与 `.zd-toast` **共享选择器** ⇒ 不直接改它（会波及 toast），
#     改为在最后一条 background 规则里**只给菜单**追加 backdrop-filter 覆盖。
ZD_MIX_OLD = u'.zd-menu.giencoder-dropdown-popup { background: color-mix(in srgb, var(--color-bg-popup) 82%, transparent); }'
ZD_MIX_NEW = u'.zd-menu.giencoder-dropdown-popup { background: rgba(var(--gray-1),0.88); }'
ZD_LAST_OLD = u'.zd-menu.giencoder-dropdown-popup { background: var(--color-bg-popup); }'
ZD_LAST_NEW = (u'.zd-menu.giencoder-dropdown-popup { background: rgba(var(--gray-1),0.88); '
               u'backdrop-filter: blur(10px) saturate(100%); '
               u'-webkit-backdrop-filter: blur(10px) saturate(100%); }')

PAIRS_CSS = [
    (SEL_POPUP_OLD, SEL_POPUP_NEW, 10, u'select 浮层底 → 基准半透明磨砂（10 页）'),
]
PAIRS_JS = [(ADD_OLD, ADD_NEW, 2, u'添加菜单面板底 + 磨砂 → 基准（base/conversation）')]

# ★ ZD_* 两条**不再替换**：查明它是 r108 第十六拍③ 的**有意设计**——
#   conversation.html 注释明写「四件各自沿用各自的原底色 token（.zd-menu/.zd-toast 原本是
#   --color-bg-popup）—— 一律换成 --color-bg-2 会让暗色下的弹层比面板白一档」
#   ⇒ 菜单比卡片亮一档是刻意的层次；blur(18px) saturate(160%) 也是毛玻璃方案的一部分。
#   按红线（不擅动其他模块的有意设计），撤出本层，列 KEEP 待邵先生裁决。

EXPECT = {SEL_POPUP_OLD: 10, ADD_OLD: 2}

KEEP = [
    (u'.zd-menu.giencoder-dropdown-popup（conversation）',
     u'★ r108 有意设计：菜单比卡片**亮一档**是刻意层次，blur(18px) saturate(160%) 属毛玻璃方案 ⇒ 待裁决'),
    (u'.giencoder-date-picker-popup（kanban/req-kanban/task-detail）',
     u'日期选择器面板，结构不同（需较实底色才看得清日期）⇒ 待裁决'),
    (u'.giencoder-popup{background:var(--color-bg-white)}',
     u'通用弹层；实测 DOM 实例 = 0（死规则）。⚠ 但其暗色档 #f6f6f6 近白，属隐患'),
    (u'.giencoder-date-picker-popup{background:var(--color-bg-popup)}',
     u'日期选择器面板，独立组件，待邵先生确认'),
    (u'.zd-menu.giencoder-dropdown-popup{color-mix(...)}',
     u'ZCode 复刻菜单（conversation），待邵先生确认'),
]


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def comment_spans(t):
    """HTML 注释 <!-- --> 与 CSS 注释 /* */ 的区间（old 命中落在其中 ⇒ 拒绝改写）"""
    out = []
    for m in re.finditer(u'<!--', t):
        e = t.find(u'-->', m.end())
        out.append((m.start(), (e + 3) if e > 0 else len(t)))
    for m in re.finditer(u'/\\*', t):
        e = t.find(u'*/', m.end())
        out.append((m.start(), (e + 2) if e > 0 else len(t)))
    return out


def apply_page(t, sink, warn):
    spans = comment_spans(t)
    for old, new, _n, _note in PAIRS_CSS + PAIRS_JS:
        if old not in t:
            continue
        i = 0
        while True:
            k = t.find(old, i)
            if k < 0:
                break
            if any(a <= k < b for a, b in spans):
                warn.append(u'命中落在注释里，拒绝改写：%s…' % old[:40])
                i = k + len(old)
                continue
            t = t[:k] + new + t[k + len(old):]
            sink[(old, new)] += 1
            i = k + len(new)
    return t


def snapshot():
    if os.path.isdir(BAK):
        shutil.rmtree(BAK)
    os.makedirs(BAK)
    for pg in ALL:
        src = os.path.join(PAGES, pg + u'.html')
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(BAK, pg + u'.html'))
    print(u'  快照 → mg-work/r109/ev/bak-popup/（%d 页）' % len(ALL))


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
        before = len(t.replace(u'\r\n', u'\n'))
        t2 = apply_page(t, sink, warn)
        after = len(t2.replace(u'\r\n', u'\n'))
        per_page[pg] = after - before
        if t2 != t:
            staged.append((p, t2))

    if warn:
        problems.append(u'／'.join(warn))
    for old, _new, _d, _note in PAIRS_CSS + PAIRS_JS:
        got = sink.get((old, _new), 0)
        if got and got != EXPECT[old]:
            problems.append(u'总量不符：期望 %d 实得 %d（%s…）' % (EXPECT[old], got, old[:36]))

    if problems:
        print(u'✗ 前置校验失败，拒绝落盘：')
        for x in problems:
            print(u'   ' + x)
        return 2

    if staged and not args.check:
        snapshot()
        for p, t2 in staged:
            wr(p, t2)

    print(u'=== r109 第九拍 · 下拉菜单面板配色统一到基准（%s）==='
          % (u'检查' if args.check else u'落盘'))
    print()
    for old, new, d, note in PAIRS_CSS:
        print(u'  [CSS] ×%-3d %s' % (sink.get((old, new), 0), note))
        print(u'        旧底 %s' % old[old.find(u'background:'):old.find(u'border-radius')])
        print(u'        新底 %s' % new[new.find(u'background:'):new.find(u'border-radius')])
    for old, new, d, note in PAIRS_JS:
        print(u'  [JS ] ×%-3d %s' % (sink.get((old, new), 0), note))
    print()
    print(u'── 每页字符数变化（规范化 \\r\\n→\\n 后）──')
    for pg, d in per_page.items():
        print(u'   %-12s %+d' % (pg, d))
    print()
    print(u'── 刻意保留（不在本次统一范围）──')
    for k, why in KEEP:
        print(u'   %-52s %s' % (k[:52], why))
    return 0


if __name__ == '__main__':
    sys.exit(main())
