(() => {
  const s = document.querySelector(".r93-tobottom");
  if (!s) return JSON.stringify({err:"no"});
  const cs = getComputedStyle(s);
  const r = s.getBoundingClientRect();
  return JSON.stringify({color: cs.color, bg: cs.backgroundColor, border: cs.borderTopColor, bw: cs.borderTopWidth, cursor: cs.cursor, w: Math.round(r.width), h: Math.round(r.height)});
})();
