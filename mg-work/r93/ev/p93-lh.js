JSON.stringify((function(){
  function R(el){var r=el.getBoundingClientRect();return [+r.x.toFixed(1),+r.y.toFixed(1),+r.width.toFixed(1),+r.height.toFixed(1)];}
  var OVER=['text-xs','text-sm','text-lg','text-2xl'];
  function clip(s,n){s=String(s||'');return s.length>n?s.slice(0,n)+'…':s;}
  function scan(root,label){
    var out=[];
    if(!root) return out;
    var all=root.querySelectorAll('*');
    for(var i=0;i<all.length;i++){
      var el=all[i], cls=el.className;
      if(typeof cls!=='string') continue;
      if(cls.indexOf('leading-')<0) continue;
      var hit=null;
      for(var k=0;k<OVER.length;k++){ if((' '+cls+' ').indexOf(' '+OVER[k]+' ')>-1){hit=OVER[k];break;} }
      if(!hit) continue;
      var c=getComputedStyle(el);
      out.push({where:label,tag:el.tagName.toLowerCase(),cls:clip(cls,90),also:hit,
                fs:c.fontSize,lh:c.lineHeight,rect:R(el),txt:clip(el.textContent,18)});
    }
    return out;
  }
  // 只带 leading-* 的全部元素（含无 text class 的），用于看 aside 全貌
  function scanLeading(root,label){
    var out=[];
    if(!root) return out;
    var all=root.querySelectorAll('[class*="leading-"]');
    for(var i=0;i<all.length;i++){
      var el=all[i], c=getComputedStyle(el);
      out.push({where:label,cls:clip(el.className,90),fs:c.fontSize,lh:c.lineHeight,h:+el.getBoundingClientRect().height.toFixed(1),txt:clip(el.textContent,18)});
    }
    return out;
  }
  var aside=document.querySelector('aside');
  var main=document.querySelector('main');
  // 分组标题行（r85 / 工作台 aside）
  var gts=[];
  [].slice.call(document.querySelectorAll('aside [class*="hover:bg-[#E9ECEE]"]')).forEach(function(el){
    var c=getComputedStyle(el);
    gts.push({cls:clip(el.className,90),h:+el.getBoundingClientRect().height.toFixed(1),
              lh:c.lineHeight,fs:c.fontSize,rect:R(el),txt:clip(el.textContent,20)});
  });
  return {conflict:scan(aside,'aside').concat(scan(main,'main')),
          leadingAside:scanLeading(aside,'aside'),
          leadGt:gts,
          ratio:getComputedStyle(document.documentElement).getPropertyValue('--ui-fs-ratio'),
          rootFs:getComputedStyle(document.documentElement).fontSize};
})())
