(function () {
  var pane = document.querySelector('.td-browse');
  var m = pane.querySelector('.td-mod-menu');
  var mc = getComputedStyle(m);
  var r = m.getBoundingClientRect();
  var it = m.querySelector('.td-mm-item');
  var ic = getComputedStyle(it);
  var cap = m.querySelector('.td-mm-cap');
  var cc = getComputedStyle(cap);
  var ico = m.querySelector('.td-mm-ico');
  var mark = m.querySelector('.td-mm-mark');
  var out = {
    menu: {
      hidden: m.hasAttribute('hidden'), cls: m.className,
      vis: mc.visibility, op: mc.opacity, transform: mc.transform, scale: mc.scale,
      bg: mc.backgroundColor, border: mc.borderTopWidth + ' ' + mc.borderTopColor,
      r: mc.borderTopLeftRadius, shadow: mc.boxShadow,
      maxH: mc.maxHeight, pad: mc.paddingTop + ' ' + mc.paddingLeft + ' ' + mc.paddingBottom + ' ' + mc.paddingRight,
      w: Math.round(r.width * 100) / 100, x: Math.round(r.x), y: Math.round(r.y)
    },
    item: { h: ic.height, r: ic.borderTopLeftRadius, pl: ic.paddingLeft, fs: ic.fontSize, bg: ic.backgroundColor, gap: ic.gap, border: ic.borderTopWidth },
    icon: { display: getComputedStyle(ico).display, flex: getComputedStyle(ico).flex },
    cap: { cls: cap.className, fs: cc.fontSize, pl: cc.paddingLeft, pt: cc.paddingTop, color: cc.color },
    mark: mark ? { w: getComputedStyle(mark).width, op: getComputedStyle(mark).opacity } : null,
    itemCount: m.querySelectorAll('.td-mm-item').length
  };
  /* 换到审查标签，验「对比范围 / 显示选项 / 提交」三枚下拉也是 DS 组件 + 选中态 */
  var tabSrc = pane.querySelector('[data-td-open-mod="review"]');
  tabSrc.click();
  pane.querySelector('[data-td-add]').click();     /* 关掉 + 菜单 */
  var opts = pane.querySelector('.td-rv-opts');
  pane.querySelector('[data-td-rv-opts]').click();
  var oc = getComputedStyle(opts);
  out.opts = {
    cls: opts.className, hidden: opts.hasAttribute('hidden'), vis: oc.visibility,
    w: Math.round(opts.getBoundingClientRect().width), items: opts.querySelectorAll('.td-mm-item').length
  };
  var sel1 = opts.querySelector('.giencoder-menu-item-selected');
  if (sel1) {
    var s1 = getComputedStyle(sel1);
    out.optsSelected = { txt: sel1.textContent.trim(), bg: s1.backgroundColor, color: s1.color, w: s1.fontWeight, r: s1.borderTopLeftRadius };
  }
  pane.querySelector('[data-td-rv-opts]').click();
  var scope = pane.querySelector('.td-rv-scope-menu');
  pane.querySelector('[data-td-rv-scope]').click();
  out.scope = {
    cls: scope.className, hidden: scope.hasAttribute('hidden'),
    items: scope.querySelectorAll('.td-mm-item').length,
    head: scope.querySelector('.td-mm-cap') ? scope.querySelector('.td-mm-cap').textContent.trim() : null
  };
  var sel2 = scope.querySelector('.giencoder-menu-item-selected');
  if (sel2) out.scopeSelected = { txt: sel2.textContent.trim(), bg: getComputedStyle(sel2).backgroundColor };
  pane.querySelector('[data-td-rv-scope]').click();
  var cm = pane.querySelector('.td-commit-menu');
  pane.querySelector('[data-td-commit]').click();
  out.commit = { cls: cm.className, hidden: cm.hasAttribute('hidden'), items: cm.querySelectorAll('.td-mm-item').length };
  pane.querySelector('[data-td-commit]').click();
  out.allClosed = [].every.call(pane.querySelectorAll('.td-mod-menu, .td-rv-menu'), function (e) { return e.hasAttribute('hidden'); });
  return JSON.stringify(out);
})()
