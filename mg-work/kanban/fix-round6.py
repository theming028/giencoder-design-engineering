# -*- coding: utf-8 -*-
"""
第 6 轮修复（任务看板 / 需求看板公共外壳）
 1. kb-fab 智能助手悬浮球支持按住拖动
 2. kb-stat（任务看板）hover 不改边框色，只加投影
 3. 进行中泳道 kb-card.is-dashed 虚线边框持续流动
 4. kb-btn-exec 卡片 hover 才显示，且为常规主按钮
 5. 待开始泳道卡片 hover 显示「转派」次要按钮
 6. 所有卡片默认无边框，hover 才显示（预留 1px 透明边框，不抖动）
 7. kb-search → 重命名为项目文件夹选择器（kb-proj-select），实现为下拉菜单
"""
import re, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, 'pages')
BAK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_bak6')

# 文件中 JS 字符串里的转义双引号：反斜杠 + 引号 两个字符
Q = chr(92) + '"'
QRE = re.escape(Q)

os.makedirs(BAK, exist_ok=True)
log = []


def rep(s, old, new, tag):
    """幂等替换：命中返回新串，未命中返回 None"""
    if old not in s:
        log.append('MISS  ' + tag)
        return None
    n = s.count(old)
    log.append('OK    %s (x%d)' % (tag, n))
    return s.replace(old, new)


def rep1(s, old, new, tag):
    """只替换第一处"""
    if old not in s:
        log.append('MISS  ' + tag)
        return None
    log.append('OK    ' + tag)
    return s.replace(old, new, 1)


# ============ 公共 CSS：kb-search -> kb-proj-select ============
OLD_SEARCH_CSS = """      .kb-search {
        position: absolute; left: 20px; top: 8px; width: 200px; height: 32px;
        background: var(--color-fill-1); border-radius: 8px;
      }
      .kb-search-ico { position: absolute; left: 12px; top: 8px; width: 16px; height: 16px; line-height: 0; }
      .kb-search-txt {
        position: absolute; left: 36px; top: 5px; color: var(--color-text-1);
        font-size: 14px; font-weight: 500; line-height: 22px; white-space: nowrap;
      }
      .kb-search-arw { position: absolute; left: 180px; top: 10px; width: 12px; height: 12px; color: var(--color-neutral-7); line-height: 0; }
"""

NEW_PROJ_CSS = """      /* 项目文件夹选择器：原 kb-search 命名与"搜索"无关，实为下拉选择项目文件夹 */
      .kb-proj-select { position: absolute; left: 20px; top: 8px; width: 200px; }
      .kb-proj-select .giencoder-select-view {
        height: 32px; min-height: 32px; padding: 0 12px; border-radius: 8px;
        background: var(--color-fill-1); border-color: transparent; box-shadow: none;
      }
      .kb-proj-select .giencoder-select-view:hover { background: var(--color-fill-2); box-shadow: none; }
      .kb-proj-select .giencoder-select-view[aria-expanded='true'] {
        background: var(--color-fill-1); border-color: var(--color-primary-6); box-shadow: none;
      }
      .kb-proj-select .kb-proj-ico { width: 16px; height: 16px; line-height: 0; flex: none; }
      .kb-proj-select .kb-proj-ico svg { width: 16px; height: 16px; display: block; }
      .kb-proj-select .giencoder-select-view-text {
        margin-left: 8px; font-size: 14px; font-weight: 500; line-height: 22px;
      }
      .kb-proj-select .giencoder-select-suffix { color: var(--color-neutral-7); }
      .kb-proj-select .giencoder-select-popup { width: 200px; min-width: 200px; }
"""

# ============ 公共 CSS：kb-fab 可拖动 ============
OLD_FAB_CSS = "      .kb-fab svg { width: 20px; height: 20px; line-height: 0; }\n"
NEW_FAB_CSS = OLD_FAB_CSS + """      /* 可拖动：按住悬浮球在页面内自由移动 */
      .kb-fab { cursor: grab; touch-action: none; -webkit-user-select: none; user-select: none; }
      .kb-fab.is-dragging { cursor: grabbing; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18); }
"""

# ============ 任务看板 CSS ============
OLD_STAT = """      .kb-stat {
        position: relative; flex: 1; min-width: 0; height: 64px;
        background: var(--color-bg-1); border: 1px solid var(--color-border-2);
        border-radius: 8px; cursor: pointer;
      }"""
NEW_STAT = """      .kb-stat {
        position: relative; flex: 1; min-width: 0; height: 64px;
        background: var(--color-bg-1); border: 1px solid var(--color-border-2);
        border-radius: 8px; cursor: pointer;
        transition: box-shadow .15s;
      }"""

OLD_STAT_HOVER = "      .kb-stat:hover { border-color: var(--color-border-3); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }"
NEW_STAT_HOVER = """      /* hover 只显示投影，边框颜色保持不变 */
      .kb-stat:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }"""

OLD_CARD = """      .kb-card {
        flex: none; background: var(--color-bg-1); border: 1px solid var(--color-border-2);
        border-radius: 8px; padding: 12px; cursor: pointer;
      }"""
NEW_CARD = """      .kb-card {
        flex: none; position: relative; background: var(--color-bg-1);
        /* 1px 边框常驻但透明：hover 仅换色，不产生位移/抖动 */
        border: 1px solid transparent;
        border-radius: 8px; padding: 12px; cursor: pointer;
        transition: border-color .15s, box-shadow .15s;
      }
      .kb-card:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }"""

OLD_DASHED = "      .kb-card.is-dashed { border-style: dashed; border-color: var(--color-warning-6); }"
NEW_DASHED = """      /* 待介入状态：橙色虚线常驻并持续流动（SVG 描边，圆角与卡片一致） */
      .kb-card.is-dashed { border-color: transparent; }
      .kb-card.is-dashed:hover { border-color: transparent; }
      .kb-card-dash { position: absolute; left: 0; top: 0; pointer-events: none; overflow: visible; }
      .kb-card-dash rect {
        fill: none; stroke: var(--color-warning-6); stroke-width: 1;
        stroke-dasharray: 6 5; animation: kb-dash-run .7s linear infinite;
      }
      @keyframes kb-dash-run { to { stroke-dashoffset: -22px; } }"""

OLD_EXEC = """      .kb-btn-exec {
        margin-left: auto; padding: 2px 16px; background: var(--kb-exec-bg); border-radius: 6px;
        color: var(--kb-exec-tx); font-size: 12px; font-weight: 500; line-height: 18px;
      }"""
NEW_EXEC = """      /* 执行：常规主按钮（primary），卡片 hover 时才出现 */
      .kb-btn-exec {
        margin-left: auto; display: inline-flex; align-items: center; justify-content: center;
        height: 24px; padding: 0 12px; border: none; border-radius: 6px;
        background: var(--color-primary-6); color: var(--color-white);
        font-size: 12px; font-weight: 500; line-height: 18px; cursor: pointer;
        opacity: 0; visibility: hidden;
        transition: opacity .15s, visibility .15s, background .15s;
      }
      .kb-card:hover .kb-btn-exec, .kb-card:focus-within .kb-btn-exec { opacity: 1; visibility: visible; }
      .kb-btn-exec:hover { background: var(--color-primary-5); }
      .kb-btn-exec:active { background: var(--color-primary-7); }
      /* 转派：次要按钮（secondary），卡片 hover 时才出现 */
      .kb-btn-assign {
        margin-left: auto; display: inline-flex; align-items: center; justify-content: center;
        height: 24px; padding: 0 12px; border: 1px solid var(--color-border-2); border-radius: 6px;
        background: var(--color-bg-5); color: var(--color-text-1);
        font-size: 12px; font-weight: 400; line-height: 18px; cursor: pointer;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        opacity: 0; visibility: hidden;
        transition: opacity .15s, visibility .15s, background .15s, border-color .15s;
      }
      .kb-card:hover .kb-btn-assign, .kb-card:focus-within .kb-btn-assign { opacity: 1; visibility: visible; }
      .kb-btn-assign:hover { background: var(--color-fill-1); border-color: var(--color-border-3); }
      .kb-btn-assign:active { background: var(--color-bg-5); }"""

# ============ 公共 JS ============
JS_FAB = r"""  /* ===== 智能助手悬浮球：按住可拖动 ===== */
  function bindFab(root) {
    var fab = root.querySelector('.kb-fab');
    if (!fab || fab._dragBound) return;
    fab._dragBound = true;
    var panel = fab.closest ? fab.closest('.kb-panel') : null;
    if (!panel) panel = fab.parentElement;
    var dragging = false, moved = false, sx = 0, sy = 0, ox = 0, oy = 0;

    /* right/bottom 定位换算成 left/top，便于自由拖动 */
    function toLeftTop() {
      if (fab.style.left) return;
      var pr = panel.getBoundingClientRect(), fr = fab.getBoundingClientRect();
      fab.style.left = (fr.left - pr.left) + 'px';
      fab.style.top = (fr.top - pr.top) + 'px';
      fab.style.right = 'auto';
      fab.style.bottom = 'auto';
    }
    function bounds() {
      return { x: Math.max(0, panel.clientWidth - fab.offsetWidth),
               y: Math.max(0, panel.clientHeight - fab.offsetHeight) };
    }
    function clamp(v, max) { return v < 0 ? 0 : (v > max ? max : v); }

    fab.addEventListener('pointerdown', function (ev) {
      if (ev.button !== 0) return;
      toLeftTop();
      dragging = true; moved = false;
      sx = ev.clientX; sy = ev.clientY;
      ox = parseFloat(fab.style.left) || 0;
      oy = parseFloat(fab.style.top) || 0;
      fab.classList.add('is-dragging');
      try { fab.setPointerCapture(ev.pointerId); } catch (e) {}
      ev.preventDefault();
    });
    fab.addEventListener('pointermove', function (ev) {
      if (!dragging) return;
      var dx = ev.clientX - sx, dy = ev.clientY - sy;
      if (!moved && Math.abs(dx) + Math.abs(dy) < 3) return;
      moved = true;
      var b = bounds();
      fab.style.left = clamp(ox + dx, b.x) + 'px';
      fab.style.top = clamp(oy + dy, b.y) + 'px';
    });
    function endDrag(ev) {
      if (!dragging) return;
      dragging = false;
      fab.classList.remove('is-dragging');
      try { fab.releasePointerCapture(ev.pointerId); } catch (e) {}
    }
    fab.addEventListener('pointerup', endDrag);
    fab.addEventListener('pointercancel', endDrag);
    /* 拖动结束后紧随的 click 不应触发悬浮球点击行为 */
    fab.addEventListener('click', function (ev) {
      if (moved) { moved = false; ev.stopImmediatePropagation(); ev.preventDefault(); }
    });
  }

  /* ===== 待介入卡片：橙色虚线持续流动 ===== */
  function bindDashedCards(root) {
    var NS = 'http://www.w3.org/2000/svg';
    Array.prototype.forEach.call(root.querySelectorAll('.kb-card.is-dashed'), function (card) {
      if (card.querySelector('.kb-card-dash')) return;
      var svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('class', 'kb-card-dash');
      svg.setAttribute('aria-hidden', 'true');
      var rect = document.createElementNS(NS, 'rect');
      svg.appendChild(rect);
      card.insertBefore(svg, card.firstChild);
      function size() {
        var w = card.clientWidth, h = card.clientHeight;
        if (!w || !h) return;
        svg.setAttribute('width', w);
        svg.setAttribute('height', h);
        svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
        rect.setAttribute('x', '0.5');
        rect.setAttribute('y', '0.5');
        rect.setAttribute('width', String(Math.max(0, w - 1)));
        rect.setAttribute('height', String(Math.max(0, h - 1)));
        rect.setAttribute('rx', '7.5');
        rect.setAttribute('ry', '7.5');
      }
      size();
      if (window.ResizeObserver) new ResizeObserver(size).observe(card);
      else window.addEventListener('resize', size);
    });
  }

"""

# ============ 项目文件夹下拉（HTML 重写） ============
SEARCH_PAT = re.compile(
    '<div class=' + QRE + 'kb-search' + QRE + ' role=' + QRE + 'search' + QRE + '>", "(.*?)'
    '<span class=' + QRE + 'kb-search-ico' + QRE + '>(.*?)</span>", "(.*?)'
    '<span class=' + QRE + 'kb-search-txt' + QRE + '>(.*?)</span>", "(.*?)'
    '<span class=' + QRE + 'kb-search-arw' + QRE + '>(.*?)</span>", "(.*?)</div>',
    re.S)

PROJ_OPTIONS = ['我的坚果云', '团队共享空间', 'giencoder-design-engineering', 'yuanqi-design-vue']


def build_proj(m):
    ico = m.group(2)
    label = m.group(4)
    arrow = m.group(6)
    lis = []
    for i, name in enumerate(PROJ_OPTIONS):
        sel = ' giencoder-select-option-selected' if name == label or (i == 0 and not lis) else ''
        aria = 'true' if sel else 'false'
        lis.append(
            '<li class=' + Q + 'giencoder-select-option' + sel + Q + ' role=' + Q + 'option' + Q +
            ' aria-selected=' + Q + aria + Q + '>' + name + '</li>')
    return (
        '<div class=' + Q + 'giencoder-select kb-proj-select' + Q +
        ' data-component=' + Q + 'select' + Q + ' data-variant=' + Q + 'single' + Q +
        ' data-state=' + Q + 'default' + Q + ' data-size=' + Q + 'small' + Q +
        ' style=' + Q + 'position:absolute; left:20px; top:8px; width:200px;' + Q + '>", "'
        '<div class=' + Q + 'giencoder-select-view' + Q + ' tabindex=' + Q + '0' + Q +
        ' role=' + Q + 'combobox' + Q + ' aria-expanded=' + Q + 'false' + Q +
        ' aria-haspopup=' + Q + 'listbox' + Q + '>", "'
        '<span class=' + Q + 'kb-proj-ico' + Q + '>' + ico + '</span>", "'
        '<span class=' + Q + 'giencoder-select-view-text' + Q +
        ' data-placeholder=' + Q + '选择项目文件夹' + Q + '>' + label + '</span>", "'
        '<span class=' + Q + 'giencoder-select-suffix' + Q + '>' + arrow + '</span>", "'
        '</div>", "'
        '<div class=' + Q + 'giencoder-select-popup' + Q + ' style=' + Q + 'display:none;' + Q + '>", "'
        '<ul class=' + Q + 'giencoder-select-option-list' + Q + ' role=' + Q + 'listbox' + Q + '>", "' +
        ('", "'.join(lis)) + '", "'
        '</ul>", "'
        '</div>", "'
        '</div>'
    )


def process(fname, kanban_only):
    p = os.path.join(PAGES, fname)
    s = open(p, encoding='utf-8').read()
    orig = s
    shutil.copy2(p, os.path.join(BAK, fname))

    # 1/7 CSS
    s = rep(s, OLD_SEARCH_CSS, NEW_PROJ_CSS, fname + ' : kb-search css -> kb-proj-select css') or s
    # 1 CSS + JS
    s = rep(s, OLD_FAB_CSS, NEW_FAB_CSS, fname + ' : kb-fab drag css') or s

    if kanban_only:
        s = rep(s, OLD_STAT, NEW_STAT, fname + ' : kb-stat transition') or s
        s = rep(s, OLD_STAT_HOVER, NEW_STAT_HOVER, fname + ' : kb-stat hover 不改边框') or s
        s = rep(s, OLD_CARD, NEW_CARD, fname + ' : kb-card 透明边框 + hover') or s
        s = rep(s, OLD_DASHED, NEW_DASHED, fname + ' : is-dashed 流动虚线') or s
        s = rep(s, OLD_EXEC, NEW_EXEC, fname + ' : kb-btn-exec / kb-btn-assign') or s
        # 执行按钮 -> 真 <button>
        s = rep(s,
                '<span class=' + Q + 'kb-btn-exec' + Q + '>执行</span>',
                '<button type=' + Q + 'button' + Q + ' class=' + Q + 'kb-btn-exec' + Q + '>执行</button>',
                fname + ' : kb-btn-exec -> button') or s
        # 待开始泳道卡片加「转派」
        a = s.find('kb-col kb-col--todo')
        b = s.find('kb-col kb-col--doing')
        if a > 0 and b > a:
            seg = s[a:b]
            needle = '<span class=' + Q + 'kb-val' + Q + '>2026/08/31</span></div>'
            if needle in seg:
                cnt = seg.count(needle)
                newseg = seg.replace(
                    needle,
                    '<span class=' + Q + 'kb-val' + Q + '>2026/08/31</span>'
                    '<button type=' + Q + 'button' + Q + ' class=' + Q + 'kb-btn-assign' + Q + '>转派</button></div>')
                s = s[:a] + newseg + s[b:]
                log.append('OK    %s : 待开始泳道加转派按钮 (x%d)' % (fname, cnt))
            else:
                log.append('MISS  %s : 待开始泳道卡尾' % fname)
        else:
            log.append('MISS  %s : 待开始/进行中泳道定位' % fname)

    # 7 HTML
    s, n = SEARCH_PAT.subn(build_proj, s)
    log.append(('OK    %s : kb-search html -> select (x%d)' % (fname, n)) if n else
               ('MISS  %s : kb-search html' % fname))

    # JS
    anchor = '  function inject() {'
    if 'function bindFab(root)' not in s and anchor in s:
        s = s.replace(anchor, JS_FAB + anchor, 1)
        log.append('OK    %s : 注入 bindFab/bindDashedCards' % fname)
    else:
        log.append('SKIP  %s : bindFab 已存在或缺少 inject 锚点' % fname)
    s = rep(s, '    bindComponents(wrap);',
            '    bindComponents(wrap);\n    bindFab(wrap);\n    bindDashedCards(wrap);',
            fname + ' : inject 内调用') or s

    if s != orig:
        open(p, 'w', encoding='utf-8', newline='').write(s)
        log.append('WRITE ' + fname)
    return s


process('kanban.html', True)
process('req-kanban.html', False)

print('\n'.join(log))
