/* r108 第十八拍（第七层补丁）· 四条真机取证。
   相位（window.__M）：base / menuOpen / menuRead / menuClose
                        rvOpen / rvRead / rvScroll / rvScrollBack
                        pvOpen / pvRead
   ⚠ 「点击」与「读值」分帧（硬规则 29）；⚠ 采集同一次 eval 内跑完（硬规则 25 ②）。
   ⚠ 同一次 eval 内既点又读会吃掉过渡/重排 —— 所以 open 与 read 一律拆相位。 */
(function () {
  var M = window.__M || 'base';
  function q(s) { return document.querySelector(s); }
  function qa(s) { return [].slice.call(document.querySelectorAll(s)); }
  function r(e) { if (!e) return null; var b = e.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(e, p) { return e ? getComputedStyle(e)[p] : null; }
  /* 祖先链：h = 实测高；ch/sh = clientHeight / scrollHeight；
     of = overflow-y；fx = flex；mh = min-height；pos = position。
     ⚠ 判据：只要某层出现「h 被内容撑大（ch 远大于零且 sh == ch 且 h 很大）」= 断链层。 */
  function chain(e) {
    var out = [], n = e, i = 0;
    while (n && n.tagName && i < 12) {
      var cls = (typeof n.className === 'string') ? n.className : '';
      out.push([n.tagName.toLowerCase() + (cls ? '.' + cls.split(' ').join('.') : ''),
                Math.round(n.getBoundingClientRect().height), n.clientHeight, n.scrollHeight,
                cs(n, 'overflowY'), cs(n, 'display'), cs(n, 'flex'), cs(n, 'minHeight'), cs(n, 'position')]);
      n = n.parentElement; i++;
    }
    return out;
  }
  /* ★ 侧栏在页面加载时是 `translateX` 收在视口外的（旧坑：此时几何量「正确」但截图全空）
     ⇒ 截图前必须先开一个模块把侧栏滑进来。 */
  function act(mod) {
    var t = qa('.td-browse-tabs [data-td-tab]').filter(function (x) {
      return x.getAttribute('data-td-mod') === mod;
    })[0];
    if (t) { t.click(); return 'tab:' + mod; }
    var o = q('[data-td-open-mod="' + mod + '"]');
    if (o) { o.click(); return 'open:' + mod; }
    return 'miss:' + mod;
  }
  var out = {};
  if (M === 'openTabs') {
    out.done = [act('terminal'), act('browser'), act('review')];
    out.browse = r(q('.td-browse'));
    out.sidebarOn = !!(q('.td-browse') && /av-browse-on/.test(q('.td-browse').className));
  }
  if (M === 'base') {
    out.browseActs = qa('.td-browse-acts .td-browse-ico').map(function (b) { return b.getAttribute('aria-label'); });
    out.maxBtn = qa('[data-td-max]').length;
    out.menuItems = qa('.td-mod-menu .td-mm-item .td-mm-name').map(function (s) { return s.textContent; });
    out.winW = window.innerWidth;
  }
  if (M === 'menuOpen') { var b0 = q('[data-td-add]'); if (b0) b0.click(); out.clicked = !!b0; }
  if (M === 'menuRead') {
    out.menuItems = qa('.td-mod-menu .td-mm-item').map(function (it) {
      var nm = it.querySelector('.td-mm-name');
      return [nm ? nm.textContent : '?', it.getAttribute('data-td-open-mod'),
              Math.round(it.getBoundingClientRect().top)];
    });
    out.menuRect = r(q('.td-mod-menu'));
  }
  if (M === 'menuClose') { var b1 = q('[data-td-add]'); if (b1) b1.click(); out.clicked = !!b1; }
  if (M === 'rvOpen') {
    var t = q('.td-browse-tabs [data-td-tab][data-td-mod="review"]');
    if (t) { t.click(); out.act = 'tab:review'; }
    else { var o = q('[data-td-open-mod="review"]'); if (o) { o.click(); out.act = 'open:review'; } }
  }
  if (M === 'rvRead') {
    var body = q('.td-rv-body');
    out.body = r(body);
    out.bodySz = body ? [body.clientHeight, body.scrollHeight] : null;
    out.bodyOf = cs(body, 'overflowY');
    var card0 = q('.td-rv-body > .td-diff');
    out.cardFlex = cs(card0, 'flex');
    out.cardFlexGrow = cs(card0, 'flexGrow');
    out.cardFlexShrink = cs(card0, 'flexShrink');
    out.cardNatural = qa('.td-rv-body > .td-diff').map(function (c) {
      return [Math.round(c.getBoundingClientRect().height), c.clientHeight, c.scrollHeight];
    });
    out.chain = chain(body);
    out.docSh = document.scrollingElement.scrollHeight;
    out.docCh = document.scrollingElement.clientHeight;
    out.docOverflow = out.docSh - out.docCh;      /* > 0 ⇒ 整页可以滚（= 故障） */
    out.diffs = qa('.td-diff').length;
    out.openDiffs = qa('.td-diff.is-open').length;
  }
  if (M === 'rvScroll') {
    var body2 = q('.td-rv-body');
    var before = document.scrollingElement.scrollTop;
    if (body2) body2.scrollTop = 9999;
    out.bodyScrollTop = body2 ? body2.scrollTop : null;
    out.bodyScrollable = body2 ? (body2.scrollHeight - body2.clientHeight) : null;
    out.pageScrollTopBefore = before;
    out.pageScrollTopAfter = document.scrollingElement.scrollTop;
    /* 再用「滚轮事件打给容器」验一次真链路（scroll 是否被容器吃掉） */
    out.diffRowsTop = r(q('.td-diff-rows'));
  }
  if (M === 'pvOpen') {
    var a = q('.td-sum-art[data-td-art]');
    if (a) { var tb = a.querySelector('.td-diff-btn'); (tb || a).click(); out.act = 'sum-art'; }
    else out.act = 'miss';
  }
  if (M === 'pvRead') {
    var bar = q('#av-browse-pane-preview .td-mod-bar');
    out.barActs = qa('#av-browse-pane-preview .td-mod-bar-acts > *').map(function (b) {
      return [b.tagName.toLowerCase(), b.className, (b.textContent || '').trim(),
              b.getAttribute('data-td-prev-open'), b.getAttribute('data-td-prev-save'),
              b.getAttribute('data-td-prev-reveal')];
    });
    out.barActsBox = qa('#av-browse-pane-preview .td-mod-bar-acts > *').map(function (b) {
      return r(b);
    });
    out.barRect = r(bar);
    out.tabs = qa('.td-browse-tabs [data-td-tab]').map(function (x) { return x.getAttribute('data-td-mod'); });
  }
  return JSON.stringify(out);
})()
