# -*- coding: utf-8 -*-
"""r92 · 邵先生四条（本脚本负责 ① 与 ④，②③ 在设置页 ⇒ 落 mg-work/r88/apply88.py）

① 基础工作台顶栏 header 加装饰背景图（邵先生给的 assets/images/bg-img-1.png）
   素材实测 1580×134：平底 #F6F8FA，右侧是 **4px 方点 / 8px 点距**、密度自左向右递增的
   #DDE3EB 点阵（点阵从 x=1067 起，占图宽 32.5%）。按「居右、不重复」铺 ⇒
   不写 background-size（CSS 默认 auto = 原尺寸），右对齐、竖直居中。

② 设置页「返回」钮图标+文字深一级      → mg-work/r88/apply88.py 就地返工
③ 设置页 aside「r85-gt」左间距 12px     → mg-work/r88/apply88.py 就地返工

④ 基础工作台 main 对话框「默认权限」选中「完全访问」时，触发器上的文字与图标转危险色
   —— 触发器是 React 条件渲染的，色值分别来自「尾风任意类」与「内联 style」，两者都不吃
   后置 CSS（任意类是构建期产物、内联 style 优先级最高）⇒ 只能**就地改 React 源**：
     · 图标：className 尾巴的 `size-[14px] shrink-0 `+(…) 里加一档 s===`完全访问`
     · 文字：内联 style 的 color 三目里加同一档，取 var(--color-danger-6)
   （r77 需求 3 改 base.html 版权行序就是同一套路：直接 replace 压缩后的 React 字符串。）

幂等三要素（沿用 r77 的 replace_once / inject_tail）：
  ① 先判 NEW 标记命中即 skip；② 再判 count(OLD) 恰为 1，否则 sys.exit；③ 跑完复跑一遍确认
     全是 skip（`应用:0 项 / 跳过:N 项`）。

用法：python mg-work/r92/apply92.py [--dry]
"""
import argparse
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
PAGES = os.path.join(REPO, 'pages')

applied = 0
skipped = 0


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)


def replace_once(path, old, new, label, mark=None, dry=False):
    """幂等单处替换。mark 默认取 new（新串特征）。"""
    global applied, skipped
    s = rd(path)
    mm = new if mark is None else mark
    if mm in s:
        print('  skip  %-40s 已应用' % label)
        skipped += 1
        return False
    n = s.count(old)
    if n != 1:
        sys.exit('!! %s：锚点出现 %d 次（期望 1）\n   old=%r' % (label, n, old[:160]))
    s = s.replace(old, new, 1)
    if not dry:
        wr(path, s)
    print('  ok    %-40s 1 处' % label)
    applied += 1
    return True


def inject_tail(path, style_id, css, label, dry=False):
    """在文件**收尾的** </body> 前注入 <style id=...>，带标签级计数断言（同 r77）。

    ⚠ 不能直接断言 `count('</body>') == 1`：base.html 的 r76 CSS 注释里也出现过一次
      `</body>`（讲「落点必须在 </body> 前」那段说明），所以全文有 2 处。
      改为取 **rfind** 的最后一处，并要求它就在文件尾部（后面只剩 </html>）。
    """
    global applied, skipped
    s = rd(path)
    mark = '<style id="%s">' % style_id
    if mark in s:
        print('  skip  %-40s 已应用' % label)
        skipped += 1
        return False
    idx = s.rfind('</body>')
    if idx < 0:
        sys.exit('!! %s：找不到 </body>' % label)
    if len(s) - idx > 80:
        sys.exit('!! %s：最后一处 </body> 距文件尾 %d 字符（不像收尾标签）' % (label, len(s) - idx))
    n_hits = s.count('</body>')
    n_style = s.count('<style')
    n_end = s.count('</style>')
    block = '<style id="%s">\n%s\n</style>\n' % (style_id, css)
    s = s[:idx] + block + s[idx:]
    if s.count('<style') != n_style + 1:
        sys.exit('!! %s：<style> 计数 %d → %d（期望 +1）' % (label, n_style, s.count('<style')))
    if s.count('</style>') != n_end + 1:
        sys.exit('!! %s：</style> 计数 %d → %d（期望 +1）' % (label, n_end, s.count('</style>')))
    if not dry:
        wr(path, s)
    print('  ok    %-40s 1 处（<style> %d→%d；全文 </body> %d 处）'
          % (label, n_style, n_style + 1, n_hits))
    applied += 1
    return True


# ---------------------------------------------------------------- ① 顶栏背景图

# 基础工作台 5 页（按 DEV_PAGES 分组：dev/kanban/req-kanban/task-detail 属研发工作台）
BASE_PAGES = ['base', 'settings', 'avatar', 'skills', 'automation']

HDR_CSS = """  /* r92 ①：基础工作台顶栏装饰背景图 —— 素材 assets/images/bg-img-1.png（邵先生提供）。
     实测 1580×134：平底 #F6F8FA；右侧自 x=1067 起是 4px 方点、8px 点距、密度递增的
     #DDE3EB 点阵（占图宽 32.5%）。
     铺法按邵先生原话「图片居右、不重复」⇒ 只给 image / repeat / position 三件，
     **不写 background-size**（= CSS 默认 auto，即素材原尺寸）：
       · background-repeat: no-repeat     —— 不重复
       · background-position: right center —— 居右；竖直居中（素材 134px 高于顶栏 48px，
         竖直居中取中间那条 48px 横带）
     ⚠ 选择器刻意用 header[class*="h-12"]，**不能用裸 header 标签**：avatar.html 里还有
       av-main-head / av-hs-bar / td-right-bar / td-browse-bar 共 4 个 <header>，
       task-detail.html 有 td-bar / td-right-bar / td-browse-bar 共 3 个 —— 裸标签会误伤。
     ⚠ 只落基础工作台这 5 页：研发工作台 4 页（dev / kanban / req-kanban / task-detail）顶栏
       底色是 #E5EDF5，而本图平底是 #F6F8FA（不透明，会整块盖住）⇒ 铺上去会把那一档蓝调抹掉。
     ⚠ 素材平底 #F6F8FA 与顶栏自身底色 #F4F5F6 差 Δ=(2,3,4)：原尺寸铺满 1440 宽时图片
       覆盖整条顶栏（差值不可辨）；视口比 1580 更宽时图片右对齐，左端会出现一条
       Δ≈3 的接缝（近乎不可见）。 */
  header[class*="h-12"] {
    background-image: url("../assets/images/bg-img-1.png");
    background-repeat: no-repeat;
    background-position: right center;
  }"""

# ---------------------------------------------------------------- ④ 完全访问危险色

PERM_CSS = """  /* r92 ④：「默认权限」选中「完全访问」时，触发器上的图标转危险色。
     图标色原本来自**尾风任意类** [color:var(--color-text-1|2)]（构建期产物，新增类名不会
     进产物 CSS）⇒ 这里用本页自有的 .r92-perm-danger，由 base.html 的 React 源在
     s===`完全访问` 时条件挂载；文字那一半是内联 style，同处 React 源里直接取
     var(--color-danger-6)，不需本块。 */
  .r92-perm-danger { color: var(--color-danger-6); }"""

# React 源锚点（base.html，压缩后的单行 bundle；两处都实测唯一）
ANCHOR_ICON_OLD = ("`size-[14px] shrink-0 `+(l===`perm`?`[color:var(--color-text-1)]`"
                   ":`[color:var(--color-text-2)]`)")
ANCHOR_ICON_NEW = ("`size-[14px] shrink-0 `+(s===`完全访问`?`r92-perm-danger`"
                   ":(l===`perm`?`[color:var(--color-text-1)]`:`[color:var(--color-text-2)]`))")

ANCHOR_TEXT_OLD = ("style:{color:l===`perm`?`var(--color-text-1)`:`var(--color-text-2)`"
                   ",lineHeight:`19px`,flex:`none`,overflow:`visible`,textOverflow:`clip`}"
                   ",children:s}")
ANCHOR_TEXT_NEW = ("style:{color:s===`完全访问`?`var(--color-danger-6)`"
                   ":(l===`perm`?`var(--color-text-1)`:`var(--color-text-2)`)"
                   ",lineHeight:`19px`,flex:`none`,overflow:`visible`,textOverflow:`clip`}"
                   ",children:s}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()

    print('\n=== 需求 ①：基础工作台顶栏装饰背景图（%s）===' % '/'.join(BASE_PAGES))
    for pg in BASE_PAGES:
        inject_tail(os.path.join(PAGES, pg + '.html'), 'r92-hdr-css', HDR_CSS,
                    '%s.html 顶栏背景图' % pg, dry=a.dry)

    print('\n=== 需求 ④：base.html「完全访问」触发器转危险色 ===')
    BASE = os.path.join(PAGES, 'base.html')
    replace_once(BASE, ANCHOR_ICON_OLD, ANCHOR_ICON_NEW,
                 'base.html 权限图标 className', dry=a.dry)
    replace_once(BASE, ANCHOR_TEXT_OLD, ANCHOR_TEXT_NEW,
                 'base.html 权限文字内联色', dry=a.dry)
    inject_tail(BASE, 'r92-perm-css', PERM_CSS, 'base.html 权限危险色样式', dry=a.dry)

    print('\n应用: %d 项 | 跳过: %d 项' % (applied, skipped))
    if a.dry:
        print('（--dry：未写盘）')


if __name__ == '__main__':
    main()
