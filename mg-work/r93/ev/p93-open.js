(function () {
  function clip(s, n) { s = String(s || '').replace(/\s+/g, ' ').trim(); return s.length > n ? s.slice(0, n) + '…' : s; }
  var out = {};
  var aside = document.querySelector('aside');
  var b = aside && aside.querySelector('button.min-w-0.flex-1');
  out.found = !!b;
  out.txt = b ? clip(b.textContent, 30) : null;
  if (b) b.click();
  return out;
})()
