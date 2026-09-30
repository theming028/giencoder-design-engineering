(function () {
  function info(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return {
      tag: el.tagName.toLowerCase(),
      cls: (el.className && el.className.toString()) || '',
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height)
    };
  }
  function brief(el) {
    var i = info(el);
    if (!i) return null;
    i.text = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40);
    i.aria = el.getAttribute('aria-label') || '';
    i.nkids = el.children.length;
    return i;
  }
  var out = {};
  var main = document.querySelector('main');
  var inner = main ? main.querySelector(':scope > div') : null;
  out.main = info(main);
  out.inner = info(inner);
  out.innerKids = inner ? [].map.call(inner.children, brief) : [];

  /* hero：mainInner 第 1 个 <div class*=justify-center> */
  var hero = null;
  if (inner) {
    for (var i = 0; i < inner.children.length; i++) {
      if (/justify-center/.test(inner.children[i].className || '')) { hero = inner.children[i]; break; }
    }
  }
  out.hero = brief(hero);
  out.heroKids = hero ? [].map.call(hero.children, brief) : [];

  /* composer 外层（w-[800px]）与内层卡片（rounded-[16px] border bg-white p-3） */
  var wrap = document.querySelector('div[class*="mt-8"][class*="flex-col"]');
  out.wrap = brief(wrap);
  var outer = document.querySelector('div[class*="w-[800px]"]');
  out.outer = brief(outer);
  var card = document.querySelector('div[class*="rounded-[16px]"][class*="bg-white"]');
  out.card = brief(card);

  /* 内层卡片的直接子节点 + 底排按钮全枚举 */
  out.cardKids = card ? [].map.call(card.children, brief) : [];
  var row = card ? card.querySelector(':scope > div.mt-auto') : null;
  out.row = brief(row);
  out.rowKids = row ? [].map.call(row.children, brief) : [];
  var left = row ? row.children[0] : null;
  out.leftKids = left ? [].map.call(left.children, brief) : [];
  /* 底排所有 button 的可访问名 */
  out.rowBtns = row ? [].map.call(row.querySelectorAll('button'), function (b) {
    return { aria: b.getAttribute('aria-label') || '', cls: b.className, t: (b.textContent || '').trim().slice(0, 20), size: info(b) };
  }) : [];
  /* 卡内所有 input/textarea */
  out.inputs = card ? [].map.call(card.querySelectorAll('input,textarea'), brief) : [];

  /* 会话详情注入宿主是否在 */
  out.host = brief(document.querySelector('.r93-conv-host'));
  /* aside 会话项 */
  out.asideConv = [].map.call(document.querySelectorAll('aside button.min-w-0.flex-1'), function (b) {
    return { t: (b.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 28), h: Math.round(b.getBoundingClientRect().height) };
  });
  return JSON.stringify(out);
})()
