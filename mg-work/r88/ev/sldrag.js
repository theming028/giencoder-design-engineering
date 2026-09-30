(function(){
  var sl=document.querySelector('.r85-slider');
  var r=sl.getBoundingClientRect();
  var L=r.left, Y=r.top+r.height/2;
  var st=function(){return sl.getAttribute('aria-valuenow')+'/'+sl.getAttribute('aria-valuetext')
    +' ui-fs='+getComputedStyle(document.documentElement).getPropertyValue('--ui-fs')
    +' ls='+localStorage.getItem('gi-ui-fs')+' drag='+sl.classList.contains('is-drag');};
  var log=[], toasts=[];
  var mo=new MutationObserver(function(){ if(document.querySelector('.r85-toast')) toasts.push(document.querySelector('.r85-toast').textContent); });
  mo.observe(document.body,{childList:true,subtree:true,characterData:true});
  function pe(t,x){ return new PointerEvent(t,{bubbles:true,cancelable:true,clientX:x,clientY:Y,pointerId:7,pointerType:'mouse',button:0,buttons:1,isPrimary:true}); }
  log.push('T0 初始: '+st());
  // 1) 真·拖拽：从左端按下 → 逐段拖到右端 → 松手
  sl.dispatchEvent(pe('pointerdown', L+6));
  log.push('T1 按下左端(容器内 x=6): '+st());
  [60,120,180,240].forEach(function(dx){ window.dispatchEvent(pe('pointermove', L+dx)); });
  log.push('T2 拖到 x=240: '+st());
  window.dispatchEvent(pe('pointermove', L+400));   // 越界
  log.push('T3 拖出容器外 400: '+st());
  window.dispatchEvent(pe('pointerup', L+400));
  log.push('T4 松手: '+st());
  window.dispatchEvent(pe('pointermove', L+6));      // 松手后划过 → 不应再拖
  log.push('T5 松手后划过 x=6(应不变): '+st());
  // 2) 点击跳档（单点，不拖）
  sl.dispatchEvent(pe('pointerdown', L+102)); window.dispatchEvent(pe('pointerup', L+102));
  log.push('T6 点中 x=102(第3档): '+st());
  // 3) 键盘
  sl.focus();
  sl.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true,cancelable:true}));
  log.push('T7 ArrowLeft: '+st());
  sl.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true,cancelable:true}));
  log.push('T8 Home: '+st());
  sl.dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true,cancelable:true}));
  log.push('T9 End: '+st());
  sl.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,cancelable:true}));
  log.push('T10 已在末档再 ArrowRight(应不变): '+st());
  mo.disconnect();
  return JSON.stringify({log:log, toastCount:toasts.length, toasts:toasts.slice(0,12)});
})()
