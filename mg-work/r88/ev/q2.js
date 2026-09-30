(function(){
  var log=[];
  window.addEventListener('error', function(e){ log.push('ERR '+(e.message||'')+' @'+(e.filename||'')+':'+(e.lineno||'')); });
  window.addEventListener('unhandledrejection', function(e){ log.push('REJ '+e.reason); });
  var t=[].find.call(document.querySelectorAll('.r85-navi'), function(b){return b.getAttribute('data-set-tab')==='archived';});
  try { t.click(); } catch (e) { log.push('THROW '+e.message+'\n'+e.stack); }
  return JSON.stringify({
    log: log,
    host: (document.querySelector('.r85-page-host')||{}).innerHTML ? 'has' : 'empty',
    hasArch: !!document.querySelector('.r88-arch'),
    cssBlock: !!document.getElementById('r88-set-css'),
    jsBlock: !!document.getElementById('r88-set-js'),
    iconKeys: (function(){ try { return Object.keys(ICON).length; } catch(e){ return 'ICON not global'; } })()
  });
})()
