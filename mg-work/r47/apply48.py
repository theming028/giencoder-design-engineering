#!/usr/bin/env python3
# 第 47 轮第 2 项：右栏 td-right-acts 右侧加「打开侧栏」按钮，
#                  点击后在 AI 会话栏右侧展开文件预览栏（设计稿节点 1350:18310）
import os, re, sys, shutil

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
F = os.path.join(ROOT, 'pages/task-detail.html')
BK = '/tmp/r47-backup'
os.makedirs(BK, exist_ok=True)
if not os.path.exists(os.path.join(BK, 'td-r47-b2.html')):
    shutil.copy2(F, os.path.join(BK, 'td-r47-b2.html'))

S = open(F, encoding='utf-8').read()
MARK = '第 47 轮第 2 项'


def esc_h(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def esc_js(t):
    return t.replace('"', '\\"')


# ---------------------------------------------------------------- 图标
ICON = {
    'panel': '<path d="M3 5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M15 3v18"/>',
    'plus': '<path d="M5 12h14"/><path d="M12 5v14"/>',
    'chev-r': '<path d="m9 18 6-6-6-6"/>',
    'chev-d': '<path d="m6 9 6 6 6-6"/>',
    'folder': '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.7-.9l-.8-1.2A2 2 0 0 0 7.9 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/>',
    'file': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
    'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    'list': '<path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/>',
    'help': '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
}


def svg(name, size=14):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="%d" height="%d" '
            'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>') % (size, size, ICON[name])


# ---------------------------------------------------------------- 文件树
TREE = [
    (0, 'chev-d', '.giencoder-x', 0),
    (1, 'chev-r', 'memory', 0),
    (1, 'chev-d', 'games', 0),
    (2, 'chev-d', 'snake-game', 0),
    (3, 'chev-r', 'dist', 0),
    (3, 'chev-r', 'node_modules', 0),
    (3, 'chev-r', 'public', 0),
    (3, 'chev-d', 'src', 0),
    (4, 'file', 'package-lock.html', 0),
    (4, 'file', 'Controls.tsx', 0),
    (4, 'file', 'useSnakeGame...', 1),
    (3, 'file', 'index.html', 0),
    (3, 'file', 'giencoder-website-v4...', 0),
    (3, 'file', 'map-dashboard.html', 0),
    (3, 'file', 'SUBPROJECTS.md', 0),
    (3, 'file', 'electron-builder.config...', 0),
    (3, 'file', 'package.json', 0),
    (3, 'file', 'eslint.config.js', 0),
    (3, 'file', 'server-entry.js', 0),
]

# ---------------------------------------------------------------- 代码内容
JSON_TEXT = '''{
  "name": "snake-game",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/react": "^16.1.0",
    "@testing-library/user-event": "^14.5.2",
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.12",
    "@vitejs/plugin-react": "^4.7.0",
    "autoprefixer": "^10.4.20",
    "jsdom": "^25.1.0",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.17",
    "typescript": "~5.7.2",
    "vite": "^6.0.5",
    "vitest": "^2.1.8"
  }
}'''

TOKEN = re.compile(r'("(?:[^"\\]|\\.)*")(\s*:)?|\b(true|false|null)\b|(\d+(?:\.\d+)*)')


def colorize(line):
    t = esc_h(line)          # ★ 只在这一层转义；rep 内不得再 esc_h（否则 & 会二次转义）

    def rep(m):
        if m.group(1):
            if m.group(2):
                return '<span class="td-code-k">%s</span>%s' % (m.group(1), m.group(2))
            return '<span class="td-code-s">%s</span>' % m.group(1)
        if m.group(3):
            return '<span class="td-code-k">%s</span>' % m.group(3)
        return '<span class="td-code-n">%s</span>' % m.group(4)
    return TOKEN.sub(rep, t)


# ---------------------------------------------------------------- 组装 HTML
H = []
H.append('<aside class="td-browse" aria-label="文件预览">')
H.append('  <header class="td-browse-bar">')
H.append('    <span class="td-browse-tab">%s摘要</span>' % svg('panel'))
H.append('    <button class="td-browse-add" type="button" aria-label="新建标签">%s</button>' % svg('plus'))
H.append('    <span class="td-browse-sep"></span>')
H.append('    <div class="td-browse-acts">')
H.append('      <button class="td-browse-ico" type="button" aria-label="收起侧栏" title="收起侧栏" data-td-browse-close="1">%s</button>' % svg('chev-r'))
H.append('    </div>')
H.append('  </header>')
H.append('  <div class="td-browse-body">')
H.append('    <section class="td-browse-tree">')
H.append('      <div class="td-browse-tree-title">文件目录</div>')
H.append('      <div class="td-browse-search">%s<span>搜索文件</span></div>' % svg('search'))
H.append('      <div class="td-browse-files">')
for d, kind, name, active in TREE:
    cls = 'td-bf is-active' if active else 'td-bf'
    H.append('        <div class="%s" style="--d:%d">%s%s<span>%s</span></div>'
             % (cls, d, svg(kind), svg('folder' if kind.startswith('chev') else 'file'), name))
H.append('      </div>')
H.append('    </section>')
H.append('    <section class="td-browse-code">')
H.append('      <div class="td-browse-crumb">')
H.append('        <div class="td-browse-crumb-path">gientech / second / third / index.html</div>')
H.append('        <div class="td-browse-crumb-acts">')
H.append('          <button class="td-browse-ico" type="button" aria-label="列表视图">%s</button>' % svg('list'))
H.append('          <button class="td-browse-ico" type="button" aria-label="帮助">%s</button>' % svg('help'))
H.append('        </div>')
H.append('      </div>')
H.append('      <div class="td-browse-pre">')
for i, ln in enumerate(JSON_TEXT.split('\n'), 1):
    H.append('        <div class="td-code"><span class="td-code-no">%d</span>'
             '<span class="td-code-tx">%s</span></div>' % (i, colorize(ln)))
H.append('      </div>')
H.append('    </section>')
H.append('  </div>')
H.append('</aside>')

HTML_BLOCK = ''.join('        "%s",\n' % esc_js(x) for x in H)

# ---------------------------------------------------------------- 按钮
BTN = ('<button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default '
       'giencoder-btn-icon td-round-btn" type="button" aria-label="打开侧栏" title="打开侧栏" '
       'aria-pressed="false" data-td-browse-toggle="1">%s</button>' % svg('panel', 16))
BTN_JS = ('        "%s",\n' % esc_js('          ' + BTN))

# ---------------------------------------------------------------- CSS
CSS = '''      /* ★ 第 47 轮第 2 项：「打开侧栏」→ 在 AI 会话栏右侧展开文件预览栏（设计稿节点 1350:18310）。
         展开时左栏（任务详情）让位隐藏，AI 会话栏随之向左移出 —— 与设计稿
         「AI 会话 + 文件目录 + 代码预览」三栏同构。 */
      .td-browse {
        display: none; flex: 1 1 auto; min-width: 0; box-sizing: border-box;
        flex-direction: column; overflow: hidden; margin-left: 8px;
        background: var(--color-bg-1); border-radius: 8px; box-shadow: var(--td-panel-shadow);
      }
      .td-root.is-browse .td-left { display: none; }
      .td-root.is-browse .td-gutter { display: none; }
      .td-root.is-browse .td-browse { display: flex; }
      .td-browse-bar {
        height: 40px; flex: none; box-sizing: border-box;
        display: flex; align-items: center; gap: 8px; padding: 4px 16px;
      }
      .td-browse-tab {
        display: inline-flex; align-items: center; gap: 5px; height: 32px; padding: 0 8px;
        border-radius: 4px; font-size: var(--font-size-body-3); color: var(--color-text-1);
      }
      .td-browse-tab svg { color: var(--color-text-2); }
      .td-browse-add, .td-browse-ico {
        display: inline-flex; align-items: center; justify-content: center; flex: none;
        width: 24px; height: 24px; padding: 0; border: 0; border-radius: 4px;
        background: transparent; color: var(--color-text-2); cursor: pointer;
      }
      .td-browse-add:hover, .td-browse-ico:hover { background: var(--color-fill-1); color: var(--color-text-1); }
      .td-browse-sep { width: 1px; height: 20px; flex: none; background: var(--color-border-2); }
      .td-browse-acts { margin-left: auto; display: flex; align-items: center; gap: 8px; }
      .td-browse-body { flex: 1; min-height: 0; display: flex; }
      .td-browse-tree {
        flex: none; width: 256px; box-sizing: border-box; padding: 4px 0 8px;
        display: flex; flex-direction: column; gap: 8px; overflow: auto;
        border-right: 1px solid var(--color-border-1);
      }
      .td-browse-tree-title { padding: 0 8px; font-size: 12px; font-weight: 500; line-height: 20px; color: var(--color-text-2); }
      .td-browse-search {
        margin: 0 8px; height: 32px; flex: none; box-sizing: border-box;
        display: flex; align-items: center; gap: 8px; padding: 0 8px; border-radius: 4px;
        background: var(--color-fill-1); color: var(--color-text-3); font-size: var(--font-size-body-3);
      }
      .td-browse-files { display: flex; flex-direction: column; }
      .td-bf {
        display: flex; align-items: center; gap: 6px; height: 22px; box-sizing: border-box;
        padding-right: 8px; padding-left: calc(8px + var(--d, 0) * 20px);
        font-size: var(--font-size-body-3); color: var(--color-text-1);
        white-space: nowrap; overflow: hidden;
      }
      .td-bf > svg { flex: none; color: var(--color-text-3); }
      .td-bf > span { overflow: hidden; text-overflow: ellipsis; }
      .td-bf.is-active { background: var(--color-primary-light-2, var(--color-fill-1)); }
      .td-browse-code { flex: 1; min-width: 0; display: flex; flex-direction: column; }
      .td-browse-crumb {
        height: 36px; flex: none; box-sizing: border-box; display: flex; align-items: center; gap: 8px;
        padding: 0 16px; font-size: 12px; color: var(--color-text-2);
      }
      .td-browse-crumb-path { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .td-browse-crumb-acts { display: flex; align-items: center; gap: 4px; }
      .td-browse-pre {
        flex: 1; min-height: 0; overflow: auto; margin: 0; padding: 8px 0 16px;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 12px; line-height: 20px;
      }
      .td-code { display: flex; gap: 12px; padding: 0 16px; }
      .td-code-no { flex: none; width: 18px; text-align: right; color: var(--color-text-3); }
      .td-code-tx { white-space: pre; color: var(--color-text-1); }
      .td-code-k { color: #0451A5; }
      .td-code-s { color: #A31515; }
      .td-code-n { color: #098658; }
'''

# ---------------------------------------------------------------- JS
JS = '''  <script>
    /* ★ 第 47 轮第 2 项：「打开侧栏」按钮 —— 在 AI 会话栏右侧展开 / 收起文件预览栏 */
    (function () {
      function init() {
        var root = document.querySelector('.td-root');
        if (!root) return false;
        var btn = root.querySelector('[data-td-browse-toggle]');
        var pane = root.querySelector('.td-browse');
        if (!btn || !pane) return false;
        if (btn.dataset.tdBrowseBound === '1') return true;
        btn.dataset.tdBrowseBound = '1';
        function setOpen(on) {
          root.classList.toggle('is-browse', on);
          btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        }
        btn.addEventListener('click', function () {
          setOpen(!root.classList.contains('is-browse'));
        });
        var close = pane.querySelector('[data-td-browse-close]');
        if (close) close.addEventListener('click', function () { setOpen(false); });
        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && root.classList.contains('is-browse')) setOpen(false);
        });
        return true;
      }
      if (!init()) {
        var mo = new MutationObserver(function () { if (init()) mo.disconnect(); });
        mo.observe(document.body, { childList: true, subtree: true });
      }
    })();
  </script>
'''

# ---------------------------------------------------------------- 应用
applied = []
fail = 0

if 'data-td-browse-toggle' not in S:
    key = 'M16 21v-3a2 2 0 0 1 2-2h3'          # 全屏按钮 td-ico-min 的 path（唯一）
    if S.count(key) != 1:
        print('!! 全屏按钮锚点异常 x%d' % S.count(key)); sys.exit(1)
    i = S.find(key)
    j = S.find('</button>",', i)
    if j < 0:
        print('!! 找不到全屏按钮收尾'); sys.exit(1)
    j += len('</button>",')
    S = S[:j] + '\n' + BTN_JS.rstrip('\n') + S[j:]
    applied.append('按钮')
else:
    applied.append('按钮(已存在)')

ANCHOR_HTML = '        "  </aside>",\n        "</div>",\n        "",\n        "<!-- ★ 第 32 轮第 5 项'
if 'class=\\"td-browse\\"' not in S:
    if S.count(ANCHOR_HTML) != 1:
        print('!! 新栏锚点异常 x%d' % S.count(ANCHOR_HTML)); sys.exit(1)
    S = S.replace(ANCHOR_HTML, '        "  </aside>",\n' + HTML_BLOCK + '        "</div>",\n        "",\n        "<!-- ★ 第 32 轮第 5 项', 1)
    applied.append('新栏 HTML')
else:
    applied.append('新栏 HTML(已存在)')

CSS_ANCHOR = '.td-round-btn { box-sizing: border-box; width: 32px; padding: 0; border-color: transparent; line-height: 0; }\n'
if MARK + '：「打开侧栏」' not in S:
    if S.count(CSS_ANCHOR) != 1:
        print('!! CSS 锚点异常 x%d' % S.count(CSS_ANCHOR)); sys.exit(1)
    S = S.replace(CSS_ANCHOR, CSS_ANCHOR + CSS, 1)
    applied.append('CSS')
else:
    applied.append('CSS(已存在)')

JS_ANCHOR = '<!-- /SHELL-TABS-FIX -->\n\n  </body>'
if 'tdBrowseBound' not in S:
    if S.count(JS_ANCHOR) != 1:
        print('!! JS 锚点异常 x%d' % S.count(JS_ANCHOR)); sys.exit(1)
    S = S.replace(JS_ANCHOR, '<!-- /SHELL-TABS-FIX -->\n\n' + JS + '\n  </body>', 1)
    applied.append('JS')
else:
    applied.append('JS(已存在)')

open(F, 'w', encoding='utf-8').write(S)
print('已应用:', ', '.join(applied))

# ---------------------------------------------------------------- 自检
S = open(F, encoding='utf-8').read()
A = open(os.path.join(BK, 'td-r47-b2.html'), encoding='utf-8').read()
ok = True
for k in ['<style', '</style>', 'td-right-bar']:      # CSS/HTML 插在既有结构内部，标签数不变
    if S.count(k) < A.count(k):
        print('  !! 结构减少 %s: %d -> %d' % (k, A.count(k), S.count(k))); ok = False
if S.count('<script') < A.count('<script'):           # 新增 1 个 JS 块
    print('  !! script 未增加'); ok = False
if S.count('</aside>') != A.count('</aside>') + 1:    # 新增文件预览栏
    print('  !! </aside> 未 +1: %d -> %d' % (A.count('</aside>'), S.count('</aside>'))); ok = False
# 2 次 = 按钮 1 处 + JS 选择器 1 处
if S.count('data-td-browse-toggle') != 2:
    print('  !! browse-toggle 数量 %d（应为 2）' % S.count('data-td-browse-toggle')); ok = False
if S.count('class=\\"td-browse\\"') != 1:
    print('  !! 新栏数量异常'); ok = False
if S.count('td-code-k') < 20:
    print('  !! 代码着色缺失 x%d' % S.count('td-code-k')); ok = False
if S.count('<style') != S.count('</style>'):
    print('  !! style 标签不配平'); ok = False
print('OK' if ok else 'FAIL')
sys.exit(0 if ok else 1)
