(()=>{const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]};
 return {avatar:r(document.querySelector('.av-main-avatar')), face:r(document.querySelector('.av-main-avatar-face')),
         btn:r(document.querySelector('[data-av-chat-toggle]')),
         row:r(document.querySelector('[data-av-chat-toggle]').parentElement)};})()
