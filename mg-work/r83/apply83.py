#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""r83 —— 需求 4：数字分身 AI 会话栏内的「会话历史」二级视图。

设计稿：MasterGo `layer 1389:18518`（page 263:05935，file 193158744355579），
容器 482 × 984。取数：`python mg-work/mgfetch.py <goto 链接> --out mg-work/r83/raw`。

落点：`pages/avatar.html`（全仓只有这一页有 `.av-chat-drawer` + `[aria-label="会话历史"]`）。
在 `.td-right-inner` 内新增一个 `.av-hs` 视图；点击标题栏「会话历史」→ 栏内切到该视图；
「返回」/ 点会话行 → 切回对话视图。

本脚本只做三件事：
  ① 在 `<div class="td-right-inner">` 之后插入 `.av-hs` 的**静态表头**（行由 JS 生成）；
  ② 在 `</body>` 前插入 `<style id="r83-hs-css">` + `<script id="r83-hs-js">`；
  ③ 幂等：先按 id / 注释标记摘掉上一版三块，再插回。

用法：python mg-work/r83/apply83.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # 仓库根

PAGES = ['avatar.html']


# ────────────────────────────────────────────────────────────────
# 1. 视图标记（插进 .td-right-inner）
# ────────────────────────────────────────────────────────────────
VIEW_OPEN = '<!-- r83-hs-view -->'
VIEW_CLOSE = '<!-- /r83-hs-view -->'

# ⚠ 块内必须自带首尾空白：幂等自证要求「摘掉后字符数完全回到改前」，
#   故不能在 replace 时另加缩进（那会留下摘不掉的 7 个字符）。
VIEW_HTML = (VIEW_OPEN + '\n'
             '      <div class="av-hs" id="av-hs">\n'
             '        <header class="av-hs-bar">\n'
             '          <button class="av-hs-back" type="button" aria-label="返回" data-av-hs-back="1">\n'
             '            <svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true"><path d="M3.8 6.72h9.2v1.56H3.8l3.4 3.62-1.03 1.1L1 7.5l5.17-5.5 1.03 1.1z" fill="currentColor"/></svg>\n'
             '          </button>\n'
             '          <span class="av-hs-rule" aria-hidden="true"></span>\n'
             '          <h2 class="av-hs-title">会话历史</h2>\n'
             '        </header>\n'
             '        <div class="av-hs-list" id="av-hs-list" role="list"></div>\n'
             '      </div>\n'
             '      ' + VIEW_CLOSE)


# ────────────────────────────────────────────────────────────────
# 2. CSS
#    全部数值来自设计稿 PNG（488×990，节点原点落在 PNG (3,2)）逐像素实测。
# ────────────────────────────────────────────────────────────────
HS_CSS = """
/* ★ 第 83 轮 · 需求 4：AI 会话栏内的「会话历史」二级视图
   设计稿 MasterGo 1389:18518（482 × 984）—— 数值全部来自设计稿 PNG 导出的逐像素实测
   （PNG 488×990，节点原点落在 PNG (3,2)；下述 x/y 均为节点内坐标）：
     · 表头 48 高，含 1px 底线（实测 rgb(231,235,241)）；
       返回按钮 24×24 @(20,12)、图标 14×14；竖分隔线 1×16 @x52 = 20 + 24 + 8，色取灰阶 4（实测 #C9C9C9）；
       标题「会话历史」起笔 x65（= 分隔线右缘 53 + 12），16px / 字重 600。
     · 列表内边距 20；行 442 × 56（= 482 − 20 × 2）、圆角 4、行距 2、行内边距 0 10px；
       标题行 14px / 行高 22，时间行 12px / 行高 16，两行间隔 3（文本块 41，行内垂直居中）；
       右侧两枚图标按钮各 24 × 24（内边距 5 ⇒ 图标 14 × 14）、间距 8、图标色取 text-3（实测 #868686）；
       末枚按钮右缘距行右缘 10（实测 452）。
     · 行底：默认透出面板白；悬停、「当前会话」与「删除确认态」均为 fill-2（实测 242,242,242；
       ⚠ 设计稿里第 1 行与正在确认的第 3 行同时是 242 ⇒ 确认态同样吃 fill-2）。
     · 删除确认态：图标组换成 [取消][确定删除]，两者间距 8、整组同样右对齐（实测 取消 48 宽、
       确定删除 72 宽、底 #F53F3F = 危险 6）。 */
:root {
  --av-hs-line: #E7EBF1;               /* 表头底线，设计稿实测 rgb(231,235,241) */
  --av-hs-rule: rgb(var(--gray-4));    /* 表头竖分隔线，设计稿实测 #C9C9C9 = 灰阶 4 */
}
[giencoder-theme='dark'] {
  --av-hs-line: rgb(var(--gray-3));
}

/* ---------- 视图切换：只有 #av-chat-drawer[data-av-hs] 时才显示二级页 ---------- */
.av-hs { display: none; }
#av-chat-drawer[data-av-hs] > .td-right-inner > .av-hs {
  display: flex; flex-direction: column; flex: 1; min-height: 0;
}
#av-chat-drawer[data-av-hs] > .td-right-inner > :not(.av-hs) { display: none; }

/* ---------- 表头 ---------- */
.av-hs-bar {
  flex: none; height: 48px; box-sizing: border-box;
  display: flex; align-items: center; padding: 0 20px;
  border-bottom: 1px solid var(--av-hs-line);
}
.av-hs-back {
  flex: none; width: 24px; height: 24px; box-sizing: border-box;
  display: flex; align-items: center; justify-content: center;
  margin: 0; padding: 0; border: 0; border-radius: 4px; background: transparent;
  color: var(--color-text-1); cursor: pointer;
  transition: background-color 120ms linear;
}
.av-hs-back:hover { background: var(--color-fill-2); }
.av-hs-back svg { width: 14px; height: 14px; }
.av-hs-rule {
  flex: none; width: 1px; height: 16px;
  margin: 0 12px 0 8px;
  background: var(--av-hs-rule);
}
.av-hs-title {
  margin: 0; padding: 0; min-width: 0;
  font-size: var(--font-size-title-1); font-weight: 600; line-height: 24px;
  color: var(--color-text-1);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

/* ---------- 列表 ---------- */
.av-hs-list {
  flex: 1; min-height: 0; overflow-y: auto; overflow-x: hidden;
  padding: 20px;
  display: flex; flex-direction: column; gap: 2px;
}
/* 滚动条与设计稿一致：6px 宽、rgba(0,0,0,.16)（实测 #D6D6D6）、圆角 3 */
.av-hs-list::-webkit-scrollbar { width: 6px; }
.av-hs-list::-webkit-scrollbar-track { background: transparent; }
.av-hs-list::-webkit-scrollbar-thumb { background: rgba(0, 0, 0, .16); border-radius: 3px; }

/* ---------- 会话行 ---------- */
.av-hs-item {
  flex: none; height: 56px; box-sizing: border-box;
  display: flex; align-items: center; gap: 8px;
  padding: 0 10px; border-radius: 4px; background: transparent;
  transition: background-color 120ms linear;
}
.av-hs-item:hover, .av-hs-item.is-on, .av-hs-item.is-confirm { background: var(--color-fill-2); }

.av-hs-txt { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.av-hs-name {
  display: block; width: 100%; margin: 0; padding: 0; border: 0; background: none;
  font-family: inherit; text-align: left; cursor: pointer;
  font-size: var(--font-size-body-3); font-weight: 500; line-height: 22px;
  color: var(--color-text-1);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.av-hs-time {
  display: block; min-height: 16px;
  font-size: var(--font-size-body-1); line-height: 16px; color: var(--color-text-3);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

.av-hs-acts { flex: none; display: flex; align-items: center; gap: 8px; }
.av-hs-ibtn {
  flex: none; width: 24px; height: 24px; box-sizing: border-box; padding: 5px;
  display: flex; align-items: center; justify-content: center;
  margin: 0; border: 0; border-radius: 4px; background: transparent;
  color: var(--color-text-3); cursor: pointer;
  transition: background-color 120ms linear, color 120ms linear;
}
.av-hs-ibtn:hover { background: var(--color-fill-3); color: var(--color-text-1); }
.av-hs-ibtn svg { width: 14px; height: 14px; }

/* 删除确认态 */
.av-hs-confirm { flex: none; display: none; align-items: center; gap: 8px; }
.av-hs-item.is-confirm .av-hs-acts { display: none; }
.av-hs-item.is-confirm .av-hs-confirm { display: flex; }
/* 适配层：DS Button(size-mini) 收敛到设计稿的 28 高 / 左右内边距 12
   （实测 取消 48 宽、确定删除 72 宽 = 12px 字宽 + 12 × 2 内边距 + 2 × 1 描边） */
.giencoder-btn.giencoder-btn-size-mini.av-hs-btn {
  height: 28px; padding: 0 12px; border-radius: 4px;
}
"""


# ────────────────────────────────────────────────────────────────
# 3. JS
#    图标形状说明：
#      · 导出 = 设计稿 asset `svg_5f4f2e22`（mastergo 导出时带 matrix(0,1,1,0,..) 转置，
#        换回后即「托盘 ⊓ + 下箭头」。此处按该 asset 的顶点坐标写成紧凑路径，
#        逐像素核对过托盘/箭杆/箭头三段的位置与线宽 1.167 ≈ 1.2）。
#      · 删除 = 按设计稿 PNG 灰度矩阵重建（圆角盖 + 桶身 + 内袋），
#        核对：盖 x434..445 / y90..92、桶身竖边 x435..436 与 x443..444 / y93..101、
#              内袋 x438..441 / y94..98。
# ────────────────────────────────────────────────────────────────
HS_JS = """
/* SHELL-AV-HS v1 —— AI 会话栏内的「会话历史」二级视图
   ⚠ 勿手改此块；落地脚本 mg-work/r83/apply83.py；设计稿 MasterGo 1389:18518。 */
(function () {
  var drawer = document.getElementById('av-chat-drawer');
  var view = document.getElementById('av-hs');
  var list = document.getElementById('av-hs-list');
  if (!drawer || !view || !list) return;
  if (drawer.__avHs) return;
  drawer.__avHs = 1;

  var ATTR = 'data-av-hs';

  /* 左：导出（= 设计稿 asset svg_5f4f2e22 的转置形态）；右：删除（按 PNG 重建） */
  var ICON_EXPORT = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true">' +
    '<path d="M1.8 9.04V1.8h9.92v7.24" stroke="currentColor" stroke-width="1.2"/>' +
    '<path d="M6.76 4.92v5.63" stroke="currentColor" stroke-width="1.2"/>' +
    '<path d="M3.7 9.73h6.12L6.76 12.78z" fill="currentColor"/></svg>';
  var ICON_TRASH = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true">' +
    '<rect x="1" y="1.2" width="12" height="2.8" rx="1.4" fill="currentColor"/>' +
    '<path d="M3 4v8h8V4" stroke="currentColor" stroke-width="2"/>' +
    '<rect x="5.5" y="5.5" width="3" height="4" rx="0.8" stroke="currentColor" stroke-width="1"/></svg>';

  /* 会话数据：[标题, 时间, 是否当前会话]。文案与排序照抄设计稿（首行为当前会话、无时间）。
     ⚠ 这三行是占位数据 —— 真实数据接入后只改这个数组即可。 */
  var ROWS = [
    ['银行金融科技IT开发服务AI智能体平台与IDE插件...', '', 1],
    ['SimplAI AI应用部署平台介绍', '半小时前', 0],
    ['可视化工作流编排可视化工作流编排...', '昨天 11:12', 0],
    ['成都到深圳海边性价比方案', '07/12 09:32', 0],
    ['自动任务手动触发对话创建', '07/12 09:32', 0],
    ['Git Worktree多分支并行开发', '07/12 09:32', 0],
    ['Codex自定义大模型方法', '07/12 09:32', 0]
  ];

  function rowHTML(r) {
    return '<div class="av-hs-item' + (r[2] ? ' is-on' : '') + '" role="listitem">' +
      '<span class="av-hs-txt">' +
        '<button class="av-hs-name" type="button" data-av-hs-pick="1">' + r[0] + '</button>' +
        '<span class="av-hs-time">' + r[1] + '</span>' +
      '</span>' +
      '<span class="av-hs-acts">' +
        '<button class="av-hs-ibtn" type="button" aria-label="导出会话" title="导出会话" data-av-hs-export="1">' + ICON_EXPORT + '</button>' +
        '<button class="av-hs-ibtn" type="button" aria-label="删除会话" title="删除会话" data-av-hs-del="1">' + ICON_TRASH + '</button>' +
      '</span>' +
      '<span class="av-hs-confirm">' +
        '<button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini av-hs-btn" type="button" data-av-hs-cancel="1">取消</button>' +
        '<button class="giencoder-btn giencoder-btn-danger giencoder-btn-size-mini av-hs-btn" type="button" data-av-hs-ok="1">确定删除</button>' +
      '</span>' +
    '</div>';
  }

  if (!list.childElementCount) {
    var buf = '';
    for (var i = 0; i < ROWS.length; i++) buf += rowHTML(ROWS[i]);
    list.innerHTML = buf;
  }

  /* ---------- 轻提示：复用页面自身的 .td-dp-msg（同构造），没有就按同构造建一个 ---------- */
  var MSG_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true">' +
    '<circle cx="7" cy="7" r="6.2" fill="currentColor"/>' +
    '<path d="M4.3 7.2l1.9 1.9 3.5-3.7" stroke="var(--color-white)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function toast(text) {
    var box = document.querySelector('.td-dp-msg');
    if (!box) {
      box = document.createElement('div');
      box.className = 'td-dp-msg';
      box.innerHTML = '<div class="giencoder-message" role="status">' +
        '<span class="giencoder-message-icon" aria-hidden="true">' + MSG_SVG + '</span>' +
        '<span class="giencoder-message-content"></span></div>';
      box.hidden = true;
      document.body.appendChild(box);
    }
    var c = box.querySelector('.giencoder-message-content');
    if (!c) return;
    c.textContent = text;
    box.hidden = false;
    clearTimeout(box._t);
    box._t = setTimeout(function () { box.hidden = true; }, 2400);
  }

  /* ---------- 视图开合 ---------- */
  function isOpen() { return drawer.hasAttribute(ATTR); }
  function syncAria(open) { view.setAttribute('aria-hidden', open ? 'false' : 'true'); }

  function openView() {
    if (isOpen()) return;
    drawer.setAttribute(ATTR, '');
    syncAria(true);
    var back = view.querySelector('[data-av-hs-back]');
    if (back) back.focus();
  }
  function closeView() {
    if (!isOpen()) return;
    var c = list.querySelector('.av-hs-item.is-confirm');
    if (c) c.classList.remove('is-confirm');
    drawer.removeAttribute(ATTR);
    syncAria(false);
    var entry = chatEntry();
    if (entry && entry.isConnected) entry.focus();
  }
  function chatEntry() {
    return drawer.querySelector('.td-right-acts [aria-label="会话历史"]');
  }

  /* ---------- 点击委托（⚠ 挂在整个视图上：返回按钮在 .av-hs-bar 里，不在列表内） ---------- */
  function brief(el) {
    var t = el ? el.textContent : '';
    return t.length > 14 ? t.slice(0, 14) + '…' : t;
  }
  view.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!t || !t.closest) return;

    if (t.closest('[data-av-hs-back]')) { closeView(); return; }   /* 返回 → 回到对话视图 */

    var row = t.closest('.av-hs-item');
    if (!row) return;

    if (t.closest('[data-av-hs-del]')) {                           /* 删除 → 行内确认态 */
      var other = list.querySelector('.av-hs-item.is-confirm');
      if (other && other !== row) other.classList.remove('is-confirm');
      row.classList.add('is-confirm');
      var c = row.querySelector('[data-av-hs-cancel]');
      if (c) c.focus();
      return;
    }
    if (t.closest('[data-av-hs-cancel]')) {                        /* 取消 */
      row.classList.remove('is-confirm');
      var d = row.querySelector('[data-av-hs-del]');
      if (d) d.focus();
      return;
    }
    if (t.closest('[data-av-hs-ok]')) {                            /* 确定删除 */
      var nm = row.querySelector('.av-hs-name');
      var txt = nm ? brief(nm) : '';
      row.parentNode.removeChild(row);
      toast('已删除「' + txt + '」');
      return;
    }
    if (t.closest('[data-av-hs-export]')) {                        /* 导出（本轮只做回执） */
      toast('已导出「' + brief(row.querySelector('.av-hs-name')) + '」');
      return;
    }
    if (t.closest('[data-av-hs-pick]')) {                          /* 点会话 → 选中并回到对话视图 */
      var on = list.querySelector('.av-hs-item.is-on');
      if (on && on !== row) on.classList.remove('is-on');
      row.classList.add('is-on');
      closeView();
    }
  });

  /* Esc 返回上一层（优先级低于页面自己的弹层/全屏裁决：它们消费掉后不会走到这里） */
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape' && ev.key !== 'Esc') return;
    if (!isOpen()) return;
    if (document.querySelector('.td-dp-msg') && !document.querySelector('.td-dp-msg').hidden) return;
    closeView();
  }, true);

  /* 「会话历史」入口 */
  var entry = chatEntry();
  if (entry) entry.addEventListener('click', function () { openView(); });

  /* 整个 AI 会话栏关掉时，二级页要复位（下次打开回到对话视图） */
  if (window.MutationObserver) {
    new MutationObserver(function () {
      if (!document.documentElement.hasAttribute('data-av-chat-open')) closeView();
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-av-chat-open'] });
  }

  /* 入口按钮若晚于本脚本出现（外壳克隆），用观察器兜住，只绑一次 */
  if (!entry) {
    var boot = new MutationObserver(function () {
      var b = chatEntry();
      if (!b) return;
      b.addEventListener('click', function () { openView(); });
      boot.disconnect();
    });
    boot.observe(document.body, { childList: true, subtree: true });
  }

  syncAria(false);
})();
"""


# ────────────────────────────────────────────────────────────────
# 4. 装配与注入
# ────────────────────────────────────────────────────────────────
def style_block(bid, css):
    return '<style id="%s">\n%s\n</style>' % (bid, css)


def script_block(bid, js):
    return '<script id="%s">\n%s\n</script>' % (bid, js)


HS_STYLE = style_block('r83-hs-css', HS_CSS)
HS_SCRIPT = script_block('r83-hs-js', HS_JS)

# ⚠ 两条块规则必须把**尾随换行**一起吃掉 —— 注入时写的是 `块 + \n` 接下一件，
#   不带上它，幂等自证会残留 2 个字符（每个块各 1 个）。
PRIOR = (
    (re.compile(r'<style id="r83-hs-css">.*?</style>\n', re.S), 1),
    (re.compile(r'<script id="r83-hs-js">.*?</script>\n', re.S), 1),
    (re.compile(re.escape(VIEW_OPEN) + r'.*?' + re.escape(VIEW_CLOSE), re.S), 1),
)

ANCHOR_INNER = '<div class="td-right-inner">'
TOKENS = ['av-hs-bar', 'av-hs-back', 'av-hs-rule', 'av-hs-title',
          'av-hs-list', 'av-hs-item', 'av-hs-name', 'av-hs-time',
          'av-hs-acts', 'av-hs-ibtn', 'av-hs-confirm', 'av-hs-btn']


def meta_guard():
    """护身符：新块里不得出现会破坏 HTML 结构的标签字面量。"""
    common = (('</body>', 0), ('</html>', 0), ('</head>', 0), ('<body', 0), ('<html', 0), ('<head', 0))
    rules = {
        'css': common + (('</style>', 1), ('<style', 1), ('</script>', 0), ('<script', 0)),
        'js': common + (('</script>', 1), ('<script', 1), ('</style>', 0), ('<style', 0)),
    }
    for part, name, key in ((HS_STYLE, 'hs/css', 'css'), (HS_SCRIPT, 'hs/js', 'js')):
        for bad, allowed in rules[key]:
            n = part.count(bad)
            if n != allowed:
                sys.exit('!! 元守卫失败：%s 里 %r 出现 %d 次（应为 %d）' % (name, bad, n, allowed))
    if '<div' in HS_STYLE or '</div>' in HS_STYLE:
        sys.exit('!! 元守卫失败：hs/css 里出现 div 标签字面量')
    # 视图块的注释标记不得出现在 CSS / JS 里，否则幂等摘除会错位
    for part, name in ((HS_STYLE, 'hs/css'), (HS_SCRIPT, 'hs/js')):
        if VIEW_OPEN in part or VIEW_CLOSE in part:
            sys.exit('!! 元守卫失败：%s 里出现视图注释标记' % name)
    if VIEW_OPEN in VIEW_HTML.replace(VIEW_OPEN, '', 1) or VIEW_CLOSE in VIEW_HTML.replace(VIEW_CLOSE, '', 1):
        sys.exit('!! 元守卫失败：视图块内的注释标记重复')


def strip_all(s):
    """按 PRIOR 摘掉本轮的三个块，返回 (剩余文本, 摘掉件数)。"""
    n = 0
    for pat, want in PRIOR:
        s, k = re.subn(pat, '', s, count=want)
        n += k
    return s, n


def apply_page(fname):
    page = os.path.join(ROOT, 'pages', fname)
    with open(page, encoding='utf-8') as f:
        s0 = f.read()

    # —— 先摘旧块，得到「本轮基线」 ——
    s, dropped = strip_all(s0)
    if dropped not in (0, 1, 2, 3):
        sys.exit('!! %s 旧块删除数量异常：%d' % (fname, dropped))
    for tok in ('id="r83-hs-css"', 'id="r83-hs-js"', VIEW_OPEN, VIEW_CLOSE):
        if tok in s:
            sys.exit('!! %s 摘除旧块后仍残留 %s' % (fname, tok))
    base_txt = s                       # 本轮基线（摘掉旧块后的文本）
    n_base = len(base_txt)

    # —— 锚点防呆 ——
    if s.count(ANCHOR_INNER) != 1:
        sys.exit('!! %s 的 %s 不是恰好 1 个（%d）' % (fname, ANCHOR_INNER, s.count(ANCHOR_INNER)))
    if '<div class="td-chat">' not in s:
        sys.exit('!! %s 里找不到 .td-chat（落点可能已变）' % fname)
    if s.count('</body>') != 1:
        sys.exit('!! %s 的 </body> 不是恰好 1 个（%d）' % (fname, s.count('</body>')))

    # —— 基线计数 ——
    base = {
        'style': s.count('<style'), 'estyle': s.count('</style>'),
        'script': s.count('<script'), 'escript': s.count('</script>'),
        'body': s.count('</body>'),
        'inner': s.count(ANCHOR_INNER),
    }

    # —— 插视图 ——
    s = s.replace(ANCHOR_INNER, ANCHOR_INNER + VIEW_HTML, 1)

    # —— 插 CSS + JS ——
    s = s.replace('</body>', HS_STYLE + '\n' + HS_SCRIPT + '\n</body>', 1)

    # —— 断言：标签级精确增减 ——
    checks = (('<style', base['style'] + 1), ('</style>', base['estyle'] + 1),
              ('<script', base['script'] + 1), ('</script>', base['escript'] + 1),
              ('</body>', base['body']))
    for tok, want in checks:
        got = s.count(tok)
        if got != want:
            sys.exit('!! %s 标签计数 %r = %d（应为 %d）' % (fname, tok, got, want))
    if s.count(ANCHOR_INNER) != base['inner']:
        sys.exit('!! %s 锚点计数变了' % fname)

    # —— 断言：被改对象的精确计数 ——
    # 判据：`av-hs-*` 是本轮新造的前缀，原页面里一个都不该有
    #       ⇒ 全页计数 必须 == 三个块里的出现次数之和。
    blob = HS_CSS + HS_JS + VIEW_HTML
    for tok in TOKENS:
        want = blob.count(tok)
        if want == 0:
            sys.exit('!! 块内不存在 token %r' % tok)
        got = s.count(tok)
        if got != want:
            sys.exit('!! %s token %r 计数 %d（块内 %d）' % (fname, tok, got, want))
    if s.count('id="av-hs-list"') != 1 or s.count('id="av-hs"') != 1:
        sys.exit('!! %s 视图 id 计数异常' % fname)

    # —— 幂等自证：把刚插的三块按同样规则摘掉，必须**逐字节等于本轮基线** ——
    t, dropped2 = strip_all(s)
    if dropped2 != 3:
        sys.exit('!! %s 幂等自证失败：只摘掉 %d 件（应为 3）' % (fname, dropped2))
    if t != base_txt:
        sys.exit('!! %s 幂等自证失败：摘回后 %d 字符 ≠ 基线 %d 字符' % (fname, len(t), n_base))

    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)

    return n_base, len(s), dropped


def main():
    meta_guard()
    print('')
    for fname in PAGES:
        a, b, dropped = apply_page(fname)
        print('%-18s %d → %d (%+d)  视图=av-hs  （摘掉上一版块 %d 件）' % (fname, a, b, b - a, dropped))
    print('')


if __name__ == '__main__':
    main()
