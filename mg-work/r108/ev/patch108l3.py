# -*- coding: utf-8 -*-
"""r108 第十四拍（第三层补丁）—— 邵先生四条：

  ① 「zd-card」里 Git 工具的三行（更改 / 分支 / 提交或推送）点击都无响应 ⇒ 逐行接上交互：
        · 更改            → 复用右栏自己的「打开模块」链路：建 / 激活「审查」标签 + 自动展开侧栏
                            （上游 `GitStatusSection` 的 `onClick={() => onOpenGitReview?.(...)}`）
        · 分支            → 就地弹 DS Dropdown「分支」列表（当前项 ✓），选中即换行内显示
                            （上游 `GitBranchSwitcher`）
        · 提交或推送      → 就地弹 DS Dropdown 动作菜单（提交 / 提交并推送）
                            （上游 `GitActionMenu`；本页右栏 `.td-commit-menu` 是同一套落地的范例）
  ② 「计划」分区不需要 ⇒ 整段删掉（含它那条 `.zd-row` 与随之变成死代码的 icons 复用）
  ③ 「目标」分区按上游逐项校准：
        · 图标      未完成项用的是自绘「旗子」⇒ 换回上游 lucide `Goal` 原路径
                    （本轮另把 `file-diff` / `git-branch` / `list-checks` 一并换回 lucide 原路径）
        · 尺寸      `.zd-cv` 折叠箭头 12 → **14**（上游 `size-3.5`）；
                    图标按钮 28 → **24**（上游 `size-6`）、其内 svg 16 → **14**（上游 `size-3.5`）
        · 间距      迭代行内距 `6px 8px` → **`8px`**（上游 `px-2 py-2`）；圆角 4 → **8**（`rounded-lg`）
        · 行高      迭代标题 `20px` → **`16px`**（上游 `leading-4`）
        · 缺件      trailing 少了 elapsed 与控件之间的 **`·`**（上游 `{control ? <span>·</span> : null}`）
        · 文案      行标签「提交 / 推送」→ 上游 `git.actionMenu.trigger` = **「提交或推送」**
  ④ 折叠 / 展开要带**弹性微动效**：
        · 分区折展  照上游同一机制（Radix Collapsible = `grid-template-rows` 0fr ⇄ 1fr + 透明度），
                    缓动换成 DS 的 spring token（`--transition-timing-function-spring`）
        · 面板⇄胶囊 出场快速淡出 + 微缩，入场 spring 回弹

改序（只能下→上，硬规则 22）：
    1. `mg-work/r108/part108/_mods.html`   ①②③ 的 DOM
    2. `mg-work/r108/part108/panel.css`    ③ 的就地改 + ①④ 的新规则 + 8 处选择器组扩员
    3. `mg-work/r108/part108/panel.js`     ①④ 的控制器（就地替换末尾那段）
    4. `python mg-work/r108/ev/splice108.py`   → `part108/browse.html`
    5. `python mg-work/r108/apply108.py`       → 落 `pages/conversation.html`

★ 为什么另起一层（l3）而不是就地改 l1 / l2：r108 未提交 ⇒ **不另起代数**，但在代内分层。
  l1 / l2 都已跑过且各自有独立 `mark` ⇒ 三层互不干扰、复跑各自「应用 0 / 跳过 N」。
  ⚠ l3 改的是 l2 写进 `_mods.html` / `panel.css` / `panel.js` 的那些块 ⇒ **不能**把 l3 的内容
    再搬回 l2 的常量：那样「l2 重跑」会先铺新内容、l3 的锚点随即失配而 `sys.exit`。
    三层的**唯一事实**是 part108 下那三个产物文件（`acceptance.md` 记最终态）。

幂等判据：每处都带 `mark`（**只有改完之后才存在的串**）；删除类改动没有 mark ⇒
         判据改用「**模式不再命中**」（与 l2 的 `drop_re` 同口径）。
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
PJS = os.path.join(P108, 'panel.js')

APPLIED = []
SKIPPED = []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark):
    t, nl = rd(p)
    if mark and mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）\n   old=%r' % (label, n, old[:200]))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


def edit_all(p, old, new, label, mark, expect):
    t, nl = rd(p)
    if mark and mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != expect:
        sys.exit('!! %s：锚点命中 %d 次（应 %d 次）' % (label, n, expect))
    wr(p, t.replace(old, new), nl)
    APPLIED.append(label)
    print('   应用  %s（%d 处，%d → %d 字符）' % (label, n, len(t), len(t) + n * (len(new) - len(old))))


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
# 图标：上游用 lucide-react，这里取 **lucide 原路径**逐字落成内联 SVG。
#   ⚠ 上一版是「按名字手绘近似」的（`goal` 画成了旗子、`file-diff` 缺一条减号、
#     `git-branch` 多了一个圆），邵先生第 ③ 条点的就是它。
#   来源：lucide-static v1.49.0（ISC），24 网格 / stroke-width 2 / 圆头圆角。
# ================================================================================
ICO_DIFF = ('<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588'
            'A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M9 10h6"/><path d="M12 13V7"/>'
            '<path d="M9 17h6"/>')
ICO_BRANCH = ('<path d="M15 6a9 9 0 0 0-9 9V3"/><circle cx="18" cy="6" r="3"/>'
              '<circle cx="6" cy="18" r="3"/>')
ICO_COMMIT = ('<circle cx="12" cy="12" r="3"/><line x1="3" x2="9" y1="12" y2="12"/>'
              '<line x1="15" x2="21" y1="12" y2="12"/>')
ICO_GOAL = ('<path d="M12 13V2l8 4-8 4"/><path d="M20.561 10.222a9 9 0 1 1-12.55-5.29"/>'
            '<path d="M8.002 9.997a5 5 0 1 0 8.9 2.02"/>')
ICO_CHECKS = ('<path d="M13 5h8"/><path d="M13 12h8"/><path d="M13 19h8"/>'
              '<path d="m3 17 2 2 4-4"/><path d="m3 7 2 2 4-4"/>')
ICO_PAUSE = ('<rect x="14" y="3" width="5" height="18" rx="1"/>'
             '<rect x="5" y="3" width="5" height="18" rx="1"/>')
ICO_MIN2 = ('<path d="m14 10 7-7"/><path d="M20 10h-6V4"/><path d="m3 21 7-7"/>'
            '<path d="M4 14h6v6"/>')
ICO_PLUS = '<path d="M5 12h14"/><path d="M12 5v14"/>'
ICO_PUSH = ('<path d="m18 9-6-6-6 6"/><path d="M12 3v14"/><path d="M5 21h14"/>')

# 改前的自绘近似（逐字取自 part108/_mods.html）
OLD_DIFF = ('<path d="M4 2h11.5l3.5 5.5v13a1.5 1.5 0 0 1-1.5 1.5H4a1.5 1.5 0 0 1-1.5-1.5v-17'
            'A1.5 1.5 0 0 1 4 2Z"/><path d="M14 10v6"/><path d="M11 13h6"/>')
OLD_BRANCH = ('<circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/>'
              '<circle cx="18" cy="6" r="2.5"/><path d="M6 8.5v7"/>'
              '<path d="M18 8.5a6 6 0 0 1-6 6H9"/>')
OLD_COMMIT = '<circle cx="12" cy="12" r="3"/><path d="M3 12h6"/><path d="M15 12h6"/>'
OLD_GOAL = '<path d="M5 21V3"/><path d="M5 4h12l-2.5 3.5L17 11H5"/>'
OLD_CHECKS = ('<path d="m3 6 1.5 1.5L7 5"/><path d="m3 12 1.5 1.5L7 11"/>'
              '<path d="m3 18 1.5 1.5L7 17"/><path d="M11 7h9"/><path d="M11 12h9"/>'
              '<path d="M11 17h9"/>')


def zsvg(inner, size=16):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="%d" height="%d" '
            'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, inner))


# ================================================================================
# ① 两枚下拉 + 轻提示（插在 `.zd-card` 之外、`.zd-host` 之内）
# ★ 为什么必须挂在卡片外：`.zd-card` 带 `overflow: hidden`（圆角 + 内部滚动），
#   DS 弹层放进去会被整块裁掉 —— 右栏那边改用 `.td-browse` 当包含块是同一个理由。
# ★ 位置不用 CSS 钉死：`.zd-host` 是 `position: absolute` ⇒ 它天然是这两枚菜单的包含块，
#   坐标由 panel.js 在**打开瞬间**按触发行现场摆（与右栏 `placeRv()` 同一套做法）。
# ================================================================================
MENUS_HTML = '''
      <!-- ★ 第十四拍 ①：Git 工具的两枚下拉。复用 DS 的 Dropdown 族（`.giencoder-dropdown-popup`
           + `.zd-menu`，第 1 节那几组选择器已把 `.zd-menu` 收作第四个成员）。 -->
      <div class="zd-menu giencoder-dropdown-popup zd-menu-branch" role="menu" aria-label="分支" hidden>
        <div class="td-mm-cap giencoder-menu-group-title">分支</div>
        <button class="td-mm-item giencoder-dropdown-item is-checked" type="button" role="menuitemradio" aria-checked="true" data-zd-br="main"><span class="td-mm-ico">''' + zsvg(ICO_BRANCH, 14) + '''</span><span class="td-mm-name">main</span><span class="td-mm-mark">✓</span></button>
        <button class="td-mm-item giencoder-dropdown-item" type="button" role="menuitemradio" aria-checked="false" data-zd-br="feature/right-panel"><span class="td-mm-ico">''' + zsvg(ICO_BRANCH, 14) + '''</span><span class="td-mm-name">feature/right-panel</span><span class="td-mm-mark">✓</span></button>
        <button class="td-mm-item giencoder-dropdown-item" type="button" role="menuitemradio" aria-checked="false" data-zd-br="fix/zd-card"><span class="td-mm-ico">''' + zsvg(ICO_BRANCH, 14) + '''</span><span class="td-mm-name">fix/zd-card</span><span class="td-mm-mark">✓</span></button>
        <button class="td-mm-item giencoder-dropdown-item" type="button" role="menuitemradio" aria-checked="false" data-zd-br="release/0.9"><span class="td-mm-ico">''' + zsvg(ICO_BRANCH, 14) + '''</span><span class="td-mm-name">release/0.9</span><span class="td-mm-mark">✓</span></button>
        <span class="td-mm-line giencoder-dropdown-divider"></span>
        <button class="td-mm-item giencoder-dropdown-item" type="button" role="menuitem" data-zd-br-new="1"><span class="td-mm-ico">''' + zsvg(ICO_PLUS, 14) + '''</span><span class="td-mm-name">创建并检出新分支...</span></button>
      </div>
      <div class="zd-menu giencoder-dropdown-popup zd-menu-commit" role="menu" aria-label="提交或推送" hidden>
        <button class="td-mm-item giencoder-dropdown-item" type="button" role="menuitem" data-zd-commit="commit"><span class="td-mm-ico">''' + zsvg(ICO_COMMIT, 14) + '''</span><span class="td-mm-name">提交</span><span class="td-mm-key">⌥⌘C</span></button>
        <button class="td-mm-item giencoder-dropdown-item" type="button" role="menuitem" data-zd-commit="push"><span class="td-mm-ico">''' + zsvg(ICO_PUSH, 14) + '''</span><span class="td-mm-name">提交并推送</span><span class="td-mm-key">⌥⌘P</span></button>
      </div>
      <!-- ★ 第十四拍 ①：动作类反馈的轻提示。用右栏那条 `.td-toast` 会在侧栏收起时不可见
           （它挂在 `.td-browse` 里）⇒ 面板自带一份，样式同款（见 panel.css 19.4）。 -->
      <div class="zd-toast" hidden></div>
'''

# ================================================================================
# ④ 选择器组扩员：把 `.zd-menu` 收进第 1 节那几组「DS Dropdown 适配层」
#   ★ 这四组本来就是「一套规则 + 多成员」的写法（`.td-mod-menu` / `.td-rv-menu` /
#     `.td-ctxmenu`）⇒ 加成员是该体位的扩展点，不是重写。
#   ⚠ 加完**必须复跑**右栏那四枚下拉的回归：本组只增成员、不改任何声明的值。
# ================================================================================
# ⚠ 每处必须自带**互不相同**的 mark：若八处共用同一个 mark（比如都取
#   `.zd-menu.giencoder-dropdown-popup {`），第一处一落地，后面七处就全被判「已应用」而跳过
#   —— 静默漏改（本轮初稿真踩过）。mark 一律取「只有这一处改完才出现」的那行选择器。
GROUP_EDITS = [
    # (旧, 新, 说明, mark)
    ('.td-mod-menu.giencoder-dropdown-popup,\n'
     '.td-rv-menu.giencoder-dropdown-popup,\n'
     '.td-ctxmenu.giencoder-dropdown-popup {\n',
     '.td-mod-menu.giencoder-dropdown-popup,\n'
     '.td-rv-menu.giencoder-dropdown-popup,\n'
     '.td-ctxmenu.giencoder-dropdown-popup,\n'
     '.zd-menu.giencoder-dropdown-popup {\n',
     'G1 骨架组 + `.zd-menu`',
     '.zd-menu.giencoder-dropdown-popup {\n'),
    ('.td-mod-menu.giencoder-dropdown-popup.giencoder-popup-open,\n'
     '.td-rv-menu.giencoder-dropdown-popup.giencoder-popup-open,\n'
     '.td-ctxmenu.giencoder-dropdown-popup.giencoder-popup-open {\n',
     '.td-mod-menu.giencoder-dropdown-popup.giencoder-popup-open,\n'
     '.td-rv-menu.giencoder-dropdown-popup.giencoder-popup-open,\n'
     '.td-ctxmenu.giencoder-dropdown-popup.giencoder-popup-open,\n'
     '.zd-menu.giencoder-dropdown-popup.giencoder-popup-open {\n',
     'G2 开态组 + `.zd-menu`',
     '.zd-menu.giencoder-dropdown-popup.giencoder-popup-open {\n'),
    ('.td-mod-menu .giencoder-dropdown-item,\n'
     '.td-rv-menu .giencoder-dropdown-item,\n'
     '.td-ctxmenu .giencoder-dropdown-item {\n',
     '.td-mod-menu .giencoder-dropdown-item,\n'
     '.td-rv-menu .giencoder-dropdown-item,\n'
     '.td-ctxmenu .giencoder-dropdown-item,\n'
     '.zd-menu .giencoder-dropdown-item {\n',
     'G3 条目基态组 + `.zd-menu`',
     '.zd-menu .giencoder-dropdown-item {\n'),
    ('.td-mod-menu .giencoder-dropdown-item:hover,\n'
     '.td-rv-menu .giencoder-dropdown-item:hover,\n'
     '.td-ctxmenu .giencoder-dropdown-item:hover { background: var(--color-fill-2); }\n',
     '.td-mod-menu .giencoder-dropdown-item:hover,\n'
     '.td-rv-menu .giencoder-dropdown-item:hover,\n'
     '.td-ctxmenu .giencoder-dropdown-item:hover,\n'
     '.zd-menu .giencoder-dropdown-item:hover { background: var(--color-fill-2); }\n',
     'G4 条目 hover 组 + `.zd-menu`',
     '.zd-menu .giencoder-dropdown-item:hover { background: var(--color-fill-2); }\n'),
    ('.td-mod-menu .giencoder-dropdown-item.is-checked,\n'
     '.td-rv-menu .giencoder-dropdown-item.is-checked { color: var(--color-primary-6); }\n',
     '.td-mod-menu .giencoder-dropdown-item.is-checked,\n'
     '.td-rv-menu .giencoder-dropdown-item.is-checked,\n'
     '.zd-menu .giencoder-dropdown-item.is-checked { color: var(--color-primary-6); }\n',
     'G5 选中文字色组 + `.zd-menu`',
     '.zd-menu .giencoder-dropdown-item.is-checked { color: var(--color-primary-6); }\n'),
    ('.td-mod-menu .giencoder-dropdown-item.is-checked .td-mm-mark,\n'
     '.td-rv-menu .giencoder-dropdown-item.is-checked .td-mm-mark { opacity: 1; }\n',
     '.td-mod-menu .giencoder-dropdown-item.is-checked .td-mm-mark,\n'
     '.td-rv-menu .giencoder-dropdown-item.is-checked .td-mm-mark,\n'
     '.zd-menu .giencoder-dropdown-item.is-checked .td-mm-mark { opacity: 1; }\n',
     'G6 选中勾组 + `.zd-menu`',
     '.zd-menu .giencoder-dropdown-item.is-checked .td-mm-mark { opacity: 1; }\n'),
    ('.td-mod-menu .giencoder-dropdown-divider,\n'
     '.td-rv-menu .giencoder-dropdown-divider,\n'
     '.td-ctxmenu .giencoder-dropdown-divider {\n',
     '.td-mod-menu .giencoder-dropdown-divider,\n'
     '.td-rv-menu .giencoder-dropdown-divider,\n'
     '.td-ctxmenu .giencoder-dropdown-divider,\n'
     '.zd-menu .giencoder-dropdown-divider {\n',
     'G7 分隔线组 + `.zd-menu`',
     '.zd-menu .giencoder-dropdown-divider {\n'),
    ('.td-mod-menu.giencoder-dropdown-popup[hidden],\n'
     '.td-rv-menu.giencoder-dropdown-popup[hidden],\n'
     '.td-ctxmenu.giencoder-dropdown-popup[hidden] { display: none; }\n',
     '.td-mod-menu.giencoder-dropdown-popup[hidden],\n'
     '.td-rv-menu.giencoder-dropdown-popup[hidden],\n'
     '.td-ctxmenu.giencoder-dropdown-popup[hidden],\n'
     '.zd-menu.giencoder-dropdown-popup[hidden] { display: none; }\n',
     'G8 `[hidden]` 兜底组 + `.zd-menu`',
     '.zd-menu.giencoder-dropdown-popup[hidden] { display: none; }\n'),
]

# ================================================================================
# ③④ 第 19 节就地改 + 新规则（追加在 `/* r108-l2 */` 之前）
# ================================================================================
CSS_TAIL = '''/* ---------------------------------------------------------------- 19.1 第十四拍
   ① Git 工具三行接上交互（下拉本体见 19.2）
   ③ 「目标」按上游逐项校准（图标在 DOM 侧；这里管尺寸 / 间距 / 圆角 / 行高）
   ④ 折展与面板⇄胶囊的弹性微动效
   ---------------------------------------------------------------------------- */
/* ③ 图标按钮：上游面板里的控件是 `size-6`（24px）、内部图标 `size-3.5`（14px）。
   ❌ 不能直接改 `.td-browse-ico`：那是右栏工具条的既定口径（28 / 16），改了会连带右栏。
   ⇒ 面板里单挂一个体量类。 */
.zd-ico { width: 24px; height: 24px; }
.zd-ico svg { width: 14px; height: 14px; }
.zd-ico[hidden] { display: none; }
/* ③ 「目标」trailing 的 `·`：上游只在**有控件**时才渲染（`{control ? <span>·</span> : null}`），
   分隔 elapsed 与暂停钮；颜色取 trailing 容器那一档（foreground-subtlest）。 */
.zd-sep { flex: none; color: var(--color-text-3); }

/* ② 「计划」分区已删（DOM 侧） ⇒ 上一版那条「计划」行用的 `list-checks` 图标继续由
   「进程」分区与胶囊复用，规则无残留（图标是内联 SVG，没有配对的选择器）。 */

/* ④ 分区折展：上游 `CollapsibleContent` 的机制就是 `grid-template-rows` 0fr ⇄ 1fr
   （ZCode 产物里能直接读到 `.grid-rows-[0fr]` / `.grid-rows-[1fr]` /
   `.transition-[grid-template-rows]` 三条工具类），外层再叠一层透明度淡入淡出。
   本版照同一机制用**纯 CSS 过渡**表达，缓动换成 DS 的 spring token —— 这就是「弹性」那一下。
   ⚠ 用 `grid-template-rows` 而不是 `height`：后者对 `auto` 不可动画，前者可以且不需要 JS 量高。
   ⚠ 网格项必须 `min-height: 0` + 容器 `overflow: hidden`，否则 `0fr` 收不下去。 */
.zd-sec-b {
  display: grid; grid-template-rows: 1fr;
  /* ⚠ 时长必须 ≤ 300ms：`verify-design.py` 的 CRAFT-ANIM 上限就是 300ms，
     超了会让门禁输出比 r107 基线多出条目（本层初稿用 340ms，当场被逮）。
     「弹性」来自缓动曲线的过冲（spring 的 y1 = 1.56），不是靠拉长时长。 */
  transition: grid-template-rows 300ms var(--transition-timing-function-spring);
}
.zd-sec-b > * {
  min-height: 0; overflow: hidden;
  transition: opacity 200ms ease,
              translate 300ms var(--transition-timing-function-spring),
              scale 300ms var(--transition-timing-function-spring);
}
.zd-sec.is-closed .zd-sec-b { grid-template-rows: 0fr; }
.zd-sec.is-closed .zd-sec-b > * { opacity: 0; translate: 0 -4px; scale: 0.98; }

/* ④ 面板 ⇄ 胶囊：出场（快速淡出 + 微缩）/ 入场（spring 回弹）。
   两边都常驻文档流、只有 `hidden` 那一刻才摘 ⇒ 过渡看得见（摘除时机由 panel.js 掐）。 */
.zd-card, .zd-mini {
  transition: opacity 170ms ease,
              scale 300ms var(--transition-timing-function-spring),
              translate 300ms var(--transition-timing-function-spring);
}
.zd-card.is-zd-out, .zd-mini.is-zd-out {
  opacity: 0; scale: 0.94; translate: 0 -6px; pointer-events: none;
}
@keyframes zd-panel-in {
  from { opacity: 0; scale: 0.94; translate: 0 -6px; }
  to   { opacity: 1; scale: 1;    translate: 0 0; }
}
.zd-card.is-zd-in, .zd-mini.is-zd-in {
  animation: zd-panel-in 300ms var(--transition-timing-function-spring) both;
}

/* ---------------------------------------------------------------- 19.2 ① 两枚下拉 */
/* 包含块 = `.zd-host`（它是 `position: absolute`）。`left/top` 由 panel.js 现场写行内值：
   垂直 = 触发行下缘 + 6px；水平 = 右对齐卡片右缘（卡片就是 host 的内容宽，320）。
   ⚠ 本页 `.td-rv-menu.giencoder-dropdown-popup` 那条 `top: 83px` 不命中这里（类名不同）——
     但**将来若把它写成 `.giencoder-dropdown-popup` 通配就会**，所以这里显式给上 top/left。 */
.zd-menu { position: absolute; top: 0; left: 0; z-index: 40; pointer-events: auto; }
/* 面板在 `<main>` 里，不在右栏 ⇒ 复用不到 `.td-browse` 的坐标；菜单比 host 窄时贴右缘，
   比 host 宽时由 JS 夹进去（见 placeZdMenu）。宽度上限取卡片宽（320，上游弹层 `w-80`）。 */
.zd-menu-branch, .zd-menu-commit { max-width: 320px; }

/* ---------------------------------------------------------------- 19.3 ① 轻提示 */
.zd-toast {
  position: absolute; right: 0; top: 100%; margin-top: 8px;
  z-index: 45; max-width: 320px; box-sizing: border-box;
  padding: 6px 12px; border-radius: 8px;
  background: var(--color-bg-popup);
  border: 1px solid var(--color-border-2);
  box-shadow: var(--shadow2-down);
  font-size: var(--font-size-body-1); color: var(--color-text-1);
  pointer-events: none;
}
.zd-toast[hidden] { display: none; }
/* r108-l3 */
'''

JS_OLD = '''  /* ②/③ 面板 ⇄ 胶囊 互斥切换 */
  function toMini() {
    if (!card || !mini) return;
    card.setAttribute('hidden', '');
    mini.removeAttribute('hidden');
  }
  function toCard() {
    if (!card || !mini) return;
    mini.setAttribute('hidden', '');
    card.removeAttribute('hidden');
  }
  var minBtn = card ? card.querySelector('[data-zd-min]') : null;
  if (minBtn) minBtn.addEventListener('click', toMini);
  if (mini) mini.addEventListener('click', toCard);
'''

JS_NEW = '''  /* ==================== 第十四拍 ① Git 工具三行：接上交互 ====================
     上游（`packages/ui/src/v4/ConversationStatusPanel.tsx` 的 `GitStatusSection`）：
       · `changes` 行  → `onOpenGitReview()`                       = 打开 git 审查
       · `branch` 行   → `<GitBranchSwitcher>`                      = 分支下拉
       · `commitPush` 行 → `<GitActionMenu triggerLayout="status-row">` = 提交 / 推送
     本页落地（全部是静态交互）：
       · 更改           复用右栏自己的「打开模块」链路（建 / 激活「审查」标签 + 自动展开侧栏）
       · 分支 / 提交     就地弹 DS Dropdown（`_mods.html` 里那两枚 `.zd-menu`）
     ⚠ 菜单必须在**触发行的 click 里 `stopPropagation`**：本 IIFE 末尾那条 document click
       负责「点空白一律收起」，不挡住的话菜单会在同一次点击里被自己关掉。 */
  var gitReview = card ? card.querySelector('[data-zd-git="review"]') : null;
  var gitBranch = card ? card.querySelector('[data-zd-git="branch"]') : null;
  var gitCommit = card ? card.querySelector('[data-zd-git="commit"]') : null;
  var branchVal = card ? card.querySelector('[data-zd-branch]') : null;

  /* 轻提示（动作类反馈；1.4s 自动收，与右栏 `.td-toast` 同口径） */
  var ztoast = host.querySelector('.zd-toast');
  var ztimer = 0;
  function zsay(text) {
    if (!ztoast) return;
    ztoast.textContent = text;
    ztoast.removeAttribute('hidden');
    if (ztimer) clearTimeout(ztimer);
    ztimer = setTimeout(function () { ztoast.setAttribute('hidden', ''); }, 1400);
  }

  var POP_OPEN = 'giencoder-popup-open';
  var menuBranch = host.querySelector('.zd-menu-branch');
  var menuCommit = host.querySelector('.zd-menu-commit');
  var zdMenus = [];
  if (menuBranch) zdMenus.push(menuBranch);
  if (menuCommit) zdMenus.push(menuCommit);

  function zdMenuShow(m) {
    for (var i = 0; i < zdMenus.length; i++) if (!zdMenus[i].hasAttribute('hidden')) return true;
    return false;
  }
  function closeZdMenus(except) {
    for (var i = 0; i < zdMenus.length; i++) {
      var m = zdMenus[i];
      if (m === except) continue;
      m.setAttribute('hidden', '');
      m.classList.remove(POP_OPEN);
    }
    if (gitBranch) gitBranch.setAttribute('aria-expanded', menuBranch === except ? 'true' : 'false');
    if (gitCommit) gitCommit.setAttribute('aria-expanded', menuCommit === except ? 'true' : 'false');
  }
  /* 摆放：垂直 = 触发行下缘 + 6px（与右栏 `placeRv()` 同口径）；水平 = 右对齐卡片右缘。
     ⚠ 必须在 `[hidden]` 摘掉**之后**调用（否则量到 0×0）；
       量宽高用 `offsetWidth` —— 不受入场 `scale(0.96)` 影响（`getBoundingClientRect()` 会乘进去）。 */
  var ZD_GAP = 6;
  function placeZdMenu(menu, trigger) {
    var hr = host.getBoundingClientRect();
    var tr = trigger.getBoundingClientRect();
    var top = tr.bottom - hr.top + ZD_GAP;
    var left = host.clientWidth - menu.offsetWidth;      /* 右对齐卡片右缘 */
    if (left < 0) left = 0;                              /* 菜单比卡片宽 ⇒ 贴左缘 */
    menu.style.top = Math.round(top) + 'px';
    menu.style.left = Math.round(left) + 'px';
    menu.style.right = 'auto';
  }
  function toggleZdMenu(menu, trigger) {
    if (!menu) return;
    var willOpen = menu.hasAttribute('hidden');
    closeZdMenus(willOpen ? menu : null);
    if (willOpen) {
      menu.removeAttribute('hidden');
      menu.classList.add(POP_OPEN);
      placeZdMenu(menu, trigger);
    } else {
      menu.setAttribute('hidden', '');
      menu.classList.remove(POP_OPEN);
    }
  }

  /* · 更改 → 复用右栏那条链路：`[data-td-open-mod="review"]` 的 click 会建 / 激活标签，
     并且内部 `ensureOpen()` 会在侧栏收起时点一下「打开侧栏」。**不自己写一套 openTab**，
     免得与右栏的标签状态机各说各话。兜底：连模块项都没了就只开侧栏。 */
  if (gitReview) gitReview.addEventListener('click', function (e) {
    e.stopPropagation();
    closeZdMenus(null);
    var op = document.querySelector('[data-td-open-mod="review"]');
    if (op) { op.click(); return; }
    var toggle = document.querySelector('.r93-baract[data-r93-browse]');
    if (toggle) toggle.click();
  });
  if (gitBranch) gitBranch.addEventListener('click', function (e) {
    e.stopPropagation();
    toggleZdMenu(menuBranch, gitBranch);
  });
  if (gitCommit) gitCommit.addEventListener('click', function (e) {
    e.stopPropagation();
    toggleZdMenu(menuCommit, gitCommit);
  });

  /* 分支项：选中即换行内显示（radio 型 ⇒ 勾 + 主色文字，见 panel.css 第 1 节） */
  var brItems = host.querySelectorAll('[data-zd-br]');
  for (var bi = 0; bi < brItems.length; bi++) {
    (function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        for (var k = 0; k < brItems.length; k++) {
          var on = brItems[k] === b;
          brItems[k].classList.toggle('is-checked', on);
          brItems[k].setAttribute('aria-checked', on ? 'true' : 'false');
        }
        var name = b.getAttribute('data-zd-br');
        if (branchVal) branchVal.textContent = name;
        closeZdMenus(null);
        zsay('已切换到 ' + name + '（视觉演示）');
      });
    })(brItems[bi]);
  }
  var brNew = host.querySelector('[data-zd-br-new]');
  if (brNew) brNew.addEventListener('click', function (e) {
    e.stopPropagation();
    closeZdMenus(null);
    zsay('已打开创建分支（视觉演示）');
  });
  /* 提交菜单：文案对齐本页既有 `.td-commit-menu`（右栏那份是同一个上游组件的落地） */
  var cmItems = host.querySelectorAll('[data-zd-commit]');
  for (var ci = 0; ci < cmItems.length; ci++) {
    (function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        var push = b.getAttribute('data-zd-commit') === 'push';
        closeZdMenus(null);
        zsay(push ? '已提交并推送到 origin/main（视觉演示）' : '已提交到本地（视觉演示）');
      });
    })(cmItems[ci]);
  }
  /* 点空白一律收起（菜单内部不关） */
  document.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('.zd-menu')) return;
    closeZdMenus(null);
  });
  /* ★ Esc：挂 `window` **捕获段**（比任何 `document` 捕获段都早），且**只有真的消费掉了
     这一下才 `stopPropagation`** —— 否则「关菜单」会静默漏给下游，把整条侧栏 / 面板一起关掉
     （右栏 r107 那条 Esc 处理器踩过同型的坑，见 panel.js 第 1272 行那段注释）。 */
  window.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!zdMenuShow()) return;
    e.preventDefault();
    e.stopPropagation();
    closeZdMenus(null);
  }, true);

  /* ==================== 第十四拍 ④ 面板 ⇄ 胶囊（带弹性微动效） ====================
     上一版是「点一下立刻 hidden ⇒ 硬切」。这一版：先给离场件挂 `.is-zd-out`
     （CSS 里是 170ms 淡出 + 微缩），到点再 `hidden` 并给入场件挂 `.is-zd-in`
     （CSS 里是 spring 回弹的关键帧）。计时器都存起来 ⇒ 连点不会留下半截状态。 */
  var zdOutTimer = 0, zdInTimer = 0;
  function zdSwap(from, to) {
    if (!from || !to) return;
    if (zdOutTimer) clearTimeout(zdOutTimer);
    if (zdInTimer) clearTimeout(zdInTimer);
    from.classList.add('is-zd-out');
    zdOutTimer = setTimeout(function () {
      from.setAttribute('hidden', '');
      from.classList.remove('is-zd-out');
      to.removeAttribute('hidden');
      to.classList.add('is-zd-in');
      zdInTimer = setTimeout(function () { to.classList.remove('is-zd-in'); }, 380);
    }, 180);
  }
  function toMini() { closeZdMenus(null); zdSwap(card, mini); }
  function toCard() { zdSwap(mini, card); }
  var minBtn = card ? card.querySelector('[data-zd-min]') : null;
  if (minBtn) minBtn.addEventListener('click', toMini);
  if (mini) mini.addEventListener('click', toCard);
'''


def main():
    print('=== 1/3  _mods.html ===')
    # ② 删「计划」分区（连它前后那圈空行一起去掉，避免留下三连换行）。
    #    ⚠ 判据是「模式不再命中」——删除类改动没有「改完才出现」的 mark。
    #    ⚠⚠ 必须 `(?s)`：`.*?` 默认不跨行，而这个 section 有 9 行 ⇒ 不加就**永远 0 命中**、
    #        被 `drop_re` 判成「已应用」而静默跳过（本轮初稿真踩过）。
    drop_re(MODS, r'(?s)\n\n          <section class="zd-sec" data-zd-sec="plan">.*?</section>',
            '② 删「计划」分区', 1)
    _t, _nl = rd(MODS)
    if 'data-zd-sec="plan"' in _t:
        sys.exit('!! ② 「计划」分区还在（正则应已删净）——不写入')
    if _t.count('data-zd-sec=') != 3:
        sys.exit('!! ② 分区数应为 3（git / goal / todo），实测 %d' % _t.count('data-zd-sec='))
    # ③ `.zd-cv` 折叠箭头 12 → 14（上游 `size-3.5`）。锚点必须带 `class="zd-cv"`：
    #    `width="12" height="12"` 在全文件里到处都是（所有 12px 小图标）。
    edit_all(MODS,
             '<svg class="zd-cv" xmlns="http://www.w3.org/2000/svg" '
             'viewBox="0 0 24 24" width="12" height="12"',
             '<svg class="zd-cv" xmlns="http://www.w3.org/2000/svg" '
             'viewBox="0 0 24 24" width="14" height="14"',
             '③ `.zd-cv` 12 → 14px（3 个分区头）',
             'viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
             'aria-hidden="true"><path d="m6 9 6 6 6-6"/>',
             expect=3)
    # ① 三行 Git 行：整行重写（新图标 + `data-zd-git` + 上游文案）。
    edit_all(MODS,
             '<button class="zd-row" type="button"><span class="zd-row-i">' + zsvg(OLD_DIFF)
             + '</span><span class="zd-row-n">更改</span><span class="zd-row-v">'
               '<span class="zd-add">+566</span> <span class="zd-del">\u2212228</span></span></button>',
             '<button class="zd-row" type="button" data-zd-git="review"><span class="zd-row-i">'
             + zsvg(ICO_DIFF) + '</span><span class="zd-row-n">更改</span><span class="zd-row-v">'
               '<span class="zd-add">+566</span> <span class="zd-del">\u2212228</span></span></button>',
             '① 行「更改」：接交互 + 换 lucide file-diff',
             'data-zd-git="review"', expect=1)
    edit_all(MODS,
             '<button class="zd-row" type="button"><span class="zd-row-i">' + zsvg(OLD_BRANCH)
             + '</span><span class="zd-row-n">分支</span><span class="zd-row-v">main</span></button>',
             '<button class="zd-row" type="button" data-zd-git="branch" aria-haspopup="menu" '
             'aria-expanded="false"><span class="zd-row-i">' + zsvg(ICO_BRANCH)
             + '</span><span class="zd-row-n">分支</span>'
               '<span class="zd-row-v" data-zd-branch="1">main</span></button>',
             '① 行「分支」：接交互 + 换 lucide git-branch',
             'data-zd-branch="1"', expect=1)
    edit_all(MODS,
             '<button class="zd-row" type="button"><span class="zd-row-i">' + zsvg(OLD_COMMIT)
             + '</span><span class="zd-row-n">提交 / 推送</span></button>',
             '<button class="zd-row" type="button" data-zd-git="commit" aria-haspopup="menu" '
             'aria-expanded="false"><span class="zd-row-i">' + zsvg(ICO_COMMIT)
             + '</span><span class="zd-row-n">提交或推送</span></button>',
             '① 行「提交或推送」（文案取上游 git.actionMenu.trigger）+ 接交互',
             'data-zd-git="commit"', expect=1)
    # ③ 「目标」未完成项的图标：自绘旗子 → 上游 lucide `goal`（邵先生点名的那个）
    edit_all(MODS, '<i class="zd-it-i">' + zsvg(OLD_GOAL) + '</i>',
             '<i class="zd-it-i">' + zsvg(ICO_GOAL) + '</i>',
             '③ 「目标」未完成项图标 → lucide goal',
             'M20.561 10.222a9 9 0 1 1-12.55-5.29', expect=1)
    # ③ 「进程」分区与胶囊的 list-checks。⚠ 删掉「计划」分区后只剩 **1** 处
    #    （上一版「计划」行与胶囊各一枚 = 2）⇒ 这里期望 1；若 drop_re 没删成，这一步会
    #    「命中 2 次」而 `sys.exit`，正好当成「② 没生效」的兜底断言。
    edit_all(MODS, zsvg(OLD_CHECKS), zsvg(ICO_CHECKS),
             '③ list-checks → lucide 原路径（进程分区 / 胶囊）',
             'm3 17 2 2 4-4', expect=1)
    # ③ 「目标」trailing：补上游那个 `·` 分隔符（只在有控件时渲染）
    edit_all(MODS, '<span class="zd-sec-x">2 分 18 秒',
             '<span class="zd-sec-x">2 分 18 秒<span class="zd-sep">\u00b7</span>',
             '③ 「目标」trailing 补 `·` 分隔符',
             '<span class="zd-sec-x">2 分 18 秒<span class="zd-sep">', expect=1)
    # ③ 暂停钮：`.td-browse-ico`(28/16) → `.zd-ico`(24/14) + lucide `pause`（两个圆角矩形）
    edit_all(MODS,
             '<button class="td-browse-ico" type="button" title="暂停目标" aria-label="暂停目标">'
             + zsvg('<path d="M9 4v16"/><path d="M15 4v16"/>') + '</button>',
             '<button class="zd-ico" type="button" title="暂停目标" aria-label="暂停目标">'
             + zsvg(ICO_PAUSE, 14) + '</button>',
             '③ 暂停钮 → `.zd-ico`(24) + lucide pause(14)',
             'rect x="14" y="3" width="5" height="18" rx="1"', expect=1)
    # ③ 头部「收起为胶囊」：上游是 `Minimize2Icon`（size-6 + size-3.5），
    #    上一版用了自绘的「上折角」chevron-up ⇒ 换成 lucide `minimize-2`。
    edit_all(MODS,
             '<button class="td-browse-ico" type="button" title="收起为胶囊" '
             'aria-label="收起为胶囊" data-zd-min="1">'
             + zsvg('<path d="m6 15 6-6 6 6"/>') + '</button>',
             '<button class="zd-ico" type="button" title="收起为胶囊" '
             'aria-label="收起为胶囊" data-zd-min="1">'
             + zsvg(ICO_MIN2, 14) + '</button>',
             '③ 收起为胶囊 → `.zd-ico`(24) + lucide minimize-2(14)',
             'm14 10 7-7', expect=1)
    # ① 两枚下拉 + 轻提示（插在 `.zd-mini` 之后、`.zd-host` 闭合之前）
    edit(MODS,
         '        <span class="zd-mini-v">3/5</span>\n      </button>\n    </div>\n',
         '        <span class="zd-mini-v">3/5</span>\n      </button>\n' + MENUS_HTML + '    </div>\n',
         '① 两枚下拉 + 轻提示 DOM',
         'class="zd-menu giencoder-dropdown-popup zd-menu-branch"')

    print('=== 2/3  panel.css ===')
    # ③ `.zd-sec-h` 高度 28 → 32（上游 `h-8`）
    edit(PCS,
         '.zd-sec-h {\n'
         '  display: flex; align-items: center; gap: 6px;\n'
         '  box-sizing: border-box; padding: 0 8px;\n'
         '  height: calc(28px * var(--ui-fs-ratio));\n'
         '  min-height: calc(28px * var(--ui-fs-ratio));\n'
         '  font-size: var(--font-size-body-1); color: var(--color-text-3);\n'
         '}\n',
         '.zd-sec-h {\n'
         '  display: flex; align-items: center; gap: 6px;\n'
         '  box-sizing: border-box; padding: 0 8px;\n'
         '  /* ③ 上游 `h-8` = 32px（上一版 28 是按「紧凑」自己压的）。 */\n'
         '  height: calc(32px * var(--ui-fs-ratio));\n'
         '  min-height: calc(32px * var(--ui-fs-ratio));\n'
         '  font-size: var(--font-size-body-1); color: var(--color-text-3);\n'
         '}\n',
         '③ 分区头 28 → 32px',
         '/* ③ 上游 `h-8` = 32px')
    # ③ 折叠箭头 12 → 14 + 折叠方向改走 spring
    edit(PCS,
         '.zd-cv { flex: none; width: 12px; height: 12px; opacity: 0; '
         'transition: opacity 120ms, transform 120ms; }\n',
         '.zd-cv { flex: none; width: 14px; height: 14px; opacity: 0;\n'
         '  transition: opacity 140ms, transform 300ms var(--transition-timing-function-spring); }\n',
         '③ 折叠箭头 12 → 14px + spring',
         '.zd-cv { flex: none; width: 14px; height: 14px;')
    # ④ 折展：`display:none` → `grid-template-rows` 弹性过渡（19.1 里给了新块）
    edit(PCS,
         '.zd-sec.is-closed .zd-cv { transform: rotate(-90deg); }\n'
         '.zd-sec.is-closed .zd-sec-b { display: none; }\n',
         '.zd-sec.is-closed .zd-cv { transform: rotate(-90deg); }\n'
         '/* ④ 折展的可见性改由 19.1 的 `grid-template-rows` 过渡裁决（原来是 `display:none`，'
         '硬切无动效）。 */\n',
         '④ 删「折展=display:none」（交给 19.1 的过渡）',
         '④ 折展的可见性改由 19.1')
    # ③ 迭代行：内距 8px / 圆角 8 / hover 底色（上游 `rounded-lg px-2 py-2 hover:bg-hover`）
    edit(PCS,
         '.zd-it {\n'
         '  display: flex; align-items: flex-start; gap: 8px;\n'
         '  box-sizing: border-box; padding: 6px 8px;\n'
         '  border-radius: 4px;\n'
         '  font-size: var(--font-size-body-2); color: var(--color-text-1);\n'
         '}\n',
         '.zd-it {\n'
         '  display: flex; align-items: flex-start; gap: 8px;\n'
         '  /* ③ 上游 `px-2 py-2`（8px 四边）+ `rounded-lg`（8）+ `hover:bg-hover`。\n'
         '     ⚠ 基态与 `:hover` 写在**同一块、基态在前**（硬规则 28）—— 别指望靠文档序压别人。 */\n'
         '  box-sizing: border-box; padding: 8px;\n'
         '  border-radius: 8px; background: transparent;\n'
         '  font-size: var(--font-size-body-2); color: var(--color-text-1);\n'
         '}\n'
         '.zd-it:hover { background: var(--color-fill-1); }\n',
         '③ 迭代行内距/圆角/hover',
         '③ 上游 `px-2 py-2`（8px 四边）')
    # ③ 迭代标题行高 20 → 16（上游 `leading-4`）；带行高 ⇒ 规则体内必须有字号 token
    edit(PCS,
         '.zd-it-t {\n'
         '  flex: 1 1 auto; min-width: 0; margin: 0;\n'
         '  font-size: var(--font-size-body-2);\n'
         '  line-height: calc(20px * var(--ui-fs-ratio));\n'
         '}\n',
         '.zd-it-t {\n'
         '  flex: 1 1 auto; min-width: 0; margin: 0;\n'
         '  font-size: var(--font-size-body-2);\n'
         '  /* ③ 上游 `leading-4` = 16px（上一版 20 偏松）。\n'
         '     ⚠ 带 `line-height` 的规则**必须**同时声明字号 token：收尾的 `apply88b.converge()`\n'
         '       会把 `calc(Npx * ratio)` 压平成裸 px，只在规则体内含 `var(--font-size-*)` 时\n'
         '       才重新派生（`mg-work/r108/ev/scan-flatten.py` 会抓）。 */\n'
         '  line-height: calc(16px * var(--ui-fs-ratio));\n'
         '}\n',
         '③ 迭代标题行高 20 → 16px',
         '③ 上游 `leading-4` = 16px')
    # ③ 圆形序号必须**等比**（本轮第五次回归时发现的边界缺陷）：
    #    本规则含 `var(--font-size-*)` ⇒ `apply88b` 的 scale_block 会把裸 `height:16px`
    #    派生成 `calc(16px * var(--ui-fs-ratio))`，而 `width` 不动 ⇒ 在 `--ui-fs` ≠ 14
    #    时会变成椭圆（实测 18 档：16 × 20.57）。约定见 apply108.py 头注释
    #    「带 `var(--font-size-*)` 的规则都不得声明 `height:Npx`」。
    #    两边都显式写 `calc` ⇒ 派生与收敛都幂等，任意字号下都是正圆。
    edit(PCS,
         '.zd-it-no {\n'
         '  flex: none; box-sizing: border-box;\n'
         '  width: 16px; height: 16px; border-radius: 50%;\n',
         '.zd-it-no {\n'
         '  flex: none; box-sizing: border-box;\n'
         '  /* ③ 圆序号**宽高必须同源**：本规则含字号 token ⇒ `apply88b` 只派生 `height`，\n'
         '     裸 `width:16px` 不跟 ⇒ 非默认字号下成椭圆。两边都写 calc 即恒为正圆。 */\n'
         '  width: calc(16px * var(--ui-fs-ratio)); height: calc(16px * var(--ui-fs-ratio));\n'
         '  border-radius: 50%;\n',
         '③ 圆序号宽高同比（修非默认字号下的椭圆）',
         'width: calc(16px * var(--ui-fs-ratio)); height: calc(16px * var(--ui-fs-ratio));')
    # ④ / ① ③ 新规则（追加在 `/* r108-l2 */` 之前）
    # ★★ 必须把 l2 的标记**原样接回去**（`CSS_TAIL + '/* r108-l2 */\n'`）：
    #    l2 的 `tail()` 判据就是这个标记，l3 若只把它换掉，下次复跑 `patch108l2.py`
    #    会判定「第 19 节还没写过」而**把整节 CSS 再追加一份**（本轮真踩过：panel.css
    #    78431 字符、`19. 任务信息面板` 与 `.zd-card {` 各 2 处）。
    #    ⇒ 各层的 mark 是「后一层必须替前一层保住的契约」，收尾有兜底断言。
    edit(PCS, '/* r108-l2 */\n', CSS_TAIL + '/* r108-l2 */\n',
         '④ 19.1~19.3 新规则（折展弹性 / 两枚下拉 / 轻提示）',
         '/* r108-l3 */')
    # ④ 选择器组扩员：`.zd-menu` 收进第 1 节的 DS Dropdown 适配层（8 处）
    for old, new, label, gm in GROUP_EDITS:
        edit(PCS, old, new, label, gm)

    print('=== 3/3  panel.js ===')
    # ①④ 就地替换末尾那段（原来只有「立刻 hidden」的硬切，且没有 Git 三行）
    edit(PJS, JS_OLD, JS_NEW,
         '①④ Git 三行交互 + 两枚下拉 + 弹性切换',
         '第十四拍 ① Git 工具三行：接上交互')

    print('=== 4/4  跨层标记兜底断言 ===')
    # ★★ 各代的 mark 是「后一层必须替前一层保住」的契约：谁把它删掉，谁就会让**上一层**
    #   复跑时误判「还没写过」而整块重挂（本轮 l2 的 `/* r108-l2 */` 就被 l3 初稿覆盖过一次，
    #   panel.css 里第 19 节当场变两份）。这里把三层的存活性一次盯住。
    marks = [
        (MODS, 'id="av-zd-status"', 'l2 · 面板静态 DOM'),
        (PCS, '/* r108-l2 */', 'l2 · 第 19 节'),
        (PJS, 'av-zd-status', 'l2 · 面板控制器'),
        (PCS, '/* r108-l3 */', 'l3 · 第 19.1~19.3 节'),
        (MODS, 'class="zd-menu giencoder-dropdown-popup zd-menu-branch"', 'l3 · 两枚下拉'),
    ]
    bad = []
    for p, mk, label in marks:
        if mk not in rd(p)[0]:
            bad.append('%s：%s（在 %s 里找不到）' % (label, mk, os.path.basename(p)))
    for p in (MODS, PCS, PJS):
        t = rd(p)[0]
        if t.count('19. 任务信息面板') > 1 or t.count('.zd-card {') > 1:
            bad.append('%s：第 19 节疑似重复（19节=%d / .zd-card=%d）'
                       % (os.path.basename(p), t.count('19. 任务信息面板'), t.count('.zd-card {')))
    if bad:
        sys.exit('!! 跨层标记自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')

    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))


if __name__ == '__main__':
    main()
