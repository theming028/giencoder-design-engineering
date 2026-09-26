# -*- coding: utf-8 -*-
"""
第 7 轮修复
 1. kb-fab 智能助手按钮改用 iOS Liquid Glass（液态玻璃）CSS 效果
 2. kb-proj-select 容器宽度自适应内容
 3. kb-card.is-dashed 虚线描边加粗到 1.6px
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, 'pages')
BAK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_bak7')
Q = chr(92) + '"'          # 文件里 JS 字符串中的转义双引号
os.makedirs(BAK, exist_ok=True)
log = []


def rep(s, old, new, tag):
    if old not in s:
        log.append('MISS  ' + tag)
        return s
    n = s.count(old)
    log.append('OK    %s (x%d)' % (tag, n))
    return s.replace(old, new)


# ============ 1) Liquid Glass ============
# 原（上一轮加的拖动样式）
OLD_FAB_DRAG = """      .kb-fab { cursor: grab; touch-action: none; -webkit-user-select: none; user-select: none; }
      .kb-fab.is-dragging { cursor: grabbing; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18); }
"""
NEW_FAB_GLASS = """      /* ===== Liquid Glass（iOS 液态玻璃）=====
         结构：半透明渐变底 + backdrop blur/saturate + 1px 玻璃描边
               + 外投影 + 内高光/内底缘 + ::before 折射亮环 + ::after 顶部镜面高光 */
      .kb-fab {
        cursor: grab; touch-action: none; -webkit-user-select: none; user-select: none;
        background:
          linear-gradient(135deg,
            rgba(255, 255, 255, 0.70) 0%,
            rgba(255, 255, 255, 0.32) 46%,
            rgba(255, 255, 255, 0.48) 100%);
        -webkit-backdrop-filter: blur(18px) saturate(190%) brightness(1.08);
        backdrop-filter: blur(18px) saturate(190%) brightness(1.08);
        border: 1px solid rgba(255, 255, 255, 0.60);
        box-shadow:
          0 8px 24px rgba(15, 23, 42, 0.14),
          0 1px 2px rgba(15, 23, 42, 0.06),
          inset 0 1px 1px rgba(255, 255, 255, 0.90),
          inset 0 -1px 1px rgba(255, 255, 255, 0.38);
        transition: box-shadow .18s, -webkit-backdrop-filter .18s, backdrop-filter .18s, transform .18s;
      }
      /* 玻璃边缘折射亮环：用 mask 抠出 1px 环，只保留左上/右下两段高光 */
      .kb-fab::before {
        content: ''; position: absolute; inset: 0; border-radius: 50%; padding: 1px;
        pointer-events: none; box-sizing: border-box;
        background: linear-gradient(140deg,
          rgba(255, 255, 255, 0.95) 0%,
          rgba(255, 255, 255, 0) 38%,
          rgba(255, 255, 255, 0) 62%,
          rgba(255, 255, 255, 0.60) 100%);
        -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
        -webkit-mask-composite: xor;
        mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
        mask-composite: exclude;
      }
      /* 顶部镜面高光 */
      .kb-fab::after {
        content: ''; position: absolute; left: 10%; top: 7%; width: 80%; height: 44%;
        border-radius: 50% 50% 42% 42% / 72% 72% 28% 28%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.70), rgba(255, 255, 255, 0));
        pointer-events: none;
      }
      .kb-fab svg { position: relative; z-index: 1; }
      .kb-fab:hover { transform: translateY(-1px); }
      .kb-fab:active { transform: translateY(0); }
      .kb-fab.is-dragging {
        cursor: grabbing;
        box-shadow:
          0 14px 32px rgba(15, 23, 42, 0.20),
          0 2px 6px rgba(15, 23, 42, 0.10),
          inset 0 1px 1px rgba(255, 255, 255, 0.90),
          inset 0 -1px 1px rgba(255, 255, 255, 0.38);
      }
      /* 深色主题下的玻璃：改为暗色半透明 + 弱高光 */
      [giencoder-theme='dark'] .kb-fab {
        background:
          linear-gradient(135deg,
            rgba(255, 255, 255, 0.18) 0%,
            rgba(255, 255, 255, 0.06) 46%,
            rgba(255, 255, 255, 0.11) 100%);
        border-color: rgba(255, 255, 255, 0.20);
        box-shadow:
          0 8px 24px rgba(0, 0, 0, 0.45),
          0 1px 2px rgba(0, 0, 0, 0.30),
          inset 0 1px 1px rgba(255, 255, 255, 0.22),
          inset 0 -1px 1px rgba(255, 255, 255, 0.06);
      }
      [giencoder-theme='dark'] .kb-fab::after {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.20), rgba(255, 255, 255, 0));
      }
"""

# ============ 2) 项目选择器宽度自适应 ============
OLD_PROJ_W = "      .kb-proj-select { position: absolute; left: 20px; top: 8px; width: 200px; }"
NEW_PROJ_W = """      /* 宽度自适应内容：随选中的项目文件夹名称伸缩 */
      .kb-proj-select { position: absolute; left: 20px; top: 8px; width: max-content; min-width: 140px; max-width: 360px; }"""

OLD_PROJ_POPUP = "      .kb-proj-select .giencoder-select-popup { width: 200px; min-width: 200px; }\n"
NEW_PROJ_POPUP = """      .kb-proj-select .giencoder-select-popup { width: max-content; min-width: 100%; }
      .kb-proj-select .giencoder-select-view-text { flex: 0 1 auto; }
"""

OLD_INLINE_W = ' kb-proj-select' + Q + ' data-component'
NEW_INLINE_W = ' kb-proj-select' + Q + ' data-component'
# 内联 style 里的 width:200px 需去掉（在 HTML 字符串中）
OLD_INLINE_STYLE = 'position:absolute; left:20px; top:8px; width:200px;'
NEW_INLINE_STYLE = 'position:absolute; left:20px; top:8px;'

# ============ 3) 虚线 1.6px ============
OLD_DASH_CSS = """      .kb-card-dash rect {
        fill: none; stroke: var(--color-warning-6); stroke-width: 1;
        stroke-dasharray: 6 5; animation: kb-dash-run .7s linear infinite;
      }"""
NEW_DASH_CSS = """      .kb-card-dash rect {
        fill: none; stroke: var(--color-warning-6); stroke-width: 1.6;
        stroke-linecap: round; stroke-dasharray: 7 6; animation: kb-dash-run .7s linear infinite;
      }"""

OLD_DASH_JS = """        rect.setAttribute('x', '0.5');
        rect.setAttribute('y', '0.5');
        rect.setAttribute('width', String(Math.max(0, w - 1)));
        rect.setAttribute('height', String(Math.max(0, h - 1)));
        rect.setAttribute('rx', '7.5');
        rect.setAttribute('ry', '7.5');"""
NEW_DASH_JS = """        /* 描边 1.6px：内缩半个线宽，圆角同步减半，保证描边完整落在卡片内 */
        rect.setAttribute('x', '0.8');
        rect.setAttribute('y', '0.8');
        rect.setAttribute('width', String(Math.max(0, w - 1.6)));
        rect.setAttribute('height', String(Math.max(0, h - 1.6)));
        rect.setAttribute('rx', '7.2');
        rect.setAttribute('ry', '7.2');"""

OLD_DASH_KEY = "      @keyframes kb-dash-run { to { stroke-dashoffset: -22px; } }"
NEW_DASH_KEY = "      @keyframes kb-dash-run { to { stroke-dashoffset: -26px; } }"


def process(fname, kanban_only):
    p = os.path.join(PAGES, fname)
    s = open(p, encoding='utf-8').read()
    orig = s
    shutil.copy2(p, os.path.join(BAK, fname))

    s = rep(s, OLD_FAB_DRAG, NEW_FAB_GLASS, fname + ' : fab Liquid Glass') or s
    s = rep(s, OLD_PROJ_W, NEW_PROJ_W, fname + ' : proj 宽度自适应') or s
    s = rep(s, OLD_PROJ_POPUP, NEW_PROJ_POPUP, fname + ' : popup 宽度跟随') or s
    s = rep(s, OLD_INLINE_STYLE, NEW_INLINE_STYLE, fname + ' : 去掉内联定宽') or s

    if kanban_only:
        s = rep(s, OLD_DASH_CSS, NEW_DASH_CSS, fname + ' : 虚线 1.6px') or s
        s = rep(s, OLD_DASH_KEY, NEW_DASH_KEY, fname + ' : dash 周期同步') or s
        s = rep(s, OLD_DASH_JS, NEW_DASH_JS, fname + ' : rect 内缩 0.8') or s

    if s != orig:
        open(p, 'w', encoding='utf-8', newline='').write(s)
        log.append('WRITE ' + fname)
    return s


process('kanban.html', True)
process('req-kanban.html', False)
print('\n'.join(log))
