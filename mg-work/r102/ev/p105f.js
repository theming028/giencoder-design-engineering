(function () {
  function R(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function info(el) {
    if (!el) return null;
    var cs = getComputedStyle(el);
    return { cls: (el.className || '').toString().slice(0, 60), rect: R(el), disp: cs.display, bg: cs.backgroundColor, bd: cs.borderColor, fs: cs.fontSize };
  }
  var out = {};
  out.win = [innerWidth, innerHeight];
  out.full = document.documentElement.getAttribute('data-r93-full');
  out.baractsWrap = info(document.querySelector('.r93-baracts'));
  var bs = document.querySelectorAll('.r93-baract');
  out.nBaract = bs.length;
  out.btnFs = info(bs[0]);
  out.btnBr = info(bs[1]);
  var b0 = bs[0];
  if (b0) {
    out.fsLabels = [b0.getAttribute('aria-label'), b0.getAttribute('title'), b0.getAttribute('aria-pressed')];
    out.icoMax = info(b0.querySelector('.r93-ico-max'));
    out.icoMin = info(b0.querySelector('.r93-ico-min'));
    out.svgBox = R(b0.querySelector('.r93-ico-max svg'));
  }
  out.morebtn = document.querySelectorAll('.r93-morebtn').length;
  out.seg = info(document.querySelector('.r93-seg'));
  var sl = document.querySelector('.r93-seg .giencoder-radio-button-slider');
  out.slider = info(sl);
  if (sl) { out.sliderTX = getComputedStyle(sl).transform; out.sliderTr = getComputedStyle(sl).transitionProperty + ' / ' + getComputedStyle(sl).transitionDuration; }
  out.segInit = document.querySelector('.r93-seg').getAttribute('data-r93-seg-init');
  out.aside = info(document.querySelector('aside'));
  out.main = info(document.querySelector('main'));
  out.host = info(document.querySelector('.r93-conv-host'));
  out.slot = info(document.getElementById('av-browse-slot'));
  out.slotPlaced = document.getElementById('av-browse-slot') ? document.getElementById('av-browse-slot').className : null;
  out.split = info(document.getElementById('av-browse-split'));
  out.pane = info(document.querySelector('.td-browse'));
  out.rowOn = !!document.querySelector('.av-browse-on');
  out.rowChildren = [].map.call(document.querySelector('div:has(> main)').children, function (c) { return c.tagName + '.' + (c.className || '').toString().split(' ')[0] + ' ' + JSON.stringify(R(c)); });
  return JSON.stringify(out);
})()
