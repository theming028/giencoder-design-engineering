(function(){
  var navi=[].slice.call(document.querySelectorAll('.r85-navi'));
  var host=document.querySelector('.r85-page-host');
  return JSON.stringify({
    url: location.href,
    navi: navi.map(function(b){return b.getAttribute('data-set-tab')+':'+b.getAttribute('aria-current');}),
    pageHost: !!host,
    pageHostHTML: host? host.innerHTML.length : 0,
    pageAttr: host && host.firstElementChild ? host.firstElementChild.getAttribute('data-set-page') : null,
    cls: host && host.firstElementChild ? host.firstElementChild.className : null,
    hasArch: !!document.querySelector('.r88-arch'),
    navHoverRule: /\.r85-navi:hover\{[^}]*\}/.exec((document.getElementById('r88-set-css')||{}).textContent||'')
  });
})()
