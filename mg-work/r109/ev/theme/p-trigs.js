/* r109 · 枚举页面上「所有可展开下拉/浮层」的触发器（不只是第一个）。
   候选：aria-haspopup / role=combobox / 类名含 trigger|dropdown|select-view|sel-|more|add */
(function () {
  function R(e) { var r = e.getBoundingClientRect(); return r; }

  window.__alltrig = function () {
    var out = [], seen = {};
    var sels = [
      '[aria-haspopup]', '[role="combobox"]', '[role="button"][aria-expanded]',
      '.giencoder-select-view', '[class*="trigger"]', '[class*="dropdown"]',
      '[class*="Trigger"]', '[class*="Dropdown"]', '[class*="r85-ctl"]'
    ];
    for (var s = 0; s < sels.length; s++) {
      var all;
      try { all = document.querySelectorAll(sels[s]); } catch (e) { continue; }
      for (var i = 0; i < all.length; i++) {
        var e = all[i], r = R(e), st = getComputedStyle(e);
        if (r.width < 24 || r.width > 420 || r.height < 14 || r.height > 64) continue;
        if (st.visibility === 'hidden' || st.display === 'none' || st.opacity === '0') continue;
        if (r.top < 0 || r.top > 880 || r.left < 0 || r.left > 1430) continue;
        var key = Math.round(r.left) + ':' + Math.round(r.top);
        if (seen[key]) continue;
        seen[key] = 1;
        out.push({
          sel: sels[s],
          x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
          w: Math.round(r.width), h: Math.round(r.height),
          cls: (e.getAttribute('class') || '').slice(0, 46),
          tag: e.tagName,
          t: (e.innerText || e.getAttribute('aria-label') || '').replace(/\s+/g, ' ').slice(0, 20)
        });
      }
    }
    return JSON.stringify(out);
  };

  /* 点开后：列出当前所有「可见浮层面板」的底色/描边/模糊，用于横向比对 */
  window.__panels = function () {
    var out = [], all = document.querySelectorAll('*'), i, e, st, r;
    for (i = 0; i < all.length; i++) {
      e = all[i];
      var c = e.getAttribute('class') || '';
      var role = e.getAttribute('role') || '';
      if (!(role === 'menu' || role === 'listbox' || /popup|dropdown|menu|pop/.test(c))) continue;
      st = getComputedStyle(e); r = e.getBoundingClientRect();
      if (st.visibility === 'hidden' || st.display === 'none' || st.opacity === '0') continue;
      if (r.width < 60 || r.height < 30) continue;
      out.push({
        tag: e.tagName, role: role, cls: c.slice(0, 46),
        bg: st.backgroundColor, bc: st.borderTopColor, bw: st.borderTopWidth,
        bf: st.backdropFilter || st.webkitBackdropFilter,
        w: Math.round(r.width), h: Math.round(r.height),
        x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
        t: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 24)
      });
    }
    return JSON.stringify(out);
  };
})();
