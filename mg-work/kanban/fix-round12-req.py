# -*- coding: utf-8 -*-
"""round12 / req-kanban.html（需求看板 · 研发工作台）
1) 彻底移除左上角「切换工作空间」模块（消除切换页签时的闪现）
2) 智能助手悬浮球视觉升级（与任务看板保持一致）
幂等。
"""
import io, sys, re

P = r'E:\GienCoder\giencoder-design-engineering\pages\req-kanban.html'
s = io.open(P, encoding='utf-8').read()
orig = len(s)
log = []

# ---------------------------------------------------------------- 1. ws-hide
WS_CSS = """/* r12: 研发工作台不含「切换工作空间」模块 —— 外壳把它包在一个带 transition:opacity .3s 的 div 里，
   切换页签时首帧可见、随后淡出，表现为"闪现"。这里在首帧就彻底移除（display:none 不参与绘制）。
   该块的终态本就是 opacity:0 / pointer-events:none，故移除不损失任何可见功能。 */
header > div.w-60 > div:nth-child(2),
header div:has(> div.relative > button[aria-label="切换侧边栏"]) { display: none !important; }
"""
if 'r12: 研发工作台不含' in s:
    log.append('[1] ws-hide 已存在，跳过')
else:
    m = re.search(r'<style>\s*svg\.animate-spin', s)
    if not m:
        log.append('[1] !! 首个 <style> 块锚点未找到'); sys.exit(1)
    idx = s.index('</style>', m.end())
    s = s[:idx] + WS_CSS + s[idx:]
    log.append('[1] ws-hide 写入首个 <style> 块')

# ---------------------------------------------------------------- 2. FAB
FAB_START = '      /* 可拖动：按住悬浮球在页面内自由移动 */'
FAB_END = '      /* ===== giencoder DatePicker'
FAB_NEW = """      /* ===== r12: 智能助手悬浮球（视觉升级）=====
         结构：品牌渐变球体（primary → purple）+ 顶部玻璃高光 + 主题色柔光晕 + 内高光/内底缘
         交互：idle 静置发光 → hover 上浮放大 + 光晕加强 → active 回落 → dragging 收缩 */
      .kb-fab {
        cursor: grab; touch-action: none; -webkit-user-select: none; user-select: none;
        background: linear-gradient(150deg, var(--color-primary-6) 0%, rgb(var(--purple-6)) 100%);
        border: none; color: var(--color-white);
        box-shadow:
          0 6px 16px rgba(var(--giencoderblue-6), 0.38),
          0 2px 6px rgba(15, 23, 42, 0.16),
          inset 0 1px 1px rgba(255, 255, 255, 0.45),
          inset 0 -2px 6px rgba(0, 0, 0, 0.14);
        transition: transform .18s cubic-bezier(0.23, 1, 0.32, 1), box-shadow .18s ease;
      }
      .kb-fab::after {
        content: ''; position: absolute; left: 14%; top: 8%; width: 72%; height: 38%;
        border-radius: 50%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0));
        pointer-events: none;
      }
      .kb-fab svg { position: relative; z-index: 1; width: 22px; height: 22px; }
      .kb-fab:hover {
        transform: translateY(-2px) scale(1.04);
        box-shadow:
          0 10px 24px rgba(var(--giencoderblue-6), 0.46),
          0 3px 8px rgba(15, 23, 42, 0.18),
          inset 0 1px 1px rgba(255, 255, 255, 0.50),
          inset 0 -2px 6px rgba(0, 0, 0, 0.14);
      }
      .kb-fab:active { transform: translateY(0) scale(0.98); }
      .kb-fab.is-dragging { cursor: grabbing; transform: scale(0.96); }
      @media (prefers-reduced-motion: reduce) { .kb-fab { transition: none; } }
      [giencoder-theme='dark'] .kb-fab {
        border: none;
        background: linear-gradient(150deg, rgb(var(--giencoderblue-6)) 0%, rgb(var(--purple-5)) 100%);
        box-shadow:
          0 6px 16px rgba(0, 0, 0, 0.50),
          0 1px 2px rgba(0, 0, 0, 0.35),
          inset 0 1px 1px rgba(255, 255, 255, 0.28),
          inset 0 -2px 6px rgba(0, 0, 0, 0.35);
      }
      [giencoder-theme='dark'] .kb-fab::after {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0));
      }
"""
if 'r12: 智能助手悬浮球（视觉升级）' in s:
    log.append('[2] FAB 已升级，跳过')
else:
    i = s.index(FAB_START); j = s.index(FAB_END, i)
    s = s[:i] + FAB_NEW + s[j:]
    log.append('[2] FAB 视觉升级写入')

OLD_ICON = ('<svg viewBox=\\"0 0 20 20\\" fill=\\"none\\"><rect x=\\"2.5\\" y=\\"4.5\\" width=\\"13\\" height=\\"11\\" rx=\\"3\\" '
            'stroke=\\"currentColor\\" stroke-width=\\"1.3\\"/><path d=\\"M6.5 9.5v1.5M10 9.5v1.5\\" stroke=\\"currentColor\\" '
            'stroke-width=\\"1.3\\" stroke-linecap=\\"round\\"/><path d=\\"M14.5 2.5l.6 1.4 1.4.6-1.4.6-.6 1.4-.6-1.4-1.4-.6 1.4-.6.6-1.4Z\\" '
            'fill=\\"currentColor\\"/></svg>')
NEW_ICON = ('<svg viewBox=\\"0 0 20 20\\" fill=\\"none\\" aria-hidden=\\"true\\">'
            '<path d=\\"M9 4.2C9.36 7.5 12.3 10.44 15.6 10.8C12.3 11.16 9.36 14.1 9 17.4C8.64 14.1 5.7 11.16 2.4 10.8'
            'C5.7 10.44 8.64 7.5 9 4.2Z\\" fill=\\"currentColor\\"/>'
            '<path d=\\"M16.2 1.2C16.35 2.55 17.55 3.75 18.9 3.9C17.55 4.05 16.35 5.25 16.2 6.6C16.05 5.25 14.85 4.05 13.5 3.9'
            'C14.85 3.75 16.05 2.55 16.2 1.2Z\\" fill=\\"currentColor\\"/></svg>')
if 'M9 4.2C9.36 7.5' in s:
    log.append('[2b] FAB 图标已替换，跳过')
elif OLD_ICON in s:
    s = s.replace(OLD_ICON, NEW_ICON, 1)
    log.append('[2b] FAB 图标替换为 AI 四角星')
else:
    log.append('[2b] !! FAB 图标锚点未找到（继续）')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
for l in log:
    print(l)
print('DONE  %d -> %d chars' % (orig, len(s)))
