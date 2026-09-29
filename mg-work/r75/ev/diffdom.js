(() => {
  const cnt = () => document.querySelectorAll('*').length;
  const fixed = () => Array.from(document.querySelectorAll('body > div, body > *')).filter(e => /fixed|absolute/.test(getComputedStyle(e).position)).length;
  const before = { n: cnt(), f: fixed(), bodyKids: document.body.children.length };
  const t = document.querySelector(window.__T);
  if (!t) return 'NO-TRIGGER';
  const fire = (el, type, Ctor) => el.dispatchEvent(new Ctor(type, { bubbles: true, cancelable: true, clientX: 140, clientY: 24, button: 0, buttons: type === 'mousedown' ? 1 : 0 }));
  fire(t, 'pointerdown', PointerEvent); fire(t, 'mousedown', MouseEvent); fire(t, 'pointerup', PointerEvent);
  fire(t, 'mouseup', MouseEvent); fire(t, 'click', MouseEvent);
  return new Promise(res => setTimeout(() => {
    const after = { n: cnt(), f: fixed(), bodyKids: document.body.children.length };
    window.__D = { before, after, newBodyKids: Array.from(document.body.children).map(e => e.tagName + '.' + String(e.className).slice(0, 50) + ' pos=' + getComputedStyle(e).position + ' z=' + getComputedStyle(e).zIndex) };
    res(JSON.stringify(window.__D));
  }, 400));
})()
