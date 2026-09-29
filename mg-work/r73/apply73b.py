# -*- coding: utf-8 -*-
"""
第 73 轮 · 补丁 b（需求 1：4px 圆角的「按钮」提到 8px，9 页）

【范围界定 —— 只动按钮】
DS 的 --border-radius-medium = 4px 是「按钮 / 输入框 / 卡片」的**共用默认档**
（tokens.md「圆角分级」明文：按钮/输入框/卡片 4px，标签 2px，弹窗/抽屉 8px）。
用户明确选「只改按钮」⇒ 本块**只**命中按钮，下列一律保持 4px 不动：
  · 输入框 / 下拉框  .giencoder-select-view / .giencoder-select-option
  · 菜单项          .giencoder-menu-item / .add-menu-item / .td-ctx .giencoder-dropdown-item
  · 标签 / 行        .kb-tag / .rq-type / .rq-status / .skill-row / .giencoder-menu-submenu-title
  · 骨架屏 / 进度条  .giencoder-skeleton-line / -title / .giencoder-progress-inner / -bar
  · 浏览栏 tab       .td-browse-tab

【实际命中的三类按钮（已取证）】
① 页面自定义的图标按钮 —— 圆角**写在内联 style 里**（React 产物，如「切换侧边栏」按钮
   style="width:24px;height:24px;border-radius:4px;…"，9 页共 112 个）。
   内联声明只能被 !important 的 CSS 压过 ⇒ 必须写 !important。
   实测无 `border-radius: 4px 4px …` 的多值写法，`[style*="border-radius: 4px"]` 精准。
② DS 编译产物的关闭按钮：原规则 `.giencoder-modal-close-btn,.giencoder-drawer-close-btn{border-radius:4px}`
③ 页面自定义按钮类：`.td-browse-add/.td-browse-ico`（浏览栏图标按钮）、`.kb-refresh`（刷新按钮）

【落点】`</body>` 之前 —— 层叠最晚，与页面中部的共享样式表同特异性时后者胜，无需 !important
（仅 ① 因内联需要 !important）。

幂等三要素：newmark 命中即 SKIP；锚点异常即 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r73b-backup'
PAGES = 'pages'

MARK = u'<style id="r73-radius-css">'
ANCHOR = u'</body>'

NEW = (
    u'<style id="r73-radius-css">\n'
    u'  /* ★ 第 73 轮 · 需求 1：把「按钮」的 4px 圆角提到 8px。\n'
    u'     ⚠️ 只动按钮。DS 的 --border-radius-medium（4px）是「按钮 / 输入框 / 卡片」的共用档，\n'
    u'        tokens.md「圆角分级」有明文 ⇒ 输入框、下拉框、菜单项、标签、骨架屏、进度条、\n'
    u'        浏览栏 tab 一律保持 4px，不在本块范围内。 */\n'
    u'\n'
    u'  /* ① DS 主按钮基类：.giencoder-btn{border-radius:var(--border-radius-medium)} = 4px\n'
    u'     （CDP CSS.getMatchedStylesForNode 实锤）。primary / secondary / text / icon 各变体都走这条。\n'
    u'     ⚠️ size-small 变体实测是 6px（小按钮配小圆角），**不属「4px 按钮」范围** ⇒ :not() 排除。\n'
    u'     ⚠️ 已带 Tailwind rounded-md（本项目 --radius:.625rem ⇒ 8px）的按钮本来就是 8px，不受影响。 */\n'
    u'  .giencoder-btn:not(.giencoder-btn-size-small) {\n'
    u'    border-radius: 8px;\n'
    u'  }\n'
    u'\n'
    u'  /* ② 弹窗页脚按钮在页面里另有 6px 设计（.td-modal .giencoder-btn）——\n'
    u'     特异性 (0,3,0) 压过 ①，显式还原成 6px，不参与本次提升。 */\n'
    u'  .td-modal .giencoder-btn:not(.giencoder-btn-size-small) {\n'
    u'    border-radius: 6px;\n'
    u'  }\n'
    u'\n'
    u'  /* ③ 例外：small + text 组合实测仍是 4px（如 .td-expand-btn）⇒ 属于「4px 按钮」，照提 */\n'
    u'  .giencoder-btn-size-small.giencoder-btn-text {\n'
    u'    border-radius: 8px;\n'
    u'  }\n'
    u'\n'
    u'  /* ② 页面自定义的图标按钮：圆角写在内联 style 里（React 产物），只有 !important 压得过 */\n'
    u'  button[style*="border-radius: 4px"] {\n'
    u'    border-radius: 8px !important;\n'
    u'  }\n'
    u'\n'
    u'  /* ③ Tailwind .rounded = .25rem = 4px（实测 base 的图标按钮）*/\n'
    u'  button.rounded {\n'
    u'    border-radius: 8px;\n'
    u'  }\n'
    u'\n'
    u'  /* ④ DS 关闭按钮：基类规则写的是 4px（CDP 实锤）⇒ 提到 8px。\n'
    u'     ⚠️ 同页还并存「被页面定制成 6px」的同类按钮（协作弹窗的 ×）：\n'
    u'        · kanban 走 .kb-coop-close（硬编码 6px）\n'
    u'        · task-detail 走 .td-coop .giencoder-modal-close-btn（var(--td-radius-card)）\n'
    u'     ⇒ 必须**先提升、再还原**（同特异性时后置者胜）—— 见紧跟其后的 ④b。\n'
    u'     实测反例：创建任务弹窗的 .kb-crt-close 无任何定制 ⇒ 真是 4px，属提升范围。 */\n'
    u'  .giencoder-modal-close-btn,\n'
    u'  .giencoder-drawer-close-btn {\n'
    u'    border-radius: 8px;\n'
    u'  }\n'
    u'\n'
    u'  /* ④b 还原「页面已定制为 6px」的关闭按钮 */\n'
    u'  .kb-coop-close,\n'
    u'  .td-coop .giencoder-modal-close-btn,\n'
    u'  .td-coop .giencoder-drawer-close-btn {\n'
    u'    border-radius: 6px;\n'
    u'  }\n'
    u'\n'
    u'  /* ⑤ 页面自定义按钮类（agent-browser 逐页扫 computed=4px 得出）+ 分页按钮 */\n'
    u'  .kb-crt-tb,\n'
    u'  .kb-crt-btn,\n'
    u'  .kb-crt-upbtn,\n'
    u'  .kb-refresh,\n'
    u'  .td-browse-add,\n'
    u'  .td-browse-ico,\n'
    u'  .td-expand-btn,\n'
    u'  .td-round-btn,\n'
    u'  .td-coop-btn,\n'
    u'  .av-main-edit,\n'
    u'  .av-link,\n'
    u'  .giencoder-pagination-item {\n'
    u'    border-radius: 8px;\n'
    u'  }\n'
    u'</style>\n'
)


def files():
    out = []
    for f in sorted(os.listdir(os.path.join(ROOT, PAGES))):
        if f.endswith('.html'):
            out.append(f)
    return out


def load(name):
    with io.open(os.path.join(ROOT, PAGES, name), encoding='utf-8') as f:
        return f.read()


def save(name, s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    src = os.path.join(ROOT, PAGES, name)
    dst = os.path.join(BACKUP, name)
    if not os.path.exists(dst):
        with io.open(src, encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(src, 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    for bad in ('</body', '</html'):
        if bad in payload:
            sys.exit('!! 元守卫失败：%s 载荷含 %s' % (label, bad))


def main():
    guard(u'圆角块', NEW)

    applied, skipped, failed = [], [], []
    for name in files():
        s = load(name)
        if MARK in s:
            skipped.append(name)
            continue
        n = s.count(ANCHOR)
        if n != 1:
            failed.append('%s: </body> 命中 %d 次' % (name, n))
            continue
        before = s
        s = s.replace(ANCHOR, NEW + ANCHOR)
        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            expect = 1 if tag in ('<style', '</style>') else 0
            if d != expect:
                failed.append('%s: 标签计数 %s Δ%d（期望 Δ%d）' % (name, tag, d, expect))
                break
        else:
            save(name, s)
            applied.append(name)

    print(u'应用: %d 页 | 跳过: %d 页 | 失败: %d 页' % (len(applied), len(skipped), len(failed)))
    if applied:
        print(u'  已改: ' + ', '.join(applied))
    if skipped:
        print(u'  已就位: ' + ', '.join(skipped))
    for f in failed:
        print(u'  ✗ ' + f)
    if failed:
        sys.exit(1)

    # ================= 自检 =================
    print(u'\n--- 自检 ---')
    checks = []
    for name in files():
        t = load(name)
        checks.append((u'%s: r73 圆角块恰好 1 个' % name, t.count(MARK) == 1))
        checks.append((u'%s: 内联图标按钮规则在位' % name, t.count(u'button[style*="border-radius: 4px"]') == 1))
        checks.append((u'%s: DS 主按钮基类规则在位（:not 排除 small）' % name, t.count(u'.giencoder-btn:not(.giencoder-btn-size-small) {\n    border-radius: 8px;') == 1))
        checks.append((u'%s: 弹窗 6px 还原规则在位' % name, t.count(u'.td-modal .giencoder-btn:not(.giencoder-btn-size-small) {') == 1))
        checks.append((u'%s: small+text 例外规则在位' % name, t.count(u'.giencoder-btn-size-small.giencoder-btn-text {') == 1))
        checks.append((u'%s: 分页按钮已纳入' % name, t.count(u'.giencoder-pagination-item {\n    border-radius: 8px;') == 1))
        checks.append((u'%s: Tailwind rounded 规则在位' % name, t.count(u'button.rounded {') == 1))
        checks.append((u'%s: 关闭按钮提升规则在位' % name, t.count(u'.giencoder-drawer-close-btn {\n    border-radius: 8px;') == 1))
        checks.append((u'%s: 6px 关闭按钮还原规则在位' % name, t.count(u'.td-coop .giencoder-modal-close-btn,') == 1))
        checks.append((u'%s: </body> 仍为 1' % name, t.count(ANCHOR) == 1))
    ok = 0
    for nm, cond in checks:
        if cond:
            ok += 1
        else:
            print(u'  ✗ %s' % nm)
    print(u'自检：%d/%d 通过' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
