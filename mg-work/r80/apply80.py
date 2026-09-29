# -*- coding: utf-8 -*-
"""
r80 · 研发工作台右上角「切换工艺流程空间」

需求：研发工作台（pages/dev.html）右上角新增「切换工艺流程空间」，交互与基础工作台的
      「切换工作空间」完全一样。
设计稿：
  · 触发器  page_id=pu489:07981 layer=1381:20099
  · 浮窗    page_id=pu489:07981 layer=1389:18323
取数通道：本地 mastergo-mcp HTTP 端点（见 PLAYBOOK P7），落盘 mg-work/r80/raw/。

落地方式：dev.html 是 Vite 单文件产物，React 内部的工作空间组件不可从外部挂载，
          顶栏右簇是空壳（div.flex.w-60.items-center.justify-end，children=0），
          故沿用本仓既有前例（r73/r74 页尾脚本）：注入
            <style id="r80-ws-css">  … 页尾最后一块（同特异性下后者胜）
            <script id="r80-ws-js">   … </body> 前，MutationObserver 等外壳渲染
          两件都带唯一 id，幂等。

用法：
  python mg-work/r80/apply80.py            # 应用（幂等，可重复跑）
  cp mg-work/r80/before/dev.html pages/dev.html   # 回滚
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # mg-work/r80
ROOT = os.path.dirname(os.path.dirname(HERE))              # 仓库根
PAGE = os.path.join(ROOT, 'pages', 'dev.html')
SVGD = os.path.join(HERE, 'raw', 'svg')

CSS_ID = 'r80-ws-css'
JS_ID = 'r80-ws-js'


# ────────────────────────────────────────────────────────────────
# 0. 从设计稿落盘的 SVG 里取 path（避免手抄长路径出错）
# ────────────────────────────────────────────────────────────────
def svg_body(fname):
    """返回 (viewBox, 去掉 defs/clipPath 包装后的内容)。设计稿里 clipPath 都是整幅矩形（no-op），
    去掉后同一段 SVG 可安全重复使用（无重复 id）。"""
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
#    说明：成色变量（设计稿 DevMode 直出、DS 无对应 token）提到自定义属性上，
#          既有惯例见 PLAYBOOK P3.4「把可变数值提到自定义属性上」。
#          悬停反馈复用本页既有的 .ws-trigger-hover / .ws-item-hover / .ws-search-input::placeholder。
# ────────────────────────────────────────────────────────────────
CSS = """
/* ★ 第 80 轮：研发工作台右上角「切换工艺流程空间」。 */
/* 几何逐项取自设计稿 layer 1381:20099（触发器 251x26）与 1389:18323（浮窗 388 宽）。 */
/* 触发器：padding 2/8/2/4、radius 6、gap 8；logo 20x20 radius 4；名称 lh22；胶囊 radius 4 padding 0/6；箭头 12x12。 */
/* 浮窗：面板 radius 8、1px 描边、投影 0 8 20；分隔行 lh22、线 1px；搜索框 356x32 radius 8； */
/* 条目 356x56 radius 8 gap 4、选中态换底色 + 描边、logo 32x32 radius 6、图标 18x18 居中； */
/* 标题列 left60 top8、字 14/500 lh20；副标题 12/400 lh18；角色胶囊 48x20 右上角 radius 3。 */
/* ⚠ 面板 padding 用 15px 而不是 16px：设计稿里 16px 是「从面板外缘算起」的净距， */
/*   1px 描边已经占掉 1px，故 border-box 下本体留 15px，内宽才等于设计稿的 356（388-2-30）。 */
/* 悬停反馈沿用本页既有悬停类，不再自造同色规则。 */
/* 定位：浮窗右缘对齐触发器右缘（触发器在右上角，沿用左对齐会右溢出视口）。 */

:root {
  --r80-logo-bg: #3491FA;
  --r80-pill-bg: #96ABC2;
  --r80-chip-bg: #F7F7F7;
  --r80-desc-fg: #5E5E5E;
}
.r80-ws-trigger {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  flex: none;
  height: 26px;
  padding: 2px 8px 2px 4px;
  border: none;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
  font-family: inherit;
}
.r80-ws-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: none;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: var(--r80-logo-bg);
  color: #FFFFFF;
  font-size: var(--font-size-body-1);
  font-weight: 500;
  line-height: 16px;
}
.r80-ws-link {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
  border-radius: 4px;
  overflow: hidden;
}
.r80-ws-name {
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
.r80-ws-pill {
  display: flex;
  align-items: center;
  flex: none;
  height: 20px;
  padding: 0 6px;
  border-radius: 4px;
  background: var(--r80-pill-bg);
  color: #1F1F1F;
  font-size: var(--font-size-body-1);
  line-height: 20px;
  white-space: nowrap;
}
.r80-ws-chev {
  display: flex;
  align-items: center;
  flex: none;
  width: 12px;
  height: 12px;
  color: #6B6B6B;
}
.r80-ws-chev svg {
  display: block;
}
.r80-ws-pop {
  position: fixed;
  z-index: 1000;
  width: 388px;
  max-height: calc(100vh - 48px);
}
.r80-ws-pop[hidden] {
  display: none;
}
.r80-ws-panel {
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
.r80-ws-divider {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex: none;
  height: 22px;
}
.r80-ws-divider i {
  flex: 1 1 0;
  min-width: 0;
  height: 1px;
  background: #F2F2F2;
}
.r80-ws-divider span {
  flex: 0 0 auto;
  color: #8E8E8E;
  font-size: var(--font-size-body-1);
  font-weight: 400;
  line-height: 22px;
  text-align: center;
  white-space: nowrap;
}
.r80-ws-search {
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
.r80-ws-search svg {
  display: block;
  flex: none;
}
.r80-ws-input {
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
.r80-ws-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
}
/* ⚠ 条目本体不描边：设计稿把底/描边画在「另一个背景层」上，条目容器本身无边框， */
/*   故内部绝对定位元素（logo/标题列/角色胶囊）的 12/60/8 才是净距； */
/*   若给条目本体加 1px 边框（border-box 会把绝对定位的包含块缩 1px）会让它们整体偏 1px。 */
/*   选中态改用 inset 环表达同一根 1px 描边，零布局代价、也不产生选中前后的 1px 抖动。 */
.r80-ws-item {
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
.r80-ws-item[aria-selected="true"] {
  background: #ECF2FF;
  box-shadow: inset 0 0 0 1px #D3E2FF;
}
.r80-ws-ibadge {
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
.r80-ws-itext {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: absolute;
  left: 60px;
  top: 8px;
  gap: 2px;
}
.r80-ws-iname {
  color: #1E1E1E;
  font-size: var(--font-size-body-3);
  font-weight: 500;
  line-height: 20px;
  text-align: left;
  white-space: nowrap;
}
.r80-ws-idesc {
  color: var(--r80-desc-fg);
  font-size: var(--font-size-body-1);
  font-weight: 400;
  line-height: 18px;
  text-align: left;
  white-space: nowrap;
}
.r80-ws-ipill {
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
  background: var(--r80-chip-bg);
  color: #6B6B6B;
  font-size: var(--font-size-body-1);
  font-weight: 400;
  line-height: 18px;
  white-space: nowrap;
}
"""


# ────────────────────────────────────────────────────────────────
# 2. JS
#    列表数据 = 设计稿现值：7 个 logo 底色 + 角色胶囊（管理员/创建者/管理员）取自设计稿，
#    名称/副标题设计稿未导出（text/title 实例为空），按用户指示沿用现有 7 个工作空间名占位。
# ────────────────────────────────────────────────────────────────
JS = """
/* SHELL-PROCESS-SWITCH v1 —— 研发工作台右上角「切换工艺流程空间」（勿手改此块） */
/* 落地脚本：mg-work/r80/apply80.py。设计稿 layer 1381:20099 / 1389:18323。 */
/* 做法：顶栏右簇是空壳，没有可复用的 React 挂载点；故新建「触发器 + 浮窗」两件， */
/*       浮窗 portal 到 body（与外壳既有浮窗同为 body 直接子级、同样 z-index 层级）。 */
/* 交互对齐基础工作台的「切换工作空间」：点开 → 搜索过滤 → 点条目选中并关闭 → */
/*       控件外指针按下关闭 → Escape 关闭；悬停反馈复用本页既有的悬停类。 */
(function () {
  if (window.__r80ws) return;
  window.__r80ws = 1;

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

  // —— 触发器（右上角）——
  var trig = mk('button', 'r80-ws-trigger ws-trigger-hover');
  trig.type = 'button';
  trig.setAttribute('aria-label', '切换工艺流程空间');
  trig.setAttribute('aria-haspopup', 'listbox');
  trig.setAttribute('aria-expanded', 'false');
  trig.setAttribute('data-r80-ws', 'trigger');
  trig.innerHTML =
    '<span class="r80-ws-logo">P</span>' +
    '<span class="r80-ws-link">' +
      '<span class="r80-ws-name"></span>' +
      '<span class="r80-ws-pill">工艺流程空间</span>' +
      '<span class="r80-ws-chev">' + CHEV + '</span>' +
    '</span>';
  var nameEl = trig.querySelector('.r80-ws-name');
  nameEl.textContent = SPACES[sel].n;

  // —— 浮窗（portal 到 body）——
  var pop = mk('div', 'r80-ws-pop');
  pop.hidden = true;
  pop.setAttribute('data-r80-ws', 'pop');
  var panel = mk('div', 'r80-ws-panel');
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', '切换工艺流程空间');
  var divider = mk('div', 'r80-ws-divider');
  divider.innerHTML = '<i></i><span>切换工艺流程空间</span><i></i>';
  var search = mk('label', 'r80-ws-search');
  search.innerHTML =
    LENS +
    '<input type="text" class="r80-ws-input ws-search-input" placeholder="搜索空间"' +
    ' autocomplete="off" aria-label="搜索空间">';
  var inputEl = search.querySelector('input');
  var list = mk('div', 'r80-ws-list');
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
      var b = mk('button', 'r80-ws-item' + (i === sel ? '' : ' ws-item-hover'));
      b.type = 'button';
      b.setAttribute('role', 'option');
      b.setAttribute('data-i', String(i));
      b.setAttribute('aria-selected', i === sel ? 'true' : 'false');
      b.innerHTML =
        '<span class="r80-ws-ibadge" style="background:' + sp.c + '">' + ICON + '</span>' +
        '<span class="r80-ws-itext">' +
          '<span class="r80-ws-iname"></span>' +
          '<span class="r80-ws-idesc"></span>' +
        '</span>' +
        (sp.r ? '<span class="r80-ws-ipill"></span>' : '');
      b.querySelector('.r80-ws-iname').textContent = sp.n;
      b.querySelector('.r80-ws-idesc').textContent = sp.d;
      if (sp.r) b.querySelector('.r80-ws-ipill').textContent = sp.r;
      list.appendChild(b);
    }
  }

  function place() {
    var r = trig.getBoundingClientRect();
    var w = pop.offsetWidth || 388;
    var left = Math.min(r.right - w, window.innerWidth - w - 8);
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
    var b = e.target && e.target.closest ? e.target.closest('.r80-ws-item') : null;
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

  // —— 挂到顶栏右簇（外壳渲染晚于本脚本，用 MutationObserver 等）——
  function mount() {
    var host = document.querySelector('header > div[class~="justify-end"]');
    if (!host) return false;
    if (host.querySelector('.r80-ws-trigger')) return true;
    host.appendChild(trig);
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


def main():
    meta_guard()
    with open(PAGE, encoding='utf-8') as f:
        s = f.read()

    n0 = len(s)
    c_script = s.count('<script')
    c_escript = s.count('</script>')
    c_style = s.count('<style')
    c_estyle = s.count('</style>')
    c_body = s.count('</body>')

    # 幂等：本块已存在即跳过
    if 'id="%s"' % JS_ID in s or 'id="%s"' % CSS_ID in s:
        if 'id="%s"' % CSS_ID in s and 'id="%s"' % JS_ID in s:
            print('跳过: 本块已存在（%s / %s）' % (CSS_ID, JS_ID))
            return
        sys.exit('!! 只找到一半注入块，请先回滚：cp mg-work/r80/before/dev.html pages/dev.html')

    if s.count('</body>') != 1:
        sys.exit('!! </body> 不是恰好 1 个（%d）' % s.count('</body>'))
    if s.count('id="r80') != 0:
        sys.exit('!! 已存在 r80 标记')

    s2 = s.replace('</body>', BLOCK + '</body>', 1)

    # —— 自检（标签级精确增减量 + 被改对象精确计数）——
    if s2.count('<script') != c_script + 1:
        sys.exit('!! <script 计数异常')
    if s2.count('</script>') != c_escript + 1:
        sys.exit('!! </script> 计数异常')
    if s2.count('<style') != c_style + 1:
        sys.exit('!! <style 计数异常')
    if s2.count('</style>') != c_estyle + 1:
        sys.exit('!! </style> 计数异常')
    if s2.count('</body>') != c_body:
        sys.exit('!! </body> 计数变化')
    if s2.count('id="%s"' % CSS_ID) != 1 or s2.count('id="%s"' % JS_ID) != 1:
        sys.exit('!! 注入块 id 计数异常')
    if s2.count(STYLE_BLOCK) != 1 or s2.count(JS_BLOCK) != 1:
        sys.exit('!! 注入内容不是恰好一份')
    # 未被本轮改动的既有锚点
    if s2.count('justify-end gap-1') != 1:
        sys.exit('!! 右簇锚点被改动')
    if s2.count('maxHeight:480') != 2:
        sys.exit('!! 既有浮窗源码被改动')
    # 新块必须落在最后一个既有注入块之后（同特异性后者胜）
    if s2.find('id="r80-ws-css"') < s2.find('id="r74-head-css"'):
        sys.exit('!! 新块未排在既有注入块之后')
    # 新增量必须为正、且写入成功
    if len(s2) != n0 + len(BLOCK):
        sys.exit('!! 字节数增量异常')
    # 新增类名只应来自本块（改前页面里一个都没有）
    if s.count('r80-ws-') != 0:
        sys.exit('!! 改前页面已含 r80-ws- 类名')
    if s2.count('r80-ws-') != BLOCK.count('r80-ws-'):
        sys.exit('!! r80-ws- 类名数量异常')
    if not (CSS.count('r80-ws-panel') == 1 and CSS.count('r80-ws-ibadge') == 1):
        sys.exit('!! CSS 关键类名缺失')
    if not (JS.count('r80-ws-panel') == 1 and JS.count('r80-ws-ibadge') == 1):
        sys.exit('!! JS 关键类名缺失')

    with open(PAGE, 'w', encoding='utf-8') as f:
        f.write(s2)

    print('应用: 1 项（%s + %s）  字符 %d → %d (+%d)' % (CSS_ID, JS_ID, n0, len(s2), len(s2) - n0))
    print('  标签增量: <script +1 / </script> +1 / <style +1 / </style> +1 / </body> +0')


if __name__ == '__main__':
    main()
