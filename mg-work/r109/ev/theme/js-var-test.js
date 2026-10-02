(function(){
  var d=document.createElement('div');
  d.innerHTML='<svg width="0" height="0">'
   +'<path id="t1" d="M0 0h10v10z" fill="var(--color-danger)"/>'
   +'<path id="t2" d="M0 0h10v10z" style="fill:var(--color-danger)"/>'
   +'<path id="t3" d="M0 0h10v10z" fill="#F53F3F"/>'
   +'</svg>';
  document.body.appendChild(d);
  var r={};
  ['t1','t2','t3'].forEach(function(id){
    var e=document.getElementById(id);
    r[id]={computed:getComputedStyle(e).fill, attr:e.getAttribute('fill')};
  });
  d.remove();
  return JSON.stringify(r);
})()
