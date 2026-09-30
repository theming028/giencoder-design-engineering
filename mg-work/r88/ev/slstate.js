(function(){
  var sl=document.querySelector('.r85-slider');
  return JSON.stringify({
    v:sl.getAttribute('aria-valuenow'), t:sl.getAttribute('aria-valuetext'),
    uiFs:getComputedStyle(document.documentElement).getPropertyValue('--ui-fs'),
    ls:(function(){try{return localStorage.getItem('gi-ui-fs')}catch(e){return 'ERR'}})(),
    thumbX:+(sl.querySelector('.r85-sl-thumb').getBoundingClientRect().x).toFixed(1),
    drag:sl.classList.contains('is-drag'),
    bodyFs:getComputedStyle(document.body).fontSize
  });
})()
