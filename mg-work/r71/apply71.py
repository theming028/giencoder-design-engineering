# -*- coding: utf-8 -*-
"""
第 71 轮 · 幂等补丁
  需求 1：base.html 侧边栏「新会话」按钮 → macOS 液态玻璃（Liquid Glass）  【仅基础工作台】
  需求 2：task-detail.html 的 .td-browse-slot 展开/收起动效 → 与 avatar 同步（宽度舒展/收拢）
  需求 3：全局下拉菜单/浮层圆角统一 8px（权限选择 12px、更多操作 5px、技能浮窗 12px、数字分身浮窗 6px）
  需求 4：avatar.html —— main 内容容器自适应重排 + 预览栏让位（MIN_PANEL 641→561 / MAIN_MIN 240→380）

约定（见 PLAYBOOK §P1）：newmark 命中即 SKIP；OLD 必须恰好命中 N 次否则 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r71-backup'


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


def guard(label, payload, page_level=False):
    """page_level=True 用于「整块 <style> 追加到 </body> 前」的载荷 —— 它自身含 </style> 是预期的，
    但仍必须自配平（<style 与 </style> 计数相等）且不得夹带 </body>/</html>。
    page_level=False 用于「插进既有 <style>/<script> 块内部」的载荷 —— 任何闭合标签都不允许。"""
    for bad in ('</body', '</html'):
        if bad in payload:
            sys.exit('!! 元守卫失败：%s 载荷含 %s' % (label, bad))
    if page_level:
        if payload.count('<style') != payload.count('</style>') or payload.count('<script') != payload.count('</script'):
            sys.exit('!! 元守卫失败：%s 载荷 <style>/<script> 未自配平' % label)
    else:
        for bad in ('</style', '</script', '<style', '<script'):
            if bad in payload:
                sys.exit('!! 元守卫失败：%s 载荷含 %s' % (label, bad))


def apply_job(store, page, jobs, tag_delta):
    """jobs = [(label, newmark_re, OLD, NEW, expect)]"""
    s = load(page)
    before = s
    applied, skipped = [], []
    for label, newmark, OLD, NEW, expect in jobs:
        if re.search(newmark, s):
            skipped.append(label)
            continue
        n = s.count(OLD)
        if n != expect:
            sys.exit('!! [%s] %s 锚点命中 %d 次（期望 %d）—— 中止' % (page, label, n, expect))
        s = s.replace(OLD, NEW)
        applied.append(label)

    if applied:
        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            if d != tag_delta.get(tag, 0):
                sys.exit('!! [%s] 标签计数异常 %s: Δ%d（期望 %d）' % (page, tag, d, tag_delta.get(tag, 0)))
        save(page, s)
        store[page] = (applied, skipped)
    else:
        store[page] = ([], skipped)
    return store


# =====================================================================================
# 需求 1 · base.html 液态玻璃
# =====================================================================================
GLASS = u'''<style id="r71-glass-css">
  /* ★ 第 71 轮第 1 项：基础工作台「新会话」按钮 → macOS 液态玻璃（Liquid Glass）
     · 材质：backdrop-filter 模糊 + 饱和提亮 —— 玻璃真的在折射它背后的东西
     · 造型：上厚下薄的白色半透明渐变，模拟玻璃体内不同光路长度造成的厚度差
     · 高光：顶部 specular 亮边 + 底部反光 + 内壁柔光（三层 inset）
     · 边界：内圈 1px 白描边（玻璃棱）+ 外圈 1px 极淡深描边（定界），
             外投影分两档（近距硬边 + 远距扩散）形成「浮在桌面上的玻璃片」
     · 交互：hover 抬升 + 一道 100° 镜面扫光；:active 轻微下压
     ⚠️ 按钮本体带 React 内联 style（background / border / boxShadow），覆盖必须 !important。
     ⚠️ 本样式块必须排在共享样式表（页面中部那一大段）之后才能压过它的 .new-chat-btn 规则。 */
  .new-chat-btn {
    --nc-glass-ease: cubic-bezier(0.22, 1, 0.36, 1);
    position: relative;
    isolation: isolate;
    overflow: hidden;
    background:
      radial-gradient(130% 105% at 16% 0%,
        rgba(255, 255, 255, 0.95) 0%,
        rgba(255, 255, 255, 0.30) 42%,
        rgba(255, 255, 255, 0) 68%),
      linear-gradient(180deg,
        rgba(252, 253, 255, 0.76) 0%,
        rgba(248, 251, 255, 0.30) 46%,
        rgba(250, 252, 255, 0.52) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.92) !important;
    -webkit-backdrop-filter: blur(18px) saturate(180%) brightness(1.04);
    backdrop-filter: blur(18px) saturate(180%) brightness(1.04);
    box-shadow:
      0 0 0 1px rgba(15, 23, 42, 0.07),
      0 1px 1.5px rgba(15, 23, 42, 0.055),
      0 10px 22px -10px rgba(15, 23, 42, 0.22),
      inset 0 1px 0 #FFFFFF,
      inset 0 1px 8px rgba(255, 255, 255, 0.85),
      inset 0 -1px 0 rgba(15, 23, 42, 0.05),
      inset 0 -8px 14px -10px rgba(15, 23, 42, 0.16) !important;
    transition: box-shadow 240ms var(--nc-glass-ease),
                border-color 240ms var(--nc-glass-ease),
                transform 180ms var(--nc-glass-ease);
  }
  /* 玻璃棱的色散：左上偏冷、右下偏暖 —— 真实玻璃在不同入射角下折出的极淡彩边，
     也是「液态玻璃」和普通半透明白块最主要的观感差别。
     z-index:-1 让它落在「自身渐变之上、文字之下」（isolation:isolate 把负层级锁在按钮内）。 */
  .new-chat-btn::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    border-radius: inherit;
    background:
      radial-gradient(130% 110% at 14% -12%,
        rgba(168, 198, 255, 0.15) 0%, rgba(255, 255, 255, 0) 56%),
      radial-gradient(130% 110% at 88% 116%,
        rgba(255, 208, 216, 0.13) 0%, rgba(255, 255, 255, 0) 56%),
      radial-gradient(110% 80% at 50% 124%,
        rgba(188, 206, 238, 0.10) 0%, rgba(255, 255, 255, 0) 62%);
  }
  /* 玻璃下的文字带一点「抬起来」的底气（极淡的顶向高光） */
  .new-chat-btn > span:nth-child(2) { text-shadow: 0 1px 0 rgba(255, 255, 255, 0.6); }
  /* 镜面扫光：hover 时一道细长反光扫过玻璃表面 */
  .new-chat-btn::after {
    content: "";
    position: absolute;
    inset: -1px;
    z-index: 1;
    pointer-events: none;
    border-radius: inherit;
    background: linear-gradient(100deg,
      rgba(255, 255, 255, 0) 42%,
      rgba(255, 255, 255, 0.92) 50%,
      rgba(255, 255, 255, 0.30) 56%,
      rgba(255, 255, 255, 0) 64%);
    opacity: 0;
    translate: -110% 0;
  }
  .new-chat-btn:hover::after { animation: ncGlassSheen 760ms var(--nc-glass-ease); }
  @keyframes ncGlassSheen {
    0%   { translate: -110% 0; opacity: 0; }
    18%  { opacity: 1; }
    78%  { opacity: 1; }
    100% { translate: 110% 0; opacity: 0; }
  }
  .new-chat-btn:hover {
    background:
      radial-gradient(130% 105% at 16% 0%,
        rgba(255, 255, 255, 1) 0%,
        rgba(255, 255, 255, 0.42) 42%,
        rgba(255, 255, 255, 0) 68%),
      linear-gradient(180deg,
        rgba(253, 254, 255, 0.88) 0%,
        rgba(250, 252, 255, 0.46) 46%,
        rgba(252, 253, 255, 0.64) 100%) !important;
    border-color: #FFFFFF !important;
    box-shadow:
      0 0 0 1px rgba(15, 23, 42, 0.08),
      0 2px 4px rgba(15, 23, 42, 0.06),
      0 14px 28px -10px rgba(15, 23, 42, 0.26),
      inset 0 1px 0 #FFFFFF,
      inset 0 1px 10px rgba(255, 255, 255, 0.95),
      inset 0 -1px 0 rgba(15, 23, 42, 0.05),
      inset 0 -8px 14px -10px rgba(15, 23, 42, 0.14) !important;
  }
  .new-chat-btn:active {
    transform: scale(0.985);
    box-shadow:
      0 0 0 1px rgba(15, 23, 42, 0.07),
      0 1px 1px rgba(15, 23, 42, 0.05),
      0 3px 8px -4px rgba(15, 23, 42, 0.16),
      inset 0 1px 0 rgba(255, 255, 255, 0.90),
      inset 0 -1px 0 rgba(255, 255, 255, 0.50) !important;
  }
  /* 不支持 backdrop-filter 时退回实色玻璃（不留半透明空壳） */
  @supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
    .new-chat-btn {
      background: linear-gradient(180deg, #FFFFFF 0%, #F4F7FB 44%, #EDF1F7 100%) !important;
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .new-chat-btn { transition: none; }
    .new-chat-btn:hover::after { animation: none; }
  }
</style>'''
guard('glass', GLASS, page_level=True)

# =====================================================================================
# 需求 3 · 下拉菜单/浮层圆角统一 8px
# =====================================================================================
P_SKILL_OLD = u'        border-radius: var(--border-radius-xl); border: 1px solid var(--color-border-2);'
P_SKILL_NEW = u'        border-radius: 8px; border: 1px solid var(--color-border-2);'

P_PERM_OLD = u',zIndex:1e3,borderRadius:`12px`,background:'
P_PERM_NEW = u',zIndex:1e3,borderRadius:`8px`,background:'

P_MORE_OLD = u'        border: 1px solid var(--color-border-2);\n        border-radius: 5px;\n        box-shadow: var(--shadow3-down);'
P_MORE_NEW = u'        border: 1px solid var(--color-border-2);\n        border-radius: 8px;\n        box-shadow: var(--shadow3-down);'

P_DP_OLD = u'.td-dp.giencoder-popover { width: 320px; border-radius: var(--td-radius-card); }'
P_DP_NEW = u'.td-dp.giencoder-popover { width: 320px; border-radius: 8px; }'

# =====================================================================================
# 需求 2 · task-detail 预览栏动效与 avatar 同步
# =====================================================================================
ANIM_OLD = u'''      /* ★ 第 54 轮第 3 项：预览栏展开/收起微动效 —— 改为「从右边推出来 / 关闭时向右收回去」。
         r53 用的是 clip-path 从左往右「抹开」，方向感不对（像被擦出来，不像被推出来）。
         现改为整栏横向位移：开 = translateX(100%) → 0；关 = 0 → translateX(100%)。
         ⚠️ 必须套一层裁剪窗口 .td-browse-slot：.td-root 是 overflow:visible
            （第 24 轮为放两栏投影特意放开的），直接给 .td-browse 加 translateX
            会让整栏溢出到外壳右侧、撑出横向滚动条。
            slot 与面板同尺寸、透明无样式，不改动任何既有几何（树宽 / 代码区 / 分栏条全不动）。
         收起仍走 .is-closing：先播 220ms 移出动画，随后由 setOpen 摘掉 is-browse（见 JS 段）。 */
      .td-browse-slot { display: none; flex: 1 1 auto; min-width: 0; overflow: hidden; }
      .td-root.is-browse .td-browse-slot { display: flex; }
      @keyframes tdBrowseIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
      }
      @keyframes tdBrowseOut {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
      }
      .td-root.is-browse .td-browse {
        animation: tdBrowseIn 280ms var(--transition-timing-function-enter, cubic-bezier(0.16, 1, 0.3, 1)) both;
      }
      .td-root.is-browse .td-browse.is-closing {
        animation: tdBrowseOut 220ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1)) both;
      }
      @media (prefers-reduced-motion: reduce) {
        .td-root.is-browse .td-browse,
        .td-root.is-browse .td-browse.is-closing { animation: none; }
      }'''

ANIM_NEW = u'''      /* ★ 第 71 轮第 2 项：预览栏展开/收起动效与「数字分身」同步 —— 由横向位移改为「宽度舒展 / 收拢」。
         r54 用的整栏 translateX 在宽面板上像「推拉门」，与左栏的宽度收放不同族；
         现改为与 avatar .td-browse-slot 完全同一套做法：容器自己过渡 flex-basis（0 ↔ 可用宽），
         面板挂在里面、被容器 overflow 裁切 ⇒ 从左往右「长出来」，收拢反向。
         · 可用宽 = calc(100% - --td-browse-right-w)：此处的 100% 是 .td-root 的内容盒宽；
           .td-split 自带 margin-right:-9px 抵消自身宽度 ⇒ 净占 0，故只需减 AI 会话栏宽。
         · flex: 0 1（可缩不可伸）：is-keep-left 态下多出 ~600px 左栏时自动让位，不会撑破整行。
         · 收起靠一条 :has 规则把 basis 打回 0 —— 动画立刻起跑；
           JS 段那 240ms 定时器与 animationend 兜底逻辑保持不变（is-closing 仍在，只是不再驱动动画）。
         ⚠️ min-width:0 必需：flex 项默认 min-width:auto 会被内容撑开，宽度过渡直接失效。
         ⚠️ 拖动分栏条时必须关掉过渡，否则跟手会滞后。 */
      .td-browse-slot {
        --td-browse-ease: cubic-bezier(0.22, 1, 0.36, 1);   /* 与左导航 aside / 数字分身同值 */
        display: flex; flex: 0 1 0px; min-width: 0; overflow: hidden;
        transition: flex-basis 200ms var(--td-browse-ease);
      }
      .td-root.is-browse .td-browse-slot {
        flex-basis: calc(100% - var(--td-browse-right-w, 480px));
      }
      .td-root.is-browse .td-browse-slot:has(> .td-browse.is-closing) {
        flex-basis: 0px;
        /* 收起时长与 JS 的 240ms 定时器对齐：收拢到位的同一刻才摘 is-browse，
           左侧内容不会先消失、留出一段空档再「啪」地回来。 */
        transition-duration: 240ms;
      }
      .td-root.is-col-dragging .td-browse-slot { transition: none; }
      @media (prefers-reduced-motion: reduce) {
        .td-browse-slot { transition: none; }
      }'''

# =====================================================================================
# 需求 4a · avatar main 内容自适应
# =====================================================================================
Q_OLD = u'''  @container (max-width: 560px) {
    .av-main-head { flex-wrap: wrap; }
    .av-main-head-actions { position: static; width: 100%; }
  }'''

Q_NEW = u'''  /* ★ 第 71 轮第 4 项：main 内容自适应（AI 会话栏 + 文件预览栏双开时 main 被挤到 ~300px）。
     用 container 查询（.av-main 已声明 container-type: inline-size）而非 @media ——
     main 的可用宽由两根侧栏决定，与视口宽无关。
     ≤560：头部换行 + 头像缩小 + 卡片改单列 + 行卡改自适应高（= r36 已定的 560 阈值，继续沿用）。
     ≤300：极端窄，头像再收一档，避免头像把文字挤到不可读。 */
  @container (max-width: 560px) {
    .av-main-head { flex-wrap: wrap; }
    .av-main-head-actions { position: static; width: 100%; flex-wrap: wrap; }
    .av-main-avatar { width: 72px; height: 72px; }
    .av-main-avatar-face { font-size: 28px; }
    .av-main-head { gap: 12px; }
    .av-main-grid { grid-template-columns: minmax(0, 1fr); }
    .av-main-rows { gap: 12px; margin-top: 12px; }
    .av-row { height: auto; min-height: 118px; }
    .av-row-head { flex-wrap: wrap; }
    .av-main-foot { width: auto; max-width: 240px; }
  }
  @container (max-width: 420px) {
    .av-card .giencoder-card-header { padding: 6px 14px; }
    .av-card .giencoder-card-body { padding: 14px 14px 12px; }
    .av-row { padding: 14px; }
  }
  @container (max-width: 300px) {
    .av-main-avatar { width: 56px; height: 56px; }
    .av-main-avatar-face { font-size: 22px; }
    .av-main-grid { gap: 12px; }
  }'''

# =====================================================================================
# 需求 4b · avatar 预览栏让位（控制器常量）
# =====================================================================================
C_OLD = u'''  var DEF_PANEL = 641, MIN_PANEL = 641, MAIN_MIN = 240;
  var DEF_TREE = 296, MIN_TREE = 240, MIN_CODE = 320;'''
C_NEW = u'''  /* ★ 第 71 轮第 4 项：预览栏不再死守 641px —— 空间不够时先让预览栏，直到 main 拿到 MAIN_MIN。
     默认宽仍是 641；MIN_PANEL 由 641 修正为 561 = 文件树 MIN_TREE(240) + 分栏条 1 + 代码区 MIN_CODE(320)
     —— 原来的 641 与「内部两栏最小宽之和」本来就自相矛盾，等于把面板钉死在默认值上。
     MAIN_MIN 240 → 380：main 重排后的舒适下限（配合 @container 单列布局）。 */
  var DEF_PANEL = 641, MIN_PANEL = 561, MAIN_MIN = 380;
  var DEF_TREE = 296, MIN_TREE = 240, MIN_CODE = 320;'''

# ---- 严格守卫：以下载荷都插进既有 <style> 块内部，任何标签都不许出现 ----
for _lb, _pl in ((u'权限弹层', P_PERM_NEW), (u'技能浮窗', P_SKILL_NEW), (u'更多操作', P_MORE_NEW),
                 (u'数字分身浮窗', P_DP_NEW), (u'预览栏动效', ANIM_NEW),
                 (u'main 容器查询', Q_NEW), (u'让位常量', C_NEW)):
    guard(_lb, _pl)

# =====================================================================================
store = {}

apply_job(store, 'base.html', [
    (u'液态玻璃按钮',
     re.compile(r'id="r71-glass-css"'),
     u'<!-- /DOT-SPOT -->\n</body>',
     u'<!-- /DOT-SPOT -->\n' + GLASS + u'\n</body>',
     1),
    (u'权限选择弹层 12px→8px',
     re.compile(r'zIndex:1e3,borderRadius:`8px`'),
     P_PERM_OLD, P_PERM_NEW, 1),
], {'<style': 1, '</style>': 1, '<script': 0, '</script>': 0})

apply_job(store, 'avatar.html', [
    (u'技能选择浮窗 12px→8px',
     re.compile(r'border-radius: 8px; border: 1px solid var\(--color-border-2\);'),
     P_SKILL_OLD, P_SKILL_NEW, 1),
    (u'main 响应式容器查询',
     re.compile(r'@container \(max-width: 300px\)'),
     Q_OLD, Q_NEW, 1),
    (u'预览栏让位常量',
     re.compile(r'MIN_PANEL = 561'),
     C_OLD, C_NEW, 1),
], {'<style': 0, '</style>': 0, '<script': 0, '</script>': 0})

apply_job(store, 'task-detail.html', [
    (u'预览栏动效同步',
     re.compile(r'--td-browse-ease'),
     ANIM_OLD, ANIM_NEW, 1),
    (u'技能选择浮窗 12px→8px',
     re.compile(r'border-radius: 8px; border: 1px solid var\(--color-border-2\);'),
     P_SKILL_OLD, P_SKILL_NEW, 1),
    (u'更多操作菜单 5px→8px',
     re.compile(r'width: 130px; padding: 4px;[\s\S]{0,320}?border-radius: 8px;'),
     P_MORE_OLD, P_MORE_NEW, 1),
    (u'数字分身选择浮窗 6px→8px',
     re.compile(r'\.td-dp\.giencoder-popover \{ width: 320px; border-radius: 8px; \}'),
     P_DP_OLD, P_DP_NEW, 1),
], {'<style': 0, '</style>': 0, '<script': 0, '</script>': 0})


# =====================================================================================
# 自检
# =====================================================================================
for page, (applied, skipped) in store.items():
    s = load(page)
    print('=== %s ===  应用: %d 项 | 跳过: %d 项' % (page, len(applied), len(skipped)))
    for a in applied:
        print('   + ' + a)
    for k in skipped:
        print('   = ' + k)

b = load('base.html')
a = load('avatar.html')
t = load('task-detail.html')
checks = [
    ('base: 玻璃样式块唯一', b.count('id="r71-glass-css"') == 1),
    ('base: 权限弹层 12px 清零', b.count('borderRadius:`12px`') == 0),
    ('base: 权限弹层 8px 唯一', b.count('borderRadius:`8px`') == 1),
    ('base: 玻璃块排在共享 style 之后', b.find('id="r71-glass-css"') > b.find('/* 技能选择浮窗 */')),
    ('avatar: --border-radius-xl 清零', a.count('var(--border-radius-xl)') == 0),
    ('avatar: 三种容器查询齐备',
     all(k in a for k in ('@container (max-width: 560px)', '@container (max-width: 420px)', '@container (max-width: 300px)'))),
    ('avatar: 560 查询唯一', a.count('@container (max-width: 560px)') == 1),
    ('avatar: MIN_PANEL=561', a.count('MIN_PANEL = 561') == 1),
    ('avatar: MAIN_MIN=380', a.count('MAIN_MIN = 380') == 1),
    ('detail: 旧位移动画清零', ('tdBrowseIn' not in t) and ('tdBrowseOut' not in t)),
    ('detail: 新动效标记齐备', t.count('--td-browse-ease') == 2),
    ('detail: slot 可缩不可伸', t.count('flex: 0 1 0px; min-width: 0; overflow: hidden;') == 1),
    ('detail: 收起触发 :has 规则唯一', t.count(':has(> .td-browse.is-closing)') == 1),
    ('detail: --border-radius-xl 清零', t.count('var(--border-radius-xl)') == 0),
    ('detail: 5px 圆角清零', t.count('border-radius: 5px') == 0),
    ('detail: td-dp 圆角 8px', t.count('.td-dp.giencoder-popover { width: 320px; border-radius: 8px; }') == 1),
    ('detail: is-closing 仍在（JS 依赖）', t.count('is-closing') >= 6),
]
bad = [k for k, ok in checks if not ok]
print()
if bad:
    for k in bad:
        print('   \u2717 ' + k)
    sys.exit('!! 自检未通过（%d 项）' % len(bad))
print('自检：%d/%d 通过' % (len(checks), len(checks)))
