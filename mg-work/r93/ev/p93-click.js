JSON.stringify((function(){
  function clip(s,n){s=String(s||'').replace(/\s+/g,' ').trim();return s.length>n?s.slice(0,n)+'…':s;}
  var aside=document.querySelector('aside');
  var main=document.querySelector('main');
  var before={mainLen:main?main.innerHTML.length:0,mainTxt:clip(main&&main.textContent,200)};
  // 找 aside 里的会话项按钮（Kn 里那个 flex-1 的 button）
  var cands=[].slice.call(document.querySelectorAll('aside div.group button.flex-1'));
  var clicked=null;
  if(cands.length){
    var b=cands[0];
    clicked=clip(b.textContent,40);
    b.click();
  }
  return {clicked:clicked, nSessionBtns:cands.length, before:before};
})())
