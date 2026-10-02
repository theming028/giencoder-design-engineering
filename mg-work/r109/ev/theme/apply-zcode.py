# -*- coding: utf-8 -*-
r"""r109 第十拍 ② · 全站 `ZCode` 文案统一替换为 `GienCoder`。

★ 起因（邵先生）：「查找全站是否有"ZCode "文案，若有统一替换为"GienCoder"。」

★ 普查结果（probe-zcode.py，raw/zcode.txt）：
   全站（排除 node_modules / .git / .workbuddy / mg-work）**仅 6 处**，
   全部集中在 `pages/conversation.html`，且全部在**注释**里 ——
   页面**没有任何用户可见**的 ZCode 文案。6 处分别是：
     · CSS 注释「19. 任务信息面板（第十三拍 ⑥）—— 复刻 ZCode 对话界面右上角…」
     · 同注释里的上游出处 `zai-org/ZCode`（Apache-2.0）
     · CSS 注释「（ZCode 产物里能直接读到 .grid-rows-[0fr] …）」
     · HTML 注释「★ 第十三拍 ⑥：任务信息面板 —— 复刻 ZCode 对话界面右上角的实时状态面板」
     · 同注释里的上游出处 `zai-org/ZCode`（Apache-2.0）
     · JS 注释「复刻 ZCode 右上角状态面板的**交互骨架**」

★ 裁决：邵先生选「全部替换为 GienCoder」（含 2 处 `zai-org/ZCode` 出处链接
   ⇒ 会变成 `zai-org/GienCoder`；若想保留上游出处请明示，我再单独摘出来）。

⚠ 与别的层相反：本层**故意改写注释区**（目标就在注释里），因此**不启用**注释护栏。

用法：
  python apply-zcode.py            # 落盘（先快照到 ev/bak-zcode/）
  python apply-zcode.py --check    # 只检查（不落盘）
  python apply-zcode.py --revert   # 从快照回滚
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
BAK = os.path.join(ROOT, 'mg-work', 'r109', 'ev', 'bak-zcode')

ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

OLD = u'ZCode'
NEW = u'GienCoder'
EXPECT_TOTAL = 6                 # 落盘前全站应有 6 处；落盘后应为 0 处

RE_DS_BUNDLE = re.compile(re.escape(u':root{--giencoderblue-1:245, 248, 255'))


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def norm(t):
    return t.replace(u'\r\n', u'\n')


def snapshot():
    if os.path.isdir(BAK):
        shutil.rmtree(BAK)
    os.makedirs(BAK)
    for pg in ALL:
        src = os.path.join(PAGES, pg + u'.html')
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(BAK, pg + u'.html'))
    print(u'  快照 → mg-work/r109/ev/bak-zcode/（%d 页）' % len(ALL))


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
    total = 0

    for pg in ALL:
        p = os.path.join(PAGES, pg + u'.html')
        t = rd(p)
        if not RE_DS_BUNDLE.search(t):
            problems.append(u'%s：找不到 DS 编译包指纹' % pg)
            continue
        n = t.count(OLD)
        if n == 0:
            per_page.append((pg, 0, 0))
            continue
        before = len(norm(t))
        t2 = t.replace(OLD, NEW)
        total += n
        per_page.append((pg, n, len(norm(t2)) - before))
        staged.append((p, t2))

    # 幂等判据：若一处都没有 ⇒ 目标态（已替换过）；若不是 0 也不是 6 ⇒ 异常
    if total not in (0, EXPECT_TOTAL):
        problems.append(u'总量不符：期望 %d（或已替换后的 0），实得 %d'
                        % (EXPECT_TOTAL, total))
    if problems:
        print(u'✗ 前置校验失败，拒绝落盘：')
        for x in problems:
            print(u'   ' + x)
        return 2

    if staged and not args.check:
        snapshot()
        for p, t2 in staged:
            wr(p, t2)

    print(u'=== r109 第十拍 ② · ZCode → GienCoder（%s）==='
          % (u'检查' if args.check else u'落盘'))
    print()
    print(u'  替换 %d 处（%s → %s）' % (total, OLD, NEW))
    print()
    print(u'  ── 每页明细 ──')
    for pg, n, d in per_page:
        print(u'     %-12s 替换 %-3d 处   字符数 %+d' % (pg, n, d))
    print()
    if total == 0:
        print(u'  （已是目标态：全站 0 处 ZCode）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
