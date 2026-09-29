(()=>{
  const w=document.querySelector('.av-main-avatar'), f=document.querySelector('.av-main-avatar-face');
  const g=f?f.firstElementChild:null;
  const b=document.querySelector('[data-av-chat-toggle]');
  return {
    avatar:!!w, face:!!f, glyph:g?g.className:null,
    faceHTML:f?f.innerHTML.slice(0,80):'',
    btnLabel:b?b.textContent.trim():null,
    btnIcon:b&&b.querySelector('svg')?b.querySelector('svg').innerHTML.slice(0,70):null,
    btnState:b?b.getAttribute('data-r74-state'):null,
    ariaExp:b?b.getAttribute('aria-expanded'):null,
    htmlOpen:document.documentElement.hasAttribute('data-av-chat-open')
  };
})()
