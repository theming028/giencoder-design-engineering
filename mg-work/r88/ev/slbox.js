(function(){
  var sl=document.querySelector('.r85-slider');
  if(!sl) return JSON.stringify({err:'no slider'});
  var r=sl.getBoundingClientRect();
  var tr=sl.querySelector('.r85-sl-track').getBoundingClientRect();
  var th=sl.querySelector('.r85-sl-thumb').getBoundingClientRect();
  return JSON.stringify({
    sl:{x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)},
    track:{x:+tr.x.toFixed(1),y:+tr.y.toFixed(1),w:+tr.width.toFixed(1),h:+tr.height.toFixed(1)},
    thumb:{x:+th.x.toFixed(1),w:+th.width.toFixed(1)},
    uiFs:getComputedStyle(document.documentElement).getPropertyValue('--ui-fs'),
    ls:(function(){try{return localStorage.getItem('gi-ui-fs')}catch(e){return 'ERR'}})(),
    val:sl.getAttribute('aria-valuenow'), valTxt:sl.getAttribute('aria-valuetext'),
    tabindex:sl.getAttribute('tabindex'), role:sl.getAttribute('role')
  });
})()
