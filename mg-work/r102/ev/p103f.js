(function(){
  window.__rec = {};
  window.__run = function(idx, key, mode){
    var fs = document.querySelectorAll('.r93-fold');
    var f = fs[idx]; if(!f) return 'no fold '+idx;
    var h = f.querySelector(':scope > .r93-fh');
    var hd = (mode==='expand') ? f.querySelector(':scope > .r93-fc') : h;
    if(!hd) return 'no header';
    hd.scrollIntoView({block:'center'});
    var fb = f.querySelector(':scope > .r93-fb');
    var rec = []; var t0 = performance.now();
    function tick(){
      var t = performance.now()-t0; var c = getComputedStyle(fb);
      var an = document.getAnimations().filter(function(a){ return a.effect && a.effect.target===fb; });
      rec.push([Math.round(t), Math.round(fb.getBoundingClientRect().height), c.maxHeight, c.opacity,
                c.transform, (c.overflow||'').slice(0,7), an.length,
                an.map(function(a){return (a.animationName||a.transitionProperty)+'@'+Math.round(a.currentTime||0);}).join(',')]);
      if(t<640) requestAnimationFrame(tick); else window.__rec[key]=rec;
    }
    requestAnimationFrame(tick);
    setTimeout(function(){ hd.click(); }, 40);
    return 'started '+key+' open='+f.getAttribute('data-open');
  };
  return JSON.stringify({folds: document.querySelectorAll('.r93-fold').length, ready:true});
})()
