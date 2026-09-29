#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 70 轮：数字分身 AI 对话框 / 预览栏四改 + 全站按钮 ring 清理

1. 数字分身 .td-right（AI 对话框）投影 → 1px 描边（取 main 容器档色）
2. 数字分身 .td-browse-slot 展开/收起动效 → 改为左导航 aside 同款「宽度舒展」
3. .td-right / .td-browse 的面板外缘线颜色 → 与 main 容器一致（avatar + task-detail）
4. 全站 9 页 .giencoder-btn-secondary 去掉 --btn-ring 参数

幂等三要素：newmark 命中即 skip → OLD 须恰好命中 1 次否则 sys.exit → 跑完复跑确认 0 应用。
"""
import re
import sys
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, 'pages')
BACKUP = '/tmp/r70-backup'

# ───────────────────────── 各 job 的 OLD / NEW ─────────────────────────

# A. 抽屉投影 → 1px 描边（avatar）
A_OLD = """.td-right {
        flex: none; width: var(--td-right-w); box-sizing: border-box;
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--color-bg-1); border-radius: 8px;
        box-shadow: var(--td-panel-shadow);   /* 同左栏：设计稿无描边，只有柔和投影 */
      }"""
A_NEW = """.td-right {
        flex: none; width: var(--td-right-w); box-sizing: border-box;
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--color-bg-1); border-radius: 8px;
        /* ★ 第 70 轮第 1 项：去掉柔和投影，改为 1px 描边（取 main 容器那一档色） */
        border: 1px solid var(--td-panel-line);
      }"""

# B. 抽屉内层宽度跟着扣掉左右各 1px 描边（avatar）
B_OLD = """  /* 关闭态宽度动画期间内部保持设计宽，避免内容被横向压扁 */
  .av-chat-drawer > .td-right-inner { width: var(--av-chat-w); }"""
B_NEW = """  /* 关闭态宽度动画期间内部保持设计宽，避免内容被横向压扁 */
  /* ★ 第 70 轮第 1b 项：抽屉改 1px 描边后，内层宽 = 设计宽 − 左右各 1px，
     否则会溢出内容盒 2px 被 overflow 裁掉。 */
  .av-chat-drawer > .td-right-inner { width: calc(var(--av-chat-w) - 2px); }"""

# C. 面板外缘线颜色（avatar）
C_AV_OLD = ':root { --td-panel-line: #DAE3ED; --td-hairline: var(--color-border-1); }'
C_AV_NEW = (':root { --td-panel-line: #ECEEF2; --td-hairline: var(--color-border-1); }\n'
            '/* ★ 第 70 轮第 3 项：面板外缘线改取 main 容器那一档色（外壳按路由给的常规档）。 */')

# C'. 面板外缘线颜色（task-detail）
C_TD_OLD = """        /* ★ 第 52 轮第 3 项：面板描边色。设计稿根帧 836:26404 实测：白面板四周有一圈 1px 线，
           在 #E5EDF5 底上按 0.5x 合成读数 #DFE8F1 ⇒ 反解原色 (223.5,232,241)*2-(229,237,245)
           = #DAE3ED。DS 无常量，故沿用本页既有惯例（--td-crumb-line）落成本页 token。 */
        --td-panel-line: #DAE3ED;"""
C_TD_NEW = """        /* ★ 第 52 轮第 3 项：面板描边色。设计稿根帧 836:26404 实测：白面板四周有一圈 1px 线，
           在 #E5EDF5 底上按 0.5x 合成读数 #DFE8F1 ⇒ 反解原色 (223.5,232,241)*2-(229,237,245)。
           DS 无常量，故沿用本页既有惯例（--td-crumb-line）落成本页 token。
           ★ 第 70 轮第 3 项：取值改与 main 容器那一档色一致。 */
        --td-panel-line: #ECEEF2;"""

# D1. .td-browse 改常驻 flex，取消 display 硬切（avatar）
D1_OLD = """.td-browse {
        display: none; flex: 1 1 auto; min-width: 0; box-sizing: border-box;"""
D1_NEW = """.td-browse {
        display: flex; flex: 1 1 auto; min-width: 0; box-sizing: border-box;"""

# D2. 动效：keyframes 位移 → 容器宽度过渡（avatar）
D2_OLD = """/* ★ 第 54 轮第 3 项：预览栏展开/收起微动效 —— 改为「从右边推出来 / 关闭时向右收回去」。
         r53 用的是 clip-path 从左往右「抹开」，方向感不对（像被擦出来，不像被推出来）。
         现改为整栏横向位移：开 = translateX(100%) → 0；关 = 0 → translateX(100%)。
         ⚠️ 必须套一层裁剪窗口 .td-browse-slot：shell 的 flex 行是 overflow:visible，
            直接给 .td-browse 加 translateX 会让整栏溢出到外壳右侧、撑出横向滚动条。
            slot 与面板同尺寸、透明无样式，不改动任何既有几何（树宽 / 代码区 / 分栏条全不动）。
         收起仍走 .is-closing：先播 220ms 移出动画，随后由 setOpen 摘掉 is-browse（见 JS 段）。 */
      .td-browse-slot { display: none; flex: 0 0 var(--av-browse-w, 641px); min-width: 0; overflow: hidden; }
      .av-browse-on .td-browse-slot { display: flex; }
      @keyframes tdBrowseIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
      }
      @keyframes tdBrowseOut {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
      }
      .av-browse-on .td-browse {
        animation: tdBrowseIn 280ms var(--transition-timing-function-enter, cubic-bezier(0.16, 1, 0.3, 1)) both;
      }
      .av-browse-on .td-browse.is-closing {
        animation: tdBrowseOut 220ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1)) both;
      }"""
D2_NEW = """/* ★ 第 70 轮第 2 项：预览栏展开/收起动效改为「宽度舒展 / 收拢」——与左导航 aside 同款
         （200ms + 同一条缓动曲线，纯宽度过渡，不做位移、不做 clip-path）。
         做法：容器 .td-browse-slot 自己过渡 flex-basis（0 ↔ --av-browse-w），
         面板以固定宽挂在里面、不参与收缩 ⇒ 被容器 overflow 裁切，形成从左往右「长出来」的观感。
         ⚠️ min-width:0 必需：flex 项默认 min-width:auto 会被内容撑开，宽度过渡直接失效。
         ⚠️ 拖动分栏条时必须关掉过渡，否则跟手会滞后。 */
      .td-browse-slot {
        --av-browse-ease: cubic-bezier(0.22, 1, 0.36, 1);   /* 与左导航 aside 展开曲线同值 */
        display: none; flex: 0 0 0px; min-width: 0; overflow: hidden;
      }
      /* 未挂进 shell flex 行之前不渲染；挂好后由 JS 打上标记 */
      .td-browse-slot.av-slot-placed { display: flex; transition: flex-basis 200ms var(--av-browse-ease); }
      .av-browse-on > .td-browse-slot { flex-basis: var(--av-browse-w, 641px); }
      .td-browse-slot > .td-browse { flex: none; width: var(--av-browse-w, 641px); }
      .av-browse-on.is-col-dragging .td-browse-slot { transition: none; }"""

# D3. place()：挂好后打标记（avatar）
D3_OLD = """    hostRow.insertBefore(splitMain, drawer.nextSibling);
    hostRow.insertBefore(slot, splitMain.nextSibling);
    bindAll();"""
D3_NEW = """    hostRow.insertBefore(splitMain, drawer.nextSibling);
    hostRow.insertBefore(slot, splitMain.nextSibling);
    slot.classList.add('av-slot-placed');   /* ★ 第 70 轮第 2 项：挂进 flex 行后才渲染 */
    bindAll();"""

# D4. setOpen：收起不再依赖 keyframes（avatar）
D4_OLD = """    if (pane.classList.contains('is-closing')) return;
    var done = function () {
      pane._browseT = null;
      pane.classList.remove('is-closing');
      hostRow.classList.remove('av-browse-on');
      if (btn) btn.setAttribute('aria-pressed', 'false');
      syncLayout();
      setTimeout(syncLayout, 260);
    };
    pane.classList.add('is-closing');
    pane._browseT = setTimeout(done, 240);
    pane.addEventListener('animationend', function onEnd(e) {
      if (e.target !== pane) return;            /* 过滤内层跟手位移动画的冒泡 */
      clearTimeout(pane._browseT);
      pane.removeEventListener('animationend', onEnd);
      done();
    });
  }"""
D4_NEW = """    if (pane.classList.contains('is-closing')) return;
    /* ★ 第 70 轮第 2 项：收起不再播 keyframes —— 摘掉状态类后由 .td-browse-slot 的
       flex-basis 过渡自然收拢（与左导航同款）。is-closing 只作 JS 防抖标记，无对应 CSS；
       期间再点开会在上方分支里清掉定时器并平滑反向。 */
    pane.classList.add('is-closing');
    hostRow.classList.remove('av-browse-on');
    if (btn) btn.setAttribute('aria-pressed', 'false');
    pane._browseT = setTimeout(function () {
      pane._browseT = null;
      pane.classList.remove('is-closing');
      syncLayout();
    }, 220);
    syncLayout();
  }"""

# E. 全站：btn-secondary 去 --btn-ring
E1_OLD = ('.giencoder-btn-secondary{--btn-bg:var(--color-bg-5);--btn-ring:var(--btn-bg);'
          'background:var(--btn-bg);color:var(--color-text-1);border-color:var(--color-border-2);'
          'box-shadow:0 1px 2px #0f172a0a, 0 0 0 1px var(--btn-ring)}')
E1_NEW = ('.giencoder-btn-secondary{--btn-bg:var(--color-bg-5);background:var(--btn-bg);'
          'color:var(--color-text-1);border-color:var(--color-border-2);'
          'box-shadow:0 1px 2px #0f172a0a}')
E2_OLD = ('.giencoder-btn-secondary:active{--btn-bg:var(--color-bg-5);background:var(--btn-bg);'
          'box-shadow:0 1px 2px #0f172a0a, 0 0 0 0 var(--btn-ring)}')
E2_NEW = ('.giencoder-btn-secondary:active{--btn-bg:var(--color-bg-5);background:var(--btn-bg);'
          'box-shadow:0 1px 2px #0f172a0a}')

# 每个 job = (名字, OLD, NEW, newmark)
AVATAR_JOBS = [
    ('A  抽屉投影→1px描边',      A_OLD,  A_NEW,  '★ 第 70 轮第 1 项'),
    ('B  抽屉内层宽度扣描边',     B_OLD,  B_NEW,  '★ 第 70 轮第 1b 项'),
    ('C  面板外缘线改色(avatar)', C_AV_OLD, C_AV_NEW, '★ 第 70 轮第 3 项'),
    ('D1 .td-browse 常驻 flex',  D1_OLD, D1_NEW, '.td-browse {\n        display: flex; flex: 1 1 auto;'),
    ('D2 动效→宽度过渡',         D2_OLD, D2_NEW, '★ 第 70 轮第 2 项：预览栏展开/收起动效'),
    ('D3 place 打 placed 标记',  D3_OLD, D3_NEW, "slot.classList.add('av-slot-placed')"),
    ('D4 setOpen 去 keyframes',  D4_OLD, D4_NEW, '★ 第 70 轮第 2 项：收起不再播 keyframes'),
    ('E1 btn-secondary 去 ring', E1_OLD, E1_NEW, E1_NEW),
    ('E2 btn-secondary:active',  E2_OLD, E2_NEW, E2_NEW),
]
TD_JOBS = [
    ('C  面板外缘线改色(detail)', C_TD_OLD, C_TD_NEW, '★ 第 70 轮第 3 项：取值改与 main 容器'),
    ('E1 btn-secondary 去 ring', E1_OLD, E1_NEW, E1_NEW),
    ('E2 btn-secondary:active',  E2_OLD, E2_NEW, E2_NEW),
]
OTHER_JOBS = [
    ('E1 btn-secondary 去 ring', E1_OLD, E1_NEW, E1_NEW),
    ('E2 btn-secondary:active',  E2_OLD, E2_NEW, E2_NEW),
]

# 元守卫：新增载荷不得含这些字面量（会污染后续标签计数断言）
GUARD = ['</style', '</script', '</body', '</html', '<style', '<script', '<body', '<html']

TAG_TOKENS = ['<style', '</style>', '<script', '</script>']


def strip_comments(t):
    return re.sub(r'/\*.*?\*/', '', t, flags=re.S)


def patch(name, jobs, asserts):
    path = os.path.join(PAGES, name)
    s0 = open(path, encoding='utf-8').read()
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    bk = os.path.join(BACKUP, name)
    if not os.path.exists(bk):
        shutil.copy2(path, bk)

    # 元守卫
    for jn, _old, new, _mk in jobs:
        for g in GUARD:
            if g in new:
                print(f'!! 元守卫失败 [{name}] {jn}: 载荷含 {g!r}')
                sys.exit(1)

    s = s0
    applied, skipped = [], []
    for jn, old, new, mk in jobs:
        if mk and mk in s:
            skipped.append(jn)
            continue
        c = s.count(old)
        if c != 1:
            print(f'!! [{name}] {jn}: OLD 命中 {c} 次（应为 1），newmark 不在文中')
            sys.exit(1)
        s = s.replace(old, new, 1)
        applied.append(jn)

    # ── 自检 ──
    errs = []
    if len(applied):                                  # 只在真的改了东西时校验结构
        for tk in TAG_TOKENS:
            d = s.count(tk) - s0.count(tk)
            if d != 0:
                errs.append(f'{tk} 计数变了 {d:+d}')
    for label, cond in asserts(s, s0):
        if not cond:
            errs.append(label)
    if errs:
        print(f'!! [{name}] 自检失败：')
        for e in errs:
            print('   ✗', e)
        sys.exit(1)

    if applied:
        open(path, 'w', encoding='utf-8').write(s)
    print(f'[{name}] 应用: {len(applied)} 项 | 跳过: {len(skipped)} 项'
          f'  ({len(s0)} → {len(s)} B)')
    for jn in applied:
        print('   应用:', jn)
    for jn in skipped:
        print('   跳过:', jn)


def av_asserts(s, s0):
    sc = strip_comments(s)
    return [
        ('box-shadow: var(--td-panel-shadow) 残留', s.count('box-shadow: var(--td-panel-shadow)') == 0),
        ('var(--td-panel-shadow) 用法未清零', sc.count('var(--td-panel-shadow)') == 0),
        # 该描边声明现在应有 2 处：抽屉 .td-right + 预览栏 .td-browse
        ('1px 面板描边声明数不对', s.count('border: 1px solid var(--td-panel-line);') == 2),
        ('--td-panel-line 仍是旧值', sc.count('--td-panel-line: #DAE3ED') == 0),
        ('--td-panel-line 新值不唯一', sc.count('--td-panel-line: #ECEEF2') == 1),
        ('抽屉内层未扣描边', s.count('width: calc(var(--av-chat-w) - 2px)') == 1),
        ('tdBrowseIn 残留', s.count('tdBrowseIn') == 0),
        ('tdBrowseOut 残留', s.count('tdBrowseOut') == 0),
        ('@keyframes tdBrowse 残留', s.count('@keyframes tdBrowse') == 0),
        ('animationend 监听残留', s.count("pane.addEventListener('animationend'") == 0),
        ('旧 slot 定宽规则残留', s.count('flex: 0 0 var(--av-browse-w, 641px); min-width: 0; overflow: hidden; }') == 0),
        ('宽度过渡未落地', s.count('transition: flex-basis 200ms') == 1),
        ('拖动时未关过渡', s.count('.av-browse-on.is-col-dragging .td-browse-slot { transition: none; }') == 1),
        ('av-slot-placed 未成对', s.count('av-slot-placed') == 2),
        ('.td-browse 未改常驻 flex', s.count('.td-browse {\n        display: flex; flex: 1 1 auto;') == 1),
        ('secondary 仍带 ring 声明', s.count('.giencoder-btn-secondary{--btn-bg:var(--color-bg-5);--btn-ring') == 0),
        ('secondary 主规则被改坏', s.count(E1_NEW) == 1),
        ('secondary :active 被改坏', s.count(E2_NEW) == 1),
    ]


def td_asserts(s, s0):
    sc = strip_comments(s)
    return [
        ('--td-panel-line 仍是旧值', sc.count('--td-panel-line: #DAE3ED') == 0),
        ('--td-panel-line 新值不唯一', sc.count('--td-panel-line: #ECEEF2') == 1),
        ('本页面板描边声明数不对', s.count('border: 1px solid var(--td-panel-line);') >= 1),
        ('secondary 仍带 ring 声明', s.count('.giencoder-btn-secondary{--btn-bg:var(--color-bg-5);--btn-ring') == 0),
        ('secondary 主规则被改坏', s.count(E1_NEW) == 1),
        ('secondary :active 被改坏', s.count(E2_NEW) == 1),
    ]


def other_asserts(s, s0):
    return [
        ('secondary 仍带 ring 声明', s.count('.giencoder-btn-secondary{--btn-bg:var(--color-bg-5);--btn-ring') == 0),
        ('secondary 主规则被改坏', s.count(E1_NEW) == 1),
        ('secondary :active 被改坏', s.count(E2_NEW) == 1),
    ]


if __name__ == '__main__':
    patch('avatar.html', AVATAR_JOBS, av_asserts)
    patch('task-detail.html', TD_JOBS, td_asserts)
    for f in sorted(os.listdir(PAGES)):
        if f.endswith('.html') and f not in ('avatar.html', 'task-detail.html'):
            patch(f, OTHER_JOBS, other_asserts)
    print('✓ 第 70 轮全部通过')
