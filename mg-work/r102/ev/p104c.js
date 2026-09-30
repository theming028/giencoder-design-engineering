(function(){
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  var hero=document.querySelector('main > div > div.flex-1.justify-center');
  var box=hero.querySelector('div.mt-8');
  var btns=box.querySelectorAll('button');
  for(var i=0;i<btns.length;i++){ btns[i].setAttribute('data-p104','b'+i+'-'+Math.round(btns[i].getBoundingClientRect().left)); }
  var views=box.querySelectorAll('.giencoder-select-view');
  for(var j=0;j<views.length;j++){ views[j].setAttribute('data-p104','s'+j+'-'+Math.round(views[j].getBoundingClientRect().left)); }
  var out=[];
  box.querySelectorAll('[data-p104]').forEach(function(e){ var r=e.getBoundingClientRect();
    out.push({k:e.getAttribute('data-p104'), txt:(e.textContent||'').trim().slice(0,16), x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width)}); });
  return JSON.stringify(out);
})()
