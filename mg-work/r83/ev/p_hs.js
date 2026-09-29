(function () {
  var out = {};
  var d = document.getElementById('av-chat-drawer');
  var v = document.getElementById('av-hs');
  if (!d || !v) return JSON.stringify({ err: 'no view' });
  document.documentElement.setAttribute('data-av-chat-open', '');
  out.opened = !!document.documentElement.hasAttribute('data-av-chat-open');

  var entry = d.querySelector('.td-right-acts [aria-label="会话历史"]');
  out.hasEntry = !!entry;
  out.displayBefore = getComputedStyle(v).display;
  if (entry) entry.click();
  out.drawerAttr = d.getAttribute('data-av-hs');
  out.displayAfter = getComputedStyle(v).display;

  function R(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)];
  }
  function rel(el, host) {
    if (!el || !host) return null;
    var a = el.getBoundingClientRect(), b = host.getBoundingClientRect();
    return [Math.round(a.left - b.left), Math.round(a.top - b.top), Math.round(a.width), Math.round(a.height)];
  }
  function cs(el, props) {
    if (!el) return null;
    var s = getComputedStyle(el), o = [];
    for (var i = 0; i < props.length; i++) o.push(s[props[i]]);
    return o;
  }

  out.view = R(v);
  var bar = v.querySelector('.av-hs-bar');
  out.bar = rel(bar, v);
  out.barBorder = cs(bar, ['borderBottomWidth', 'borderBottomColor']);
  out.back = rel(v.querySelector('.av-hs-back'), v);
  out.backIcon = cs(v.querySelector('.av-hs-back svg'), ['width', 'height']);
  out.rule = rel(v.querySelector('.av-hs-rule'), v);
  out.ruleBg = cs(v.querySelector('.av-hs-rule'), ['backgroundColor']);
  var ttl = v.querySelector('.av-hs-title');
  out.title = rel(ttl, v);
  out.titleFont = cs(ttl, ['fontSize', 'fontWeight', 'lineHeight', 'color']);

  var list = v.querySelector('.av-hs-list');
  out.list = rel(list, v);
  out.listPad = cs(list, ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'rowGap']);
  out.listRect = R(list);

  var items = v.querySelectorAll('.av-hs-item');
  out.n = items.length;
  out.item0 = rel(items[0], list);
  out.item2 = rel(items[2], list);
  out.bg0 = cs(items[0], ['backgroundColor']);
  out.bg1 = cs(items[1], ['backgroundColor']);
  out.pad0 = cs(items[0], ['paddingLeft', 'paddingRight', 'borderRadius']);

  var nm0 = items[0].querySelector('.av-hs-name');
  out.name0 = rel(nm0, items[0]);
  out.nameFont = cs(nm0, ['fontSize', 'fontWeight', 'lineHeight', 'color']);
  var tm0 = items[0].querySelector('.av-hs-time');
  out.time0 = rel(tm0, items[0]);
  out.time0Text = JSON.stringify(tm0.textContent);
  out.timeFont = cs(tm0, ['fontSize', 'lineHeight', 'color']);
  out.name2 = rel(items[2].querySelector('.av-hs-name'), items[2]);
  out.time2 = rel(items[2].querySelector('.av-hs-time'), items[2]);
  out.time2Text = items[2].querySelector('.av-hs-time').textContent;

  var ibs = items[0].querySelectorAll('.av-hs-ibtn');
  out.ib0 = rel(ibs[0], items[0]);
  out.ib1 = rel(ibs[1], items[0]);
  out.ibPad = cs(ibs[1], ['padding', 'borderRadius', 'color']);
  out.ibIconBox = cs(ibs[1].querySelector('svg'), ['width', 'height']);

  /* 删除 → 确认态（⚠ 打在第 3 行，与设计稿一致，便于逐像素对照） */
  var it2 = items[2];
  out.bg2Before = cs(it2, ['backgroundColor']);
  /* ⚠ 行有 transition: background-color 120ms ⇒ 若不掐掉过渡，读到的会是动画起点（透明） */
  it2.style.transition = 'none';
  it2.querySelectorAll('.av-hs-ibtn')[1].click();
  out.confirmOn = it2.classList.contains('is-confirm');
  out.confirmBg = cs(it2, ['backgroundColor']);
  out.actsDisplay = cs(it2.querySelector('.av-hs-acts'), ['display']);
  var cb = it2.querySelector('[data-av-hs-cancel]');
  var ok = it2.querySelector('[data-av-hs-ok]');
  out.cancel = rel(cb, it2);
  out.ok = rel(ok, it2);
  out.cancelStyle = cs(cb, ['height', 'paddingLeft', 'backgroundColor', 'borderTopColor', 'fontSize', 'borderRadius']);
  out.okStyle = cs(ok, ['height', 'paddingLeft', 'backgroundColor', 'color', 'borderRadius']);
  out.confirmRight = Math.round(it2.getBoundingClientRect().right - ok.getBoundingClientRect().right);

  /* 取消 → 复原 */
  cb.click();
  out.confirmOff = !it2.classList.contains('is-confirm');
  out.bg2After = cs(it2, ['backgroundColor']);
  out.onlyOneConfirm = v.querySelectorAll('.av-hs-item.is-confirm').length;
  it2.style.transition = '';

  /* 返回 → 对话视图 */
  v.querySelector('[data-av-hs-back]').click();
  out.attrAfterBack = d.getAttribute('data-av-hs');
  out.displayAfterBack = getComputedStyle(v).display;
  out.composerAfterBack = getComputedStyle(d.querySelector('.td-composer')).display;

  /* 再进一次，把状态摆成与设计稿一致（第 1 行「当前会话」+ 第 3 行确认态）后留给截图 */
  if (entry) entry.click();
  out.reopen = getComputedStyle(v).display;
  var its = v.querySelectorAll('.av-hs-item');
  for (var k = 0; k < its.length; k++) its[k].classList.remove('is-on');
  its[0].classList.add('is-on');
  its[2].querySelectorAll('.av-hs-ibtn')[1].click();
  out.shotState = {
    on: its[0].classList.contains('is-on'),
    confirm: its[2].classList.contains('is-confirm'),
    listScrollTop: v.querySelector('.av-hs-list').scrollTop
  };
  out.viewRectForShot = out.view;
  return JSON.stringify(out);
})()
