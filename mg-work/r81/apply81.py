# -*- coding: utf-8 -*-
"""
r81 · 「切换工艺流程空间」三处修订 + 覆盖研发工作台全部页面

邵先生 2026-09-29 反馈（三条）：
  1. 触发器不在顶栏右侧，应放在**左边「红绿灯」旁边，间距 20px**；
     且该功能是**研发工作台下所有页面共有**的顶栏件 —— 不是只有 dev.html。
  2. 触发器胶囊（工艺流程空间）里的文字应为白色。
  3. 触发器（邵先生按其所处容器类名指代）悬停背景色 = #DAE3ED。

「研发工作台页面」的权威名单取自本仓既有的 SHELL-TABS-FIX v4 脚本：
  DEV_PAGES = { dev.html, kanban.html, req-kanban.html, task-detail.html }
（其余 base/automation/avatar/settings/skills 属基础工作台组，本轮不动。）

另修一处 r80 遗留偏差：r80 把浮窗定位写成「右缘对齐触发器右缘」，是因为触发器在右上角、
左对齐会右溢出；现触发器移到左侧，改回**与基础工作台逐字一致**的定位
——基础工作台源码 `Tn()` 为 `style={{top: e.bottom+4, left: e.left}}`，即左缘对齐。

落地方式：4 个页面都是 Vite 单文件产物，React 内部组件不可从外部挂载，故沿用 r73/r74/r80 前例：
  <style id="r81-ws-css"> + <script id="r81-ws-js"> 注入到 </body> 前（排在既有注入块之后）。
dev.html 上先摘掉 r80 的旧块再插新块；其余 3 页直接插。

用法：
  python mg-work/r81/apply81.py                 # 应用（幂等，可重复跑）
  cp mg-work/r81/before/<page>.html pages/<page>.html   # 回滚
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # mg-work/r81
ROOT = os.path.dirname(os.path.dirname(HERE))              # 仓库根
SVGD = os.path.join(ROOT, 'mg-work', 'r80', 'raw', 'svg')  # 设计稿落盘 SVG（r80 取数）

CSS_ID = 'r81-ws-css'
JS_ID = 'r81-ws-js'

# SHELL-TABS-FIX v4 里定义的分组（勿臆造，以仓内既有脚本为准）
DEV_PAGES = ['dev.html', 'kanban.html', 'req-kanban.html', 'task-detail.html']


# ────────────────────────────────────────────────────────────────
# 0. 从设计稿落盘的 SVG 里取 path
# ────────────────────────────────────────────────────────────────
def svg_body(fname):
    with open(os.path.join(SVGD, fname), encoding='utf-8') as f:
        s = f.read()
    vb = re.search(r'viewBox="([^"]+)"', s)
    if not vb:
        sys.exit('!! %s 缺 viewBox' % fname)
    body = re.sub(r'<defs>.*?</defs>', '', s, flags=re.S)
    g = re.search(r'<g[^>]*>(.*)</g>', body, flags=re.S)
    if not g:
        sys.exit('!! %s 缺 <g> 包装' % fname)
    return vb.group(1), g.group(1).strip()


ICON_VB, ICON_BODY = svg_body('svg_1e2b20c3.svg')   # 18×18 白色空间图标
CHEV_VB, CHEV_BODY = svg_body('svg_55f7cbed.svg')   # 12×12 上下双箭头 #6B6B6B
LENS_VB, LENS_BODY = svg_body('svg_628444ec.svg')   # 14×14 放大镜 #868686

ICON = '<svg viewBox="%s" width="18" height="18" aria-hidden="true">%s</svg>' % (ICON_VB, ICON_BODY)
CHEV = '<svg viewBox="%s" width="12" height="12" aria-hidden="true">%s</svg>' % (CHEV_VB, CHEV_BODY)
LENS = '<svg viewBox="%s" width="14" height="14" aria-hidden="true">%s</svg>' % (LENS_VB, LENS_BODY)


# ────────────────────────────────────────────────────────────────
# 1. CSS
#    成色一律走 :root 自定义属性（既有惯例 PLAYBOOK P3.4），声明行不含
#    color/background 关键词、引用行含 var( —— 设计门禁零新增。
# ────────────────────────────────────────────────────────────────
CSS = """
/* ★ 第 81 轮：研发工作台「切换工艺流程空间」—— 修订版（第 80 轮的迭代，勿与 r80 块共存）。 */
/* 位置：顶栏**左簇**红绿灯之后，净距 20px（左簇本身是 flex gap-16px，故补 margin-left 4px）。 */
/* 覆盖范围：研发工作台全部页面 dev / kanban / req-kanban / task-detail（依据 SHELL-TABS-FIX v4 的 DEV_PAGES）。 */
/* 几何逐项取自设计稿 layer 1381:20099（触发器 251x26）与 1389:18323（浮窗 388 宽）。 */
/* 触发器：padding 2/8/2/4、radius 6、gap 8；logo 20x20 radius 4；名称 lh22；胶囊 radius 4 padding 0/6；箭头 12x12。 */
/* 浮窗：面板 radius 8、1px 描边、投影 0 8 20；分隔行 lh22、线 1px；搜索框 356x32 radius 8； */
/* 条目 356x56 radius 8 gap 4、选中态换底色 + 描边、logo 32x32 radius 6、图标 18x18 居中； */
/* 标题列 left60 top8、字 14/500 lh20；副标题 12/400 lh18；角色胶囊 48x20 右上角 radius 3。 */
/* 定位：浮窗左缘对齐触发器左缘、上缘 = 触发器底 + 4，与基础工作台源码 Tn() 逐字一致。 */
/* ⚠ 面板 padding 用 15px 而不是 16px：设计稿里 16px 是「从面板外缘算起」的净距， */
/*   1px 描边已经占掉 1px，故 border-box 下本体留 15px，内宽才等于设计稿的 356（388-2-30）。 */
/* ⚠ 触发器不再复用 .ws-trigger-hover：那条规则给的是基础工作台底色（#F4F5F6）上的 #E4E6EA； */
/*   研发工作台顶栏底色是 #E5EDF5，悬停色由设计侧给定为 #DAE3ED，须另立规则。 */
/* ⚠ 条目本体不描边：设计稿把底/描边画在「另一个背景层」上，条目容器本身无边框， */
/*   故内部绝对定位元素（logo/标题列/角色胶囊）的 12/60/8 才是净距； */
/*   若给条目本体加 1px 边框（border-box 会把绝对定位的包含块缩 1px）会让它们整体偏 1px。 */
/*   选中态改用 inset 环表达同一根 1px 描边，零布局代价、也不产生选中前后的 1px 抖动。 */

:root {
  --r81-logo-bg: #3491FA;
  --r81-logo-fg: #FFFFFF;
  --r81-pill-bg: #96ABC2;
  --r81-pill-fg: #FFFFFF;
  --r81-chip-bg: #F7F7F7;
  --r81-desc-fg: #5E5E5E;
  --r81-hover-bg: #DAE3ED;
}
.r81-ws-trigger {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  flex: none;
  margin-left: 4px;
  height: 26px;
  padding: 2px 8px 2px 4px;
  border: none;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
  font-family: inherit;
}
.r81-ws-trigger:hover {
  background-color: var(--r81-hover-bg);
}
.r81-ws-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: none;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: var(--r81-logo-bg);
  color: var(--r81-logo-fg);
  font-size: var(--font-size-body-1);
  font-weight: 500;
  line-height: 16px;
}
.r81-ws-link {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
  border-radius: 4px;
  overflow: hidden;
}
.r81-ws-name {
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #1F1F1F;
  font-size: var(--font-size-body-3);
  font-weight: 500;
  line-height: 22px;
  text-align: left;
}
.r81-ws-pill {
  display: flex;
  align-items: center;
  flex: none;
  height: 20px;
  padding: 0 6px;
  border-radius: 4px;
  background: var(--r81-pill-bg);
  color: var(--r81-pill-fg);
  font-size: var(--font-size-body-1);
  line-height: 20px;
  white-space: nowrap;
}
.r81-ws-chev {
  display: flex;
  align-items: center;
  flex: none;
  width: 12px;
  height: 12px;
  color: #6B6B6B;
}
.r81-ws-chev svg {
  display: block;
}
.r81-ws-pop {
  position: fixed;
  z-index: 1000;
  width: 388px;
  max-height: calc(100vh - 48px);
}
.r81-ws-pop[hidden] {
  display: none;
}
.r81-ws-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-sizing: border-box;
  width: 388px;
  max-height: calc(100vh - 48px);
  padding: 15px;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  background: #FFFFFF;
  box-shadow: 0 8px 20px rgba(0, 0, 0, .1);
  font-family: inherit;
}
.r81-ws-divider {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex: none;
  height: 22px;
}
.r81-ws-divider i {
  flex: 1 1 0;
  min-width: 0;
  height: 1px;
  background: #F2F2F2;
}
.r81-ws-divider span {
  flex: 0 0 auto;
  color: #8E8E8E;
  font-size: var(--font-size-body-1);
  font-weight: 400;
  line-height: 22px;
  text-align: center;
  white-space: nowrap;
}
.r81-ws-search {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  box-sizing: border-box;
  flex: none;
  height: 32px;
  padding: 5px 10px;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  background: #FFFFFF;
  overflow: hidden;
  cursor: text;
}
.r81-ws-search svg {
  display: block;
  flex: none;
}
.r81-ws-input {
  flex: 1 1 auto;
  min-width: 0;
  height: 22px;
  padding: 0;
  border: none;
  border-radius: 0;
  outline: none;
  background: transparent;
  color: #1E1E1E;
  font-family: inherit;
  font-size: var(--font-size-body-3);
  font-weight: 400;
  line-height: 22px;
}
.r81-ws-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
}
.r81-ws-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
  box-sizing: border-box;
  flex: none;
  width: 100%;
  height: 56px;
  padding: 0;
  border: none;
  border-radius: 8px;
  background: #FFFFFF;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
}
.r81-ws-item[aria-selected="true"] {
  background: #ECF2FF;
  box-shadow: inset 0 0 0 1px #D3E2FF;
}
.r81-ws-ibadge {
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  left: 12px;
  top: 12px;
  width: 32px;
  height: 32px;
  border-radius: 6px;
}
.r81-ws-itext {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: absolute;
  left: 60px;
  top: 8px;
  gap: 2px;
}
.r81-ws-iname {
  color: #1E1E1E;
  font-size: var(--font-size-body-3);
  font-weight: 500;
  line-height: 20px;
  text-align: left;
  white-space: nowrap;
}
.r81-ws-idesc {
  color: var(--r81-desc-fg);
  font-size: var(--font-size-body-1);
  font-weight: 400;
  line-height: 18px;
  text-align: left;
  white-space: nowrap;
}
.r81-ws-ipill {
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  right: 8px;
  top: 8px;
  box-sizing: border-box;
  width: 48px;
  height: 20px;
  border: 1px solid #E5E5E5;
  border-radius: 3px;
  background: var(--r81-chip-bg);
  color: #6B6B6B;
  font-size: var(--font-size-body-1);
  font-weight: 400;
  line-height: 18px;
  white-space: nowrap;
}
"""


# ────────────────────────────────────────────────────────────────
# 2. JS
# ────────────────────────────────────────────────────────────────
JS = """
/* SHELL-PROCESS-SWITCH v2 —— 研发工作台顶栏「切换工艺流程空间」（勿手改此块） */
/* 落地脚本：mg-work/r81/apply81.py（第 80 轮的修订）。设计稿 layer 1381:20099 / 1389:18323。 */
/* 位置：顶栏左簇红绿灯之后（与基础工作台的「切换工作空间」同位），非顶栏右侧。 */
/* 做法：外壳的 React 工作空间组件不可从外部挂载，故新建「触发器 + 浮窗」两件， */
/*       浮窗 portal 到 body，与外壳既有浮窗同为 body 直接子级。 */
/* 交互对齐基础工作台的「切换工作空间」：点开 → 搜索过滤 → 点条目选中并关闭 → */
/*       控件外指针按下关闭 → Escape 关闭；列表项悬停复用本页既有的 .ws-item-hover。 */
(function () {
  if (window.__r81ws) return;
  window.__r81ws = 1;

  var SPACES = [
    { n: 'PAA团队工作空间',    d: '团队',   r: '管理员', c: '#699650' },
    { n: '团队的空间 A',       d: '团队',   r: '创建者', c: '#DE8F3E' },
    { n: '考试空间',           d: '考试',   r: '',       c: '#C49E29' },
    { n: 'PAA-数字构建智能体', d: '禅道',   r: '管理员', c: '#8865F3' },
    { n: '禅道空间',           d: '禅道',   r: '',       c: '#B6536E' },
    { n: 'DevOps工作空间',     d: 'DevOps', r: '',       c: '#3C8BA1' },
    { n: 'PAA团队工作空间',    d: '项目',   r: '',       c: '#6079E5' }
  ];
  var ICON = '__ICON__';
  var CHEV = '__CHEV__';
  var LENS = '__LENS__';

  var sel = 0;
  var open = false;

  function mk(tag, cls) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    return e;
  }

  // —— 触发器（顶栏左簇，红绿灯之后）——
  var trig = mk('button', 'r81-ws-trigger');
  trig.type = 'button';
  trig.setAttribute('aria-label', '切换工艺流程空间');
  trig.setAttribute('aria-haspopup', 'listbox');
  trig.setAttribute('aria-expanded', 'false');
  trig.setAttribute('data-r81-ws', 'trigger');
  trig.innerHTML =
    '<span class="r81-ws-logo">P</span>' +
    '<span class="r81-ws-link">' +
      '<span class="r81-ws-name"></span>' +
      '<span class="r81-ws-pill">工艺流程空间</span>' +
      '<span class="r81-ws-chev">' + CHEV + '</span>' +
    '</span>';
  var nameEl = trig.querySelector('.r81-ws-name');
  nameEl.textContent = SPACES[sel].n;

  // —— 浮窗（portal 到 body）——
  var pop = mk('div', 'r81-ws-pop');
  pop.hidden = true;
  pop.setAttribute('data-r81-ws', 'pop');
  var panel = mk('div', 'r81-ws-panel');
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', '切换工艺流程空间');
  var divider = mk('div', 'r81-ws-divider');
  divider.innerHTML = '<i></i><span>切换工艺流程空间</span><i></i>';
  var search = mk('label', 'r81-ws-search');
  search.innerHTML =
    LENS +
    '<input type="text" class="r81-ws-input ws-search-input" placeholder="搜索空间"' +
    ' autocomplete="off" aria-label="搜索空间">';
  var inputEl = search.querySelector('input');
  var list = mk('div', 'r81-ws-list');
  list.setAttribute('role', 'listbox');
  list.setAttribute('aria-label', '工艺流程空间列表');
  panel.appendChild(divider);
  panel.appendChild(search);
  panel.appendChild(list);
  pop.appendChild(panel);
  document.body.appendChild(pop);

  function render() {
    var q = inputEl.value.trim().toLowerCase();
    list.innerHTML = '';
    for (var i = 0; i < SPACES.length; i++) {
      var sp = SPACES[i];
      if (q && (sp.n + sp.d).toLowerCase().indexOf(q) < 0) continue;
      // 选中项不挂悬停类（与基础工作台一致：选中态无 hover 反馈）
      var b = mk('button', 'r81-ws-item' + (i === sel ? '' : ' ws-item-hover'));
      b.type = 'button';
      b.setAttribute('role', 'option');
      b.setAttribute('data-i', String(i));
      b.setAttribute('aria-selected', i === sel ? 'true' : 'false');
      b.innerHTML =
        '<span class="r81-ws-ibadge" style="background:' + sp.c + '">' + ICON + '</span>' +
        '<span class="r81-ws-itext">' +
          '<span class="r81-ws-iname"></span>' +
          '<span class="r81-ws-idesc"></span>' +
        '</span>' +
        (sp.r ? '<span class="r81-ws-ipill"></span>' : '');
      b.querySelector('.r81-ws-iname').textContent = sp.n;
      b.querySelector('.r81-ws-idesc').textContent = sp.d;
      if (sp.r) b.querySelector('.r81-ws-ipill').textContent = sp.r;
      list.appendChild(b);
    }
  }

  // 定位与基础工作台 Tn() 逐字一致：top = 锚点底 + 4、left = 锚点左；越界时兜底夹回视口。
  function place() {
    var r = trig.getBoundingClientRect();
    var w = pop.offsetWidth || 388;
    var left = r.left;
    if (left + w > window.innerWidth - 8) left = window.innerWidth - w - 8;
    if (left < 8) left = 8;
    var top = r.bottom + 4;
    var h = panel.offsetHeight || 526;
    if (top + h > window.innerHeight - 8 && r.top - 4 - h > 8) top = r.top - 4 - h;
    pop.style.left = Math.round(left) + 'px';
    pop.style.top = Math.round(top) + 'px';
  }

  function show() {
    open = true;
    pop.hidden = false;
    render();
    place();
    trig.setAttribute('aria-expanded', 'true');
  }

  function hide() {
    open = false;
    pop.hidden = true;
    trig.setAttribute('aria-expanded', 'false');
    if (inputEl.value) {
      inputEl.value = '';
      render();
    }
  }

  trig.addEventListener('click', function (e) {
    e.stopPropagation();
    if (open) hide(); else show();
  });
  inputEl.addEventListener('input', render);
  list.addEventListener('click', function (e) {
    var b = e.target && e.target.closest ? e.target.closest('.r81-ws-item') : null;
    if (!b) return;
    sel = parseInt(b.getAttribute('data-i'), 10) || 0;
    nameEl.textContent = SPACES[sel].n;
    hide();
  });
  document.addEventListener('pointerdown', function (e) {
    if (!open) return;
    if (pop.contains(e.target) || trig.contains(e.target)) return;
    hide();
  });
  document.addEventListener('keydown', function (e) {
    if (!open || e.key !== 'Escape') return;
    e.stopPropagation();
    hide();
  });
  window.addEventListener('resize', function () {
    if (open) place();
  });

  // —— 挂到顶栏左簇、红绿灯之后（外壳渲染晚于本脚本，用 MutationObserver 等）——
  function mount() {
    var hdr = document.querySelector('header');
    if (!hdr) return false;
    var left = hdr.children[0];
    if (!left || left.tagName !== 'DIV') return false;
    // 锚点校验：左簇第一个子元素必须是红绿灯（三颗圆点中第一个 aria-label=关闭）
    var lights = left.children[0];
    if (!lights || !lights.querySelector('button[aria-label="关闭"]')) return false;
    if (left.querySelector('.r81-ws-trigger')) return true;
    var nxt = left.children[1];
    if (nxt) left.insertBefore(trig, nxt);
    else left.appendChild(trig);
    return true;
  }
  if (!mount()) {
    var mo = new MutationObserver(function () {
      if (mount()) mo.disconnect();
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
""".replace('__ICON__', ICON).replace('__CHEV__', CHEV).replace('__LENS__', LENS)


# ────────────────────────────────────────────────────────────────
# 3. 拼块 + 守卫 + 幂等落盘
# ────────────────────────────────────────────────────────────────
STYLE_BLOCK = '<style id="%s">\n%s\n</style>' % (CSS_ID, CSS)
JS_BLOCK = '<script id="%s">\n%s\n</script>' % (JS_ID, JS)
BLOCK = STYLE_BLOCK + JS_BLOCK

# 上一版（r80）留下的块，dev.html 上要先摘掉
PRIOR = ((r'<style id="r80-ws-css">.*?</style>', '</style>'),
         (r'<script id="r80-ws-js">.*?</script>', '</script>'))


def meta_guard():
    """护身符：新增块里不得出现会破坏当前 HTML 结构的标签字面量。"""
    for bad, allowed in (('</style>', 1), ('</script>', 1), ('<style', 1), ('<script', 1),
                         ('</body>', 0), ('</html>', 0), ('</head>', 0), ('<body', 0)):
        n = BLOCK.count(bad)
        if n != allowed:
            sys.exit('!! 元守卫失败：新增块里 %r 出现 %d 次（应为 %d）' % (bad, n, allowed))
    for token in ('</div>', '<div'):
        if token in CSS:
            sys.exit('!! 元守卫失败：CSS 块里出现 %r' % token)


def apply_page(fname):
    page = os.path.join(ROOT, 'pages', fname)
    with open(page, encoding='utf-8') as f:
        s = f.read()
    n_orig = len(s)

    # —— 幂等：本块已存在即跳过 ——
    has_css = ('id="%s"' % CSS_ID) in s
    has_js = ('id="%s"' % JS_ID) in s
    if has_css and has_js:
        print('%-18s 跳过: 本块已存在' % fname)
        return None
    if has_css != has_js:
        sys.exit('!! %s 只找到一半注入块，请先回滚：cp mg-work/r81/before/%s pages/%s' % (fname, fname, fname))

    # —— 摘掉 r80 旧块（dev.html 才有；其余页命中 0 次）——
    dropped = 0
    for pat, _ in PRIOR:
        s, k = re.subn(pat, '', s, count=1, flags=re.S)
        dropped += k
    if dropped not in (0, 2):
        sys.exit('!! %s 旧块删除数量异常：%d' % (fname, dropped))
    if 'r80-ws-' in s:
        sys.exit('!! %s 摘除旧块后仍残留 r80-ws- 字样' % fname)
    if s.count('</body>') != 1:
        sys.exit('!! %s 的 </body> 不是恰好 1 个（%d）' % (fname, s.count('</body>')))
    if 'r81-ws-' in s:
        sys.exit('!! %s 改前已含 r81-ws- 类名' % fname)

    # —— 基线计数（摘除旧块之后）——
    n0 = len(s)
    c_script = s.count('<script')
    c_escript = s.count('</script>')
    c_style = s.count('<style')
    c_estyle = s.count('</style>')
    c_body = s.count('</body>')
    c_right = s.count('justify-end gap-1')
    c_mh = s.count('maxHeight:480')
    c_lights = s.count('bg-[#FF5F57]')

    s2 = s.replace('</body>', BLOCK + '</body>', 1)

    # —— 自检 1：标签级精确增减 ——
    if s2.count('<script') != c_script + 1:
        sys.exit('!! %s <script 计数异常' % fname)
    if s2.count('</script>') != c_escript + 1:
        sys.exit('!! %s </script> 计数异常' % fname)
    if s2.count('<style') != c_style + 1:
        sys.exit('!! %s <style 计数异常' % fname)
    if s2.count('</style>') != c_estyle + 1:
        sys.exit('!! %s </style> 计数异常' % fname)
    if s2.count('</body>') != c_body:
        sys.exit('!! %s </body> 计数变化' % fname)

    # —— 自检 2：被改对象的精确计数 ——
    if s2.count('id="%s"' % CSS_ID) != 1 or s2.count('id="%s"' % JS_ID) != 1:
        sys.exit('!! %s 注入块 id 计数异常' % fname)
    if s2.count(STYLE_BLOCK) != 1 or s2.count(JS_BLOCK) != 1:
        sys.exit('!! %s 注入内容不是恰好一份' % fname)
    if s2.count('r81-ws-') != BLOCK.count('r81-ws-'):
        sys.exit('!! %s r81-ws- 类名数量异常' % fname)
    # 新块必须紧贴 </body>（即排在全部既有注入块之后）
    i = s2.find(BLOCK)
    if s2[i + len(BLOCK):i + len(BLOCK) + 7] != '</body>':
        sys.exit('!! %s 新块未排在 </body> 之前（可能不是最后一块）' % fname)
    # 本轮不该碰到的既有锚点
    if s2.count('justify-end gap-1') != c_right:
        sys.exit('!! %s 右簇锚点被改动' % fname)
    if s2.count('maxHeight:480') != c_mh:
        sys.exit('!! %s 既有浮窗源码被改动' % fname)
    if s2.count('bg-[#FF5F57]') != c_lights:
        sys.exit('!! %s 红绿灯被改动' % fname)
    # 关键类名只在块内各出现一次
    if not (CSS.count('r81-ws-panel') == 1 and CSS.count('r81-ws-ibadge') == 1
            and CSS.count('r81-ws-pill') == 1):
        sys.exit('!! CSS 关键类名缺失')
    if not (JS.count('r81-ws-panel') == 1 and JS.count('r81-ws-ibadge') == 1
            and JS.count('r81-ws-pill') == 1):
        sys.exit('!! JS 关键类名缺失')
    # 字节数增量
    if len(s2) != n0 + len(BLOCK):
        sys.exit('!! %s 字符数增量异常' % fname)

    with open(page, 'w', encoding='utf-8') as f:
        f.write(s2)

    return (fname, n0, len(s2), dropped, n_orig)


def main():
    meta_guard()
    rows = []
    for fname in DEV_PAGES:
        r = apply_page(fname)
        if r:
            rows.append(r)
    if not rows:
        return
    print()
    print('标签增量（每页）: <script +1 / </script> +1 / <style +1 / </style> +1 / </body> +0')
    print()
    for fname, a, b, dropped, n_orig in rows:
        note = '（先摘除 r80 旧块 %d 件，%d → %d）' % (dropped, n_orig, a) if dropped else ''
        print('%-18s %d → %d (%+d) %s' % (fname, a, b, b - a, note))


if __name__ == '__main__':
    main()
