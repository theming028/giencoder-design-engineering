JSON.stringify((function(){
  var out=[]; var list=document.querySelectorAll('.ws-dropdown-hover');
  for(var i=0;i<list.length;i++){
    var el=list[i], p=el.parentElement;
    var txt=el.querySelector('.giencoder-select-view-text');
    out.push({
      i:i,
      text:txt?txt.textContent:null,
      elStyle:el.getAttribute('style'),
      parentCls:p?p.className:null,
      parentStyle:p?p.getAttribute('style'):null,
      exp:el.getAttribute('aria-expanded'),
      icoCls:(el.querySelector('svg')||{}).getAttribute?el.querySelector('svg').getAttribute('class'):null
    });
  }
  return {n:list.length, list:out};
})())
