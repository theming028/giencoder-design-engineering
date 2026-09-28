# -*- coding: utf-8 -*-
"""第 49 轮：任务详情页文件预览栏（.td-browse）六项改动
   1) .td-right / .td-browse 衔接处可拖动，AI 对话框最小 400px
   2) .td-browse-tree / .td-browse-code 衔接处可拖动（树最小 240px、代码区最小 400px —— 用户只指定了前者=400 指 AI 对话框，这两项为兜底）
   3) .td-browse-crumb 补底部线条（设计稿实测 #E7EBF1）
   4) 「列表视图」按钮 → 文件目录显隐开关 + 图标还原为 list-tree
   5) 「帮助」按钮 → 在浏览器打开当前文件 + 图标还原为 compass
   6) .td-browse-files 还原为 tree（行距 34px / 缩进 20px / 3 级引导线 / folder-open·folder-closed / file-text / 激活行）
幂等：重复执行不改变文件。
"""
import re
import shutil
import sys

F = 'pages/task-detail.html'
BAK = '/tmp/r49-backup/task-detail.html'

s = open(F, encoding='utf-8').read()
orig = s
LOG = []


def rep(old, new, n=1, tag=''):
    global s
    c = s.count(old)
    if c != n:
        print('!! 锚点命中 %d 次（期望 %d）: %s ... %r' % (c, n, tag, old[:110]))
        sys.exit(1)
    s = s.replace(old, new)
    LOG.append(tag or old[:40])


# ============================================================ A. CSS
# A1 浏览栏局部色变量（设计稿实测，DS 无对应语义 token）
rep(
    '''        /* 代码语法配色：取设计稿实测值（VSCode Light 系），DS 暂无对应语义 token */
        --td-code-key: #0451A5; --td-code-str: #A31515; --td-code-num: #098658;
      }''',
    '''        /* 代码语法配色：取设计稿实测值（VSCode Light 系），DS 暂无对应语义 token */
        --td-code-key: #0451A5; --td-code-str: #A31515; --td-code-num: #098658;
        /* ★ 第 49 轮：设计稿实测色（DS 无对应语义 token）——
             激活行底 #ECF2FF / 激活行描边 #D3E2FF（节点 1350:18310 实测）、crumb 底线 #E7EBF1 */
        --td-tree-active-bg: #ECF2FF; --td-tree-active-bd: #D3E2FF;
        --td-crumb-line: #E7EBF1;
        --td-tree-guide: var(--color-border-2);   /* 引导线：设计稿实测 #E5E5E5 = border-2 */
      }''',
    tag='A1 浏览栏变量')

# A2 浏览态独立宽度变量 + 复位 row 方向
rep(
    '''      /* 第 48 轮第 2 项：会话栏与文件预览栏连成一体 —— 接缝两侧直角，中间一条发丝线 */
      .td-root.is-browse .td-right { border-top-right-radius: 0; border-bottom-right-radius: 0; }''',
    '''      /* 第 48 轮第 2 项：会话栏与文件预览栏连成一体 —— 接缝两侧直角，中间一条发丝线 */
      .td-root.is-browse .td-right { border-top-right-radius: 0; border-bottom-right-radius: 0; }
      /* ★ 第 49 轮第 1 项：浏览态用**独立**宽度变量（--td-browse-right-w），
         与 r35 普通态的 --td-right-w 完全隔离 —— 否则「折叠成 48px 窄条」的记忆会把浏览态也压扁。
         row 方向强制复位，否则 r35 的 .is-swapped(row-reverse) 会把文件预览栏翻到左边。 */
      .td-root.is-browse { flex-direction: row; }
      .td-root.is-browse .td-right { width: var(--td-browse-right-w, 480px); }''',
    tag='A2 浏览态宽度变量')

# A3 分隔条
rep(
    '''      .td-root.is-browse .td-browse { display: flex; }''',
    '''      .td-root.is-browse .td-browse { display: flex; }
      /* ★ 第 49 轮第 1/2 项：两条可拖动的分栏分隔条。
         宽 9px + margin-right:-9px ⇒ 净占位 0，绝不改变设计稿实测的两栏尺寸；
         覆盖在右邻栏的左内距上（树容器 padding 20px、代码区 padding 16px），不遮内容。 */
      .td-split {
        display: none; flex: none; position: relative; z-index: 3;
        width: 9px; margin-right: -9px; box-sizing: border-box;
        cursor: col-resize; touch-action: none;
      }
      .td-root.is-browse .td-split { display: block; }
      .td-root.is-col-dragging, .td-root.is-col-dragging * { cursor: col-resize; user-select: none; }
      .td-split::after {
        content: ''; position: absolute; top: 50%; left: -2px; width: 4px; height: 36px;
        transform: translateY(-50%); border-radius: 2px; background: transparent;
        transition: background 120ms var(--transition-timing-function-standard, ease);
      }
      .td-split:hover::after, .td-split.is-dragging::after { background: var(--color-primary-6); }
      .td-split:focus-visible { outline: 2px solid var(--color-primary-6); outline-offset: -2px; }
      /* 第 49 轮第 4 项：文件目录显隐 */
      .td-browse-body.is-no-tree .td-browse-tree,
      .td-browse-body.is-no-tree .td-split[data-td-split="tree"] { display: none; }''',
    tag='A3 分隔条')

# A4 树宽变量 + 行样式重写
rep(
    '''      .td-browse-tree {
        flex: none; width: 296px; box-sizing: border-box; padding: 20px;''',
    '''      .td-browse-tree {
        flex: none; width: var(--td-browse-tree-w, 296px); box-sizing: border-box; padding: 20px;''',
    tag='A4 树宽变量')

rep(
    '''      .td-browse-files { display: flex; flex-direction: column; }
      .td-bf {
        display: flex; align-items: center; gap: 6px; height: 22px; box-sizing: border-box;
        padding-right: 8px; padding-left: calc(8px + var(--d, 0) * 20px);
        font-size: var(--font-size-body-3); color: var(--color-text-1);
        white-space: nowrap; overflow: hidden;
      }
      .td-bf > svg { flex: none; color: var(--color-text-3); }
      .td-bf > span { overflow: hidden; text-overflow: ellipsis; }
      .td-bf.is-active { background: var(--color-primary-light-2, var(--color-fill-1)); }''',
    '''      /* ★ 第 49 轮第 6 项：.td-browse-files 按设计稿还原为 tree
         实测（节点 1350:18310）：行距 34px、缩进 20px/级、
         目录 chevron 盒中心 = 内容左+14、文件夹图标盒 = 内容左+28、文件图标盒 = 内容左+8、
         3 级竖向引导线（node x 34/54/74，第 4 级不再画）、
         激活行 = 内容宽 × 32px 高（上下各留 1px）+ 1px 描边 + 4px 圆角。 */
      .td-browse-files { display: flex; flex-direction: column; margin-top: 8px; }
      .td-bf {
        position: relative; display: flex; align-items: center; height: 34px; box-sizing: border-box;
        font-size: var(--font-size-body-3); color: var(--color-text-1);
        white-space: nowrap; overflow: hidden; cursor: default;
      }
      .td-bf.is-dir { padding-left: calc(6px + var(--d, 0) * 20px); }
      .td-bf.is-file { padding-left: calc(8px + var(--d, 0) * 20px); }
      .td-bf:hover { background: var(--color-fill-1); }
      .td-bf::before {
        content: ''; position: absolute; inset: 1px 0; border-radius: 4px; pointer-events: none;
        background: transparent; border: 1px solid transparent;
      }
      .td-bf.is-active::before { background: var(--td-tree-active-bg); border-color: var(--td-tree-active-bd); }
      .td-bf-guide { position: absolute; top: 0; bottom: 0; width: 1px; background: var(--td-tree-guide); }
      .td-bf-arrow {
        flex: none; width: 16px; height: 16px; padding: 0; border: 0; background: transparent;
        display: inline-flex; align-items: center; justify-content: center;
        color: var(--color-text-2); cursor: pointer;
      }
      .td-bf-arrow svg { transition: transform 120ms var(--transition-timing-function-standard, ease); }
      .td-bf.is-closed > .td-bf-arrow svg { transform: rotate(-90deg); }
      .td-bf.is-dir > .td-bf-arrow { margin-right: 6px; }
      .td-bf-ico { flex: none; width: 16px; height: 16px; color: var(--color-text-2); }
      .td-bf.is-dir > .td-bf-ico { margin-right: 8px; }
      .td-bf.is-file > .td-bf-ico { margin-right: 7px; }
      .td-bf-name { overflow: hidden; text-overflow: ellipsis; }
      .td-bf.is-hidden { display: none; }''',
    tag='A4 树行样式')

# A5 crumb 底线
rep(
    '''      .td-browse-crumb {
        height: 36px; flex: none; box-sizing: border-box; display: flex; align-items: center; gap: 8px;
        padding: 0 16px; font-size: var(--font-size-body-1); color: var(--color-text-2);
      }''',
    '''      .td-browse-crumb {
        height: 36px; flex: none; box-sizing: border-box; display: flex; align-items: center; gap: 8px;
        padding: 0 16px; font-size: var(--font-size-body-1); color: var(--color-text-2);
        /* ★ 第 49 轮第 3 项：补底部线条（设计稿实测 node y=74.7、色 #E7EBF1、贯通整个面板宽） */
        border-bottom: 1px solid var(--td-crumb-line);
      }''',
    tag='A5 crumb 底线')

# ============================================================ B. HTML
def jline(content, ind=8):
    """生成 JS 字符串数组里的一行：8 空格缩进 + "内容 转义" ,"""
    return ' ' * ind + '"' + content.replace('"', '\\"') + '",\n'


# ---- B1 主分隔条（.td-right 与 .td-browse 之间）
rep(
    '        "  </aside>",\n        "<aside class=\\"td-browse\\" aria-label=\\"文件预览\\">",',
    '        "  </aside>",\n'
    + jline('  <div class="td-split" data-td-split="main" role="separator" aria-orientation="vertical"'
            ' aria-label="拖动调整 AI 对话框宽度" tabindex="0"></div>')
    + '        "<aside class=\\"td-browse\\" aria-label=\\"文件预览\\">",',
    tag='B1 主分隔条')

# ---- B2 tree / code 之间的分隔条
rep(
    '        "    </section>",\n        "    <section class=\\"td-browse-code\\">",',
    '        "    </section>",\n'
    + jline('    <div class="td-split" data-td-split="tree" role="separator" aria-orientation="vertical"'
            ' aria-label="拖动调整文件目录宽度" tabindex="0"></div>')
    + '        "    <section class=\\"td-browse-code\\">",',
    tag='B2 树分隔条')

# ---- B3 文件树重写
SVG_HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"'
            ' fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"'
            ' stroke-linejoin="round" aria-hidden="true">')
ICON_CHEV_DOWN = SVG_HEAD + '<path d="m6 9 6 6 6-6"/></svg>'
ICON_FOLDER_OPEN = SVG_HEAD + ('<path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2"/></svg>')
ICON_FOLDER_CLOSED = SVG_HEAD + ('<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/><path d="M2 10h20"/></svg>')
ICON_FILE = SVG_HEAD + ('<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
                        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 12H8"/><path d="M16 16H10"/></svg>')
ICON_LIST_TREE = SVG_HEAD + ('<path d="M21 6H8"/><path d="M21 12h-8"/><path d="M21 18h-8"/>'
                             '<path d="M3 6v4c0 1.1.9 2 2 2h3"/><path d="M3 10v6c0 1.1.9 2 2 2h3"/></svg>')
ICON_COMPASS = SVG_HEAD + ('<circle cx="12" cy="12" r="10"/>'
                           '<polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>')

# (id, parent, kind, depth, name, state)
ROWS = [
    ('root',         '',       'dir',  0, '.giencoder-x',              'open'),
    ('memory',       'root',   'dir',  1, 'memory',                    'closed'),
    ('memory-md',    'memory', 'file', 2, 'MEMORY.md',                 ''),
    ('memory-notes', 'memory', 'file', 2, 'notes.md',                  ''),
    ('games',        'root',   'dir',  1, 'games',                     'open'),
    ('snake',        'games',  'dir',  2, 'snake-game',                'open'),
    ('dist',         'snake',  'dir',  3, 'dist',                      'closed'),
    ('dist-js',      'dist',   'file', 4, 'bundle.js',                 ''),
    ('dist-css',     'dist',   'file', 4, 'styles.css',                ''),
    ('nmod',         'snake',  'dir',  3, 'node_modules',              'closed'),
    ('nmod-react',   'nmod',   'dir',  4, 'react',                     'closed'),
    ('nmod-react-p', 'nmod-react', 'file', 5, 'package.json',          ''),
    ('nmod-dom',     'nmod',   'dir',  4, 'react-dom',                 'closed'),
    ('nmod-dom-p',   'nmod-dom', 'file', 5, 'package.json',            ''),
    ('public',       'snake',  'dir',  3, 'public',                    'closed'),
    ('public-fav',   'public', 'file', 4, 'favicon.svg',               ''),
    ('src',          'snake',  'dir',  3, 'src',                       'open'),
    ('plock',        'src',    'file', 4, 'package-lock.html',         ''),
    ('controls',     'src',    'file', 4, 'Controls.tsx',              ''),
    ('usesnake',     'src',    'file', 4, 'useSnakeGame...',           'active'),
    ('index',        'snake',  'file', 3, 'index.html',                ''),
    ('website',      'snake',  'file', 3, 'giencoder-website-v4...',   ''),
    ('map',          'snake',  'file', 3, 'map-dashboard.html',        ''),
    ('subprojects',  'snake',  'file', 3, 'SUBPROJECTS.md',            ''),
    ('electron',     'snake',  'file', 3, 'electron-builder.config...', ''),
    ('pkg',          'snake',  'file', 3, 'package.json',              ''),
    ('eslint',       'snake',  'file', 3, 'eslint.config.js',          ''),
    ('server',       'snake',  'file', 3, 'server-entry.js',           ''),
]
STATE_BY_ID = {r[0]: r[5] for r in ROWS}
PARENT_BY_ID = {r[0]: r[1] for r in ROWS}


def initially_hidden(rid):
    """任一祖先处于折叠态 → 初始隐藏（静态写入 class，省掉首帧闪烁）"""
    p = PARENT_BY_ID.get(rid, '')
    while p:
        if STATE_BY_ID.get(p) == 'closed':
            return True
        p = PARENT_BY_ID.get(p, '')
    return False


def row_html(r):
    rid, parent, kind, depth, name, state = r
    cls = 'td-bf is-' + ('dir' if kind == 'dir' else 'file')
    if kind == 'dir' and state == 'closed':
        cls += ' is-closed'
    if state == 'active':
        cls += ' is-active'
    if initially_hidden(rid):
        cls += ' is-hidden'
    # 3 级引导线：设计稿实测只有 3 条（第 4 级起不再画）
    guides = ''.join('<i class="td-bf-guide" style="--g:%d"></i>' % g for g in range(min(depth, 3)))
    attrs = ' role="treeitem" aria-level="%d" tabindex="0"' % (depth + 1)
    if parent:
        attrs += ' data-parent="%s"' % parent
    if kind == 'dir':
        attrs += ' data-node="%s" aria-expanded="%s"' % (rid, 'false' if state == 'closed' else 'true')
        inner = (guides
                 + '<button class="td-bf-arrow" type="button" tabindex="-1" aria-label="展开/折叠 %s">%s</button>'
                 % (name, ICON_CHEV_DOWN)
                 + (ICON_FOLDER_OPEN if state == 'open' else ICON_FOLDER_CLOSED)
                 + '<span class="td-bf-name">%s</span>' % name)
    else:
        attrs += ' aria-selected="%s"' % ('true' if state == 'active' else 'false')
        inner = guides + ICON_FILE + '<span class="td-bf-name">%s</span>' % name
    return '<div class="%s" style="--d:%d"%s>%s</div>' % (cls, depth, attrs, inner)


i = s.find('        "      <div class=\\"td-browse-files\\">",')
if i < 0:
    print('!! 找不到 td-browse-files 起始锚点')
    sys.exit(1)
j = s.find('        "    </section>",', i)
if j < 0:
    print('!! 找不到 td-browse-files 结束锚点')
    sys.exit(1)
block = jline('      <div class="td-browse-files" role="tree" aria-label="文件目录">')
for r in ROWS:
    block += jline('        ' + row_html(r))
block += jline('      </div>')
s = s[:i] + block + s[j:]
LOG.append('B3 文件树（%d 行）' % len(ROWS))

# ---- B4 crumb 两个按钮
new_tree_btn = jline('          <button class="td-browse-ico" type="button" aria-label="隐藏文件目录"'
                     ' title="隐藏文件目录" aria-pressed="true" data-td-tree-toggle="1">%s</button>'
                     % ICON_LIST_TREE, ind=8)
new_open_btn = jline('          <button class="td-browse-ico" type="button"'
                     ' aria-label="在浏览器中打开当前文件" title="在浏览器中打开当前文件"'
                     ' data-td-open-browser="1">%s</button>' % ICON_COMPASS, ind=8)
m = re.search(r'[ ]{8}"[ ]{10}<button class=\\"td-browse-ico\\"[^\n]*aria-label=\\"列表视图\\"[^\n]*\n', s)
if not m:
    print('!! 找不到「列表视图」按钮行')
    sys.exit(1)
s = s[:m.start()] + new_tree_btn + s[m.end():]
LOG.append('B4 文件目录开关按钮')
m = re.search(r'[ ]{8}"[ ]{10}<button class=\\"td-browse-ico\\"[^\n]*aria-label=\\"帮助\\"[^\n]*\n', s)
if not m:
    print('!! 找不到「帮助」按钮行')
    sys.exit(1)
s = s[:m.start()] + new_open_btn + s[m.end():]
LOG.append('B4 浏览器打开按钮')

# ============================================================ C. JS
NEW_JS = '''  <script>
    /* ★ 第 49 轮：文件预览栏（.td-browse）的拖动与交互
       ① 两条分隔条可拖动：AI 对话框 ≥400px（用户指定）、文件树 ≥240px、代码区 ≥400px（后两项为兜底值）；
       ② crumb 右侧两按钮：文件目录显隐开关（list-tree 图标）+ 在浏览器打开当前文件（compass 图标）；
       ③ .td-browse-files 还原为 tree：展开/折叠、选中、键盘可达。
       宽度写入 r35 的同一份布局记忆（giencoder:td-cols:v1），新增 browseRightW / browseTreeW 两个字段，
       与普通态的 rightW / swapped / collapsed 互不干扰。 */
    (function () {
      var KEY = 'giencoder:td-cols:v1';
      var DEF_RIGHT = 480, DEF_TREE = 296;
      var MIN_RIGHT = 400, MIN_TREE = 240, MIN_CODE = 400;

      function readStore() {
        try { return JSON.parse(localStorage.getItem(KEY) || 'null') || {}; }
        catch (err) { return {}; }
      }
      function writeStore(patch) {
        var d = readStore();
        for (var k in patch) { if (Object.prototype.hasOwnProperty.call(patch, k)) d[k] = patch[k]; }
        try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (err) {}
      }
      function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

      function init() {
        var root = document.querySelector('.td-root');
        if (!root) return false;
        var btn = root.querySelector('[data-td-browse-toggle]');
        var pane = root.querySelector('.td-browse');
        if (!btn || !pane) return false;
        if (btn.dataset.tdBrowseBound === '1') return true;
        btn.dataset.tdBrowseBound = '1';

        var body = pane.querySelector('.td-browse-body');
        var tree = pane.querySelector('.td-browse-tree');
        var files = pane.querySelector('.td-browse-files');
        var crumb = pane.querySelector('.td-browse-crumb-path');
        var splitMain = root.querySelector('[data-td-split="main"]');
        var splitTree = pane.querySelector('[data-td-split="tree"]');
        var curRight = DEF_RIGHT, curTree = DEF_TREE;

        /* 面板宽 = 根容器宽 − AI 对话框宽（分隔条净占位 0，故不减） */
        function rootW() { return root.getBoundingClientRect().width; }
        function maxRight() { return Math.max(MIN_RIGHT, rootW() - (MIN_TREE + 1 + MIN_CODE)); }
        function maxTree() { return Math.max(MIN_TREE, rootW() - curRight - 1 - MIN_CODE); }

        function setTree(w, persist) {
          curTree = Math.round(clamp(w, MIN_TREE, maxTree()));
          pane.style.setProperty('--td-browse-tree-w', curTree + 'px');
          if (splitTree) {
            splitTree.setAttribute('aria-valuenow', String(curTree));
            splitTree.setAttribute('aria-valuemin', String(MIN_TREE));
          }
          if (persist) writeStore({ browseTreeW: curTree });
        }
        function setRight(w, persist) {
          curRight = Math.round(clamp(w, MIN_RIGHT, maxRight()));
          root.style.setProperty('--td-browse-right-w', curRight + 'px');
          if (splitMain) {
            splitMain.setAttribute('aria-valuenow', String(curRight));
            splitMain.setAttribute('aria-valuemin', String(MIN_RIGHT));
          }
          /* AI 对话框变宽 → 面板变窄 → 树可能越界，同步钳位 */
          if (curTree > maxTree()) setTree(maxTree(), false);
          if (persist) writeStore({ browseRightW: curRight });
        }

        function setOpen(on) {
          root.classList.toggle('is-browse', on);
          btn.setAttribute('aria-pressed', on ? 'true' : 'false');
          if (on) { setRight(curRight, false); setTree(curTree, false); }
        }
        btn.addEventListener('click', function () { setOpen(!root.classList.contains('is-browse')); });
        var close = pane.querySelector('[data-td-browse-close]');
        if (close) close.addEventListener('click', function () { setOpen(false); });
        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && root.classList.contains('is-browse')) setOpen(false);
        });

        /* ---------- 分隔条拖动 ---------- */
        function draggable(el, applyFrom, persist) {
          if (!el) return;
          var on = false;
          el.addEventListener('pointerdown', function (e) {
            if (!root.classList.contains('is-browse')) return;
            on = true;
            el.classList.add('is-dragging');
            root.classList.add('is-col-dragging');
            if (el.setPointerCapture) { try { el.setPointerCapture(e.pointerId); } catch (err) {} }
            e.preventDefault();
          });
          el.addEventListener('pointermove', function (e) { if (on) applyFrom(e.clientX); });
          function end() {
            if (!on) return;
            on = false;
            el.classList.remove('is-dragging');
            root.classList.remove('is-col-dragging');
            persist();   /* 与 r35 同策略：只在收手时落盘，pointermove 里不写 */
          }
          el.addEventListener('pointerup', end);
          el.addEventListener('pointercancel', end);
        }
        draggable(splitMain, function (x) { setRight(x - root.getBoundingClientRect().left, false); },
                  function () { writeStore({ browseRightW: curRight }); });
        draggable(splitTree, function (x) { setTree(x - tree.getBoundingClientRect().left, false); },
                  function () { writeStore({ browseTreeW: curTree }); });

        function keyboard(el, getCur, set) {
          if (!el) return;
          el.addEventListener('keydown', function (e) {
            var step = e.shiftKey ? 48 : 16;
            if (e.key === 'ArrowLeft') { set(getCur() - step, true); e.preventDefault(); }
            else if (e.key === 'ArrowRight') { set(getCur() + step, true); e.preventDefault(); }
          });
        }
        keyboard(splitMain, function () { return curRight; }, setRight);
        keyboard(splitTree, function () { return curTree; }, setTree);
        if (splitMain) {
          splitMain.setAttribute('title', '拖动调整 AI 对话框宽度（最小 400px）· 双击复位');
          splitMain.addEventListener('dblclick', function () { setRight(DEF_RIGHT, true); });
        }
        if (splitTree) {
          splitTree.setAttribute('title', '拖动调整文件目录宽度（最小 240px）· 双击复位');
          splitTree.addEventListener('dblclick', function () { setTree(DEF_TREE, true); });
        }

        /* 视口变化后重新钳位（钳位值不落盘，与 r35 同策略） */
        var raf = 0;
        window.addEventListener('resize', function () {
          if (raf) cancelAnimationFrame(raf);
          raf = requestAnimationFrame(function () { raf = 0; setRight(curRight, false); setTree(curTree, false); });
        });

        /* ---------- crumb 右侧两个按钮（第 49 轮第 4/5 项） ---------- */
        var tgl = pane.querySelector('[data-td-tree-toggle]');
        if (tgl) {
          tgl.addEventListener('click', function () {
            var hidden = body.classList.toggle('is-no-tree');
            tgl.setAttribute('aria-pressed', hidden ? 'false' : 'true');
            var label = hidden ? '显示文件目录' : '隐藏文件目录';
            tgl.setAttribute('aria-label', label);
            tgl.setAttribute('title', label);
            if (!hidden) setTree(curTree, false);
          });
        }
        var openBtn = pane.querySelector('[data-td-open-browser]');
        if (openBtn) {
          openBtn.addEventListener('click', function () {
            var name = crumb && crumb.textContent ? crumb.textContent.split('/').pop().trim() : '';
            if (!name) return;
            /* 当前文件 = crumb 末段（设计稿里是 index.html）。原型约定：映射到仓库根的同名文件
               （本页在 pages/ 下）→ ../index.html 在磁盘上真实存在，双击打开时即交给系统默认浏览器。
               ⚠️ 在内置 http 预览里 ../ 会落到 static-html 根，路径未必存在 —— file:// 直开是标准用法。 */
            window.open(new URL('../' + name, location.href).href, '_blank', 'noopener');
          });
        }

        /* ---------- tree：展开/折叠 + 选中（第 49 轮第 6 项） ---------- */
        function refresh() {
          var rows = pane.querySelectorAll('.td-bf'), i;
          for (i = 0; i < rows.length; i++) {
            var p = rows[i].dataset.parent || '', ok = true;
            while (p) {
              var pr = pane.querySelector('.td-bf[data-node="' + p + '"]');
              if (!pr || pr.classList.contains('is-closed')) { ok = false; break; }
              p = pr.dataset.parent || '';
            }
            rows[i].classList.toggle('is-hidden', !ok);
          }
        }
        function toggleDir(row) {
          var closed = row.classList.toggle('is-closed');
          row.setAttribute('aria-expanded', closed ? 'false' : 'true');
          refresh();
        }
        function selectFile(row) {
          var old = pane.querySelector('.td-bf.is-active');
          if (old) { old.classList.remove('is-active'); old.setAttribute('aria-selected', 'false'); }
          row.classList.add('is-active');
          row.setAttribute('aria-selected', 'true');
        }
        if (files) {
          files.addEventListener('click', function (e) {
            var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
            if (!row) return;
            if (row.classList.contains('is-dir')) toggleDir(row); else selectFile(row);
          });
          files.addEventListener('keydown', function (e) {
            var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
            if (!row || row !== e.target) return;
            var isDir = row.classList.contains('is-dir'), closed = row.classList.contains('is-closed');
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              if (isDir) toggleDir(row); else selectFile(row);
            } else if (e.key === 'ArrowRight' && isDir && closed) { e.preventDefault(); toggleDir(row); }
            else if (e.key === 'ArrowLeft' && isDir && !closed) { e.preventDefault(); toggleDir(row); }
          });
        }

        /* ---------- 恢复本次浏览态记忆 ---------- */
        function restore() {
          var d = readStore();
          if (typeof d.browseRightW === 'number') setRight(d.browseRightW, false);
          if (typeof d.browseTreeW === 'number') setTree(d.browseTreeW, false);
        }
        if (root.getBoundingClientRect().width > 0) restore(); else requestAnimationFrame(restore);

        return true;
      }

      if (!init()) {
        var mo = new MutationObserver(function () { if (init()) mo.disconnect(); });
        mo.observe(document.body, { childList: true, subtree: true });
      }
    })();
  </script>
'''

a = s.find('  <script>\n    /* ★ 第 47 轮第 2 项')
b = s.find('  </body>')
if a < 0 or b < 0 or a > b:
    print('!! 找不到 JS 块锚点')
    sys.exit(1)
s = s[:a] + NEW_JS + '\n' + s[b:]
LOG.append('C1 浏览栏 JS（拖动/开关/浏览器打开/tree）')

# ============================================================ D. 自检
ok = True
checks = [
    ('<style', s.count('<style'), lambda v: v == orig.count('<style')),
    ('</style>', s.count('</style>'), lambda v: v == orig.count('</style')),
    ('</aside>', s.count('</aside>'), lambda v: v == orig.count('</aside>')),
    ('split 标记(main)', s.count('data-td-split=\\"main\\"'), lambda v: v == 1),
    ('split 标记(tree)', s.count('data-td-split=\\"tree\\"'), lambda v: v == 1),
    ('split 选择器 main', s.count('[data-td-split="main"]'), lambda v: v == 1),
    ('split 选择器 tree', s.count('[data-td-split="tree"]'), lambda v: v == 2),       # JS + CSS
    ('data-td-tree-toggle', s.count('data-td-tree-toggle'), lambda v: v == 2),        # 标记 + JS
    ('data-td-open-browser', s.count('data-td-open-browser'), lambda v: v == 2),
    ('td-bf-guide', s.count('td-bf-guide'), lambda v: v == 75),                       # 74 处标记 + 1 条 CSS
    ('目录行', s.count('td-bf is-dir'), lambda v: v == 10),
    ('文件行', s.count('td-bf is-file'), lambda v: v == 18),
    ('旧「列表视图」', s.count('列表视图'), lambda v: v == 0),
    ('旧 aria-label="帮助"', s.count('aria-label=\\"帮助\\"'), lambda v: v == 0),
    ('folder-open 路径', s.count('m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20'), lambda v: v == 4),   # 4 个展开目录
    ('list-tree 路径', s.count('M3 6v4c0 1.1.9 2 2 2h3'), lambda v: v == 1),
    ('compass polygon', s.count('16.24 7.76 14.12 14.12'), lambda v: v == 1),
    ('td-browse-files 行数', s.count('td-bf is-dir') + s.count('td-bf is-file'), lambda v: v >= 25),
    ('--td-browse-right-w 定义', s.count('var(--td-browse-right-w, 480px)'), lambda v: v == 1),
    ('--td-browse-tree-w 定义', s.count('var(--td-browse-tree-w, 296px)'), lambda v: v == 1),
    ('--td-crumb-line 使用', s.count('var(--td-crumb-line)'), lambda v: v == 1),
]
for name, val, pred in checks:
    good = pred(val)
    ok = ok and good
    print('  %-28s = %-5s %s' % (name, val, 'OK' if good else 'FAIL'))

if not ok:
    print('FAIL —— 未写入任何改动')
    sys.exit(1)

import os
os.makedirs('/tmp/r49-backup', exist_ok=True)
if not os.path.exists(BAK):
    shutil.copy(F, BAK)
    print('备份 ->', BAK)
open(F, 'w', encoding='utf-8').write(s)
print('改动：')
for t in LOG:
    print('  -', t)
print('原 %d 字节 → 现 %d 字节（+%d）' % (len(orig), len(s), len(s) - len(orig)))
print('OK')
