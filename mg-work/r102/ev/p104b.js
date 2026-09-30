(function(){
  function cls(el){ return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||''; }
  function R(el){ var r=el.getBoundingClientRect(); return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)}; }
  var out={};
  var hero=document.querySelector('main > div > div.flex-1.justify-center');
  var box=hero?hero.querySelector('div.mt-8'):null;
  out.box=box?R(box):null;
  out.btns=[];
  if(box){ [].forEach.call(box.querySelectorAll('button,[role="button"],div[tabindex]'),function(b){
      var r=b.getBoundingClientRect();
      out.btns.push({tag:b.tagName.toLowerCase(),cls:cls(b).toString().slice(0,90),
        txt:(b.textContent||'').trim().slice(0,20),title:b.getAttribute('title')||'',
        rect:R(b)});
  }); }
  return JSON.stringify(out,null,1);
})()
