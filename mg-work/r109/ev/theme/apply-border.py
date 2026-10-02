# -*- coding: utf-8 -*-
r"""r109 第十拍 ① · 暗色档描边令牌各降一级（`--color-border-1/2/3`）。

★ 起因（邵先生实测反馈）：
     「当前暗色模式下的 var(--color-border-2) 的色值在暗色模式下看着太亮了，
       与整体风格不搭调，但是在浅色模式下的 var(--color-border-2) 看着却很合适。」

★ 根因（量化）：
   DS 的暗色档把 border-1/2/3 声明成与浅色档**同一级灰度索引**
   （border-1 = gray-2、border-2 = gray-3、border-3 = gray-4）。
   但暗色档的灰度阶梯是浅色档的**镜像**（N ↔ 11−N），于是「同一个索引」
   在暗色下落在阶梯的**亮端**：

        令牌        浅（底 #fff = 255）   暗旧（底 #17171a = 23）   暗新
        border-1    242   Δ13             43   Δ20                  31   Δ8
        border-2    229   Δ26             78   Δ55                  43   Δ20
        border-3    201   Δ54            107   Δ84                  78   Δ55

   暗色的 Δ 系统性地比浅色大 2~3 倍 ⇒ 观感「太亮、不搭调」。

★ 修法：只把**暗色档**的 border-1/2/3 各降一级（gray-2→1、gray-3→2、gray-4→3）。
   - 浅色档**一字不动**（覆盖块只在 `[giencoder-theme=dark]` 下生效）。
   - **非侵入**：不改写 DS 编译包，只追加 `<style id="r109-border-css">` 覆盖块
     （与 r109-theme-css / r109-dark-css / r109-tw-css 同一架构），可整块摘除回滚。
   - 只动 border-1/2/3：`--color-border-4` 与 `--color-border` 全站 **var() 引用量 = 0**
     （死令牌），按红线（不擅动不必涉及的）不动。

★ 插入点：**真正的** `</head>` 之前（在 DS 包与所有 r109 头内块之后）
   ⇒ 选择器与 DS 暗色块**逐字相同**、位置更靠后 ⇒ 覆盖必然生效。
   ⚠ 每页 `</head>` 字面出现 **2 次**：第一次是 `r109-dark-css` 注释里的行文
     （「本块注入在 `</head>` 前」）⇒ 必须用「不在注释区间内」筛出真标签。

用法：
  python apply-border.py            # 落盘（先快照到 ev/bak-border/）
  python apply-border.py --check    # 只检查（不落盘）
  python apply-border.py --revert   # 从快照回滚
"""
import argparse
import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
PAGES = os.path.join(ROOT, 'pages')
BAK = os.path.join(ROOT, 'mg-work', 'r109', 'ev', 'bak-border')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

BLOCK_ID = u'r109-border-css'

# DS 编译包指纹（每页必须存在，否则拒绝落盘）
RE_DS_BUNDLE = re.compile(re.escape(u':root{--giencoderblue-1:245, 248, 255'))
# 暗色档指纹（证明 DS 暗色变量块确实在 </head> 之前）
DARK_MARK = u'--color-bg-1:#17171a'

# ── 覆盖块正文 ────────────────────────────────────────────────────────────────
# ⚠ 注释里**刻意不写** `--color-border-N:rgb(var(--gray-M))` 这种完整声明串：
#   后面的层（含「全站禁硬编码」审计）会按字面扫全文，注释里的旧串会造成假命中。
BLOCK = u'''<style id="r109-border-css">
  /* ★ r109 第十拍 ①：暗色档描边令牌各降一级。
     起因：邵先生实测 —— 暗色下 border-2「看着太亮，与整体风格不搭调」，
           而浅色下同一个令牌「看着很合适」。
     根因：DS 的暗色档把 border-1/2/3 声明成与浅色档**同一级灰度索引**
           （border-1 = gray-2、border-2 = gray-3、border-3 = gray-4）；
           但暗色档的灰度阶梯是浅色档的**镜像**（N 对应 11-N），
           于是同一索引在暗色下落在阶梯的亮端：
             浅（底 #fff = 255）   ：242 / 229 / 201  → 与底差 13 / 26 / 54
             暗旧（底 #17171a = 23）： 43 /  78 / 107  → 与底差 20 / 55 / 84
     修法：暗色档三个令牌各降一级（gray-2→1、gray-3→2、gray-4→3）得 31 / 43 / 78，
           与底差 8 / 20 / 55 ≈ 浅色档的 13 / 26 / 54。
     约束：① 本块只在 [giencoder-theme=dark] 下生效 ⇒ 浅色档零变化；
           ② 非侵入，不改写 DS 编译包，摘掉本块即回到原样；
           ③ 只动 border-1/2/3 —— border-4 与无后缀的那个令牌全站引用量为 0（死令牌）。 */
  body[giencoder-theme=dark],[giencoder-theme=dark]{
    --color-border-1:rgb(var(--gray-1));
    --color-border-2:rgb(var(--gray-2));
    --color-border-3:rgb(var(--gray-3));
  }
</style>
'''

RE_BLOCK = re.compile(u'<style id="%s">.*?</style>\\n?' % BLOCK_ID, re.S)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def norm(t):
    return t.replace(u'\r\n', u'\n')


def comment_spans(t):
    """HTML 注释 <!-- --> 与 CSS 注释 /* */ 的区间。"""
    out = []
    for m in re.finditer(u'<!--', t):
        e = t.find(u'-->', m.end())
        out.append((m.start(), (e + 3) if e > 0 else len(t)))
    for m in re.finditer(u'/\\*', t):
        e = t.find(u'*/', m.end())
        out.append((m.start(), (e + 2) if e > 0 else len(t)))
    return out


def real_head(t):
    """返回真正的 </head> 下标（排除注释区里的同名行文）；不唯一则 None。"""
    spans = comment_spans(t)
    pos = [m.start() for m in re.finditer(u'</head>', t)
           if not any(a <= m.start() < b for a, b in spans)]
    return pos[0] if len(pos) == 1 else None


def snapshot():
    if os.path.isdir(BAK):
        shutil.rmtree(BAK)
    os.makedirs(BAK)
    for pg in ALL:
        src = os.path.join(PAGES, pg + u'.html')
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(BAK, pg + u'.html'))
    print(u'  快照 → mg-work/r109/ev/bak-border/（%d 页）' % len(ALL))


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

    problems = []
    per_page = []
    staged = []
    n_fresh = n_refresh = n_skip = 0

    for pg in ALL:
        p = os.path.join(PAGES, pg + u'.html')
        t = rd(p)

        if not RE_DS_BUNDLE.search(t):
            problems.append(u'%s：找不到 DS 编译包指纹' % pg)
            continue

        n_all = len(re.findall(u'</head>', t))
        hi = real_head(t)
        if hi is None:
            problems.append(u'%s：真正的 </head> 不唯一（字面 %d 次）'
                            % (pg, n_all))
            continue

        dk = t.find(DARK_MARK)
        if dk < 0:
            problems.append(u'%s：找不到 DS 暗色档指纹 %s' % (pg, DARK_MARK))
            continue
        if dk > hi:
            problems.append(u'%s：DS 暗色块在 </head> 之后 ⇒ 覆盖块会失效' % pg)
            continue

        before = len(norm(t))
        m = RE_BLOCK.search(t)
        # ★ 比较一律**先规范化换行**：本块用 \n 写入，但别的层重写页面时若以
        #   newline=None 落盘会把 \n 翻成 \r\n ⇒ 逐字节比会永远「有差异」，
        #   与本层反复互相刷新。按工程字符口径（\r\n→\n）判定即可根治。
        if m and norm(m.group(0)) == norm(BLOCK):
            n_skip += 1                                   # 已是目标态
            per_page.append((pg, 0))
            continue
        if m:
            t2 = t[:m.start()] + BLOCK + t[m.end():]      # 刷新旧版本
            n_refresh += 1
        else:
            t2 = t[:hi] + BLOCK + t[hi:]                  # 全新注入
            n_fresh += 1
        per_page.append((pg, len(norm(t2)) - before))
        staged.append((p, t2))

    if problems:
        print(u'✗ 前置校验失败，拒绝落盘：')
        for x in problems:
            print(u'   ' + x)
        return 2

    if staged and not args.check:
        snapshot()
        for p, t2 in staged:
            wr(p, t2)

    print(u'=== r109 第十拍 ① · 暗色档描边令牌各降一级（%s）==='
          % (u'检查' if args.check else u'落盘'))
    print()
    print(u'  新注入 %d 页 / 刷新 %d 页 / 已是目标态 %d 页' % (n_fresh, n_refresh, n_skip))
    print()
    print(u'  ── 取值对照（灰度索引 → 实际灰阶）──')
    print(u'     %-10s %-12s %-12s %-12s' % (u'令牌', u'浅（不变）', u'暗旧', u'暗新'))
    rows = [(u'border-1', u'gray-2 = 242', u'gray-2 = 43', u'gray-1 = 31'),
            (u'border-2', u'gray-3 = 229', u'gray-3 = 78', u'gray-2 = 43'),
            (u'border-3', u'gray-4 = 201', u'gray-4 = 107', u'gray-3 = 78')]
    for r in rows:
        print(u'     %-10s %-12s %-12s %-12s' % r)
    print()
    print(u'  ── 每页字符数变化（规范化 \\r\\n→\\n 后）──')
    for pg, d in per_page:
        print(u'     %-12s %+d' % (pg, d))
    print()
    print(u'  ── 刻意不动 ──')
    print(u'     %-34s %s' % (u'--color-border-4', u'全站 var() 引用 = 0（死令牌）'))
    print(u'     %-34s %s' % (u'--color-border（无后缀）', u'全站 var() 引用 = 0（死令牌）'))
    print(u'     %-34s %s' % (u'浅色档三个令牌', u'本块只在 dark 下生效 ⇒ 零变化'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
