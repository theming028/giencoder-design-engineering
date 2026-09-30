(function(){
  window.__rec = [];
  var doc=document.documentElement;
  function s(e){ if(!e) return null; var c=getComputedStyle(e); return {h:e.hidden,o:+c.opacity,t:c.transform,d:c.display}; }
  function tick(){
    var chat=document.querySelector('.r93-conv-host > [data-r93-pane="chat"]');
    var trace=document.querySelector('.r93-conv-host > .r93-trace');
    var box=document.querySelector('main > div > div.flex-1.justify-center > div.mt-8');
    var hero=document.querySelector('main > div > div.flex-1.justify-center');
    window.__rec.push({t:Math.round(performance.now()),app:doc.getAttribute('data-r93-app'),tab:doc.getAttribute('data-r93-tab'),
      chat:s(chat),trace:s(trace),box:box?s(box):null,heroD:hero?getComputedStyle(hero).display:null,
      hostH:document.querySelector('.r93-conv-host')?Math.round(document.querySelector('.r93-conv-host').getBoundingClientRect().height):null});
    if(window.__rec.length<100) requestAnimationFrame(tick);
  }
  tick();
  return 'armed';
})()
