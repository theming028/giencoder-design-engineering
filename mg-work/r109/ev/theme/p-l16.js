/* r109 第十六拍 · 真机探针：产物卡可点开右栏 + 一文件一页签 */
(function () {
  var out = { ok: true };
  var cards = Array.prototype.slice.call(document.querySelectorAll('.r93-artcard'));
  out.cardCount = cards.length;
  out.cards = cards.map(function (c) {
    return {
      name: c.getAttribute('data-r93-artname') || '',
      cls: c.className,
      cursor: getComputedStyle(c).cursor,
      hasIco: !!c.querySelector('.r93-artic svg'),
      meta: (function () { var m = c.querySelector('.r93-artmeta'); return m ? m.textContent : ''; })()
    };
  });

  var tabsEl = document.querySelector('#av-browse-slot .td-browse-tabs') ||
               document.querySelector('.td-browse-tabs');
  function tabs() {
    return Array.prototype.slice.call(document.querySelectorAll('[data-td-tab]')).map(function (t) {
      return {
        mod: t.getAttribute('data-td-mod'),
        file: t.getAttribute('data-td-file') || '',
        active: t.classList.contains('is-active'),
        name: (t.querySelector('.td-browse-tabn') || t).textContent.trim().slice(0, 24)
      };
    });
  }
  out.tabsBefore = tabs();

  var slot = document.querySelector('#av-browse-slot');
  out.slotOpenBefore = slot ? (slot.className || '') : '(no slot)';

  /* 点第 1 张产物卡（真正派发一次 click，走 document 委托） */
  function fire(el) {
    el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
  }
  var targetA = null, targetB = null;
  cards.forEach(function (c) {
    var n = c.getAttribute('data-r93-artname') || '';
    if (!targetA && n === 'prd-template.html') targetA = c;
    if (!targetB && n === 'spec-template.md') targetB = c;
  });
  if (targetA) fire(targetA);
  out.tabsAfterA = tabs();
  out.paneA = (function () {
    var pn = document.querySelector('[data-td-prev-name]');
    var pm = document.querySelector('[data-td-prev-meta]');
    var vis = Array.prototype.slice.call(document.querySelectorAll('[data-td-prev-kind]'))
      .filter(function (b) { return !b.hasAttribute('hidden'); })
      .map(function (b) { return b.getAttribute('data-td-prev-kind'); });
    return { name: pn ? pn.textContent : '', meta: pm ? pm.textContent : '', visible: vis };
  })();
  out.slotOpenAfterA = document.querySelector('#av-browse-slot').className;

  if (targetB) fire(targetB);
  out.tabsAfterB = tabs();
  out.paneB = (function () {
    var pn = document.querySelector('[data-td-prev-name]');
    var pm = document.querySelector('[data-td-prev-meta]');
    return { name: pn ? pn.textContent : '', meta: pm ? pm.textContent : '' };
  })();

  /* 点回 A 页签 ⇒ 面板切回 A */
  (function () {
    var tb = null;
    Array.prototype.slice.call(document.querySelectorAll('[data-td-tab]')).forEach(function (t) {
      if (t.getAttribute('data-td-file') === 'prd-template.html') tb = t;
    });
    if (tb) {
      fire(tb);
      out.paneBackToA = (function () {
        var pn = document.querySelector('[data-td-prev-name]');
        return { name: pn ? pn.textContent : '', tabs: tabs() };
      })();
    }
  })();

  /* 「查看所有产物 (12)」不应可点开预览（无 data-r93-artname） */
  (function () {
    var all = null;
    cards.forEach(function (c) {
      if ((c.textContent || '').indexOf('查看所有产物') >= 0) all = c;
    });
    out.artallHasAttr = all ? all.hasAttribute('data-r93-artname') : null;
    var before = tabs().length;
    if (all) fire(all);
    out.tabsAfterArtall = tabs().length;
    out.artallNoNewTab = (tabs().length === before);
  })();

  return JSON.stringify(out, null, 1);
})();
