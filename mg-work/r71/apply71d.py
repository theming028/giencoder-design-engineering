# -*- coding: utf-8 -*-
"""
第 71 轮 · 补丁 d（需求 4 修正 2：修 r71 引入的「棘轮」回归）

现象（运行时实测）：
  1440 视口把预览栏钳到 561 后，把视口放大到 1920，预览栏**仍是 561**，不再回到默认 641。
  原因：本页只维护一个 `panelW` 变量，既当「用户期望宽」又当「生效宽」；
        window resize 处理里 clampNow() 调 setPanelW(panelW, false)，
        于是「被压缩后的值」被写回期望位 —— 一旦缩过就永久缩，形成棘轮。

  改前不会出现：那时 MIN_PANEL = DEF_PANEL = 641，clamp(641,641,641) 恒等。
  r71 把 MIN_PANEL 降到 561（= 树 240 + 条 1 + 代码 320）后才暴露。

修法：把「期望宽」与「生效宽」拆成两个变量。
  · 期望宽（want）：只由 恢复记忆 / 拖动 / 键盘 / 双击复位 改写 —— 即用户意图；
  · 生效宽（panelW/treeW）：每次由 期望宽 + 当前可用宽 重新钳出，可被临时压缩。
  clampNow() / setOpen() 一律从「期望宽」重钳 → 视口变大时自动长回来。

幂等三要素：newmark 命中即 SKIP；每个 OLD 必须恰好命中 N 次否则 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r71d-backup'
PAGE = 'avatar.html'

JOBS = [
    # ---- 1) 变量声明：新增一对「期望宽」（注释里不写变量名，避免污染断言计数） ----
    (
        u'声明期望宽变量',
        re.compile(r'/\* \u2605 \u671f\u671b\u5bbd\uff08\u7528\u6237\u610f\u56fe\uff09'),
        u'  var panelW = DEF_PANEL, treeW = DEF_TREE;\n'
        u'  var bound = false, ctxBound = false;',
        u'  /* \u751f\u6548\u5bbd\uff1a\u6bcf\u6b21\u7531\u671f\u671b\u5bbd + \u5f53\u524d\u53ef\u7528\u5bbd\u91cd\u94b3\uff0c\u53ef\u88ab\u4e34\u65f6\u538b\u7f29 */\n'
        u'  var panelW = DEF_PANEL, treeW = DEF_TREE;\n'
        u'  /* \u2605 \u671f\u671b\u5bbd\uff08\u7528\u6237\u610f\u56fe\uff09\uff1a\u4ec5\u7531\u300c\u6062\u590d\u8bb0\u5fc6 / \u62d6\u52a8 / \u952e\u76d8 / \u53cc\u51fb\u590d\u4f4d\u300d\u6539\u5199\u3002\n'
        u'     clampNow / setOpen \u4e00\u5f8b\u4ece\u5b83\u91cd\u94b3 \u2192 \u89c6\u53e3\u53d8\u5927\u65f6\u751f\u6548\u5bbd\u4f1a\u81ea\u52a8\u957f\u56de\u6765\uff0c\u907f\u514d\u300c\u4e00\u7f29\u5230\u5e95\u300d\u7684\u68d8\u8f6e\u3002 */\n'
        u'  var wantPanel = DEF_PANEL, wantTree = DEF_TREE;\n'
        u'  var bound = false, ctxBound = false;',
        1,
    ),
    # ---- 2) setPanelW：先记期望宽，再由期望宽钳出生效宽 ----
    (
        u'setPanelW 记期望宽',
        re.compile(r'wantPanel = Math\.round\(w\);'),
        u'    panelW = Math.round(clamp(w, MIN_PANEL, maxPanelW()));',
        u'    wantPanel = Math.round(w);\n'
        u'    panelW = Math.round(clamp(wantPanel, MIN_PANEL, maxPanelW()));',
        1,
    ),
    # ---- 3) setTree：同上 ----
    (
        u'setTree 记期望宽',
        re.compile(r'wantTree = Math\.round\(w\);'),
        u'    treeW = Math.round(clamp(w, MIN_TREE, maxTree()));',
        u'    wantTree = Math.round(w);\n'
        u'    treeW = Math.round(clamp(wantTree, MIN_TREE, maxTree()));',
        1,
    ),
    # ---- 4) 持久化「期望宽」而不是被压缩后的生效宽 ----
    (
        u'setPanelW 持久化期望宽',
        re.compile(r'writeStore\(\{ panelW: wantPanel \}\)'),
        u'    if (persist) writeStore({ panelW: panelW });',
        u'    if (persist) writeStore({ panelW: wantPanel });',
        1,
    ),
    (
        u'setTree 持久化期望宽',
        re.compile(r'writeStore\(\{ treeW: wantTree \}\)'),
        u'    if (persist) writeStore({ treeW: treeW });',
        u'    if (persist) writeStore({ treeW: wantTree });',
        1,
    ),
    # ---- 5) 拖拽结束时的落盘同样写期望宽 ----
    (
        u'拖拽落盘写期望宽',
        re.compile(r'\{ panelW: wantPanel \} : \{ treeW: wantTree \}'),
        u'      writeStore(kind === \'panel\' ? { panelW: panelW } : { treeW: treeW });',
        u'      writeStore(kind === \'panel\' ? { panelW: wantPanel } : { treeW: wantTree });',
        1,
    ),
    # ---- 6) clampNow 从期望宽重钳（关键：棘轮就是这里来的） ----
    (
        u'clampNow 从期望宽重钳',
        re.compile(r'setPanelW\(wantPanel, false\);'),
        u'  function clampNow() {\n'
        u'    if (!hostRow) return;\n'
        u'    setPanelW(panelW, false);\n'
        u'    setTree(treeW, false);\n'
        u'  }',
        u'  function clampNow() {\n'
        u'    if (!hostRow) return;\n'
        u'    setPanelW(wantPanel, false);\n'
        u'    setTree(wantTree, false);\n'
        u'  }',
        1,
    ),
    # ---- 7) setOpen 展开时同样从期望宽重钳 ----
    (
        u'setOpen 从期望宽重钳',
        re.compile(r'setPanelW\(wantPanel, false\);\n      setTree\(wantTree, false\);'),
        u'      setPanelW(panelW, false);\n'
        u'      setTree(treeW, false);',
        u'      setPanelW(wantPanel, false);\n'
        u'      setTree(wantTree, false);',
        1,
    ),
    # ---- 8b) 「显示文件目录」重新展开时也从期望宽重钳（第三处调用点） ----
    (
        u'显示目录时从期望宽重钳',
        re.compile(r'if \(!hidden\) setTree\(wantTree, false\);'),
        u'        if (!hidden) setTree(treeW, false);',
        u'        if (!hidden) setTree(wantTree, false);',
        1,
    ),
    # ---- 8) 恢复记忆：期望宽一起恢复 ----
    (
        u'恢复记忆同步期望宽',
        re.compile(r'wantPanel = d\.panelW;'),
        u'    var d = readStore();\n'
        u'    if (typeof d.panelW === \'number\') panelW = d.panelW;\n'
        u'    if (typeof d.treeW === \'number\') treeW = d.treeW;\n'
        u'    clampNow();',
        u'    var d = readStore();\n'
        u'    if (typeof d.panelW === \'number\') { panelW = d.panelW; wantPanel = d.panelW; }\n'
        u'    if (typeof d.treeW === \'number\') { treeW = d.treeW; wantTree = d.treeW; }\n'
        u'    clampNow();',
        1,
    ),
]


def load():
    with io.open(os.path.join(ROOT, 'pages', PAGE), encoding='utf-8') as f:
        return f.read()


def save(s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    dst = os.path.join(BACKUP, PAGE)
    if not os.path.exists(dst):
        with io.open(os.path.join(ROOT, 'pages', PAGE), encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(os.path.join(ROOT, 'pages', PAGE), 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    for bad in ('</style', '</script', '<style', '<script', '</body', '</html'):
        if bad in payload:
            sys.exit('!! \u5143\u5b88\u536b\u5931\u8d25\uff1a%s \u8f7d\u8377\u542b %s' % (label, bad))
    for l in label.split(u'\uff5c'):
        pass


def main():
    s = load()
    before = s
    applied, skipped = [], []
    for label, newmark, OLD, NEW, expect in JOBS:
        guard(label, NEW)
        if newmark.search(s):
            skipped.append(label)
            continue
        n = s.count(OLD)
        if n != expect:
            sys.exit('!! [%s] \u951a\u70b9\u547d\u4e2d %d \u6b21\uff08\u671f\u671b %d\uff09\u2014\u2014 \u4e2d\u6b62' % (label, n, expect))
        s = s.replace(OLD, NEW)
        applied.append(label)

    if applied:
        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            if d != 0:
                sys.exit('!! \u6807\u7b7e\u8ba1\u6570\u5f02\u5e38 %s: \u0394%d\uff08\u671f\u671b 0\uff09' % (tag, d))
        save(s)
    print(u'\u5e94\u7528: %d \u9879 %s' % (len(applied), applied))
    print(u'\u8df3\u8fc7: %d \u9879 %s' % (len(skipped), skipped))

    # ================= 自检 =================
    print(u'\n--- \u81ea\u68c0 ---')
    t = load()
    checks = [
        (u'期望宽赋值（panel）唯一', t.count(u'wantPanel = Math.round(w);') == 1),
        (u'期望宽赋值（tree）唯一', t.count(u'wantTree = Math.round(w);') == 1),
        (u'clampNow/setOpen 均从期望宽重钳',
         t.count(u'setPanelW(wantPanel, false);') == 2 and t.count(u'setTree(wantTree, false);') == 3),
        (u'显示目录切换也从期望宽重钳', t.count(u'if (!hidden) setTree(wantTree, false);') == 1),
        (u'生效宽不再进入持久化', t.count(u'{ panelW: panelW }') == 0 and t.count(u'{ treeW: treeW }') == 0),
        (u'持久化写期望宽', t.count(u'writeStore({ panelW: wantPanel });') == 1 and t.count(u'writeStore({ treeW: wantTree });') == 1),
        (u'拖拽落盘写期望宽', t.count(u'{ panelW: wantPanel } : { treeW: wantTree }') == 1),
        (u'恢复记忆同步期望宽',
         t.count(u'panelW = d.panelW; wantPanel = d.panelW;') == 1 and t.count(u'treeW = d.treeW; wantTree = d.treeW;') == 1),
        (u'旧写法 setPanelW(panelW, false) 清零', t.count(u'setPanelW(panelW, false);') == 0),
        (u'旧写法 setTree(treeW, false) 清零', t.count(u'setTree(treeW, false);') == 0),
        (u'钳制常量仍是 561 / 380 / 641',
         t.count(u'var DEF_PANEL = 641, MIN_PANEL = 561, MAIN_MIN = 380;') == 1),
        (u'<style>/</style> 配平', t.count(u'<style') == t.count(u'</style>')),
    ]
    ok = 0
    for name, cond in checks:
        if cond:
            ok += 1
        else:
            print(u'  \u2717 %s' % name)
    print(u'自检\uff1a%d/%d \u901a\u8fc7' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
