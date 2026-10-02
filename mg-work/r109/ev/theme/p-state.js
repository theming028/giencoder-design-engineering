(function () {
  /* r109 第四拍（裁决③落地）· **真鼠标驱动**的逐状态亮面探针（分两步用）。

     ★★ 为什么要真鼠标（本拍真踩，记下来）：
       第一版把「点开每个触发件」放进同一个 `eval` 里用 `el.click()`（JS 合成事件）——
       实测**打不开**：点完 `div.giencoder-select-view.ws-dropdown-hover` 后
       `aria-expanded` 仍是 `"false"`（真鼠标点同一个元素 → `"true"`）。
       于是整轮「逐状态」退化成「默认态重复扫描」，base/conversation 的
       **权限下拉浮层（内联 `rgba(255,255,255,.88)`）** 从来没进过 DOM ⇒ **假阴性**。
       与 PLAYBOOK「探针假失败八类」第 6 类（合成事件绕过手势）同源。
     ⇒ 拆成两步：本脚本只**采集触发点坐标**（`__pts()`）与**逐个扫描**（`__one()`），
       真正的点击交给 bash 侧的 `mouse move / down / up`（真事件）。

     ★ 判据与 `p-mix.js` 完全一致（不透明亮底 > 0.55、亮边框、渐变亮色、亮 box-shadow），
       只是多了「逐状态」。**不查 `fill`**：暗色档下亮色图标是正常的，
       图形侧的正经判据在 `p-dim.js`，两者互补。 */
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
      var base = { sel: path(el), x: Math.round(r.x), y: Math.round(r.y + window.scrollY),
                   w: Math.round(r.width), h: Math.round(r.height),
                   area: Math.round(r.width * r.height),
                   st: (el.getAttribute('style') || '').slice(0, 120),
                   cls: String(el.className || '').slice(0, 80) };
      var lb = lum(cs.backgroundColor);
      if (lb !== null && lb > 0.55 && alpha(cs.backgroundColor) > 0.5) {
        out.push(Object.assign({ k: 'bg', v: cs.backgroundColor }, base));
      } else if (lb !== null && lb > 0.55 && alpha(cs.backgroundColor) > 0.10) {
        out.push(Object.assign({ k: 'bgA', v: cs.backgroundColor }, base));
      }
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
      var bw = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderRightWidth)
             + parseFloat(cs.borderBottomWidth) + parseFloat(cs.borderLeftWidth);
      if (bw > 0) {
        var bl = lum(cs.borderTopColor);
        if (bl !== null && bl > 0.55 && alpha(cs.borderTopColor) > 0.3) {
          out.push(Object.assign({ k: 'border', v: cs.borderTopColor }, base));
        }
      }
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

  var KW = /设置|权限|模型|大模型|工作目录|技能|更多|详情|预览|协作|分享|导出|历史|版本|折叠|展开|收起|筛选|排序|切换|选择|添加|新建|管理|查看|菜单|列表|选项/;
  function pts() {
    var sel = '[aria-haspopup],[aria-expanded],[role="combobox"],[role="tab"],' +
              '.ws-trigger-hover,.ws-dropdown-hover,.giencoder-select-view,' +
              '.td-browse-tab,.session-action-item,.model-dropdown-menu-item,[aria-pressed],' +
              '.giencoder-popover-reference > button,button.giencoder-btn';
    var list = document.querySelectorAll(sel);
    var out = [], seen = {};
    function add(el, byKw) {
      if (el.closest && el.closest('a[href]')) return;
      if (el.tagName === 'A') return;
      if (!vis(el, getComputedStyle(el))) return;
      var lab = (el.getAttribute('aria-label') || '') + ' ' + (el.textContent || '');
      if (byKw && !KW.test(lab)) return;
      var r = el.getBoundingClientRect();
      if (r.width > 400 || r.height > 120) return;      /* 大块不是触发件 */
      var cx = Math.round(r.x + Math.min(r.width / 2, 40));
      var cy = Math.round(r.y + r.height / 2);
      if (cx < 1 || cy < 1 || cy > window.innerHeight - 2) return;
      var k = cx + ',' + cy;
      if (seen[k]) return;
      seen[k] = 1;
      out.push({ x: cx, y: cy, sel: path(el), lab: lab.trim().slice(0, 24) });
    }
    for (var i = 0; i < list.length; i++) add(list[i], false);
    var btns = document.querySelectorAll('button');
    for (var j = 0; j < btns.length; j++) add(btns[j], true);
    return out;
  }

  /* ★★ 累加器放 `localStorage`，不放 `window`（本拍真踩，记下来）：
     页面里混着**会跳路由**的可点件（`安装技能` → skills.html、顶栏「研发工作台」→ dev.html）。
     一跳转，挂在 `window` 上的全局全没了 ⇒ 之后每次 `eval` 都是
     `TypeError: window.__one is not a function`，整页数据白跑。
     `localStorage` 同源共享、跨导航存活 ⇒ 驱动侧跳转后重新注入探针即可无缝续跑。
     键在**每页开始时由驱动清空**（否则上一页的账会串到下一页）。
     ★ 顺便去重（`k|v|sel`）—— 同一元素在 20 多个状态里反复命中，不去重会把台账撑爆。 */
  var KEY = '__giBrightAcc';
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function save(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  }
  window.__acc = load();
  window.__one = function (label) {
    /* ★★ 只在**确实不是暗色**时才重设主题（本拍真踩第二坑，记下来）：
       上一版无条件 `__giTheme.set('dark')` —— 而「设置主题」这个动作在本站是**重渲染**，
       会把刚被真鼠标点开的浮层状态（`l==='perm'` / `'skills'`）一并复位
       ⇒ 权限浮层、技能浮层**每次扫描前一刻被自己关掉** ⇒ 连续两轮假阴性
       （定点复核：真鼠标点开后 `[aria-label="权限选择"]` 的计算底确实是
       `rgba(255,255,255,0.88)`，280×126 —— 判据没问题，是取样时机被自己破坏了）。
       ⇒ 改成「已暗就别动」，且**先钉 transition 再扫**，不动任何会触发重渲染的接口。 */
    if (document.documentElement.getAttribute('giencoder-theme') !== 'dark') {
      try { window.__giTheme.set('dark'); } catch (e) {}
    }
    noTrans();
    void document.documentElement.offsetHeight;
    var r = scan(), add = 0;
    for (var i = 0; i < r.length; i++) {
      r[i].state = label;
      var k = r[i].k + '|' + r[i].v + '|' + r[i].sel;
      if (window.__acc[k]) continue;
      window.__acc[k] = r[i];
      add++;
    }
    save(window.__acc);
    return JSON.stringify({ scanned: r.length, added: add, total: Object.keys(window.__acc).length });
  };
  window.__pts = function () {
    return JSON.stringify({ theme: document.documentElement.getAttribute('giencoder-theme'), pts: pts() });
  };
  window.__close = function () {
    /* ⚠ 这里**不再重设主题**：理由同 `__one`（重设会重渲染、把浮层复位）。
       收尾只需要「把当前浮层关掉」——Esc 一把，再往 body 派发一次 pointerdown 让自收。 */
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true }));
    document.body.dispatchEvent(new MouseEvent('pointerdown', { bubbles: true }));
    return '1';
  };
  window.__dump = function () {
    var DE = getComputedStyle(document.documentElement);
    var acc = load(), items = [];
    for (var k in acc) items.push(acc[k]);
    return JSON.stringify({
      sanity: { attr: document.documentElement.getAttribute('giencoder-theme'),
                dataGiDark: document.documentElement.getAttribute('data-gi-dark'),
                bg1: DE.getPropertyValue('--color-bg-1').trim(), htmlBg: DE.backgroundColor },
      total: items.length,
      items: items.slice(0, 400)
    });
  };
  window.__reset = function () { try { localStorage.removeItem(KEY); } catch (e) {} window.__acc = {}; return '0'; };

  noTrans();
  window.__giTheme.set('dark');
  noTrans();
  void document.documentElement.offsetHeight;
  window.__one('默认态');
  return 'ready';
})()
