JSON.stringify((function(){
  var hs=document.querySelectorAll('header');
  var out=[];
  for(var i=0;i<hs.length;i++){
    var el=hs[i],b=el.getBoundingClientRect(),cs=getComputedStyle(el);
    out.push({i:i,cls:el.className,bg:cs.backgroundColor,bgi:cs.backgroundImage,w:+b.width.toFixed(1),h:+b.height.toFixed(1),x:+b.x.toFixed(1),y:+b.y.toFixed(1)});
  }
  var tabs=[];
  document.querySelectorAll('[data-tab]').forEach(function(t){
    tabs.push({tab:t.getAttribute('data-tab'),sel:t.getAttribute('aria-selected')});
  });
  return {innerW:window.innerWidth,innerH:window.innerHeight,n:hs.length,hdrs:out,tabs:tabs,
          bodyTheme:document.body.getAttribute('giencoder-theme'),
          bodyAttrs:[].slice.call(document.body.attributes).map(function(a){return a.name+'='+a.value;}).join('|')};
})())
