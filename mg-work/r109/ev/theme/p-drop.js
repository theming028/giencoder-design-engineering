/* r109 第七拍 · 下拉菜单「暗色统一」实测探针（真鼠标 hover）
 *
 * 验证链条（静态已证的部分不重复测）：
 *   静态：基准「默认权限」下拉的行 hover  = `.perm-menu-item:hover { background-color: var(--color-fill-2) !important }`
 *   实测：① 暗色档下 `--color-fill-2` 的计算值（= 镜像后的深灰）
 *         ② 其他下拉的菜单项 **真鼠标 hover** 后的实际底色
 *   判据：② == ①（且 ≠ 浅色档值）⇒ 全站下拉已统一到基准。
 *
 * ★ 铁律：hover 必须用真鼠标（合成事件绕过 :hover）；eval 输出是 JSON 套 JSON，别裁 tail。
 */
(function () {
  function gv(k) { return getComputedStyle(document.documentElement).getPropertyValue(k).trim(); }

  /* ① 两档变量真值 */
  window.__vars = function () {
    var ks = ['--gray-1', '--gray-2', '--gray-3', '--gray-4', '--gray-9', '--gray-10',
              '--color-fill-1', '--color-fill-2', '--color-fill-3', '--color-fill-4',
              '--color-border-1', '--color-border-2', '--color-bg-1', '--color-bg-2', '--color-text-1'];
    var o = {};
    ks.forEach(function (k) { o[k] = gv(k); });
    o.__theme = document.documentElement.getAttribute('giencoder-theme') || '(无)';
    o.__dark = document.documentElement.getAttribute('data-gi-dark') || '(无)';
    o.__bodyBg = getComputedStyle(document.body).backgroundColor;
    return JSON.stringify(o);
  };

  /* ② 找可见的候选菜单项（默认找带 fill-2 hover 类的） */
  window.__find = function (needle, maxW, maxH) {
    maxW = maxW || 460; maxH = maxH || 60;
    var out = [], all = document.querySelectorAll('*');
    for (var i = 0; i < all.length; i++) {
      var e = all[i], c = e.getAttribute('class') || '';
      if (needle && c.indexOf(needle) < 0) continue;
      var r = e.getBoundingClientRect();
      if (r.width < 40 || r.width > maxW || r.height < 12 || r.height > maxH) continue;
      var st = getComputedStyle(e);
      if (st.visibility === 'hidden' || st.display === 'none' || st.opacity === '0') continue;
      out.push({
        x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
        w: Math.round(r.width), h: Math.round(r.height),
        bg: st.backgroundColor,
        t: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 28),
        c: c.slice(0, 80)
      });
      if (out.length >= 14) break;
    }
    return JSON.stringify(out);
  };

  /* ③ 读某坐标处的分层计算样式（hover 态下用） */
  window.__peek = function (x, y) {
    var e = document.elementFromPoint(x, y);
    if (!e) return JSON.stringify({ found: false });
    var chain = [], i = 0;
    while (e && i < 4) {
      var st = getComputedStyle(e), r = e.getBoundingClientRect();
      chain.push({
        tag: e.tagName, cls: (e.getAttribute('class') || '').slice(0, 74),
        bg: st.backgroundColor, color: st.color, radius: st.borderRadius,
        bf: (st.backdropFilter || st.webkitBackdropFilter || '').slice(0, 40),
        bw: st.borderTopWidth, bc: st.borderColor,
        w: Math.round(r.width), h: Math.round(r.height)
      });
      e = e.parentElement; i++;
    }
    return JSON.stringify(chain);
  };

  /* ④ 读某个选择器的容器级样式（浮层容器） */
  window.__sel = function (sel) {
    var e = document.querySelector(sel);
    if (!e) return JSON.stringify({ found: false, sel: sel });
    var st = getComputedStyle(e), r = e.getBoundingClientRect();
    return JSON.stringify({
      found: true, sel: sel, bg: st.backgroundColor, radius: st.borderRadius,
      bf: (st.backdropFilter || '').slice(0, 40), bc: st.borderColor, bw: st.borderTopWidth,
      sh: st.boxShadow.slice(0, 90), w: Math.round(r.width), h: Math.round(r.height)
    });
  };

  window.__setDark = function () {
    try { window.__giTheme.set('dark'); } catch (e) { return 'ERR ' + e.message; }
    return 'ok';
  };
  window.__setLight = function () {
    try { window.__giTheme.set('light'); } catch (e) { return 'ERR ' + e.message; }
    return 'ok';
  };
  return 'ready';
})();
