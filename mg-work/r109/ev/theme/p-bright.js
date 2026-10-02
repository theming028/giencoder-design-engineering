(function () {
  /* r109 第四拍（裁决③落地）· 侦察：**暗色档下「亮面」逐状态审计**。

     ★ 与 `p-mix.js` 的关系：判据**完全一致**（不透明亮底的相对亮度 > 0.55、亮边框、渐变亮色、
       亮 box-shadow），但**多了「逐状态」**这一维 —— `p-mix.js` 只扫**首屏默认态**，
       而邵先生指出的那批（工作目录下拉激活底 `#E2E3E4`、浮层白底 `rgba(255,255,255,.88)`
       + 描边 `#F2F2F2`）**只在展开 / 选中时**才进 DOM ⇒ 默认态扫不到。

     ★★ 为什么**不查 `fill`**（第一版踩到，记下来）：暗色档下**亮色的矢量图标是正常的**
       （本来就该由 token 翻成浅色）。第一版把 `fill` 一并纳入 ⇒ 1548 条命中里
       绝大多数是 `rgb(247,247,247)` 压在 `rgb(78,78,78)` 这种**正确**搭配。
       图形侧的正经判据在 `p-dim.js`（找「暗底上发暗的图形」）——两者是**互补**的，
       不要合并。本探针只回答一个问题：**在这块暗底上，有没有不该亮的「面/线/发光」**。

     ⚠ 只读，不改任何样式（唯一例外：钉死 transition，避免读到过渡中间值）。 */
  function noTrans() {
    if (document.getElementById('probe-notrans')) return;
    var s = document.createElement('style');
    s.id = 'probe-notrans';
    s.textContent = '*,*::before,*::after{transition:none!important;animation:none!important;}';
    (document.head || document.documentElement).appendChild(s);
  }
  function lum(c) {
    var m = String(c).match(/[\d.]+/g);
    if (!m || m.length < 3) return null;
    function f(x) { x = x / 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }
    return 0.2126 * f(+m[0]) + 0.7152 * f(+m[1]) + 0.0722 * f(+m[2]);
  }
  function alpha(c) {
    var m = String(c).match(/[\d.]+/g);
    if (!m) return 1;
    return m.length > 3 ? +m[3] : 1;
  }
  function path(el) {
    var p = [], n = 0;
    while (el && el.nodeType === 1 && el !== document.body && n < 5) {
      var s = el.tagName.toLowerCase();
      if (el.id) s += '#' + el.id;
      else {
        var c = (typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
        if (c) s += '.' + c;
      }
      p.unshift(s); el = el.parentElement; n++;
    }
    return p.join('>');
  }
  function vis(el, cs) {
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width >= 1 && r.height >= 1;
  }

  function scan() {
    noTrans();
    var out = [];
    var all = document.querySelectorAll('body *');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (el.id === 'probe-notrans') continue;
      var cs = getComputedStyle(el);
      if (!vis(el, cs)) continue;
      var r = el.getBoundingClientRect();
      var area = Math.round(r.width * r.height);
      var base = { sel: path(el), x: Math.round(r.x), y: Math.round(r.y + window.scrollY),
                   w: Math.round(r.width), h: Math.round(r.height), area: area,
                   st: (el.getAttribute('style') || '').slice(0, 120),
                   cls: String(el.className || '').slice(0, 80) };

      var lb = lum(cs.backgroundColor);
      /* ① 自己有不透明亮底 ⇒ 「浅色残留块」 */
      if (lb !== null && lb > 0.55 && alpha(cs.backgroundColor) > 0.5) {
        out.push(Object.assign({ k: 'bg', v: cs.backgroundColor }, base));
      }
      /* ② 半透明亮底（遮罩/叠色）—— 单独记，避免被当成整块误判 */
      else if (lb !== null && lb > 0.55 && alpha(cs.backgroundColor) > 0.10) {
        out.push(Object.assign({ k: 'bgA', v: cs.backgroundColor }, base));
      }

      /* ③ 渐变里的亮色 */
      var bgi = cs.backgroundImage;
      if (bgi && bgi !== 'none') {
        var cols = bgi.match(/rgba?\([^)]*\)|#[0-9a-fA-F]{3,8}/g) || [];
        for (var j = 0; j < cols.length; j++) {
          var lj = lum(cols[j]);
          if (lj !== null && lj > 0.55 && alpha(cols[j]) > 0.35) {
            out.push(Object.assign({ k: 'bgimg', v: cols[j], img: bgi.slice(0, 90) }, base));
            break;
          }
        }
      }

      /* ④ 亮边框（1px 亮线在暗底上非常扎眼） */
      var bw = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderRightWidth)
             + parseFloat(cs.borderBottomWidth) + parseFloat(cs.borderLeftWidth);
      if (bw > 0) {
        var bl = lum(cs.borderTopColor);
        if (bl !== null && bl > 0.55 && alpha(cs.borderTopColor) > 0.3) {
          out.push(Object.assign({ k: 'border', v: cs.borderTopColor }, base));
        }
      }

      /* ⑤ 亮 box-shadow（"发光"卡） */
      var sh = cs.boxShadow;
      if (sh && sh !== 'none') {
        var cs2 = sh.match(/rgba?\([^)]*\)/g) || [];
        for (var m = 0; m < cs2.length; m++) {
          var lm = lum(cs2[m]);
          if (lm !== null && lm > 0.70 && alpha(cs2[m]) > 0.10) {
            out.push(Object.assign({ k: 'shadow', v: cs2[m], img: sh.slice(0, 70) }, base));
            break;
          }
        }
      }
    }
    return out;
  }

  /* ---- 触发件发现：只挑**不改路由**的可点开元素（排除 `a[href]` 与任何含 a[href] 祖先的）----
     ★ 两轮：
       ① 语义件 —— `aria-haspopup` / `aria-expanded` / `role=combobox` / `role=tab` 等；
       ② 关键词件 —— 浮层/弹窗/下拉的入口常常只是普通 `<button>`，靠 aria 属性认不出来
          （实测漏网：avatar 的 640×640 弹窗、task-detail 的协作弹窗与技能浮层）。
          故按「文案/aria-label 关键词」补一轮**白名单**（不放开全量 button，
          因为页面里有 `安装技能` 这种 `window.location.href=` 的跳转件，点了会离开本页）。 */
  var KW = /设置|权限|模型|大模型|工作目录|技能|更多|详情|预览|协作|分享|导出|历史|版本|折叠|展开|收起|筛选|排序|切换|选择|添加|新建|管理|查看|菜单|列表|选项/;
  function safe(el) {
    if (el.closest && el.closest('a[href]')) return false;
    if (el.tagName === 'A') return false;
    if (!vis(el, getComputedStyle(el))) return false;
    var lab = (el.getAttribute('aria-label') || '') + ' ' + (el.textContent || '');
    return true;
  }
  function triggers() {
    var sel = '[aria-haspopup],[aria-expanded],[role="combobox"],[role="tab"],' +
              '.ws-trigger-hover,.ws-dropdown-hover,.giencoder-select-view,' +
              '.td-browse-tab,.session-action-item,.model-dropdown-menu-item,[aria-pressed],' +
              '.giencoder-popover-reference > button,button.giencoder-btn';
    var list = document.querySelectorAll(sel);
    var out = [], seen = {};
    function add(el, byKw) {
      if (!safe(el)) return;
      var lab = (el.getAttribute('aria-label') || '') + ' ' + (el.textContent || '');
      if (byKw && !KW.test(lab)) return;
      var r = el.getBoundingClientRect();
      var k = path(el) + '@' + Math.round(r.x) + ',' + Math.round(r.y);
      if (seen[k]) return;
      seen[k] = 1;
      out.push(el);
    }
    for (var i = 0; i < list.length; i++) add(list[i], false);
    var btns = document.querySelectorAll('button');
    for (var j = 0; j < btns.length; j++) add(btns[j], true);
    return out;
  }

  window.__brightScan = function (label) {
    /* ★★ 必须每次**重新钉死暗色**：settings 页的「主题」分组本身就是一组可点件，
       探针把它们当普通触发件点了一次 ⇒ 页面切回**浅色** ⇒ 之后每个状态都在浅色档取样，
       报出来的「亮面」全是浅色档的正常值（第一版实测：settings 一次性冒出 200 条假阳性，
       含 `body 1440x900 background rgb(244,245,246)` 这种一眼假的）。
       ⇒ 每次扫描前重设，把「主题被自己点掉」这条路径堵死。 */
    try { window.__giTheme.set('dark'); } catch (e) {}
    noTrans();
    void document.documentElement.offsetHeight;
    var r = scan();
    for (var i = 0; i < r.length; i++) r[i].state = label;
    return r;
  };

  noTrans();
  window.__giTheme.set('dark');
  noTrans();
  void document.documentElement.offsetHeight;

  var DE = getComputedStyle(document.documentElement);
  var SANITY = {
    attr: document.documentElement.getAttribute('giencoder-theme'),
    dataGiDark: document.documentElement.getAttribute('data-gi-dark'),
    bg1: DE.getPropertyValue('--color-bg-1').trim(),
    htmlBg: DE.backgroundColor
  };

  var arr = window.__brightScan('默认态');
  var nT = 0, fired = [];

  var list = triggers();
  for (var t = 0; t < list.length && t < 60; t++) {
    var el = list[t];
    var label = path(el);
    try {
      el.click();
      void document.documentElement.offsetHeight;
      var got = window.__brightScan('展开:' + label);
      if (got.length) { arr = arr.concat(got); fired.push(label); }
      try { el.click(); } catch (e2) {}
      document.body.dispatchEvent(new MouseEvent('pointerdown', { bubbles: true }));
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      void document.documentElement.offsetHeight;
      nT++;
    } catch (e3) {}
  }

  window.__giTheme.set('light');
  return JSON.stringify({
    sanity: SANITY, triggered: nT, firedWithFindings: fired,
    total: arr.length, items: arr.slice(0, 200)
  });
})()
