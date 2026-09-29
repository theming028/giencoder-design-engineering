/* r85 探针 v2：基准 = .r85-page（即设计稿 1389:18725 的内容坐标原点） */
JSON.stringify((function () {
  function rel(el, base) {
    if (!el) return null;
    var r = el.getBoundingClientRect(), b = base.getBoundingClientRect();
    return [Math.round(r.left - b.left), Math.round(r.top - b.top), Math.round(r.width), Math.round(r.height)];
  }
  function cs(el, p) { return el ? getComputedStyle(el)[p] : null; }
  function box(el) { return el ? [Math.round(el.getBoundingClientRect().width), Math.round(el.getBoundingClientRect().height)] : null; }
  var page = document.querySelector('.r85-page-host .r85-page') || document.querySelector('.r85-page');
  var out = { page: box(page) };

  var t = document.querySelector('.r85-title');
  out.title = { box: rel(t, page), fs: cs(t, 'fontSize'), fw: cs(t, 'fontWeight'), lh: cs(t, 'lineHeight') };

  out.cards = [].map.call(page.querySelectorAll('.r85-card'), function (c) {
    var st = getComputedStyle(c);
    return {
      box: rel(c, page), bg: cs(c, 'backgroundColor'),
      outline: st.outlineStyle + ' ' + st.outlineWidth + ' ' + st.outlineOffset,
      borderW: cs(c, 'borderTopWidth'),
      rows: [].map.call(c.querySelectorAll('.r85-row'), function (r) {
        var tt = r.querySelector('.r85-t'), dd = r.querySelector('.r85-d'), ctl = r.querySelector('.r85-ctl');
        return {
          t: tt.textContent,
          box: rel(r, page),
          ic: rel(r.querySelector('.r85-ic'), page),
          tx: rel(r.querySelector('.r85-tx'), page),
          tBox: rel(tt, page), tFs: cs(tt, 'fontSize'),
          dBox: rel(dd, page), dColor: cs(dd, 'color'),
          ctl: rel(ctl, page),
          kids: [].map.call(ctl ? ctl.children : [], function (k) {
            return {
              c: (k.className || '').split(' ')[0] || k.tagName.toLowerCase(),
              box: rel(k, page), wh: box(k),
              bw: cs(k, 'borderTopWidth'), bd: cs(k, 'borderTopStyle'), bg: cs(k, 'backgroundColor')
            };
          })
        };
      })
    };
  });

  var sl = document.querySelector('.r85-slider');
  out.slider = sl && {
    box: rel(sl, page),
    track: rel(sl.querySelector('.r85-sl-track'), sl),
    done: rel(sl.querySelector('.r85-sl-done'), sl),
    thumb: rel(sl.querySelector('.r85-sl-thumb'), sl),
    ticks: [].map.call(sl.querySelectorAll('.r85-sl-tick'), function (k) { return [rel(k, sl), cs(k, 'backgroundColor')]; }),
    lbls: [].map.call(sl.querySelectorAll('.r85-sl-lbls > span'), function (s) { return [s.textContent, rel(s, sl)]; })
  };

  out.switch = [].map.call(page.querySelectorAll('.r85-sw'), function (s) {
    return { box: rel(s, page), wh: box(s), bg: cs(s, 'backgroundColor'), r: cs(s, 'borderTopLeftRadius'),
             handle: rel(s.querySelector('.giencoder-switch-handle'), s) };
  });

  var m = document.querySelector('.r85-cb .giencoder-checkbox-mask');
  out.cbMask = m && { box: rel(m, page), wh: box(m), bg: cs(m, 'backgroundColor') };

  out.segs = [].map.call(page.querySelectorAll('.r85-seg > button'), function (b) {
    return { t: b.textContent, box: rel(b, page), bd: cs(b, 'borderTopStyle'), bw: cs(b, 'borderTopWidth') };
  });

  var sv = document.querySelector('.r85-nav-host');
  if (sv) {
    out.nav = {
      wh: box(sv),
      items: [].map.call(sv.querySelectorAll('.r85-navi'), function (b) {
        return { t: b.textContent, box: rel(b, sv), bg: cs(b, 'backgroundColor'),
                 ic: rel(b.querySelector('svg'), sv), icColor: cs(b.querySelector('svg'), 'color') };
      }),
      groups: [].map.call(sv.querySelectorAll('.r85-gt'), function (g) { return [g.textContent, rel(g, sv)]; })
    };
  }
  return JSON.stringify(out);
})())
