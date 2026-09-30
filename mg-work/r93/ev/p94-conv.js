(function () {
  function info(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    var cs = getComputedStyle(el);
    return { tag: el.tagName.toLowerCase(), cls: (el.className && el.className.toString()) || '',
             x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
             disp: cs.display, order: cs.order, flex: cs.flex };
  }
  var out = {};
  out.htmlAttr = document.documentElement.getAttribute('data-r93-page');
  out.title = document.title;
  var main = document.querySelector('main');
  var inner = main ? main.querySelector(':scope > div') : null;
  out.innerKids = inner ? [].map.call(inner.children, info) : [];
  var host = document.querySelector('.r93-conv-host');
  out.host = info(host);
  out.hostKidsCls = host ? [].map.call(host.children, function (c) { return (c.className || '') + '|h=' + Math.round(c.getBoundingClientRect().height); }) : [];
  var hero = null;
  if (inner) for (var i = 0; i < inner.children.length; i++) {
    if (/justify-center/.test(inner.children[i].className || '')) hero = inner.children[i];
  }
  out.hero = info(hero);
  out.heroKids = hero ? [].map.call(hero.children, info) : [];
  out.outer = info(document.querySelector('div[class*="w-[800px]"]'));
  out.card = info(document.querySelector('div[class*="rounded-[16px]"][class*="bg-white"]'));
  var sb = host && host.querySelector('.r93-sb');
  var ag = host && host.querySelector('.r93-agents');
  out.sb = info(sb);
  out.agents = info(ag);
  out.agentN = ag ? ag.children.length : 0;
  out.agentKids = ag ? [].map.call(ag.children, function (c) { var r = c.getBoundingClientRect(); return { cls: c.className, x: Math.round(r.x), w: Math.round(r.width), h: Math.round(r.height) }; }) : [];
  out.cardRowText = (document.querySelector('div[class*="mt-auto"][class*="justify-between"]') || {}).textContent || '';
  out.workdirRow = info(document.querySelector('div[class*="pt-[6px]"]'));
  out.workdirTxt = (document.querySelector('div[class*="pt-[6px]"]') || {}).textContent || '';
  var sc = host && host.querySelector('.r93-scroll');
  out.scroll = sc ? { scrollH: sc.scrollHeight, clientH: sc.clientHeight, top: Math.round(sc.getBoundingClientRect().top) } : null;
  var wrap = host && host.querySelector('.r93-wrap');
  out.wrap = info(wrap);
  out.pageH = { doc: document.documentElement.scrollHeight, win: window.innerHeight };
  out.footer = info(document.querySelector('main > div > div.pb-6'));
  return JSON.stringify(out);
})()
