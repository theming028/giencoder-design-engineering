# -*- coding: utf-8 -*-
"""r108 第十二拍 —— 两条：① `.td-diff` 独立成小卡片；② 「在文件树中定位」右侧加一枚「文件树」按钮 ⇒
点开在右栏右缘滑出文件树抽屉。

改序（只能下→上）：
    1. `mg-work/r108/part108/_mods.html`   插按钮 + 末尾追加抽屉（树内容**从 part105 原树提取**，不手抄）
    2. `mg-work/r108/part108/panel.css`    第 18 节（① 卡片化 · ② 抽屉 + 独立类名的树）
    3. `mg-work/r108/part108/panel.js`     抽屉控制器 + Esc 裁决链接一层
    4. `python mg-work/r108/ev/splice108.py`   → `part108/browse.html`
    5. `python mg-work/r108/apply108.py`       → 落 `pages/conversation.html`

幂等判据：每处都带 `mark`（**只有改完之后才存在**的串）⇒ 复跑「应用 0 项 / 跳过 N 项」。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P108 = os.path.join(REPO, 'mg-work', 'r108', 'part108')
MODS = os.path.join(P108, '_mods.html')
PCS = os.path.join(P108, 'panel.css')
PJS = os.path.join(P108, 'panel.js')
SRC_TREE = os.path.join(REPO, 'mg-work', 'r102', 'part105', 'browse.html')

APPLIED = []
SKIPPED = []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark):
    t, nl = rd(p)
    if mark and mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）' % (label, n))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


def tail(p, mark, new, label):
    t, nl = rd(p)
    if mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    if not t.endswith('\n'):
        t += '\n'
    wr(p, t + new, nl)
    APPLIED.append(label)
    print('   应用  %s（追加 %d 字符）' % (label, len(new)))


def one_line_containing(p, needle):
    """从文件里现取「包含 needle 的那一整行」（不手抄超长 HTML 行）。"""
    t, _ = rd(p)
    for ln in t.split('\n'):
        if needle in ln:
            return ln
    sys.exit('!! 找不到含 %r 的行' % needle)


# ================================================================================
# 0. 树内容：从 part105 的原树里**按白名单提取**（零手抄）
# ================================================================================
KEEP = {
    # ⚠ root 那行的**显示名**是 `.giencoder-x`（`data-node` 才是 `root`）—— 按 name 取。
    (0, '.giencoder-x'): True,
    (1, 'memory'): True,
    (1, 'games'): True,
    (2, 'snake-game'): True,
    (3, 'dist'): True,
    (3, 'public'): True,
    (3, 'src'): True,
    (3, 'package.json'): True,
    (4, 'Controls.tsx'): True,
}


def extract_tree_rows():
    s = io.open(SRC_TREE, encoding='utf-8').read()
    i = s.find('<div class="td-browse-files"')
    k = s.find('</section>', i)
    seg = s[i:k]
    rows = re.findall(r'<div class="td-bf[^\n]*?</div>', seg)
    out = []
    for r in rows:
        md = re.search(r'style="--d:(\d+)"', r)
        mn = re.search(r'<span class="td-bf-name">([^<]*)</span>', r)
        if not md or not mn:
            continue
        d, name = int(md.group(1)), mn.group(1)
        keep = KEEP.get((d, name), False) or (d == 4 and name.startswith('useSnakeGame'))
        if not keep:
            continue
        out.append(r)
    if len(out) != 10:
        sys.exit('!! 提取到 %d 行（应 10 行）—— 白名单或原树变了' % len(out))
    return out


def build_tree_html():
    """`td-bf*` → `td-tf*`（去掉引导线：抽屉里不画父级竖线）。"""
    lines = []
    for r in extract_tree_rows():
        r = r.replace('td-bf', 'td-tf')
        r = re.sub(r'<i class="td-tf-guide"[^>]*></i>', '', r)
        lines.append('            ' + r)
    if any('td-bf' in x for x in lines):
        sys.exit('!! 改名不彻底，仍有 td-bf 残留')
    return '\n'.join(lines)


# ================================================================================
# 1. _mods.html —— ① 工具条插按钮 · ② 末尾追加抽屉
# ================================================================================
NEW_BTN = ('          <button class="td-browse-ico" type="button" aria-label="文件树" title="文件树"'
           ' aria-haspopup="dialog" aria-expanded="false" data-td-rv-act="tree">'
           '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none"'
           ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
           ' aria-hidden="true"><path d="M20 10a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2.5a1 1 0 0 1-.8-.4l-.9-1.2A1 1 0 0 0'
           ' 15 3h-2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z"/><path d="M20 21a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1h-2.5a1 1 0 0'
           ' 1-.8-.4l-.9-1.2A1 1 0 0 0 15 14h-2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z"/><path d="M3 5a2 2 0 0 0 2 2h3"/>'
           '<path d="M3 3v13a2 2 0 0 0 2 2h3"/></svg></button>\n')


def patch_mods():
    # 1a) 「在文件树中定位」右侧插一枚「文件树」按钮（整行现取，不手抄）
    old = one_line_containing(MODS, 'data-td-rv-act="reveal"')
    edit(MODS, old + '\n', old + '\n' + NEW_BTN,
         '_mods.html ①审查工具条插「文件树」按钮', 'data-td-rv-act="tree"')

    # 1b) 末尾追加文件树抽屉
    tree = build_tree_html()
    new = """
    <!-- ★ 第十二拍 ②（r108-l1）：文件树抽屉 —— 挂在审查工具条「在文件树中定位」**右侧**那枚按钮上。
         点开 = 从右栏右缘滑入一层 `min(296px, 86%)` 的文件树面板（与「文件」模块的树同宽），
         **不打断当前正在看的模块**（不必切到「文件」标签）。
         ★★ 树行刻意用**独立类名** `td-tf*`（**不是** `td-bf*`）：
            ctrl-conv.js 的 `pane.querySelectorAll('.td-bf')` 作用域是整个 `.td-browse`，
            复用同名类会把抽屉里的行一并接管（refresh / selectFile 互相打架；且它那个
            `files` 变量只绑**第一个** `.td-browse-files` ⇒ 抽屉里的行点了没反应）。
            抽屉树自己的展开 / 折叠 / 选中由 panel.js 新写一小段（同语义、互不干扰）。
         三条关闭路径：点遮罩 / 点关闭按钮 / 按 Esc（panel.js 的 Esc 裁决链已接一层）。
         ⚠ 静态标记里的 `is-hidden` 就是初始折叠态（与 ctrl-conv 的 refresh() 同一口径），
            抽屉打开时 panel.js 会再算一遍（幂等）。 -->
    <div class="td-tree" data-td-tree="1" role="dialog" aria-modal="true" aria-label="文件树" hidden>
      <div class="td-tree-scrim" data-td-tree-x="1"></div>
      <div class="td-tree-panel">
        <div class="td-tree-h">
          <span class="td-tree-t">文件树</span>
          <button class="td-browse-ico" type="button" aria-label="关闭文件树" title="关闭文件树" data-td-tree-x="1"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button>
        </div>
        <div class="td-tree-body">
          <div class="giencoder-input-wrapper td-browse-search" data-component="input" data-variant="prefix" data-size="medium" data-state="default"><span class="giencoder-input-prefix"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg></span><input class="giencoder-input" type="text" placeholder="搜索文件" aria-label="搜索文件"></div>
          <div class="td-tree-files" role="tree" aria-label="文件目录">
__TREE__
          </div>
        </div>
      </div>
    </div>
""".replace('__TREE__', tree)
    tail(MODS, 'class="td-tree" data-td-tree', new, '_mods.html ②末尾追加文件树抽屉')


# ================================================================================
# 2. panel.css —— 第 18 节
# ================================================================================
CSS_NEW = """

/* ================================================================================
   18. 第十二拍（r108-l1）—— ① diff 独立成小卡片 · ② 文件树抽屉
   ================================================================================ */

/* ---------------------------------------------------------------- 18.1 diff 独立成卡片
   改前：`.td-rv-body { padding: 4px 0 16px }` + `.td-diff { border-bottom: 1px solid --color-border-1 }`
         ⇒ 四张 diff 首尾相接、只靠一条 1px 线分隔，视觉上是「一整块长列表」。
   改后：卡片 = `1px 描边 + 8px 圆角 + --color-bg-2 底`，卡间距 8px（`.td-rv-body` 改 flex 纵列）。
   ★ `overflow: hidden` 是**必需的**：`.td-diff-h:hover { background: --color-fill-1 }` 是既有规则，
     色块铺满整行，不裁的话会在四个圆角处露出直角。
     代价 = `.td-diff-toggle:focus-visible` 的 `outline`（offset 2px）被裁掉一点 —— 可接受
     （键盘态，且描边本身仍在）。
   ★ 卡片头 / 代码区之间补一条 `border-top`：折叠态 `.td-diff-rows` 本就是 `display: none`
     （见第 3 节那条 `.td-diff:not(.is-open) .td-diff-rows`），而统一 / 并排两个 `-rows`
     同刻**必然只有一个可见** ⇒ 不会出现双线。
   ⚠ 这两条都是**同特异性、本块在后** ⇒ 靠文档顺序压过第 3 节的旧值（不写 !important）。 */
.td-rv-body {
  display: flex; flex-direction: column; gap: 8px;
  padding: 8px;
}
.td-diff {
  border: 1px solid var(--color-border-2);
  border-radius: 8px;
  background: var(--color-bg-2);
  overflow: hidden;
}
.td-diff-rows { border-top: 1px solid var(--color-border-1); }

/* ---------------------------------------------------------------- 18.2 文件树抽屉
   右栏右缘滑入的一层：宽 `min(296px, 86%)`（与「文件」模块的树 `--td-browse-tree-w: 296px` 同宽）。
   z-index 35 —— 夹在「右栏下拉菜单 30」与「提交模态 40」之间：抽屉可以盖住菜单，
   但提交模态要能盖住抽屉（Esc 裁决链的顺序与此一致：模态 → 抽屉 → 菜单）。
   ⚠ 开合 = `hidden` 属性 + `is-open` 类，**两条一起用**：
     `hidden` 负责「不在渲染树里 / 不吃点击」，`is-open` 负责过渡的目标态。
     先摘 `hidden` → 强制 reflow → 再加 `is-open`，过渡才有起点（panel.js 里那三行）。 */
.td-tree { position: absolute; inset: 0; z-index: 35; }
.td-tree[hidden] { display: none; }
.td-tree-scrim {
  position: absolute; inset: 0;
  background: var(--color-mask-bg);
  opacity: 0; transition: opacity 200ms ease;
}
.td-tree-panel {
  position: absolute; top: 0; right: 0; bottom: 0;
  width: min(296px, 86%); box-sizing: border-box;
  display: flex; flex-direction: column;
  background: var(--color-bg-2);
  border-left: 1px solid var(--color-border-2);
  box-shadow: var(--shadow3-down);
  transform: translateX(100%);
  transition: transform 220ms cubic-bezier(0.34, 0.69, 0.1, 1);
}
.td-tree.is-open .td-tree-scrim { opacity: 1; }
.td-tree.is-open .td-tree-panel { transform: none; }
.td-tree-h {
  flex: none; display: flex; align-items: center; gap: 8px;
  height: calc(40px * var(--ui-fs-ratio)); min-height: calc(40px * var(--ui-fs-ratio));
  box-sizing: border-box; padding: 0 8px 0 12px;
  border-bottom: 1px solid var(--color-border-2);
  font-size: var(--font-size-body-3);
}
.td-tree-t {
  flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1);
}
.td-tree-body {
  flex: 1 1 auto; min-height: 0; box-sizing: border-box;
  display: flex; flex-direction: column; gap: 8px; padding: 12px; overflow: hidden;
}
.td-tree-files {
  flex: 1 1 auto; min-height: 0; overflow: auto;
  display: flex; flex-direction: column; gap: 2px;
}

/* 抽屉里的树行：**独立类名 `td-tf`**，几何逐条对齐 browse.css 的 `.td-bf`
   （行高 28 · 圆角 4 · 缩进 7.5/8 + 20×级数 · hover fill-2 · 图标 13px · dir 距 7.5 / file 距 10）。
   ⚠ 为什么不用 `.td-bf`：ctrl-conv.js 的 `pane.querySelectorAll('.td-bf')` 作用域是整个
     `.td-browse` ⇒ 会把抽屉里的行一并接管，两边互相打架（详见 `_mods.html` 那段注释）。
   ⚠ `height` 与字号 token 同规则声明（PLAYBOOK 规则 9：凡声明 height/line-height 的规则，
     字号必须写 token，否则被 apply88b.converge() 压平）。 */
.td-tf {
  position: relative; display: flex; align-items: center;
  height: calc(28px * var(--ui-fs-ratio)); min-height: calc(28px * var(--ui-fs-ratio));
  box-sizing: border-box; border-radius: 4px;
  font-size: var(--font-size-body-2); color: var(--color-text-1);
  white-space: nowrap; overflow: hidden; cursor: pointer;
}
.td-tf.is-dir { padding-left: calc(7.5px + var(--d, 0) * 20px); }
.td-tf.is-file { padding-left: calc(8px + var(--d, 0) * 20px); }
.td-tf:hover { background: var(--color-fill-2); }
.td-tf.is-active { background: var(--color-primary-light-1); color: var(--color-primary-6); }
.td-tf.is-hidden { display: none; }
.td-tf-arrow {
  flex: none; width: 13px; height: 13px; padding: 0; border: 0; background: transparent;
  display: inline-flex; align-items: center; justify-content: center;
  color: var(--color-text-2); cursor: pointer;
}
.td-tf-arrow svg { transition: transform 120ms var(--transition-timing-function-standard, ease); }
.td-tf.is-closed > .td-tf-arrow svg { transform: rotate(-90deg); }
.td-tf.is-dir > .td-tf-arrow { margin-right: 7.5px; }
.td-tf-ico { flex: none; width: 13px; height: 13px; color: var(--color-text-2); }
.td-tf.is-dir > .td-tf-ico { margin-right: 7.5px; }
.td-tf.is-file > .td-tf-ico { margin-right: 10px; }
.td-tf-name { overflow: hidden; text-overflow: ellipsis; }
/* r108-l1 */
"""


def patch_css():
    tail(PCS, '/* r108-l1 */', CSS_NEW, 'panel.css 第 18 节（卡片化 + 抽屉）')


# ================================================================================
# 3. panel.js —— 抽屉控制器 + Esc 裁决链
# ================================================================================
JS_NEW = """  /* ==================== 文件树抽屉（第十二拍 ②） ====================
     对照 Codex「文件」入口补的一件：审查工具条里「在文件树中定位」**右侧**那枚按钮，
     点开 = 从右栏右缘滑入一层文件树抽屉，**不打断当前正在看的模块**（不必切到「文件」标签）。
     ★★ 树行用**独立类名 `td-tf`**（不是 `td-bf`）：ctrl-conv.js 的
        `pane.querySelectorAll('.td-bf')` 作用域是整个 `.td-browse`，复用同名类会把抽屉里的
        行一并接管（refresh / selectFile 互相打架；且它那个 `files` 变量只绑**第一个**
        `.td-browse-files` ⇒ 抽屉里的行点了没反应）。这里重写一套同语义的展开/折叠 + 选中。
     ⚠ 「点那枚按钮」必须 stopPropagation：否则会冒到下面 document 那条 closeMenus 上，
        把刚开的抽屉当「点了别处」立刻关掉。
     ⚠ 开 / 关都走 `hidden` + `is-open` 两条（CSS 那边的过渡需要「先摘 hidden 再挂类」的
        两帧节奏）⇒ 这里显式 `void offsetWidth` 强制一次 reflow 当分帧。 */
  var treeEl = pane.querySelector('[data-td-tree]');
  var treeFiles = treeEl ? treeEl.querySelector('.td-tree-files') : null;
  var treeBtn = pane.querySelector('[data-td-rv-act="tree"]');

  /* 展开 / 折叠：只认「祖先链上有没有 closed 的目录」（与 ctrl-conv 的 refresh() 同口径），
     作用域锁在抽屉自己这棵树里。 */
  function treeRefresh() {
    if (!treeFiles) return;
    var rows = treeFiles.querySelectorAll('.td-tf'), i;
    for (i = 0; i < rows.length; i++) {
      var p = rows[i].dataset.parent || '', ok = true;
      while (p) {
        var pr = treeFiles.querySelector('.td-tf[data-node="' + p + '"]');
        if (!pr || pr.classList.contains('is-closed')) { ok = false; break; }
        p = pr.dataset.parent || '';
      }
      rows[i].classList.toggle('is-hidden', !ok);
    }
  }

  function treeShow() {
    if (!treeEl || !treeEl.hasAttribute('hidden')) return;
    treeEl.removeAttribute('hidden');
    void treeEl.offsetWidth;                       /* 强制 reflow ⇒ 让下一行成为「下一帧」 */
    treeEl.classList.add('is-open');
    if (treeBtn) treeBtn.setAttribute('aria-expanded', 'true');
    treeRefresh();
  }

  function treeHide() {
    if (!treeEl || treeEl.hasAttribute('hidden')) return;
    treeEl.classList.remove('is-open');
    if (treeBtn) treeBtn.setAttribute('aria-expanded', 'false');
    /* 等过渡播完（220ms）再摘 `hidden` —— 否则关闭动作是「瞬间消失」，看不出抽屉在滑出；
       期间若又被打开（`is-open` 回到身上），这一下就不摘。 */
    setTimeout(function () {
      if (!treeEl.classList.contains('is-open')) treeEl.setAttribute('hidden', '');
    }, 240);
  }

  if (treeEl) {
    if (treeBtn) {
      treeBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (treeEl.hasAttribute('hidden')) treeShow(); else treeHide();
      });
    }
    var treeXs = treeEl.querySelectorAll('[data-td-tree-x]');
    for (var tx = 0; tx < treeXs.length; tx++) {
      treeXs[tx].addEventListener('click', function (e) { e.stopPropagation(); treeHide(); });
    }
    if (treeFiles) {
      treeFiles.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.td-tf') : null;
        if (!row) return;
        if (row.classList.contains('is-dir')) {
          var closed = row.classList.toggle('is-closed');
          row.setAttribute('aria-expanded', closed ? 'false' : 'true');
          treeRefresh();
        } else {
          var old = treeFiles.querySelector('.td-tf.is-active');
          if (old) { old.classList.remove('is-active'); old.setAttribute('aria-selected', 'false'); }
          row.classList.add('is-active');
          row.setAttribute('aria-selected', 'true');
        }
      });
      treeRefresh();
    }
    /* 点右栏里别处 = 收抽屉（与右栏四枚下拉共用「点空白收起」的口径）。
       ⚠ 判据用 `.td-tree`（抽屉整层）而不是 `.td-tree-panel`：点遮罩时由 scrim 自己的
         处理器关，这里放行即可。 */
    document.addEventListener('click', function (e) {
      if (treeEl.hasAttribute('hidden')) return;
      if (e.target && e.target.closest && e.target.closest('.td-tree')) return;
      treeHide();
    });
  }

  /* ==================== 初始化 ==================== */
"""

ESC_OLD = """    var prevOpen = prevEl && !prevEl.hasAttribute('hidden');
    if (!modal && !menuOpen && !noteOpen && !selOpen && !prevOpen) return;
    e.preventDefault();
    e.stopPropagation();
    if (selOpen) { selHide(); return; }
    if (modal) { commitModal.setAttribute('hidden', ''); return; }
    if (menuOpen) { closeMenus(null); return; }"""

ESC_NEW = """    var prevOpen = prevEl && !prevEl.hasAttribute('hidden');
    /* ★ 第十二拍 ②：文件树抽屉也占一层 —— 顺序与 z-index 同序
       （提交模态 40 → 抽屉 35 → 菜单 30）。不接进来的话，开着抽屉按 Esc 会直接
       落到 ctrl-conv 的 Esc 上**把整条侧栏关掉**。 */
    var treeOpen = treeEl && !treeEl.hasAttribute('hidden');
    if (!modal && !menuOpen && !noteOpen && !selOpen && !prevOpen && !treeOpen) return;
    e.preventDefault();
    e.stopPropagation();
    if (selOpen) { selHide(); return; }
    if (modal) { commitModal.setAttribute('hidden', ''); return; }
    if (treeOpen) { treeHide(); return; }
    if (menuOpen) { closeMenus(null); return; }"""


ACT_OLD = """        var kind = b.getAttribute('data-td-rv-act');
        closeMenus(null);
        if (kind === 'reveal') { openTab('files'); say(ACT_TEXT.reveal); return; }"""

ACT_NEW = """        var kind = b.getAttribute('data-td-rv-act');
        closeMenus(null);
        /* ★ 第十二拍 ②：`tree` = 文件树抽屉的开关。抽屉自带开合与视觉反馈 ⇒ 这里放行，
           否则会落到下面那句 `say(ACT_TEXT[kind] || '已执行')` 上弹一个没意义的「已执行」
           （ACT_TEXT 表里没有 tree 这一项）。 */
        if (kind === 'tree') return;
        if (kind === 'reveal') { openTab('files'); say(ACT_TEXT.reveal); return; }"""


def patch_js():
    edit(PJS, '  /* ==================== 初始化 ==================== */\n', JS_NEW,
         'panel.js 抽屉控制器（插在初始化段之前）', 'function treeHide()')
    edit(PJS, ESC_OLD, ESC_NEW, 'panel.js Esc 裁决链加抽屉一层', 'var treeOpen =')
    edit(PJS, ACT_OLD, ACT_NEW,
         'panel.js 「文件树」按钮不吃旧的 [data-td-rv-act] 通用循环（别弹「已执行」）',
         "if (kind === 'tree') return;")


def main():
    print('== r108 第十二拍补丁 ==')
    patch_mods()
    patch_css()
    patch_js()
    print('   应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for lbl in SKIPPED:
        print('     · 跳过：%s' % lbl)


if __name__ == '__main__':
    main()
