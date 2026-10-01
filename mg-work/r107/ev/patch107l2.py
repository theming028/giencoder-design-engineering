# -*- coding: utf-8 -*-
"""r107 第十一拍 ④ —— 对照 Codex 官方原版补缺（仍是未提交期的**就地返工**，不另起代数）。

邵先生第四条逐字：「再调查一下codex官方原版有无缺少的功能，能落地的都补充。」

官方现有能力（openai.com「Codex:全能型助手」+ 第三方教程汇总）：
  五入口 文件 / 侧边聊天 / 浏览器 / 审查 / 终端 + **摘要面板**（计划·来源·产物·摘要）；
  审查支持「本轮改动 ⇄ 整体分支改动」筛选 · 行内评论 · 暂存/撤销 · 界面内 Commit/Push/PR ·
  查看 GitHub PR 与评论 · 打开文件预览；浏览器可开本地或公网页 · **在渲染页面上直接标注** ·
  **一键截图到剪贴板** · 一次只开一页；终端与 Codex 共享工作目录 · **多标签终端**；
  **产物查看器**（PDF / 表格 / 文档 / 演示文稿预览）；SSH 远程连接（alpha，**不在侧栏**）· 多窗口 · 托盘。

对照我们右栏（r107 一~十拍已落地）：五模块 + 摘要 + 行内评论 + 暂存·撤销 + 统一⇄并排 +
自动换行/隐藏空白/词级差异/折叠未改动 + 对比范围三档 + 提交·推送·PR + 浏览器标注 + 终端
—— **真正还缺且能落地**的只有三件：

  ① **终端多标签**（官方「多标签终端」）—— 我们只有单块。
  ② **浏览器截图**（官方「一键截图到剪贴板」）—— 我们没有。
  ③ **产物预览**（官方「产物查看器」）—— 我们的「预览」按钮只弹 toast，没有真视觉。
  （SSH / 多窗口 / 托盘：静态演示页无法落地，不做；「文件」模块不能编辑：官方亦然，不动。）

改序（只能下→上）：
    1. `part107/_mods.html`  —— ① 终端标签条 + 第二块终端；② 地址栏「截图」按钮；③ 产物预览层
    2. `ev/splice107.py`     —— 由 `_head.html + part105 剪出的 Files 正文 + _mods.html` 重组 `browse.html`
    3. `part107/panel.js`    —— 终端按块绑定 / 标签切换与新建 / 截图快门 / 产物预览层开合 + Esc 裁决
    4. `part107/panel.css`   —— 第 18 节（① 标签条 · ② 快门 · ③ 预览层与两套骨架）
    5. 重跑 `mg-work/r107/apply107.py` 落页面

幂等：所有改动都带标记串 `r107-l2`（**只有改完之后才存在**）⇒ 复跑「应用 0 项 / 跳过 N 项」。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P107 = os.path.join(REPO, 'mg-work', 'r107', 'part107')
MODS = os.path.join(P107, '_mods.html')
PJS = os.path.join(P107, 'panel.js')
PCS = os.path.join(P107, 'panel.css')

MARK = 'r107-l2'

APPLIED = []
SKIPPED = []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark=None):
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


# ================================================================================
# 图标（与文件内既有图标同口径：24 网格 + 描边 currentColor）
# ================================================================================
ICO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="%d" height="%d" '
       'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
       'stroke-linejoin="round" aria-hidden="true">%s</svg>')

TERM_PATH = '<path d="m7 9 3 3-3 3"/><path d="M13 15h4"/>'
PLUS_PATH = '<path d="M12 5v14"/><path d="M5 12h14"/>'
CAM_PATH = ('<path d="M3 8.5h3.2l1.6-2.3h8.4l1.6 2.3H21a1 1 0 0 1 1 1v8.5a1 1 0 0 1-1 1H3'
            'a1 1 0 0 1-1-1V9.5a1 1 0 0 1 1-1Z"/><circle cx="12" cy="13.5" r="3.2"/>')

TERM_ICO = ICO % (12, 12, TERM_PATH)
PLUS_ICO = ICO % (12, 12, PLUS_PATH)
CAM_ICO = ICO % (16, 16, CAM_PATH)


# ================================================================================
# 1. _mods.html
# ================================================================================
def patch_mods():
    t, nl = rd(MODS)
    if MARK in t:
        SKIPPED.append('_mods.html · 全部三项')
        print('   跳过  _mods.html · 全部三项（已应用）')
        return

    # ---- ① 终端：整节重建（原 `.td-term` 正文**逐字**搬进 t1 块，保证行为零变化） ----
    SEC_START = '    <section class="td-mod td-mod-term"'
    i = t.find(SEC_START)
    if i < 0:
        sys.exit('!! _mods.html：找不到终端 section')
    if t.count(SEC_START) != 1:
        sys.exit('!! _mods.html：终端 section 起点命中 %d 次' % t.count(SEC_START))
    j = t.find('\n    </section>', i)
    if j < 0:
        sys.exit('!! _mods.html：找不到终端 section 收尾')
    j += len('\n    </section>')
    block = t[i:j]
    DIV1 = '<div class="td-term" tabindex="0" data-td-term="1">'
    d0 = block.find(DIV1)
    if d0 < 0:
        sys.exit('!! _mods.html：终端里找不到 %r' % DIV1)
    d1 = block.find('\n      </div>', d0)
    if d1 < 0:
        sys.exit('!! _mods.html：找不到原终端块收尾')
    inner = block[d0 + len(DIV1):d1]
    for need in ('npm run dev', 'data-td-term-echo', 'td-term-caret'):
        if need not in inner:
            sys.exit('!! _mods.html：剪出来的终端正文缺 %r' % need)

    term_new = (
        '    <!-- ★ 第十一拍 ④（r107-l2）：对照官方「多标签终端」补的标签条。\n'
        '         静态两枚（zsh / npm run dev），`+` 由 panel.js 现场新建（新标签 = 空提示符）。\n'
        '         切换只切 `hidden`，各块的输出与输入各自独立。 -->\n'
        '    <section class="td-mod td-mod-term" id="av-browse-pane-terminal" data-td-pane="terminal" '
        'role="tabpanel" aria-label="终端" hidden>\n'
        '      <div class="td-term-tabs" role="tablist" aria-label="终端标签">\n'
        '        <button class="td-term-tab is-active" type="button" role="tab" aria-selected="true" '
        'data-td-term-tab="t1"><span class="td-term-tab-ico">' + TERM_ICO + '</span>'
        '<span class="td-term-tab-nm">zsh</span></button>\n'
        '        <button class="td-term-tab" type="button" role="tab" aria-selected="false" '
        'data-td-term-tab="t2"><span class="td-term-tab-ico">' + TERM_ICO + '</span>'
        '<span class="td-term-tab-nm">npm run dev</span></button>\n'
        '        <button class="td-term-tabadd" type="button" aria-label="新建终端标签" title="新建终端标签" '
        'data-td-term-add="1">' + PLUS_ICO + '</button>\n'
        '      </div>\n'
        '      <div class="td-term" tabindex="0" data-td-term="1" data-td-term-pane="t1">' + inner + '\n'
        '      </div>\n'
        '      <div class="td-term" tabindex="0" data-td-term="1" data-td-term-pane="t2" hidden>\n'
        '        <div class="td-term-line"><span class="td-term-ps">giencoder-design-engineering</span>'
        '<span class="td-term-pd">$</span><span class="td-term-cmd">git status -sb</span></div>\n'
        '        <div class="td-term-out">## main...origin/main [ahead 2]</div>\n'
        '        <div class="td-term-out"> M pages/conversation.html</div>\n'
        '        <div class="td-term-out is-dim">?? mg-work/r107/</div>\n'
        '        <div class="td-term-line"><span class="td-term-ps">giencoder-design-engineering</span>'
        '<span class="td-term-pd">$</span><span class="td-term-echo" data-td-term-echo="1"></span>'
        '<span class="td-term-caret" data-td-term-caret="1"></span></div>\n'
        '      </div>\n'
        '    </section>'
    )
    t = t[:i] + term_new + t[j:]

    # ---- ② 浏览器：地址栏补一枚「截图」（放在「标注」之后、原「缩放」之前） ----
    ZOOM_BTN = ('<button class="td-browse-ico" type="button" aria-label="缩放" title="缩放" '
                'data-td-brw-act="zoom">')
    if t.count(ZOOM_BTN) != 1:
        sys.exit('!! _mods.html：「缩放」按钮锚点命中 %d 次' % t.count(ZOOM_BTN))
    shot_btn = ('<button class="td-browse-ico" type="button" aria-label="截图到剪贴板" '
                'title="截图到剪贴板" data-td-brw-act="shot">' + CAM_ICO + '</button>\n        ')
    t = t.replace(ZOOM_BTN, shot_btn + ZOOM_BTN, 1)

    # ---- ③ 摘要：产物预览层（覆盖整块摘要，由 panel.js 填文案 + 切骨架） ----
    SUM_START = '    <section class="td-mod td-sum"'
    k = t.find(SUM_START)
    if k < 0:
        sys.exit('!! _mods.html：找不到摘要 section')
    if t.count(SUM_START) != 1:
        sys.exit('!! _mods.html：摘要 section 起点命中 %d 次' % t.count(SUM_START))
    m = t.find('\n    </section>', k)
    if m < 0:
        sys.exit('!! _mods.html：找不到摘要 section 收尾')

    prev_html = (
        '\n'
        '      <!-- ★ 第十一拍 ④（r107-l2）：产物预览层（对照官方「产物查看器」）。\n'
        '           点摘要「产物」里的「预览」打开；绝对定位覆盖整块摘要、不参与文档流。\n'
        '           两套骨架（文档 / 表格）由 `data-td-prev-kind` 切，JS 只做显示切换与文案填充。 -->\n'
        '      <div class="td-sum-prev" data-td-prev="1" hidden>\n'
        '        <div class="td-sum-prev-h">\n'
        '          <i class="td-sum-arti" data-td-prev-ico="1">' + ICO % (16, 16, '<path d="M4 2h11.5l3.5'
        ' 5.5v13a1.5 1.5 0 0 1-1.5 1.5H4a1.5 1.5 0 0 1-1.5-1.5v-17A1.5 1.5 0 0 1 4 2Z"/>'
        '<path d="M7.5 9.5h6.5"/><path d="M6.5 13h3.5"/>') + '</i>\n'
        '          <span class="td-sum-prev-t">\n'
        '            <b data-td-prev-name="1">产物</b>\n'
        '            <i data-td-prev-meta="1">—</i>\n'
        '          </span>\n'
        '          <button class="td-browse-ico" type="button" aria-label="关闭预览" title="关闭预览" '
        'data-td-prev-x="1">' + ICO % (16, 16, '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>') + '</button>\n'
        '        </div>\n'
        '        <div class="td-sum-prev-b">\n'
        '          <div class="td-pv-md" data-td-prev-kind="md">\n'
        '            <div class="td-pv-h1">右栏复刻方案</div>\n'
        '            <div class="td-pv-p">把会话详情页右栏升级为标签式 Side Panel：模块可多开、切换、关闭与'
        '拖拽重排，并补齐审查 / 终端 / 浏览器 / 摘要四个面板。</div>\n'
        '            <div class="td-pv-h2">一、体位</div>\n'
        '            <span class="td-pv-bar"></span>\n'
        '            <span class="td-pv-bar is-w80"></span>\n'
        '            <span class="td-pv-bar is-w60"></span>\n'
        '            <div class="td-pv-h2">二、缺口与补齐</div>\n'
        '            <span class="td-pv-bar"></span>\n'
        '            <span class="td-pv-bar is-w40"></span>\n'
        '          </div>\n'
        '          <div class="td-pv-sheet" data-td-prev-kind="xlsx" hidden>\n'
        '            <div class="td-pv-row"><span class="td-pv-cell is-head">模块</span>'
        '<span class="td-pv-cell is-head">宽 (px)</span><span class="td-pv-cell is-head">占比</span>'
        '<span class="td-pv-cell is-head">状态</span></div>\n'
        '            <div class="td-pv-row"><span class="td-pv-cell">文件</span>'
        '<span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span>'
        '<span class="td-pv-cell">已交付</span></div>\n'
        '            <div class="td-pv-row"><span class="td-pv-cell">审查</span>'
        '<span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span>'
        '<span class="td-pv-cell">本轮新增</span></div>\n'
        '            <div class="td-pv-row"><span class="td-pv-cell">终端</span>'
        '<span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span>'
        '<span class="td-pv-cell">本轮新增</span></div>\n'
        '            <div class="td-pv-row"><span class="td-pv-cell">浏览器</span>'
        '<span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span>'
        '<span class="td-pv-cell">本轮新增</span></div>\n'
        '            <div class="td-pv-row"><span class="td-pv-cell">摘要</span>'
        '<span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span>'
        '<span class="td-pv-cell">默认页签</span></div>\n'
        '          </div>\n'
        '        </div>\n'
        '        <div class="td-sum-prev-f">\n'
        '          <button class="td-prev-btn" type="button" data-td-prev-open="1">在系统打开</button>\n'
        '          <button class="td-prev-btn is-primary" type="button" data-td-prev-close="1">关闭</button>\n'
        '        </div>\n'
        '      </div>'
    )
    t = t[:m] + prev_html + t[m:]

    wr(MODS, t, nl)
    APPLIED.append('_mods.html · ①终端标签条 + ②截图按钮 + ③产物预览层')
    print('   应用  _mods.html · ①终端标签条 + ②截图按钮 + ③产物预览层')


# ================================================================================
# 2. panel.js
# ================================================================================
TERM_START = '  /* ==================== 终端模块（本地回声，纯演示） ==================== */\n'
TERM_END = '  /* ==================== 浏览器模块（标注态 + 元素评论） ==================== */\n'

TERM_NEW = '''  /* ==================== 终端模块（本地回声，纯演示） ====================
     ★ 第十一拍 ④（r107-l2）：对照 Codex 官方「多标签终端」补齐。
       体位 —— `bindTerm(el)` 只负责「把一块 `.td-term` 变成可输入的回声终端」；
       标签条只管**显示哪一块**（切 `hidden`），各块的输出与输入各自独立、互不影响。
       ⚠ 旧实现是「一个 `term` 变量 + 闭包 `echo`」；拆成按块绑定后 `echo` 收进各自闭包，
         行为与改前逐字一致（同一份 CANNED 表、同一套 keydown 分支）。 */
  var termSec = pane.querySelector('.td-mod-term');
  var termTabsEl = termSec ? termSec.querySelector('.td-term-tabs') : null;
  var TERM_ICO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="12" height="12" '
    + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true"><path d="m7 9 3 3-3 3"/><path d="M13 15h4"/></svg>';
  var CANNED = {
    ls: ['README.md        package.json     pages/', 'mg-work/         assets/          vite.config.js'],
    pwd: ['/e/GienCoder/giencoder-design-engineering'],
    'npm run dev': ['> vite --host', '  VITE v5.4.2  ready in 208 ms', '  ➜  Local:   http://localhost:5173/']
  };
  function termPanes() {
    return termSec ? [].slice.call(termSec.querySelectorAll('[data-td-term-pane]')) : [];
  }
  function activeTerm() {
    var p = termPanes();
    for (var i = 0; i < p.length; i++) if (!p[i].hasAttribute('hidden')) return p[i];
    return p[0] || null;
  }
  function showTerm(id, focus) {
    if (!termTabsEl) return;
    var ts = [].slice.call(termTabsEl.querySelectorAll('[data-td-term-tab]')), i;
    for (i = 0; i < ts.length; i++) {
      var on = ts[i].getAttribute('data-td-term-tab') === id;
      ts[i].classList.toggle('is-active', on);
      ts[i].setAttribute('aria-selected', on ? 'true' : 'false');
    }
    var ps = termPanes();
    for (i = 0; i < ps.length; i++) {
      if (ps[i].getAttribute('data-td-term-pane') === id) ps[i].removeAttribute('hidden');
      else ps[i].setAttribute('hidden', '');
    }
    if (focus) { var a = activeTerm(); if (a) a.focus(); }
  }
  function bindTerm(term) {
    var echo = term.querySelector('[data-td-term-echo]');
    if (!echo) return;
    function termOut(text, dim) {
      var dv = document.createElement('div');
      dv.className = 'td-term-out' + (dim ? ' is-dim' : '');
      dv.textContent = text;
      term.appendChild(dv);
    }
    function newPrompt() {
      var line = document.createElement('div');
      line.className = 'td-term-line';
      line.innerHTML = '<span class="td-term-ps">giencoder-design-engineering</span>'
        + '<span class="td-term-pd">$</span>'
        + '<span class="td-term-echo" data-td-term-echo="1"></span>'
        + '<span class="td-term-caret" data-td-term-caret="1"></span>';
      term.appendChild(line);
      echo = line.querySelector('[data-td-term-echo]');
    }
    term.addEventListener('click', function () { term.focus(); });
    term.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'Enter') {
        e.preventDefault();
        var cmd = (echo.textContent || '').trim();
        if (cmd) {
          if (cmd === 'clear') {
            var outs = term.querySelectorAll('.td-term-out');
            for (var i = 0; i < outs.length; i++) outs[i].parentNode.removeChild(outs[i]);
          } else {
            var hit = CANNED[cmd];
            if (hit) { for (var j = 0; j < hit.length; j++) termOut(hit[j], j > 0); }
            else termOut('zsh: command not found: ' + cmd);
          }
        }
        newPrompt();
        term.scrollTop = term.scrollHeight;
        return;
      }
      if (e.key === 'Backspace') {
        e.preventDefault();
        echo.textContent = (echo.textContent || '').slice(0, -1);
        return;
      }
      if (e.key.length === 1) { e.preventDefault(); echo.textContent = (echo.textContent || '') + e.key; }
    });
  }
  var termTabSeq = 2;                 /* 静态已有 t1 / t2 */
  function newTermTab() {
    if (!termSec || !termTabsEl) return null;
    termTabSeq++;
    var id = 't' + termTabSeq;
    var tab = document.createElement('button');
    tab.type = 'button';
    tab.className = 'td-term-tab';
    tab.setAttribute('role', 'tab');
    tab.setAttribute('data-td-term-tab', id);
    tab.setAttribute('aria-selected', 'false');
    tab.innerHTML = '<span class="td-term-tab-ico">' + TERM_ICO + '</span>'
      + '<span class="td-term-tab-nm">终端 ' + termTabSeq + '</span>';
    var add = termTabsEl.querySelector('[data-td-term-add]');
    if (add) termTabsEl.insertBefore(tab, add); else termTabsEl.appendChild(tab);
    var box = document.createElement('div');
    box.className = 'td-term';
    box.setAttribute('tabindex', '0');
    box.setAttribute('data-td-term', '1');
    box.setAttribute('data-td-term-pane', id);
    box.setAttribute('hidden', '');
    box.innerHTML = '<div class="td-term-line"><span class="td-term-ps">giencoder-design-engineering</span>'
      + '<span class="td-term-pd">$</span>'
      + '<span class="td-term-echo" data-td-term-echo="1"></span>'
      + '<span class="td-term-caret" data-td-term-caret="1"></span></div>';
    termSec.appendChild(box);
    bindTerm(box);
    tab.addEventListener('click', function () { showTerm(id, true); });
    showTerm(id, true);
    return tab;
  }
  if (termSec) {
    var termP0 = termPanes(), tp;
    for (tp = 0; tp < termP0.length; tp++) bindTerm(termP0[tp]);
    if (termTabsEl) {
      var termT0 = [].slice.call(termTabsEl.querySelectorAll('[data-td-term-tab]'));
      for (tp = 0; tp < termT0.length; tp++) {
        (function (tb) {
          tb.addEventListener('click', function () { showTerm(tb.getAttribute('data-td-term-tab'), true); });
        })(termT0[tp]);
      }
      var termAdd = termTabsEl.querySelector('[data-td-term-add]');
      if (termAdd) termAdd.addEventListener('click', function () { newTermTab(); });
    }
    /* 静态标记已经摆好（t1 可见、t2 隐藏），这里只是把状态**对齐**一遍，
       不聚焦 —— 否则整页加载完焦点会跑到终端里（右侧面板默认还是隐藏的）。 */
    showTerm('t1', false);
  }

'''


def patch_js():
    t, nl = rd(PJS)
    if MARK in t:
        SKIPPED.append('panel.js · 全部')
        print('   跳过  panel.js · 全部（已应用）')
        return

    i = t.find(TERM_START)
    if i < 0:
        sys.exit('!! panel.js：找不到终端块起点')
    j = t.find(TERM_END, i)
    if j < 0:
        sys.exit('!! panel.js：找不到终端块终点')
    old_block = t[i:j]
    if old_block.count('CANNED') != 2 or 'npm run dev' not in old_block:
        sys.exit('!! panel.js：终端块内容不像原样（CANNED=%d）' % old_block.count('CANNED'))
    t = t[:i] + TERM_NEW + t[j:]

    # ---- 打标签：④ 的 JS 主块自带 `r107-l2`，后面的零散改动靠 mark 判重 ----
    MARKJS = '/* r107-l2 */'

    def sub(old, new, label):
        nonlocal t
        if t.count(old) != 1:
            sys.exit('!! panel.js · %s：锚点命中 %d 次' % (label, t.count(old)))
        t2 = t.replace(old, new, 1)
        wr(PJS, t2, nl)
        t = t2
        APPLIED.append('panel.js · ' + label)
        print('   应用  panel.js · %s' % label)

    # ② BRW_TEXT 加 shot
    sub("""    var BRW_TEXT = {
      send: '已把当前页面发到对话（视觉演示）',
      zoom: '缩放：100%（视觉演示）',
      more: '更多浏览器选项（视觉演示）'
    };
""",
        """    var BRW_TEXT = {
      send: '已把当前页面发到对话（视觉演示）',
      shot: '已复制截图到剪贴板（视觉演示）',
      zoom: '缩放：100%（视觉演示）',
      more: '更多浏览器选项（视觉演示）'
    };
    /* ★ 第十一拍 ④（r107-l2）：官方「一键截图到剪贴板」= 快门白闪。
       ⚠ 闪的是**整个浏览器模块**（`.td-brw`）而不是 `.td-view`：`.td-view` 自己是
         `overflow:auto` 的滚动容器，绝对定位子元素会跟着内容滚走 ⇒ 滚动后就闪不见了。 */
    function shotFlash() {
      brw.classList.remove('is-shot');
      void brw.offsetWidth;                       /* 强制回流：同一个 class 的动画能重播 */
      brw.classList.add('is-shot');
      setTimeout(function () { brw.classList.remove('is-shot'); }, 300);
    }
""", 'BRW_TEXT + shotFlash')

    sub("""        b.addEventListener('click', function () {
          say(BRW_TEXT[b.getAttribute('data-td-brw-act')] || '已执行');
        });
""",
        """        b.addEventListener('click', function () {
          var kind = b.getAttribute('data-td-brw-act');
          if (kind === 'shot') shotFlash();
          say(BRW_TEXT[kind] || '已执行');
        });
""", 'brwActs 点击分发')

    # ③ 产物预览层（替换原来「只弹 toast」的 artBtns 循环）
    sub("""  var artBtns = pane.querySelectorAll('[data-td-art]');
  for (var ar = 0; ar < artBtns.length; ar++) {
    (function (b) {
      b.addEventListener('click', function () {
        var host = b.closest('.td-sum-art');
        var nm = host && host.querySelector('.td-sum-artt b');
        say('预览 ' + (nm ? nm.textContent : '产物') + '（视觉演示）');
      });
    })(artBtns[ar]);
  }
""",
        """  /* ★ 第十一拍 ④（r107-l2）：产物预览层 —— 对照官方「产物查看器」。
     原来「预览」只弹一句 toast、没有任何视觉，属于真缺口；现在打开一层覆盖整块摘要的
     只读预览（文件名 + 元信息 + 骨架：文档 / 表格两套），并给「在系统打开」「关闭」。 */
  var prevEl = pane.querySelector('[data-td-prev]');
  function prevHide() { if (prevEl) prevEl.setAttribute('hidden', ''); }
  function prevShow(btn) {
    if (!prevEl) return;
    var host = btn && btn.closest ? btn.closest('.td-sum-art') : null;
    var nmEl = host && host.querySelector('.td-sum-artt b');
    var mtEl = host && host.querySelector('.td-sum-artt i');
    var ico = host && host.querySelector('.td-sum-arti svg');
    var name = nmEl ? nmEl.textContent : '产物';
    var kind = (/\\.(xlsx|xls|csv|tsv)$/i).test(name) ? 'xlsx' : 'md';
    var pn = prevEl.querySelector('[data-td-prev-name]');
    var pm = prevEl.querySelector('[data-td-prev-meta]');
    var pi = prevEl.querySelector('[data-td-prev-ico]');
    if (pn) pn.textContent = name;
    if (pm) pm.textContent = (mtEl ? mtEl.textContent : '') + ' · 只读预览';
    if (pi && ico) pi.innerHTML = ico.outerHTML;
    var bodies = prevEl.querySelectorAll('[data-td-prev-kind]');
    for (var q = 0; q < bodies.length; q++) {
      if (bodies[q].getAttribute('data-td-prev-kind') === kind) bodies[q].removeAttribute('hidden');
      else bodies[q].setAttribute('hidden', '');
    }
    prevEl.removeAttribute('hidden');
  }
  var artBtns = pane.querySelectorAll('[data-td-art]');
  for (var ar = 0; ar < artBtns.length; ar++) {
    (function (b) {
      b.addEventListener('click', function () { prevShow(b); });
    })(artBtns[ar]);
  }
  if (prevEl) {
    var prevXs = prevEl.querySelectorAll('[data-td-prev-x], [data-td-prev-close]');
    for (var px = 0; px < prevXs.length; px++) prevXs[px].addEventListener('click', prevHide);
    var prevOpenBtn = prevEl.querySelector('[data-td-prev-open]');
    if (prevOpenBtn) {
      prevOpenBtn.addEventListener('click', function () { say('已在系统应用中打开（视觉演示）'); });
    }
  }
""", '产物预览层')

    # ③ Esc 裁决：把预览层也算一层
    sub("""    var selOpen = selbar && !selbar.hasAttribute('hidden');
    if (!modal && !menuOpen && !noteOpen && !selOpen) return;
""",
        """    var selOpen = selbar && !selbar.hasAttribute('hidden');
    /* ★ 第十一拍 ④（r107-l2）：产物预览层也占一层（不接进来的话，开着预览按 Esc 会
       直接把**整条侧栏**关掉 —— 那是 ctrl-conv.js 的 Esc 在处理）。 */
    var prevOpen = prevEl && !prevEl.hasAttribute('hidden');
    if (!modal && !menuOpen && !noteOpen && !selOpen && !prevOpen) return;
""", 'Esc 裁决 · 计入预览层')

    sub("""    if (noteOpen) elnote.setAttribute('hidden', '');
  }, true);
""",
        """    if (noteOpen) { elnote.setAttribute('hidden', ''); return; }
    if (prevOpen) prevHide();
  }, true);
""", 'Esc 裁决 · 先关预览层')

    # ① 右键菜单：终端那三条改成「真」行为 + 当前标签名进标题
    sub("""  function ctxForTerm() {
    var host = pane.querySelector('[data-td-term]');
    var cleared = !!(host && host.classList.contains('is-cleared'));
    return { head: '终端 · giencoder-design-engineering', items: [
""",
        """  function ctxForTerm() {
    var host = activeTerm();
    var cleared = !!(host && host.classList.contains('is-cleared'));
    var curTab = termTabsEl ? ctxTxt(termTabsEl.querySelector('.td-term-tab.is-active .td-term-tab-nm')) : '';
    return { head: '终端 · ' + (curTab || 'giencoder-design-engineering'), items: [
""", 'ctxForTerm · 取当前标签')

    sub("""      { label: '新建终端标签', ico: 'plus', act: function () { say('已新建终端标签（视觉演示）'); } },
""",
        """      { label: '新建终端标签', ico: 'plus', act: function () {
        var t2 = newTermTab();
        say(t2 ? '已新建终端标签' : '终端不可用');
      } },
""", 'ctxForTerm · 新建标签落地')

    # ② 右键菜单：浏览器补一条「截图到剪贴板」（与地址栏那枚同一个入口）
    sub("""    items.push({ label: '在系统浏览器中打开', ico: 'eye', act: function () { say('已在系统浏览器中打开（视觉演示）'); } });
    return { head: 'http://' + url, items: items };
""",
        """    items.push({ label: '截图到剪贴板', key: '⇧⌘S', ico: 'pin', act: function () {
      var sb = pane.querySelector('[data-td-brw-act="shot"]');
      if (sb) sb.click();
    } });
    items.push({ label: '在系统浏览器中打开', ico: 'eye', act: function () { say('已在系统浏览器中打开（视觉演示）'); } });
    return { head: 'http://' + url, items: items };
""", 'ctxForBrw · 截图')


# ================================================================================
# 3. panel.css · 第 18 节
# ================================================================================
CSS_NEW = """
/* ---------------------------------------------------------------- 18. 对照 Codex 官方补缺（第十一拍 ④）
   ★ 官方现有能力（openai.com「Codex:全能型助手」）里，我们已经有的：五入口 / 摘要面板 /
     行内评论 / 暂存·撤销 / 统一⇄并排 / 对比范围 / 提交·推送·PR / 浏览器标注 / 终端。
     **还缺且能落地的三件**：
       ① 多标签终端（官方「多标签终端」）—— 补标签条 + 第二块会话 + `+` 新建（见 panel.js）
       ② 一键截图到剪贴板（官方）—— 补地址栏那枚相机按钮 + 快门白闪
       ③ 产物查看器（官方 PDF / 表格 / 文档 / 演示预览）—— 补「预览」预览层 + 两套骨架
     （SSH 远程连接（alpha，不在侧栏）/ 多窗口 / 系统托盘：静态演示页落不了地，不做；
       「文件」模块不能编辑：官方亦然，不动。）
     ⚠ 全部只作用于右栏内部；不引渐变（verify-design.py 会数渐变处数，多一处就进回归 diff）。 */

/* 18-① 终端标签条 */
.td-term-tabs {
  flex: none; box-sizing: border-box;
  display: flex; align-items: center; gap: 2px;
  min-height: calc(34px * var(--ui-fs-ratio)); padding: 0 8px;
  border-bottom: 1px solid var(--color-border-1);
  font-size: var(--font-size-body-1);
  overflow-x: auto;
}
.td-term-tab {
  flex: none; display: inline-flex; align-items: center; gap: 6px;
  height: calc(22px * var(--ui-fs-ratio)); padding: 0 8px;
  border: 0; border-radius: 6px; background: transparent;
  color: var(--color-text-3);
  font-family: inherit; font-size: var(--font-size-body-1); cursor: pointer;
  transition: background-color 120ms, color 120ms;
}
.td-term-tab:hover { background: var(--color-fill-1); color: var(--color-text-1); }
.td-term-tab.is-active { background: var(--color-fill-2); color: var(--color-text-1); }
.td-term-tab-ico { flex: none; display: inline-flex; color: var(--color-text-3); }
.td-term-tab.is-active .td-term-tab-ico { color: var(--color-primary-6); }
.td-term-tab-nm { white-space: nowrap; }
.td-term-tabadd {
  flex: none; display: inline-flex; align-items: center; justify-content: center;
  width: calc(22px * var(--ui-fs-ratio)); height: calc(22px * var(--ui-fs-ratio));
  margin-left: 2px; padding: 0;
  border: 0; border-radius: 6px; background: transparent;
  color: var(--color-text-3);
  font-family: inherit; font-size: var(--font-size-body-1); cursor: pointer;
  transition: background-color 120ms, color 120ms;
}
.td-term-tabadd:hover { background: var(--color-fill-1); color: var(--color-text-1); }

/* 18-② 浏览器「截图」快门 —— 闪整个模块（`.td-view` 是滚动容器，覆盖层会跟着内容滚走） */
.td-mod.td-brw { position: relative; }
.td-brw.is-shot::after {
  content: ''; position: absolute; inset: 0; z-index: 5;
  background: var(--color-bg-2); opacity: 0;
  pointer-events: none;
  animation: td-shot-flash 260ms ease;
}
@keyframes td-shot-flash { 0% { opacity: .9; } 100% { opacity: 0; } }

/* 18-③ 产物预览层（覆盖整块摘要；`.td-mod.td-sum` 当包含块 ⇒ 不参与文档流、不撑高） */
.td-mod.td-sum { position: relative; }
.td-sum-prev {
  position: absolute; inset: 0; z-index: 6;
  display: flex; flex-direction: column;
  background: var(--color-bg-2);
}
.td-sum-prev[hidden] { display: none; }
.td-sum-prev-h {
  flex: none; box-sizing: border-box;
  display: flex; align-items: center; gap: 8px;
  min-height: calc(40px * var(--ui-fs-ratio)); padding: 6px 12px;
  border-bottom: 1px solid var(--color-border-1);
  font-size: var(--font-size-body-1);
}
.td-sum-prev-t { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; }
.td-sum-prev-t b {
  font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.td-sum-prev-t i { font-style: normal; font-size: var(--font-size-body-1); color: var(--color-text-3); }
.td-sum-prev-b { flex: 1 1 auto; min-height: 0; overflow: auto; padding: 14px 16px; }
.td-sum-prev-f {
  flex: none; box-sizing: border-box;
  display: flex; align-items: center; justify-content: flex-end; gap: 8px;
  min-height: calc(48px * var(--ui-fs-ratio)); padding: 8px 12px;
  border-top: 1px solid var(--color-border-1);
  font-size: var(--font-size-body-1);
}
.td-prev-btn {
  flex: none; height: calc(28px * var(--ui-fs-ratio)); padding: 0 14px;
  border: 1px solid var(--color-border-2); border-radius: 6px;
  background: transparent; color: var(--color-text-1);
  font-family: inherit; font-size: var(--font-size-body-2); cursor: pointer;
  transition: background-color 120ms, border-color 120ms;
}
.td-prev-btn:hover { background: var(--color-fill-1); border-color: var(--color-border-3); }
.td-prev-btn.is-primary {
  border-color: transparent; background: var(--color-primary-6); color: var(--color-white);
}
.td-prev-btn.is-primary:hover { background: var(--color-primary-5); }
/* 两套骨架互斥。⚠ 必须显式写 `[hidden]`：`.td-pv-md` 自己声明了 `display:flex`，
   会压过 UA 的 `[hidden]{display:none}`（历代踩过的同一个坑）。 */
.td-pv-md[hidden], .td-pv-sheet[hidden] { display: none; }
/* 文档骨架 */
.td-pv-md { display: flex; flex-direction: column; gap: 10px; }
.td-pv-h1 { font-size: var(--font-size-title-1); font-weight: 600; color: var(--color-text-1); line-height: 1.4; }
.td-pv-h2 { font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1); line-height: 1.5; }
.td-pv-p { font-size: var(--font-size-body-2); line-height: calc(22px * var(--ui-fs-ratio)); color: var(--color-text-2); }
.td-pv-bar {
  display: block; width: 100%; height: calc(10px * var(--ui-fs-ratio));
  border-radius: 4px; background: var(--color-fill-2);
  font-size: var(--font-size-body-1);
}
.td-pv-bar.is-w80 { width: 80%; }
.td-pv-bar.is-w60 { width: 60%; }
.td-pv-bar.is-w40 { width: 40%; }
/* 表格骨架 */
.td-pv-sheet {
  display: flex; flex-direction: column; gap: 1px;
  border: 1px solid var(--color-border-1); border-radius: 6px;
  background: var(--color-border-1); overflow: hidden;
}
.td-pv-row { display: flex; gap: 1px; }
.td-pv-cell {
  flex: 1 1 0; min-width: 0; box-sizing: border-box;
  display: flex; align-items: center;
  height: calc(26px * var(--ui-fs-ratio)); padding: 0 8px;
  background: var(--color-bg-2); color: var(--color-text-2);
  font-size: var(--font-size-body-1);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.td-pv-cell.is-head { background: var(--color-fill-1); color: var(--color-text-1); font-weight: 500; }
/* r107-l2 */
"""


def patch_css():
    tail(PCS, MARK, CSS_NEW, 'panel.css · 第 18 节（①标签条 ②快门 ③预览层）')


# ================================================================================
def main():
    print('== r107 第十一拍 ④ · 对照 Codex 官方补缺 ==')
    patch_mods()
    patch_js()
    patch_css()
    print('--- 应用 %d 项 / 跳过 %d 项 ---' % (len(APPLIED), len(SKIPPED)))


if __name__ == '__main__':
    main()
