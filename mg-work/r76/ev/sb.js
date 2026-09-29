/* r76 · 验收 1：滚动条 thumb hover 的**级联**取证
   逐张样式表、按文档顺序列出所有命中 scrollbar-thumb:hover 的规则与值，
   并给出「在纯白底上合成后的颜色」，用于对照「浅一级」。
   ⚠️ 伪元素 :hover 态无法用 getComputedStyle 直接读（Chromium 不支持复合伪类），
   故改为「级联顺序 + 声明值」取证。 */
(function () {
  const hits = [];
  let idx = 0;
  for (const sh of document.styleSheets) {
    let rules;
    try { rules = sh.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    const walk = (list, media) => {
      for (const r of list) {
        idx++;
        if (r.media) { walk(r.cssRules, r.conditionText || r.media.mediaText); continue; }
        if (r.selectorText && /scrollbar-thumb:hover/.test(r.selectorText)) {
          hits.push({
            order: idx, media: media || '(none)',
            sel: r.selectorText,
            bg: r.style.backgroundColor || r.style.background || '(未写)',
            raw: (r.cssText || '').slice(0, 160)
          });
        }
      }
    };
    walk(rules, null);
  }
  /* 默认档（用于对比） */
  const base = [];
  let j = 0;
  for (const sh of document.styleSheets) {
    let rules; try { rules = sh.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    const walk = (list) => {
      for (const r of list) {
        j++;
        if (r.media) { walk(r.cssRules); continue; }
        if (r.selectorText === '::-webkit-scrollbar-thumb') {
          base.push({ order: j, bg: r.style.backgroundColor || r.style.background || '(未写)' });
        }
      }
    };
    walk(rules);
  }
  const alpha = v => { const m = /([\d.]+)\)\s*$/.exec(v); return m ? parseFloat(m[1]) : null; };
  const composited = v => {
    const m = /rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)/.exec(v);
    if (!m) return null;
    const a = m[4] === undefined ? 1 : parseFloat(m[4]);
    const c = i => Math.round(255 - a * (255 - parseInt(m[i], 10)));
    return 'rgb(' + c(1) + ',' + c(2) + ',' + c(3) + ')';
  };
  const out = [];
  out.push('== 默认档（::-webkit-scrollbar-thumb）文档顺序命中 ==');
  base.forEach(b => out.push('  #' + b.order + '  ' + b.bg + '  → 白底合成 ' + (composited(b.bg) || '?')));
  out.push('== hover 档命中（越靠后越胜） ==');
  hits.forEach(h => out.push('  #' + h.order + ' [media ' + h.media + ']\n      ' + h.sel + '\n      ' + h.bg + '  → 白底合成 ' + (composited(h.bg) || '?') + '  α=' + alpha(h.bg)));
  out.push('== 胜出者（文档顺序最后一条） ==');
  const w = hits[hits.length - 1];
  out.push(w ? '  ' + w.sel + '  ' + w.bg + '  → ' + composited(w.bg) : '  (无)');
  return out.join('\n');
})()
