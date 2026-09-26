# -*- coding: utf-8 -*-
"""
第 8 轮修复
 1. req-kanban：表格容器溢出 main，改为在 main 内自适应
 2. kb-proj-select 与 kb-radio 间距自适应（跟随选择器宽度，固定 8px 间隙）
 3. awd-card-frame hover 时边框不再变化
 4. 运行中的虚线边框更细密
 5. 转派/执行按钮：各自泳道内每张卡 hover 都显示，统一 32px 高
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, 'pages')
BAK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_bak8')
Q = chr(92) + '"'
os.makedirs(BAK, exist_ok=True)
log = []


def rep(s, old, new, tag):
    if old not in s:
        log.append('MISS  ' + tag)
        return s
    n = s.count(old)
    log.append('OK    %s (x%d)' % (tag, n))
    return s.replace(old, new)


# ============ 1) 表格容器自适应收进 main ============
# .giencoder-table{width:100%} + .rq-table{margin:15px 20px 0} => 100%+40px 溢出
OLD_RQ_TABLE = """      .rq-table {
        flex: 1; min-height: 0; display: flex; flex-direction: column; margin: 15px 20px 0;
      }"""
NEW_RQ_TABLE = """      .rq-table {
        flex: 1; min-height: 0; display: flex; flex-direction: column; margin: 15px 20px 0;
        /* giencoder-table 自带 width:100%，叠加上 20px 左右外边距会溢出 main；改按父级内宽收缩 */
        width: calc(100% - 40px); min-width: 0;
      }"""

# ============ 2) 顶栏：radio 跟随 proj-select，间距自适应 ============
OLD_RADIO = """      .kb-radio {
        position: absolute; left: 228px; top: 8px; height: 32px;
        display: flex; align-items: center; background: var(--color-fill-1); border-radius: 6px;
      }"""
NEW_RADIO = """      .kb-radio {
        position: absolute; left: 228px; top: 8px; height: 32px;
        display: flex; align-items: center; background: var(--color-fill-1); border-radius: 6px;
      }
      /* 左偏移由 JS 按项目选择器实际宽度 + 8px 自适应（选择器宽度随项目名伸缩） */

      /* ===== 顶栏：项目选择器与看板切换的间距自适应 ===== */
"""

JS_TOPBAR = r"""  /* ===== 顶栏：kb-radio 跟随 kb-proj-select，固定 8px 间隙 ===== */
  function bindTopbar(root) {
    var sel = root.querySelector('.kb-proj-select');
    var radio = root.querySelector('.kb-radio');
    if (!sel || !radio) return;
    var GAP = 8;
    function place() {
      var host = radio.offsetParent || sel.parentElement;
      if (!host) return;
      var hr = host.getBoundingClientRect(), sr = sel.getBoundingClientRect();
      radio.style.left = Math.round(sr.right - hr.left + GAP) + 'px';
    }
    place();
    if (window.ResizeObserver) new ResizeObserver(place).observe(sel);
    else window.addEventListener('resize', place);
  }

"""

# ============ 3) awd-card-frame hover 不改边框 ============
OLD_AWD_HOVER = ".awd-card-frame:hover{border-color:var(--color-primary-6);background:var(--color-primary-light-1);}"
NEW_AWD_HOVER = ".awd-card-frame:hover{background:var(--color-primary-light-1);box-shadow:0 1px 8px rgba(0, 0, 0, 0.06);}"

OLD_AWD_BASE = "border-radius:12px;background:var(--color-bg-1);cursor:pointer;transition:border-color .15s, background .15s;}"
NEW_AWD_BASE = "border-radius:12px;background:var(--color-bg-1);cursor:pointer;transition:background .15s, box-shadow .15s;}"

# ============ 4) 虚线更细密 ============
OLD_DASH_CSS = """      .kb-card-dash rect {
        fill: none; stroke: var(--color-warning-6); stroke-width: 1.6;
        stroke-linecap: round; stroke-dasharray: 7 6; animation: kb-dash-run .7s linear infinite;
      }"""
NEW_DASH_CSS = """      .kb-card-dash rect {
        fill: none; stroke: var(--color-warning-6); stroke-width: 1.2;
        stroke-linecap: round; stroke-dasharray: 4 3; animation: kb-dash-run .7s linear infinite;
      }"""

OLD_DASH_KEY = "      @keyframes kb-dash-run { to { stroke-dashoffset: -26px; } }"
NEW_DASH_KEY = "      @keyframes kb-dash-run { to { stroke-dashoffset: -14px; } }"

OLD_DASH_JS = """        /* 描边 1.6px：内缩半个线宽，圆角同步减半，保证描边完整落在卡片内 */
        rect.setAttribute('x', '0.8');
        rect.setAttribute('y', '0.8');
        rect.setAttribute('width', String(Math.max(0, w - 1.6)));
        rect.setAttribute('height', String(Math.max(0, h - 1.6)));
        rect.setAttribute('rx', '7.2');
        rect.setAttribute('ry', '7.2');"""
NEW_DASH_JS = """        /* 描边 1.2px：内缩半个线宽，圆角同步减半，保证描边完整落在卡片内 */
        rect.setAttribute('x', '0.6');
        rect.setAttribute('y', '0.6');
        rect.setAttribute('width', String(Math.max(0, w - 1.2)));
        rect.setAttribute('height', String(Math.max(0, h - 1.2)));
        rect.setAttribute('rx', '7.4');
        rect.setAttribute('ry', '7.4');"""

# ============ 5) 转派 / 执行按钮：32px，各自泳道每张卡 hover 显示 ============
OLD_EXEC = """      /* 执行：常规主按钮（primary），卡片 hover 时才出现 */
      .kb-btn-exec {
        margin-left: auto; display: inline-flex; align-items: center; justify-content: center;
        height: 24px; padding: 0 12px; border: none; border-radius: 6px;
        background: var(--color-primary-6); color: var(--color-white);
        font-size: 12px; font-weight: 500; line-height: 18px; cursor: pointer;
        opacity: 0; visibility: hidden;
        transition: opacity .15s, visibility .15s, background .15s;
      }"""
NEW_EXEC = """      /* 执行：常规主按钮（primary），进行中泳道每张卡 hover 时出现，32px 高。
         绝对定位在卡尾右侧，不参与布局，hover 零尺寸影响 */
      .kb-btn-exec {
        position: absolute; right: 12px; bottom: 12px; z-index: 1;
        display: inline-flex; align-items: center; justify-content: center;
        height: 32px; padding: 0 16px; border: none; border-radius: 6px;
        background: var(--color-primary-6); color: var(--color-white);
        font-size: 12px; font-weight: 500; line-height: 18px; cursor: pointer;
        opacity: 0; visibility: hidden;
        transition: opacity .15s, visibility .15s, background .15s;
      }"""

OLD_ASSIGN = """      /* 转派：次要按钮。绝对定位在卡尾右侧，不参与布局，hover 时零尺寸影响 */
      .kb-btn-assign {
        position: absolute; right: 12px; bottom: 11px; z-index: 1;
        display: inline-flex; align-items: center; justify-content: center;
        height: 20px; padding: 0 8px; border: 1px solid var(--color-border-2); border-radius: 6px;"""
NEW_ASSIGN = """      /* 转派：次要按钮。待开始泳道每张卡 hover 时出现，32px 高。
         绝对定位在卡尾右侧，不参与布局，hover 零尺寸影响 */
      .kb-btn-assign {
        position: absolute; right: 12px; bottom: 12px; z-index: 1;
        display: inline-flex; align-items: center; justify-content: center;
        height: 32px; padding: 0 12px; border: 1px solid var(--color-border-2); border-radius: 6px;"""

# 进行中泳道 hover 时让位给「执行」按钮（原状态标签淡出）
OLD_STATUS_HIDE = "      .kb-running { margin-left: auto; display: flex; align-items: center; gap"
NEW_STATUS_HIDE = """      /* 进行中泳道：hover 时状态标签淡出，让位给「执行」按钮（避免重叠） */
      .kb-btn-confirm, .kb-running, .kb-card-foot .kb-sp { transition: opacity .15s; }
      .kb-col--doing .kb-card:hover .kb-btn-confirm,
      .kb-col--doing .kb-card:hover .kb-running,
      .kb-col--doing .kb-card:hover .kb-card-foot .kb-sp { opacity: 0; }
      .kb-running { margin-left: auto; display: flex; align-items: center; gap"""

OLD_EXEC_BTN = '<button type=' + Q + 'button' + Q + ' class=' + Q + 'kb-btn-exec' + Q + '>执行</button>'
VAL_SPAN = '<span class=' + Q + 'kb-val' + Q + '>2026/08/31</span>'


def process(fname, kanban_only):
    p = os.path.join(PAGES, fname)
    s = open(p, encoding='utf-8').read()
    orig = s
    shutil.copy2(p, os.path.join(BAK, fname))

    # 2) 顶栏间距自适应（两个页面）
    s = rep(s, OLD_RADIO, NEW_RADIO, fname + ' : kb-radio 注释') or s
    if 'function bindTopbar(root)' not in s:
        anchor = '  function inject() {'
        if anchor in s:
            s = s.replace(anchor, JS_TOPBAR + anchor, 1)
            log.append('OK    %s : 注入 bindTopbar' % fname)
        else:
            log.append('MISS  %s : inject 锚点' % fname)
    if 'bindTopbar(wrap);' not in s:
        s = rep(s, '    bindFab(wrap);',
                '    bindFab(wrap);\n    bindTopbar(wrap);',
                fname + ' : inject 内调用 bindTopbar') or s

    if fname == 'req-kanban.html':
        s = rep(s, OLD_RQ_TABLE, NEW_RQ_TABLE, fname + ' : 表格容器收进 main') or s

    if fname == 'dev.html':
        s = rep(s, OLD_AWD_HOVER, NEW_AWD_HOVER, fname + ' : frame hover 不改边框') or s
        s = rep(s, OLD_AWD_BASE, NEW_AWD_BASE, fname + ' : frame transition 去掉 border-color') or s

    if kanban_only:
        s = rep(s, OLD_DASH_CSS, NEW_DASH_CSS, fname + ' : 虚线 1.2px / 4 3') or s
        s = rep(s, OLD_DASH_KEY, NEW_DASH_KEY, fname + ' : dash 周期 -14') or s
        s = rep(s, OLD_DASH_JS, NEW_DASH_JS, fname + ' : rect 内缩 0.6') or s
        s = rep(s, OLD_EXEC, NEW_EXEC, fname + ' : 执行按钮 32px 绝对定位') or s
        s = rep(s, OLD_ASSIGN, NEW_ASSIGN, fname + ' : 转派按钮 32px') or s
        s = rep(s, OLD_STATUS_HIDE, NEW_STATUS_HIDE, fname + ' : hover 让位给执行') or s

        # 进行中泳道：每张卡都补一个「执行」
        a = s.find('kb-col kb-col--doing')
        b = s.find('kb-col kb-col--stop')
        if a > 0 and b > a:
            seg = s[a:b]
            seg = seg.replace(OLD_EXEC_BTN, '')                      # 去掉已有的那个，统一重建
            cnt = seg.count(VAL_SPAN)
            seg = seg.replace(VAL_SPAN, VAL_SPAN + OLD_EXEC_BTN)
            s = s[:a] + seg + s[b:]
            log.append('OK    %s : 进行中泳道补执行按钮 (x%d)' % (fname, cnt))
        else:
            log.append('MISS  %s : 进行中泳道定位' % fname)

    if s != orig:
        open(p, 'w', encoding='utf-8', newline='').write(s)
        log.append('WRITE ' + fname)
    return s


process('kanban.html', True)
process('req-kanban.html', False)
process('dev.html', False)
print('\n'.join(log))
