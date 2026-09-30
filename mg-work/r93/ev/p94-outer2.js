(function () {
  function brief(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { tag: el.tagName.toLowerCase(), cls: (el.className && el.className.toString()) || '',
             x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
             text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120),
             html: el.outerHTML.slice(0, 1500) };
  }
  var outer = document.querySelector('div[class*="w-[800px]"]');
  var out = { outerKids: [] };
  if (outer) {
    [].forEach.call(outer.children, function (c) { out.outerKids.push(brief(c)); });
  }
  /* hero 与 front 的样式细节 */
  var inner = document.querySelector('main > div');
  var hero = inner && inner.children[0];
  out.heroStyle = hero ? { flex: getComputedStyle(hero).flex, jc: getComputedStyle(hero).justifyContent,
                           pb: getComputedStyle(hero).paddingBottom, px: getComputedStyle(hero).paddingLeft } : null;
  var wrap = hero && hero.children[1];
  out.wrapStyle = wrap ? { mt: getComputedStyle(wrap).marginTop, h: Math.round(wrap.getBoundingClientRect().height) } : null;
  return JSON.stringify(out);
})()
