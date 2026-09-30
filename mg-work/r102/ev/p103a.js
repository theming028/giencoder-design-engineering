(function(){
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  function cs(el,p){ return getComputedStyle(el)[p]; }
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  var out = {};

  /* 1) .r93-agents 行 */
  var ag = document.querySelector('.r93-agents');
  out.agents = ag ? {
    n: ag.children.length,
    rect: R(ag),
    display: cs(ag,'display'),
    gap: cs(ag,'gap'),
    margin: cs(ag,'marginTop')+'/'+cs(ag,'marginBottom'),
    parentCls: cls(ag.parentElement),
    parentRect: R(ag.parentElement),
    kids: [].map.call(ag.children, function(k){ return {t:k.tagName, c:cls(k), r:R(k)}; }),
    nextSib: ag.nextElementSibling ? {t:ag.nextElementSibling.tagName, c:cls(ag.nextElementSibling)} : null
  } : null;

  /* 2) 底部列结构：.r93-bottom 的子孙树（前 3 层） */
  var bot = document.querySelector('.r93-bottom');
  function tree(el, d, max){
    if(!el || d>max) return null;
    return { t:el.tagName, c:cls(el), r:R(el), ov:cs(el,'overflow'), sh:cs(el,'boxShadow').slice(0,60), kids: [].map.call(el.children, function(k){ return tree(k,d+1,max); }) };
  }
  out.bottom = bot ? tree(bot,0,3) : null;

  /* 3) 折叠块清点 */
  var folds = document.querySelectorAll('.r93-fold');
  out.folds = { n: folds.length, list: [] };
  [].forEach.call(folds, function(f,i){
    var h = f.querySelector(':scope > .r93-fh'), c = f.querySelector(':scope > .r93-fc'), b = f.querySelector(':scope > .r93-fb');
    out.folds.list.push({
      i:i,
      open: f.getAttribute('data-open'),
      fh: h ? cls(h)+'|bt='+h.classList.contains('r93-bt') : null,
      fc: c ? cls(c)+'|bt='+c.classList.contains('r93-bt') : null,
      hasFb: !!b,
      fbCls: b?cls(b):null,
      fbH: b?Math.round(b.getBoundingClientRect().height):null,
      fbh: b?b.style.getPropertyValue('--r93-fbh'):null,
      parentItem: cls(f.parentElement).slice(0,80),
      title: (h?(h.textContent||'').slice(0,24):(c?(c.textContent||'').slice(0,24):''))
    });
  });

  /* 4) 折叠头种类（找到所有 .r93-bt 里带 r93-fh / r93-fc 的） */
  out.bt = { fh: document.querySelectorAll('.r93-fh.r93-bt').length,
             fc: document.querySelectorAll('.r93-fc.r93-bt').length,
             fhAll: document.querySelectorAll('.r93-fh').length,
             fcAll: document.querySelectorAll('.r93-fc').length,
             btAll: document.querySelectorAll('.r93-bt').length };

  /* 5) 字号：.r93-t14 直方图 + 关键变体 */
  var t14 = document.querySelectorAll('.r93-t14'), hist = {}, inCard = {}, outCard = {};
  [].forEach.call(t14, function(e){
    var fs = cs(e,'fontSize');
    hist[fs] = (hist[fs]||0)+1;
    var ic = !!e.closest('.r93-card');
    (ic?inCard:outCard)[fs] = ((ic?inCard:outCard)[fs]||0)+1;
  });
  out.t14 = { total: t14.length, hist: hist, inCard: inCard, outCard: outCard };
  var ell = document.querySelectorAll('.r93-t14.r93-ell');
  out.t14ell = { n: ell.length, sizes: [].map.call(ell, function(e){ return cs(e,'fontSize'); }) };
  var c1 = document.querySelectorAll('.r93-t14.r93-c1');
  out.t14c1 = { n: c1.length, sizes: [].map.call(c1, function(e){ return cs(e,'fontSize'); }),
                inCard: [].map.call(c1, function(e){ return !!e.closest('.r93-card'); }) };

  /* 6) 药丸底色 */
  var tb = document.querySelector('.r93-tobottom');
  out.tobottom = tb ? { bg: cs(tb,'backgroundColor'), bf: cs(tb,'backdropFilter')||cs(tb,'webkitBackdropFilter'), rect: R(tb) } : null;

  /* 7) 标题栏底色（对比，确认共享变量） */
  var bar = document.querySelector('.r93-bar');
  out.bar = bar ? { bg: cs(bar,'backgroundColor') } : null;

  return JSON.stringify(out, null, 1);
})()
