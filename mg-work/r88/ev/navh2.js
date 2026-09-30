(function(){
  var items=[].slice.call(document.querySelectorAll('.r85-navi'));
  return JSON.stringify(items.map(function(b){
    return b.getAttribute('data-set-tab')+' cur='+b.getAttribute('aria-current')+' bg='+getComputedStyle(b).backgroundColor;
  }));
})()
