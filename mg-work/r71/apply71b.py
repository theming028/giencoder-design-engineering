# -*- coding: utf-8 -*-
"""
第 71 轮 · 补丁 b（需求 3 后续）

背景：apply71.py 已把 4 处例外归 8px（权限选择弹层 12px / .td-more 5px / .td-skill-pop 12px / .td-dp 6px）。
      随后做「弹层容器」规则级精扫，又发现 1 处遗漏的大浮层：

        .skills-popup-bg  760×320 居中「技能选择浮窗」→ 仍 12px（9 页共享 CSS 各一份）

      它与已改成 8px 的 .td-skill-pop 是**同一个 760×320 技能面板**（avatar.html 注释原文：
      「技能面板 原 760×320 居中 → 本页右栏窄…宽度改为 min(760px, 100%)，其余几何（圆角 12…）不变」）。
      留着 12px → 同一个组件凭入口不同渲染出两种圆角，正是需求 3 要消除的不一致。
      用户对需求 3 的口径：「含大浮层，全部统一 8px」→ 本处属于大浮层，补齐到 8px。

不动的（并已在汇报中说明）：
  · .avatar-tooltip 6px       —— 是 Tooltip（微提示），不属「下拉菜单」族
  · .giencoder-modal 12px     —— DS 模态弹窗（非下拉/浮层）
  · .td-modal 16px            —— r66 用户指定的模态面板材质
  · .giencoder-dropdown-item 4px / .add-menu-item 4px / .perm-menu-item 6px
                              —— 都是**菜单项**而非面板，DS 既有档位

约定（见 PLAYBOOK §P1）：newmark 命中即 SKIP；OLD 必须恰好命中 N 次否则 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r71b-backup'

PAGES = ['automation.html', 'avatar.html', 'base.html', 'dev.html', 'kanban.html',
         'req-kanban.html', 'settings.html', 'skills.html', 'task-detail.html']


def load(name):
    with io.open(os.path.join(ROOT, 'pages', name), encoding='utf-8') as f:
        return f.read()


def save(name, s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    dst = os.path.join(BACKUP, name)
    if not os.path.exists(dst):
        with io.open(os.path.join(ROOT, 'pages', name), encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(os.path.join(ROOT, 'pages', name), 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    """块内替换（只动一条声明）—— 载荷不得夹带任何标签。"""
    for bad in ('</style', '</script', '<style', '<script', '</body', '</html'):
        if bad in payload:
            sys.exit('!! 元守卫失败：%s 载荷含 %s' % (label, bad))


# ---------------------------------------------------------------------------
# 需求 3 补遗：.skills-popup-bg 12px → 8px（9 页共享 CSS，每页恰 1 处）
# 锚点必须带 .skills-popup-bg{width:760px;height:320px; 前缀，
# 否则边框后紧跟的 `border-radius:12px;background:rgba(255,255,255,0.88)` 在别处也可能出现。
# ---------------------------------------------------------------------------
OLD = u'.skills-popup-bg{width:760px;height:320px;border-radius:12px;'
NEW = u'.skills-popup-bg{width:760px;height:320px;border-radius:8px;'
NEWMARK = re.compile(r'\.skills-popup-bg\{width:760px;height:320px;border-radius:8px;')

guard(u'skills-popup-bg', NEW)


def run():
    applied, skipped = [], []
    for page in PAGES:
        s = load(page)
        before = s
        if NEWMARK.search(s):
            skipped.append(page)
            continue
        n = s.count(OLD)
        if n != 1:
            sys.exit('!! [%s] skills-popup-bg 锚点命中 %d 次（期望 1）—— 中止' % (page, n))
        s = s.replace(OLD, NEW)
        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            if d != 0:
                sys.exit('!! [%s] 标签计数异常 %s: Δ%d（期望 0）' % (page, tag, d))
        save(page, s)
        applied.append(page)
    print(u'应用: %d 项 %s' % (len(applied), applied))
    print(u'跳过: %d 项 %s' % (len(skipped), skipped))

    # ---------------- 自检 ----------------
    print(u'\n--- 自检 ---')
    ok = 0
    total = 0
    for page in PAGES:
        s = load(page)
        checks = [
            (u'%s .skills-popup-bg 已是 8px' % page, s.count(NEW) == 1),
            (u'%s 旧 12px 清零' % page, s.count(OLD) == 0),
            (u'%s 页面内 760px;height:320px 圆角唯一 8px' % page,
             s.count(u'height:320px;border-radius:8px;') == 1),
        ]
        for name, cond in checks:
            total += 1
            if cond:
                ok += 1
            else:
                print(u'  ✗ %s' % name)
    print(u'自检：%d/%d 通过' % (ok, total))
    if ok != total:
        sys.exit(1)


if __name__ == '__main__':
    run()
