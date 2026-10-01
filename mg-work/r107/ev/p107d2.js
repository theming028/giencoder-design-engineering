(function () {
  var pane = document.querySelector('.td-browse');
  var out = {};
  var act = pane.querySelector('.td-browse-tab.is-active');
  out.activeTab = act ? act.getAttribute('data-td-mod') : null;
  out.tabFs = act ? getComputedStyle(act).fontSize : null;
  out.tabH = act ? getComputedStyle(act).height : null;
  out.visible = [].filter.call(pane.querySelectorAll('[data-td-pane], .td-browse-body'), function (e) {
    return !e.hasAttribute('hidden');
  }).map(function (e) { return e.id || e.className; });

  var secs = pane.querySelectorAll('.td-sum-sec');
  out.secCount = secs.length;
  if (secs.length) {
    var c0 = getComputedStyle(secs[0]);
    out.sec = { bw: c0.borderTopWidth, r: c0.borderTopLeftRadius, bg: c0.backgroundColor, pad: c0.paddingTop };
    out.secGap = getComputedStyle(pane.querySelector('.td-sum-body')).gap;
  }
  var src = pane.querySelector('.td-sum-src');
  if (src) {
    var cs = getComputedStyle(src);
    out.srcRow = { bw: cs.borderTopWidth, bg: cs.backgroundColor, pad: cs.paddingTop };
  }
  var art = pane.querySelector('.td-sum-art');
  if (art) {
    var ca = getComputedStyle(art);
    out.artRow = { bw: ca.borderTopWidth, bg: ca.backgroundColor, pad: ca.paddingTop };
  }
  /* 开 `+` 菜单，**故意不关** —— 交给下一次 eval 在过渡结束后量 */
  pane.querySelector('[data-td-add]').click();
  out.menuOpen = !pane.querySelector('.td-mod-menu').hasAttribute('hidden');
  return JSON.stringify(out);
})()
