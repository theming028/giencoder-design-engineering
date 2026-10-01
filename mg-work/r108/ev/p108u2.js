/* 追加相位：审查模块「内容超出时」到底谁在滚。
   相位：openRv / rvNow / expandAll / wheel
   ⚠ 上版把插入点写进了 `stub()` 里（file 被改），这版重写干净。 */
(function () {
  var M = window.__M || 'base';
  function q(s) { return document.querySelector(s); }
  function qa(s) { return [].slice.call(document.querySelectorAll(s)); }
  function r(e) { if (!e) return null; var b = e.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(e, p) { return e ? getComputedStyle(e)[p] : null; }

  function snap() {
    var body = q('.td-rv-body'), aside = q('.td-browse'), mod = q('.td-mod.td-rv');
    return {
      viewport: [window.innerWidth, window.innerHeight],
      body: r(body),
      bodySz: body ? [body.clientHeight, body.scrollHeight] : null,
      bodyScrollable: body ? (body.scrollHeight - body.clientHeight) : null,
      bodyOf: cs(body, 'overflowY'),
      mod: r(mod),
      modSz: mod ? [mod.clientHeight, mod.scrollHeight] : null,
      modOf: cs(mod, 'overflowY'),
      asideSz: aside ? [aside.clientHeight, aside.scrollHeight] : null,
      asideOf: cs(aside, 'overflowY'),
      slotSz: q('.td-browse-slot') ? [q('.td-browse-slot').clientHeight, q('.td-browse-slot').scrollHeight] : null,
      browseBodyHidden: q('.td-browse-body') ? q('.td-browse-body').hasAttribute('hidden') : null,
      docSh: document.scrollingElement.scrollHeight,
      docCh: document.scrollingElement.clientHeight,
      docOverflow: document.scrollingElement.scrollHeight - document.scrollingElement.clientHeight,
      docScrollTop: document.scrollingElement.scrollTop,
      openDiffs: qa('.td-diff.is-open').length,
      diffs: qa('.td-diff').length
    };
  }

  var out = {};
  if (M === 'openRv') {
    var o = q('[data-td-open-mod="review"]');
    out.act = null;
    if (o) { o.click(); out.act = 'menu:review'; }
    else { out.act = 'miss'; }
  }
  if (M === 'rvNow') { out = snap(); }
  if (M === 'expandAll') {
    /* ★ 只展开「当前是折叠态」的（`aria-expanded=false`）——
       无脑 toggle 会「开一个关一个」，净开数恒为 0（上版就栽在这）。 */
    var tg = qa('.td-diff-toggle');
    var clicked = 0;
    for (var i = 0; i < tg.length; i++) {
      if (tg[i].getAttribute('aria-expanded') !== 'true') { tg[i].click(); clicked++; }
    }
    out.toggles = tg.length;
    out.clicked = clicked;
    out.openAfter = qa('.td-diff.is-open').length;
  }
  if (M === 'squash') {
    /* ★ 假设：`.td-rv-body` 是 flex 纵列，子件默认 `flex: 0 1 auto` ⇒ 装不下就**压扁**
       （而不是溢出）⇒ `scrollHeight == clientHeight` 恒成立、容器永不滚。
       判据：子件的「自然高」(`scrollHeight`) > 它的「实占高」(`clientHeight`) = 被压扁。 */
    var cards = qa('.td-rv-body > *');
    out.container = { sz: [q('.td-rv-body').clientHeight, q('.td-rv-body').scrollHeight] };
    out.cards = cards.map(function (c) {
      var rows = c.querySelector('.td-diff-rows');
      return {
        cls: c.className,
        h: Math.round(c.getBoundingClientRect().height),
        ch: c.clientHeight, sh: c.scrollHeight,
        of: cs(c, 'overflowY'), fx: cs(c, 'flex'), mh: cs(c, 'minHeight'),
        rowsCh: rows ? rows.clientHeight : null,
        rowsSh: rows ? rows.scrollHeight : null,
        rowsOf: rows ? cs(rows, 'overflowY') : null,
        natH: rows ? rows.scrollHeight + (c.clientHeight - (rows.clientHeight || 0)) : null
      };
    });
    out.sumNatural = out.cards.reduce(function (a, c) { return a + (c.natH || c.h); }, 0);
    out.containerClient = q('.td-rv-body').clientHeight;
  }
  if (M === 'wheel') {
    var body = q('.td-rv-body');
    var b = body.getBoundingClientRect();
    var hit = document.elementFromPoint(Math.round(b.left + b.width / 2), Math.round(b.top + b.height / 2));
    out.hit = hit ? (hit.tagName.toLowerCase() + '.' + (typeof hit.className === 'string' ? hit.className.split(' ').join('.') : '')) : null;
    out.hitInsideBody = !!(hit && body.contains(hit));
    out.scrollable = body.scrollHeight - body.clientHeight;
    out.before = [body.scrollTop, document.scrollingElement.scrollTop];
    for (var k = 0; k < 8; k++) {
      (hit || body).dispatchEvent(new WheelEvent('wheel', { deltaY: 140, bubbles: true, cancelable: true }));
    }
    out.afterWheel = [body.scrollTop, document.scrollingElement.scrollTop];
    body.scrollTop = 99999;
    out.afterForce = [body.scrollTop, document.scrollingElement.scrollTop];
    out.rowsTopAfter = r(q('.td-diff-rows'));
  }
  return JSON.stringify(out);
})()
