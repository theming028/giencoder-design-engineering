/* r85 静态探针：量导航与内容的几何，全部相对各自 host，便于与设计稿坐标对表 */
JSON.stringify((function () {
  function rel(el, base) {
    if (!el) return null;
    var r = el.getBoundingClientRect(), b = base.getBoundingClientRect();
    return [Math.round(r.left - b.left), Math.round(r.top - b.top), Math.round(r.width), Math.round(r.height)];
  }
  function cs(el, prop) { return el ? getComputedStyle(el)[prop] : null; }
  var navHost = document.querySelector('.r85-nav-host');
  var pageHost = document.querySelector('.r85-page-host');
  var back = document.querySelector('.r85-back');
  var groups = [].map.call(document.querySelectorAll('.r85-group'), function (g) {
    return {
      title: g.querySelector('.r85-gt').textContent,
      gtBox: rel(g.querySelector('.r85-gt'), navHost),
      items: [].map.call(g.querySelectorAll('.r85-navi'), function (b) {
        var sv = b.querySelector('svg');
        return {
          t: b.textContent, box: rel(b, navHost),
          cur: b.getAttribute('aria-current'),
          bg: cs(b, 'backgroundColor'),
          icBox: rel(sv, navHost), icColor: cs(sv, 'color'), icVB: sv.getAttribute('viewBox'),
          fs: cs(b, 'fontSize')
        };
      })
    };
  });
  var title = document.querySelector('.r85-title');
  var cards = [].map.call(document.querySelectorAll('.r85-card'), function (c) {
    return {
      box: rel(c, pageHost), bg: cs(c, 'backgroundColor'), bd: cs(c, 'borderTopColor'),
      radius: cs(c, 'borderTopLeftRadius'), pad: cs(c, 'paddingTop') + '/' + cs(c, 'paddingLeft'),
      rows: [].map.call(c.querySelectorAll('.r85-row'), function (r, i) {
        var ic = r.querySelector('.r85-ic'), tx = r.querySelector('.r85-tx');
        var t = r.querySelector('.r85-t'), d = r.querySelector('.r85-d');
        var ctl = r.querySelector('.r85-ctl');
        var before = getComputedStyle(r, '::before');
        return {
          i: i, t: t.textContent, box: rel(r, pageHost),
          ic: rel(ic, pageHost), icBg: cs(ic, 'backgroundColor'), icR: cs(ic, 'borderTopLeftRadius'),
          tx: rel(tx, pageHost), tBox: rel(t, pageHost), dBox: rel(d, pageHost),
          tFs: cs(t, 'fontSize'), tFw: cs(t, 'fontWeight'), tColor: cs(t, 'color'), dColor: cs(d, 'color'), dFs: cs(d, 'fontSize'),
          ctl: rel(ctl, pageHost),
          line: i === 0 ? null : { top: before.top, bg: before.backgroundColor, content: before.content }
        };
      })
    };
  });
  /* 控件细节 */
  var sel = document.querySelector('.r85-sel');
  var sw = document.querySelector('.r85-sw');
  var seg = document.querySelector('.r85-seg > button');
  var lastSeg = document.querySelector('.r85-seg > button:last-child');
  var cb = document.querySelector('.r85-cb');
  var cbMask = document.querySelector('.r85-cb .giencoder-checkbox-mask');
  var danger = document.querySelector('.r85-btn.is-danger');
  var updBtns = document.querySelectorAll('.r85-cb ~ .r85-btn');
  var sl = document.querySelector('.r85-slider');
  var slThumb = document.querySelector('.r85-sl-thumb');
  return JSON.stringify({
    nav: { box: rel(navHost, navHost), w: Math.round(navHost.getBoundingClientRect().width), h: Math.round(navHost.getBoundingClientRect().height),
           back: rel(back, navHost), backFS: cs(back, 'fontSize'), backColor: cs(back, 'color'), groups: groups },
    page: { w: Math.round(pageHost.getBoundingClientRect().width), h: Math.round(pageHost.getBoundingClientRect().height),
            title: { box: rel(title, pageHost), fs: cs(title, 'fontSize'), fw: cs(title, 'fontWeight'), lh: cs(title, 'lineHeight') },
            padL: cs(pageHost, 'paddingLeft'),
            cards: cards },
    ctl: {
      sel: sel && { box: rel(sel, pageHost), w: Math.round(sel.getBoundingClientRect().width), h: Math.round(sel.getBoundingClientRect().height),
                    bg: cs(sel, 'backgroundColor'), bd: cs(sel, 'borderTopColor'), r: cs(sel, 'borderTopLeftRadius'), fs: cs(sel, 'fontSize') },
      sw: sw && { box: rel(sw, pageHost), bg: cs(sw, 'backgroundColor'), r: cs(sw, 'borderTopLeftRadius') },
      swOff: (function () { var s = document.querySelectorAll('.r85-sw')[1]; return s && { box: rel(s, pageHost), bg: cs(s, 'backgroundColor'), checked: s.classList.contains('giencoder-switch-checked') }; })(),
      swHandle: (function () { var h = document.querySelector('.r85-sw .giencoder-switch-handle'); return h && rel(h, h.parentNode); })(),
      seg: seg && { box: rel(seg, pageHost), w: Math.round(seg.getBoundingClientRect().width), h: Math.round(seg.getBoundingClientRect().height),
                    r: cs(seg, 'borderTopLeftRadius'), bd: cs(seg, 'borderTopStyle'), pressed: seg.getAttribute('aria-pressed'), fs: cs(seg, 'fontSize') },
      segLast: lastSeg && rel(lastSeg, pageHost),
      cb: cb && { box: rel(cb, pageHost), cls: cb.className, fs: cs(cb.children[2], 'fontSize') },
      cbMask: cbMask && { box: rel(cbMask, pageHost), bg: cs(cbMask, 'backgroundColor'), bd: cs(cbMask, 'borderTopColor') },
      danger: danger && { box: rel(danger, pageHost), color: cs(danger, 'color'), w: Math.round(danger.getBoundingClientRect().width), h: Math.round(danger.getBoundingClientRect().height) },
      updBtns: [].map.call(updBtns, function (b) { return [b.textContent, Math.round(b.getBoundingClientRect().width), Math.round(b.getBoundingClientRect().height)]; }),
      slider: sl && { box: rel(sl, pageHost), thumb: slThumb && rel(slThumb, sl), trackBg: cs(document.querySelector('.r85-sl-track'), 'backgroundColor') },
      sliderLabels: [].map.call(document.querySelectorAll('.r85-sl-lbls > span'), function (s) { return rel(s, s.parentNode); })
    }
  });
})())
