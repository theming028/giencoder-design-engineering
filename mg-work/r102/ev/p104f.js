(function(){
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  function R(el){ if(!el) return null; var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  var doc=document.documentElement;
  var hero=document.querySelector('main > div > div.flex-1.justify-center');
  var box=hero?hero.querySelector(':scope > div.mt-8'):null;
  var host=document.querySelector('.r93-conv-host');
  var out={
    app:doc.getAttribute('data-r93-app'), tab:doc.getAttribute('data-r93-tab'),
    sk:!!document.querySelector('.r93-sk'),
    hero: hero?{disp:getComputedStyle(hero).display, rect:R(hero)}:null,
    box: box?{op:getComputedStyle(box).opacity, pe:getComputedStyle(box).pointerEvents, rect:R(box)}:null,
    host: host?{z:getComputedStyle(host).zIndex, rect:R(host)}:null,
    bottom: R(document.querySelector('.r93-bottom')),
    panes:[]
  };
  [].forEach.call(document.querySelectorAll('.r93-conv-host > .r93-pane'),function(p){
    var c=getComputedStyle(p);
    out.panes.push({cls:cls(p).toString(), hidden:p.hidden, disp:c.display, op:c.opacity, tf:c.transform,
                    slide:p.getAttribute('data-r93-slide'), rect:R(p)});
  });
  var pop=document.querySelector('.giencoder-select-popup.giencoder-popup-open');
  out.pop=pop?{rect:R(pop), z:getComputedStyle(pop).zIndex}:null;
  return JSON.stringify(out,null,1);
})()
