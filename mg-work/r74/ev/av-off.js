(()=>{const b=document.querySelector('[data-av-chat-toggle]');
 b.click();
 return new Promise(r=>setTimeout(()=>{const svg=b.querySelector('svg');
   r({open:document.documentElement.hasAttribute('data-av-chat-open'),
      state:b.getAttribute('data-r74-state'),label:b.textContent.trim(),
      paths:[...svg.querySelectorAll('path')].map(p=>p.getAttribute('d')),
      anims:svg.getAnimations().length});},150));})()
