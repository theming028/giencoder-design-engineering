JSON.stringify((function(){
  function R(el){var r=el.getBoundingClientRect();return [+r.x.toFixed(1),+r.y.toFixed(1),+r.width.toFixed(1),+r.height.toFixed(1)];}
  var h=document.querySelector('header[class*="h-12"]');
  var cs=h?getComputedStyle(h):null;
  var back=document.querySelector('.r85-back');
  var svg=document.querySelector('.r85-back > svg');
  var span=document.querySelector('.r85-back > span');
  var gts=[].slice.call(document.querySelectorAll('.r85-gt'));
  var navis=[].slice.call(document.querySelectorAll('.r85-navi'));
  var out={
    hdr:h?{cls:h.className,bgi:cs.backgroundImage,rep:cs.backgroundRepeat,pos:cs.backgroundPosition,size:cs.backgroundSize,bg:cs.backgroundColor,rect:R(h)}:null,
    back:back?{color:getComputedStyle(back).color,rect:R(back)}:null,
    backSvg:svg?{color:getComputedStyle(svg).color,rect:R(svg),w:svg.getBoundingClientRect().width}:null,
    backSpan:span?{color:getComputedStyle(span).color,rect:R(span)}:null,
    theme:document.body.getAttribute('giencoder-theme'),
    gts:[],navi:[]
  };
  gts.forEach(function(g){var c=getComputedStyle(g);out.gts.push({t:g.textContent,ml:c.marginLeft,mr:c.marginRight,rect:R(g)});});
  navis.slice(0,3).forEach(function(n){
    var s=n.querySelector('span');
    out.navi.push({t:n.textContent,rect:R(n),spanX:s?R(s)[0]:null,pad:getComputedStyle(n).paddingLeft});
  });
  return out;
})())
