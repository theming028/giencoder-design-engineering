/* r109 第八拍 · 「字面值 → DS 变量」验收探针（真鼠标）
 *
 * 验收链条（三段读数，一次跑完）：
 *   ① 浅色档：hover 到目标件 ⇒ 读实际底色 = **新计算值**；与**旧字面值**比 Δ
 *   ② 暗色档：同一件再 hover ⇒ 读实际底色 = 应 = DS 变量的暗色档
 *   ③ 顺带读一批 token 的计算值（确认暗色档真的翻转）
 *
 * ★ 铁律：hover 必须真鼠标；eval 输出是 JSON 套 JSON（别裁 tail）；stdout 只重定向不接管道。
 */
(function () {
  function gv(k) { return getComputedStyle(document.documentElement).getPropertyValue(k).trim(); }

  window.__vars = function () {
    var ks = ['--gray-1', '--gray-2', '--gray-3', '--gray-5', '--gray-10',
              '--giencoderblue-1', '--color-fill-1', '--color-fill-2', '--color-fill-3',
              '--color-border-1', '--color-border-2', '--color-primary-1', '--color-primary-2',
              '--color-primary-6', '--color-text-1', '--color-text-4', '--color-bg-1'];
    var o = {};
    ks.forEach(function (k) { o[k] = gv(k); });
    o.__theme = document.documentElement.getAttribute('giencoder-theme') || '(无)';
    o.__bodyBg = getComputedStyle(document.body).backgroundColor;
    return JSON.stringify(o);
  };

  function pick(all, sub, maxW, maxH) {
    var out = [];
    for (var i = 0; i < all.length; i++) {
      var e = all[i], c = e.getAttribute('class') || '';
      if (sub && c.indexOf(sub) < 0) continue;
      var r = e.getBoundingClientRect();
      if (r.width < 36 || r.width > maxW || r.height < 10 || r.height > maxH) continue;
      var st = getComputedStyle(e);
      if (st.visibility === 'hidden' || st.display === 'none' || st.opacity === '0') continue;
      out.push({
        x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
        w: Math.round(r.width), h: Math.round(r.height), bg: st.backgroundColor,
        color: st.color, bw: st.borderTopWidth, bc: st.borderColor,
        t: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 20), c: c.slice(0, 90)
      });
      if (out.length >= 12) break;
    }
    return out;
  }

  /* 按类名子串找（默认找菜单项） */
  window.__find = function (sub, maxW, maxH) {
    return JSON.stringify(pick(document.querySelectorAll('*'), sub, maxW || 460, maxH || 60));
  };

  /* 按 CSS 选择器找 */
  window.__sel = function (sel, maxW, maxH) {
    try { return JSON.stringify(pick(document.querySelectorAll(sel), '', maxW || 600, maxH || 80)); }
    catch (e) { return JSON.stringify([]); }
  };

  /* 自动找「下拉触发器」：按优先级试一串选择器，返回第一个命中 */
  window.__trig = function () {
    var tries = [
      ['r81-ws-trigger', 'cls'],
      ['ws-trigger-hover', 'cls'],
      ['giencoder-select-view', 'cls'],
      ['r85-dd-trigger', 'cls'],
      ['r93-dd-trigger', 'cls'],
      ['[aria-haspopup="listbox"]', 'attr'],
      ['[aria-haspopup="menu"]', 'attr']
    ];
    for (var i = 0; i < tries.length; i++) {
      var all = (tries[i][1] === 'attr')
        ? document.querySelectorAll(tries[i][0])
        : document.querySelectorAll('*');
      var hit = pick(all, tries[i][1] === 'attr' ? '' : tries[i][0], 320, 48);
      if (hit.length) { hit[0].via = tries[i][0]; return JSON.stringify(hit); }
    }
    return JSON.stringify([]);
  };

  /* ★★ 按坐标 + 类名子串读「谁在该点、且它此刻的计算底色是多少」。
     为什么不用 elementFromPoint（踩过）：浮层的**背景是一个铺满面板的 SVG**
     （`.absolute` + `filter: drop-shadow(…)`，w=388 h=526），它在绘制序里**压在菜单项之上**
     ⇒ elementFromPoint 返回的是那张 SVG（bg 恒为 transparent），
     于是「读到的底色永远透明」——假失败第 4/5 类（截图框错 / 选择器层级错）。
     ⇒ 改法：遍历所有候选，取**几何包含该坐标**的那个元素，直接读它的 computed style。
        真鼠标已经物理落在那一点上，`:hover` 已生效 ⇒ 读到就是 hover 态真值。 */
  window.__bgAt = function (x, y, sub) {
    var all = document.querySelectorAll('*'), seed = null, best = 1e12;
    for (var i = 0; i < all.length; i++) {
      var e = all[i], c = e.getAttribute('class') || '';
      if (sub && c.indexOf(sub) < 0) continue;
      var r = e.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) continue;
      if (x < r.left || x > r.right || y < r.top || y > r.bottom) continue;
      var st = getComputedStyle(e);
      if (st.display === 'none' || st.visibility === 'hidden') continue;
      var a = r.width * r.height;
      if (a < best) { best = a; seed = e; }
    }
    if (!seed) return JSON.stringify([]);
    var chain = [], k = 0;
    while (seed && k < 5) {
      var st2 = getComputedStyle(seed), r2 = seed.getBoundingClientRect();
      chain.push({
        tag: seed.tagName, cls: (seed.getAttribute('class') || '').slice(0, 84),
        bg: st2.backgroundColor, color: st2.color,
        bc: st2.borderTopColor, bw: st2.borderTopWidth,
        inline: (seed.getAttribute('style') || '').slice(0, 130),
        w: Math.round(r2.width), h: Math.round(r2.height),
        t: (seed.innerText || '').replace(/\s+/g, ' ').slice(0, 16)
      });
      seed = seed.parentElement; k++;
    }
    return JSON.stringify(chain);
  };

  /* 读某坐标处分层计算样式（hover 态下用；⚠ 会被浮层背景 SVG 挡住，优先用 __bgAt） */
  window.__peek = function (x, y) {
    var e = document.elementFromPoint(x, y);
    if (!e) return JSON.stringify({ found: false });
    var chain = [], i = 0;
    while (e && i < 3) {
      var st = getComputedStyle(e), r = e.getBoundingClientRect();
      chain.push({
        tag: e.tagName, cls: (e.getAttribute('class') || '').slice(0, 70),
        bg: st.backgroundColor, color: st.color, radius: st.borderRadius,
        bw: st.borderTopWidth, bc: st.borderColor,
        inline: (e.getAttribute('style') || '').slice(0, 110),
        w: Math.round(r.width), h: Math.round(r.height)
      });
      e = e.parentElement; i++;
    }
    return JSON.stringify(chain);
  };

  /* 按 CSS 选择器读计算样式（静态件，无需 hover） */
  window.__css = function (sel, props) {
    var e = document.querySelector(sel);
    if (!e) return JSON.stringify({ found: false, sel: sel });
    var st = getComputedStyle(e), o = { found: true, sel: sel };
    (props || ['backgroundColor', 'color', 'borderTopColor', 'borderTopWidth']).forEach(function (p) {
      o[p] = st[p];
    });
    return JSON.stringify(o);
  };

  window.__setDark = function () {
    try { window.__giTheme.set('dark'); return 'ok'; } catch (e) { return 'ERR ' + e.message; }
  };
  window.__setLight = function () {
    try { window.__giTheme.set('light'); return 'ok'; } catch (e) { return 'ERR ' + e.message; }
  };
  return 'ready';
})();
