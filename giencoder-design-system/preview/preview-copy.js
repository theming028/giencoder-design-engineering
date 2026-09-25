/* GienCoder 设计系统 · 组件样式右键复制工具
 * 用途：preview 组件页内，对任意组件实例右键 → 「复制组件样式」，
 *       输出该实例可直接套用的 CSS：
 *         · 基础块：优先沿用组件设计 Token（var(--token)），无对应规则的
 *           跨源受限场景（file://）自动回退到最终计算值，保证永不落空
 *         · 状态块：:hover/:active/:focus 及 ::before/::after 原样保留
 * 零依赖原生 JS，IIFE 隔离，不改组件模板结构，file:// 与 http 均可运行。
 * 接入：组件页 </body> 前 <script src="preview-copy.js"></script>。
 */
(function () {
  'use strict';

  /* ---------- 剪贴板（含 file:// 降级） ---------- */

  function copyText(text, ok, fail) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(ok, function () { legacyCopy(text, ok, fail); });
    } else {
      legacyCopy(text, ok, fail);
    }
  }

  function legacyCopy(text, ok, fail) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    var ok1 = false;
    try { ok1 = document.execCommand('copy'); } catch (e) { ok1 = false; }
    document.body.removeChild(ta);
    ok1 ? ok() : fail();
  }

  /* 从命中规则中提取「保留 var() token 引用」的画布级基础样式块。
   * 依据：proutcss 的 components.css 组件样式全部用 token 书写，命中规则的 cssText 保留 var() 原文
   *       （浏览器 CSSOM 不展开自定义属性），因此直接解析每条规则声明即可得到规范 token 输出。
   * 层叠近似：按样式表加载顺序 + 规则顺序，逐条合并，同属性后者覆盖前者。
   * 过滤：无信息量默认值（全局 reset / 推导默认）剔除，但含 var() 的一律保留。 */
  function computedBlock(rules, mediaOf) {
    var merged = {};
    var order = 0;
    var i, r, decl, p, parts;

    for (i = 0; i < rules.length; i++) {
      r = rules[i];
      // 跳过状态/伪元素规则（它们单独输出）
      if (isStateRule(r.sel)) continue;
      // 跳过 @media 内规则（保持简单，只输出直接命中的常态规则）
      if (mediaOf && mediaOf[i]) continue;
      decl = parseDeclarations(r.cssText);
      for (p in decl) {
        if (decl.hasOwnProperty(p)) {
          merged[p] = { value: decl[p], order: order++ };
        }
      }
    }

    parts = Object.keys(merged).map(function (k) {
      return { k: k, v: merged[k].value, order: merged[k].order };
    });
    parts.sort(function (a, b) { return a.order - b.order; });

    var o = [];
    for (i = 0; i < parts.length; i++) {
      if (isNoise(parts[i].k, parts[i].v)) continue;
      o.push('  ' + parts[i].k + ': ' + tokenizeValue(parts[i].k, parts[i].v) + ';');
    }
    return o.join('\n');
  }

  /* 把写死的申明值反查为设计 Token（保留已含 var()/calc() 者）。
   * margin/padding/border-radius 这类四值简写逐边反查后重组，如 0 16px → 0 var(--spacing-7)。 */
  function tokenizeValue(prop, value) {
    if (!value) return value;
    var s = String(value).trim();
    if (s.indexOf('var(') !== -1 || s.indexOf('calc(') !== -1) return s;
    var probeT = tokenProbe();
    var group = probeGroupOf(prop);
    var grp = group ? probeT[group] : null;
    if (!grp) return s;
    var sides = s.split(/\s+/);
    if (sides.length > 1) {
      var ret = sides.map(function (v) {
        var k = v.toLowerCase();
        var tok = grp[k] || grp[v];
        return tok ? 'var(' + tok + ')' : v;
      });
      return ret.join(' ');
    }
    var k = s.toLowerCase();
    var tok = grp[k] || grp[s];
    return tok ? 'var(' + tok + ')' : s;
  }

  /* 属性 → 反查类别（与 fallback 的 probeGroup 一致） */
  function probeGroupOf(prop) {
    if (prop === 'background-color' || prop === 'color') return 'color';
    if (prop === 'border-radius') return 'radius';
    if (prop === 'font-size') return 'fontsize';
    if (prop === 'gap' || prop === 'margin' || prop === 'padding') return 'spacing';
    if (prop === 'line-height') return 'lineheight';
    if (prop === 'font-family') return 'fontfamily';
    if (prop === 'box-shadow') return 'shadow';
    return null;
  }

  /* 将 style.cssText 声明文本解析为 { prop: value }（value 保留 var() 与源简写） */
  function parseDeclarations(cssText) {
    var out = {};
    var re = /([a-zA-Z-]+)\s*:\s*([^;]*)/g;
    var m;
    while ((m = re.exec(cssText)) !== null) {
      var p = m[1].trim(), v = m[2].trim();
      if (v) out[p] = v;
    }
    return out;
  }

  /* 过滤对复制无意义 / reset 噪音（凡含 var() 一律保留） */
  function isNoise(prop, value) {
    if (value.indexOf('var(') !== -1) return false;        // 含 token，保留
    if (value.indexOf('calc(') !== -1) return false;       // calc 保留
    var v = String(value).toLowerCase().trim();
    if (v === 'transparent' || v === 'rgba(0, 0, 0, 0)') return true;
    if (['none', 'auto', 'static', 'normal', '0', '0px', 'visible', 'clip', 'baseline'].indexOf(v) !== -1) return true;
    if (prop === 'background-repeat' && v === 'repeat') return true;
    if (prop === 'background-position') return true;
    if (prop === 'opacity' && (v === '1' || v === '1.0')) return true;
    if (prop === 'font-family' && /^('?[a-z-]+'?|system-ui|-apple-system|initial)$/.test(v)) return true;
    if (prop === 'line-height' && /1\.5\d+/.test(v)) return true; // 系统默认行高噪音
    return false;
  }

  /* 去状态伪类/伪元素，得静态基选择器 */
  function baseSel(sel) {
    return sel
      .replace(/::[a-z-]+/g, '')
      .replace(/:(?:hover|active|focus|focus-visible|focus-within|visited|link|checked|disabled|enabled|required|optional|placeholder-shown)\b/g, '')
      .replace(/:nth(?:-child|-of-type)\([^)]*\)/g, '')
      .trim();
  }

  function isStateRule(sel) {
    return /:(?:hover|active|focus|focus-visible|focus-within|visited|link|checked|disabled|enabled)\b|::[a-z-]/.test(sel);
  }

  /* 命中目标元素的项目样式表规则（colors_and_type.css + components.css）
   * 每个样式表单独捕获异常：源内（同目录）样式表可正常读 cssRules；跨源/受限时跳过，
   * 由调用方依据命中数决定是否回退到计算值方案。 */
  function matchingRulesAll(el) {
    var sheets = Array.prototype.slice.call(document.styleSheets).filter(function (s) {
      var h = s.href || '';
      return /colors_and_type\.css$|components\.css$/.test(h);
    });
    var hits = [];
    var seen = {};
    function add(sel, cssText, media) {
      var key = (media || '') + '|' + sel + '|' + cssText;
      if (seen[key]) return;
      seen[key] = true;
      hits.push({ sel: sel, cssText: cssText, media: media || null });
    }
    function walk(list, media) {
      if (!list) return;
      var i, r, base;
      for (i = 0; i < list.length; i++) {
        r = list[i];
        if (r.type === CSSRule.STYLE_RULE) {
          base = baseSel(r.selectorText);
          if (base) { try { if (el.matches(base)) add(r.selectorText, r.style.cssText, media); } catch (e) {} }
        } else if (r.type === CSSRule.MEDIA_RULE && r.cssRules) {
          walk(r.cssRules, r.conditionText);
        }
      }
    }
    var s;
    for (s = 0; s < sheets.length; s++) {
      try { walk(sheets[s].cssRules, null); } catch (e) { /* 跨源受限：跳过该表 */ }
    }
    return hits;
  }

  function buildCss(el) {
    var rules, base = [], state = [], mediaOf = [], i, r;
    try { rules = matchingRulesAll(el); } catch (e) { rules = []; }

    /* 以组件实际类名作为复制输出的选择器名（取元素上最短的 .giencoder-* 核心类，如 .giencoder-btn；
     * 无则回退 data-component 组件类型名）。 */
    function classNameFor(node) {
      var list = node.classList ? Array.prototype.slice.call(node.classList) : [];
      var gcls = list.filter(function (c) { return c.indexOf('giencoder-') === 0; });
      if (gcls.length) {
        gcls.sort(function (a, b) { return a.length - b.length; });
        return '.' + gcls[0];
      }
      var dc = node.getAttribute && node.getAttribute('data-component');
      return dc ? '.giencoder-' + dc : '.keep-class-name';
    }
    var cls = classNameFor(el);

    for (i = 0; i < rules.length; i++) {
      r = rules[i];
      mediaOf.push(r.media);
      if (isStateRule(r.sel)) {
        var decl = r.cssText.replace(/;\s*$/, '').trim();
        var txt = r.media
          ? '@media ' + r.media + ' {\n  ' + r.sel + ' {\n  ' + decl + '\n  }\n}\n'
          : r.sel + ' {\n  ' + decl + '\n}';
        if (state.indexOf(txt) === -1) state.push(txt);
      } else {
        if (base.indexOf(r.sel) === -1) base.push(r.sel);
      }
    }

    var parts = [];
    var cb = '';
    if (rules.length === 0) {
      // file:// 等跨源受限场景：cssRules 读不到 → 回退到计算值方案
      try { cb = fallbackComputedBlock(el); } catch (e) { cb = ''; }
    } else {
      try { cb = computedBlock(rules, mediaOf); } catch (e) { cb = ''; }
    }
    if (!cb) {
      // 最终兜底：保证任何情况下都能复制出可复用基础块
      cb = minimalBlock(el);
    }
    parts.push('/* 组件基础样式（沿用设计 Token，粘贴到自己类名下即可） */\n' + cls + ' {\n' + cb + '\n}');
    if (state.length) {
      parts.push('/* 交互状态与伪元素（沿用 Token，原样保留） */\n' + state.join('\n\n'));
    }
    return parts.join('\n\n');
  }

  /* 极端兜底：仅输出元素最基本信息，确保复制永不落空 */
  function minimalBlock(el) {
    var tag = el.tagName ? el.tagName.toLowerCase() : 'div';
    var cs = window.getComputedStyle(el);
    var o = [];
    o.push('  display: ' + (cs.display || 'block') + ';');
    var w = cs.width, h = cs.height;
    if (w && w !== 'auto') o.push('  width: ' + w + ';');
    if (h && h !== 'auto') o.push('  height: ' + h + ';');
    return o.join('\n');
  }

  /* 运行时探测：每个 token 计算值→反查表；颜色按语义优先级覆盖(mask/menu/tooltip 弱化)。 */
  var __TOKEN_PROBE = null;
  function tokenProbe() {
    if (__TOKEN_PROBE) return __TOKEN_PROBE;
    var t = {}, host = document.createElement("div");
    document.body.appendChild(host);
    (function(){var m=t["color"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-bg-popup)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-bg-popup";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-bg-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-bg-5";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-bg-white)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-bg-white";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-bg-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-bg-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-bg-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-bg-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-bg-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-bg-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-bg-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-bg-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-fill-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-fill-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-fill-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-fill-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-fill-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-fill-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-fill-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-fill-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-border)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-border";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-border-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-border-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-border-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-border-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-border-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-border-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-border-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-border-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-text-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-text-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-text-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-text-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-text-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-text-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-text-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-text-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-link-hover)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-link-hover";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-link-light-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-link-light-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-link-light-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-link-light-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-link)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-link";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-link-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-link-6";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-danger-light-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-danger-light-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-danger-light-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-danger-light-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-danger)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-danger";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-danger-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-danger-5";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-danger-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-danger-6";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-warning-light-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-warning-light-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-warning-light-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-warning-light-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-warning)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-warning";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-warning-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-warning-5";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-warning-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-warning-6";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-success-light-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-success-light-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-success-light-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-success-light-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-success)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-success";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-success-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-success-5";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-success-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-success-6";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-secondary-hover)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-secondary-hover";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-secondary-active)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-secondary-active";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-secondary-disabled)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-secondary-disabled";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-secondary)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-secondary";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-data-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-data-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-data-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-data-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-data-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-data-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-data-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-data-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-data-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-data-5";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-5";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-6";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-7)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-7";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-8)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-8";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-9)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-9";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-neutral-10)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-neutral-10";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-light-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-light-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-light-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-light-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-light-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-light-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-light-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-light-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-10)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-10";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-9)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-9";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-8)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-8";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-7)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-7";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-6";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-5";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-4";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-3";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-2";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-primary-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-primary-1";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-purple-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-purple-6";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-black)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-black";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-white)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]="--color-white";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-mask-bg)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]=m[v.toLowerCase()]||"--color-mask-bg";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-menu-dark-bg)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]=m[v.toLowerCase()]||"--color-menu-dark-bg";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-menu-dark-hover)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]=m[v.toLowerCase()]||"--color-menu-dark-hover";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-menu-light-bg)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]=m[v.toLowerCase()]||"--color-menu-light-bg";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-spin-layer-bg)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]=m[v.toLowerCase()]||"--color-spin-layer-bg";}})();
    (function(){var e=document.createElement("div");e.style["color"]="var(--color-tooltip-bg)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("color").trim();if(v&&v!==""){m[v.toLowerCase()]=m[v.toLowerCase()]||"--color-tooltip-bg";}})();
    })();
    (function(){var m=t["radius"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["borderRadius"]="var(--border-radius-circle)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("border-radius").trim();if(v&&v!==""){m[v.toLowerCase()]="--border-radius-circle";}})();
    (function(){var e=document.createElement("div");e.style["borderRadius"]="var(--border-radius-large)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("border-radius").trim();if(v&&v!==""){m[v.toLowerCase()]="--border-radius-large";}})();
    (function(){var e=document.createElement("div");e.style["borderRadius"]="var(--border-radius-medium)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("border-radius").trim();if(v&&v!==""){m[v.toLowerCase()]="--border-radius-medium";}})();
    (function(){var e=document.createElement("div");e.style["borderRadius"]="var(--border-radius-none)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("border-radius").trim();if(v&&v!==""){m[v.toLowerCase()]="--border-radius-none";}})();
    (function(){var e=document.createElement("div");e.style["borderRadius"]="var(--border-radius-small)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("border-radius").trim();if(v&&v!==""){m[v.toLowerCase()]="--border-radius-small";}})();
    })();
    (function(){var m=t["spacing"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-1";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-10)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-10";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-11)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-11";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-12)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-12";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-13)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-13";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-14)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-14";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-15)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-15";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-16)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-16";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-17)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-17";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-18)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-18";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-19)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-19";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-2";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-20)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-20";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-21)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-21";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-22)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-22";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-3";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-4";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-5";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-6)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-6";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-7)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-7";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-8)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-8";}})();
    (function(){var e=document.createElement("div");e.style["paddingLeft"]="var(--spacing-9)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("padding-left").trim();if(v&&v!==""){m[v.toLowerCase()]="--spacing-9";}})();
    })();
    (function(){var m=t["fontsize"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-body)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-body";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-body-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-body-1";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-body-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-body-2";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-body-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-body-3";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-caption)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-caption";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-display-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-display-1";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-display-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-display-2";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-display-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-display-3";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-title-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-title-1";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-title-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-title-2";}})();
    (function(){var e=document.createElement("div");e.style["fontSize"]="var(--font-size-title-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-size").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-size-title-3";}})();
    })();
    (function(){var m=t["lineheight"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["lineHeight"]="var(--line-height-base)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("line-height").trim();if(v&&v!==""){m[v.toLowerCase()]="--line-height-base";}})();
    })();
    (function(){var m=t["fontfamily"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["fontFamily"]="var(--font-family)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("font-family").trim();if(v&&v!==""){m[v.toLowerCase()]="--font-family";}})();
    })();
    (function(){var m=t["shadow"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow-none)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow-none";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow-special)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow-special";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow1-center)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow1-center";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow1-down)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow1-down";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow1-left)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow1-left";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow1-right)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow1-right";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow1-up)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow1-up";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow2-center)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow2-center";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow2-down)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow2-down";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow2-left)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow2-left";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow2-right)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow2-right";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow2-up)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow2-up";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow3-center)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow3-center";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow3-down)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow3-down";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow3-left)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow3-left";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow3-right)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow3-right";}})();
    (function(){var e=document.createElement("div");e.style["boxShadow"]="var(--shadow3-up)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("box-shadow").trim();if(v&&v!==""){m[v.toLowerCase()]="--shadow3-up";}})();
    })();
    (function(){var m=t["tdur"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["transitionDuration"]="var(--transition-duration-1)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-duration").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-duration-1";}})();
    (function(){var e=document.createElement("div");e.style["transitionDuration"]="var(--transition-duration-2)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-duration").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-duration-2";}})();
    (function(){var e=document.createElement("div");e.style["transitionDuration"]="var(--transition-duration-3)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-duration").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-duration-3";}})();
    (function(){var e=document.createElement("div");e.style["transitionDuration"]="var(--transition-duration-4)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-duration").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-duration-4";}})();
    (function(){var e=document.createElement("div");e.style["transitionDuration"]="var(--transition-duration-5)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-duration").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-duration-5";}})();
    })();
    (function(){var m=t["ttiming"]={},host2=document.createElement("div");host.appendChild(host2);
    (function(){var e=document.createElement("div");e.style["transitionTimingFunction"]="var(--transition-timing-function-accelerate)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-timing-function").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-timing-function-accelerate";}})();
    (function(){var e=document.createElement("div");e.style["transitionTimingFunction"]="var(--transition-timing-function-decelerate)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-timing-function").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-timing-function-decelerate";}})();
    (function(){var e=document.createElement("div");e.style["transitionTimingFunction"]="var(--transition-timing-function-linear)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-timing-function").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-timing-function-linear";}})();
    (function(){var e=document.createElement("div");e.style["transitionTimingFunction"]="var(--transition-timing-function-overshoot)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-timing-function").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-timing-function-overshoot";}})();
    (function(){var e=document.createElement("div");e.style["transitionTimingFunction"]="var(--transition-timing-function-spring)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-timing-function").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-timing-function-spring";}})();
    (function(){var e=document.createElement("div");e.style["transitionTimingFunction"]="var(--transition-timing-function-standard)";host2.appendChild(e);var v=getComputedStyle(e).getPropertyValue("transition-timing-function").trim();if(v&&v!==""){m[v.toLowerCase()]="--transition-timing-function-standard";}})();
    })();
    document.body.removeChild(host);__TOKEN_PROBE=t;return t;
  }

  /* file:// 跨源受限时的兜底：直接读取目标元素最终计算值，并把可还原的值替换回 var(--token)。 */
  function fallbackComputedBlock(el) {
    var cs = window.getComputedStyle(el);
    var g = function (p) { return cs.getPropertyValue(p); };
    var probe = tokenProbe();
    var o = [];

    /* 属性→探测类别 */
    function probeGroup(prop) {
      if (prop === 'background-color' || prop === 'color') return 'color';
      if (prop === 'border-radius') return 'radius';
      if (prop === 'font-size') return 'fontsize';
      if (prop === 'gap') return 'spacing';
      if (prop === 'line-height') return 'lineheight';
      if (prop === 'font-family') return 'fontfamily';
      if (prop === 'box-shadow') return 'shadow';
      return null;
    }
    /* 注册一条输出：值若有对应 token 则写 var(--token)，否则保留写死值 */
    function push(prop, value) {
      if (!value) return;
      var grp = probe[probeGroup(prop)];
      var tok = null;
      if (grp) tok = grp[String(value).trim().toLowerCase()] || grp[String(value).trim()];
      o.push('  ' + prop + ': ' + (tok ? 'var(' + tok + ')' : value) + ';');
    }

    /* 四值简写逐边反查 token：每个单边值若命中设计 token 则写 var(--token)（如 12px→var(--spacing-6)），未命中保留原值。 */
    function pushCompact4(prop, values, group) {
      var grp = probe[group];
      var ts = values.map(function (v) {
        v = (v || '').trim();
        if (!v) return v;
        var k = String(v).toLowerCase();
        var tok = grp ? (grp[k] || grp[v]) : null;
        return tok ? 'var(' + tok + ')' : v;
      });
      var out = compact4(ts);
      if (out) o.push('  ' + prop + ': ' + out + ';');
    }

    var m = ['', '', '', ''];
    ['top', 'right', 'bottom', 'left'].forEach(function (s, i) { m[i] = g('margin-' + s); });
    pushCompact4('margin', m, 'spacing');
    var pArr = ['', '', '', ''];
    ['top', 'right', 'bottom', 'left'].forEach(function (s, i) { pArr[i] = g('padding-' + s); });
    pushCompact4('padding', pArr, 'spacing');
    var rad = ['', '', '', ''];
    ['top-left', 'top-right', 'bottom-right', 'bottom-left'].forEach(function (s, i) { rad[i] = g('border-' + s + '-radius'); });
    pushCompact4('border-radius', rad, 'radius');
    var w = g('width'), h = g('height');
    if (w) o.push('  width: ' + w + ';');
    if (h) o.push('  height: ' + h + ';');
    var disp = g('display');
    if (disp) o.push('  display: ' + disp + ';');
    var box = g('box-sizing');
    if (box && box !== 'content-box') o.push('  box-sizing: ' + box + ';');
    var bg = g('background-color');
    if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') push('background-color', bg);
    var color = g('color');
    if (color) push('color', color);
    var shadow = g('box-shadow');
    if (shadow && shadow !== 'none') o.push('  box-shadow: ' + shadow + ';');
    var cursor = g('cursor');
    if (cursor && cursor !== 'auto' && cursor !== 'default') o.push('  cursor: ' + cursor + ';');
    var wspace = g('white-space');
    if (wspace && wspace !== 'normal') o.push('  white-space: ' + wspace + ';');
    var overfl = g('text-overflow');
    if (overfl && overfl !== 'clip') o.push('  text-overflow: ' + overfl + ';');
    var textAlign = g('text-align');
    if (textAlign && textAlign !== 'start' && textAlign !== 'left') o.push('  text-align: ' + textAlign + ';');
    var fontSize = g('font-size');
    if (fontSize && fontSize !== '14px' && fontSize !== 'medium') push('font-size', fontSize);
    var fontWeight = g('font-weight');
    if (fontWeight && fontWeight !== '400' && fontWeight !== 'normal') o.push('  font-weight: ' + fontWeight + ';');
    var gap = g('gap');
    if (gap && gap !== 'normal' && gap !== '0px') push('gap', gap);
    return o.join('\n');
  }

  /* 四值 → 简写（全同为单值，最大化省略） */
  function compact4(v) {
    var vs = v.map(function (s) { return (s || '').trim(); });
    if (!vs[0] && !vs[1] && !vs[2] && !vs[3]) return '';
    if (vs[0] === vs[1] && vs[1] === vs[2] && vs[2] === vs[3]) return vs[0];
    if (vs[0] === vs[2] && vs[1] === vs[3]) return vs[0] + ' ' + vs[1];
    if (vs[3] === vs[1]) return vs[0] + ' ' + vs[1] + ' ' + vs[2];
    return vs[0] + ' ' + vs[1] + ' ' + vs[2] + ' ' + vs[3];
  }

  /* ---------- 菜单 UI ---------- */

  var M = 'gc-copy-menu', I = 'gc-copy-item', T = 'gc-copy-toast';

  function ensureMenu() {
    var m = document.querySelector('.' + M);
    if (m) return m;
    var st = document.createElement('style');
    st.textContent =
      '.' + M + '{position:fixed;z-index:99999;margin:0;padding:4px;min-width:150px;' +
      'background:#fff;border:1px solid #e5e6eb;border-radius:4px;' +
      'box-shadow:0 6px 20px rgba(15,23,42,.12);list-style:none;display:none;' +
      'font:500 14px/1.4 "Mona Sans VF",-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans Backtick Fix","Noto Sans",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";}' +
      '.' + M + '.open{display:block;animation:gcCopyIn .15s ease-out;}' +
      '@keyframes gcCopyIn{from{opacity:0;transform:scale(.96) translateY(-2px);}to{opacity:1;transform:none;}}' +
      '.' + I + '{padding:6px 12px;color:#1d2129;cursor:pointer;border-radius:2px;white-space:nowrap;}' +
      '.' + I + ':hover{background:#f7f8fa;}' +
      '.' + T + '{position:fixed;z-index:100000;left:50%;top:64px;transform:translateX(-50%);' +
      'padding:6px 14px;background:#1d2129;color:#fff;border-radius:4px;pointer-events:none;' +
      'font:500 13px/1.4 "Mona Sans VF",-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans Backtick Fix","Noto Sans",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";' +
      'opacity:0;transition:opacity .2s;}' +
      '.' + T + '.show{opacity:1;}';
    document.head.appendChild(st);

    m = document.createElement('ul');
    m.className = M;
    var li = document.createElement('li');
    li.className = I;
    li.textContent = '复制组件样式';
    m.appendChild(li);
    document.body.appendChild(m);
    return m;
  }

  var toast = null;
  function showToast(msg) {
    if (!toast) { toast = document.createElement('div'); toast.className = T; document.body.appendChild(toast); }
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.classList.remove('show'); }, 1600);
  }

  var currentEl = null;

  function openMenu(x, y, el) {
    var m = ensureMenu();
    currentEl = el;
    var r = m.getBoundingClientRect();
    m.style.left = Math.min(x, window.innerWidth - r.width - 6) + 'px';
    m.style.top = Math.min(y, window.innerHeight - r.height - 6) + 'px';
    m.classList.add('open');
  }

  function closeMenu() {
    var m = document.querySelector('.' + M);
    if (m) m.classList.remove('open');
    currentEl = null;
  }

  function findComponent(n) {
    while (n && n.nodeType === 1 && n !== document.body && n !== document) {
      if (n.getAttribute && n.getAttribute('data-component')) return n;
      n = n.parentNode;
    }
    return null;
  }

  /* ---------- 事件 ---------- */

  document.addEventListener('contextmenu', function (e) {
    var el = findComponent(e.target);
    if (!el) return;
    e.preventDefault();
    openMenu(e.clientX, e.clientY, el);
  }, true);

  document.addEventListener('click', function (e) {
    if (e.target && e.target.classList && e.target.classList.contains(I)) {
      if (!currentEl) { closeMenu(); return; }
      var css = buildCss(currentEl);
      if (!css) { showToast('未抽取到可复用样式'); closeMenu(); return; }
      copyText(css, function () { showToast('已复制组件样式'); },
        function () { showToast('复制失败，请用 Ctrl+V 手动粘贴'); });
      closeMenu();
      return;
    }
    closeMenu();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.key === 'Esc') closeMenu();
  });
  window.addEventListener('resize', closeMenu);

  /* 可选端到端调试钩子：页面存在 #gc-copy-debug 时，自动把首个组件实例的抽取结果写入该元素 */
  function runDebug() {
    var host = document.getElementById('gc-copy-debug');
    if (!host) return;
    var el = document.querySelector('[data-component]');
    if (el) {
      var pre = document.createElement('pre');
      pre.textContent = buildCss(el);
      host.appendChild(pre);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runDebug);
  } else {
    runDebug();
  }

})();
