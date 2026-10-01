/* r108 第十九拍 · 现状侦察
   问三件事：
   ① `.td-browse` 里到底有没有「可被真实鼠标拖选」的文本（含代码行）——
      以及现有划词浮条会不会为它弹出来（守卫写死 `.r93-scroll`）。
   ② `.td-mod-menu` 出现瞬间的逐帧状态（rAF 采样）：opacity / translate / scale /
      left / top / rect —— 看闪烁是「透明度」还是「位移」。
   ③ 侧栏在不在视口里（不在就拖不到）。 */
(function () {
  var M = window.__M || 'recon';
  function q(s) { return document.querySelector(s); }
  function qa(s) { return [].slice.call(document.querySelectorAll(s)); }
  function r(e) { if (!e) return null; var b = e.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(e, p) { return e ? getComputedStyle(e)[p] : null; }
  var out = { phase: M };

  function rec(p) { try { console.log('[RECON] ' + p + ' ' + (typeof p === 'string' ? '' : '') + JSON.stringify(arguments[1])); } catch (e) {} }

  /* ---- 通用：把侧栏滑进视口（与前几拍同法） ---- */
  function sidebarIn() {
    var b = q('.td-browse');
    if (!b) return null;
    var cls = b.className;
    var on = /av-browse-on/.test(cls);
    if (!on) {
      /* 侧栏开关按钮：顶栏里那一枚（沿用前几拍口径，先找 data-td-sidebar / aria-label） */
      var cands = qa('button').filter(function (x) {
        var al = x.getAttribute('aria-label') || '';
        return /侧栏|侧边|面板/.test(al);
      });
      if (cands.length) cands[0].click();
    }
    return { wasOn: on, cands: qa('button').length };
  }

  if (M === 'recon') {
    var b = q('.td-browse');
    out.browse = r(b);
    out.browseCls = b ? b.className : null;
    out.browseTx = b ? cs(b, 'transform') : null;
    out.bodyCls = document.body.className.slice(0, 200);
    out.sidebarIn = sidebarIn();
    out.winW = window.innerWidth;
    out.selbarExists = !!q('.td-selbar');
    /* 可拖选文本的候选：代码行 / diff 文本 / 摘要段落 */
    out.drT = qa('.td-dr-t').length;
    out.drT0 = r(qa('.td-dr-t')[0]);
    out.drTUserSel = cs(qa('.td-dr-t')[0], 'userSelect');
    out.rvBody = r(q('.td-rv-body'));
    out.rvBodyUserSel = cs(q('.td-rv-body'), 'userSelect');
    out.r93Scroll = r(q('.r93-scroll'));
    /* 菜单现状 */
    var m = q('.td-mod-menu');
    out.menuRect = r(m);
    out.menuCls = m ? m.className : null;
    out.menuAnim = cs(m, 'animationName');
    out.menuTrans = cs(m, 'transitionProperty');
    out.menuTransDur = cs(m, 'transitionDuration');
    out.menuOpacity = cs(m, 'opacity');
    out.menuVis = cs(m, 'visibility');
    out.menuTranslate = cs(m, 'translate');
    out.menuScale = cs(m, 'scale');
    out.menuTfOrigin = cs(m, 'transformOrigin');
    out.menuInline = m ? [m.style.left || '', m.style.top || '', m.style.right || ''] : null;
    out.addBtn = r(q('[data-td-add]'));
    out.menuOffsetParent = m && m.offsetParent ? m.offsetParent.className : null;
  }

  /* ---- 把侧栏滑进视口后停住，等下一相位再采样 ---- */
  if (M === 'in') { out.browse2 = r(q('.td-browse')); out.browseCls2 = q('.td-browse').className; }

  /* ---- ② 逐帧采样：先采样 4 帧「关态」，第 5 帧点开，再采 36 帧 ---- */
  if (M === 'arm') {
    var mm = q('.td-mod-menu');
    var trg = q('[data-td-add]');
    var log = [];
    var n = 0;
    function samp(tag) {
      var c = getComputedStyle(mm);
      var bb = mm.getBoundingClientRect();
      log.push([n, tag,
        c.opacity, c.visibility, c.translate, c.scale,
        c.left, c.top,
        Math.round(bb.left * 100) / 100, Math.round(bb.top * 100) / 100,
        Math.round(bb.width * 100) / 100, Math.round(bb.height * 100) / 100,
        mm.style.left || '', mm.style.top || '',
        mm.hasAttribute('hidden') ? 0 : 1,
        /giencoder-popup-open/.test(mm.className) ? 1 : 0]);
    }
    window.__LOG = log;
    function tick() {
      var t0 = (n < 4) ? 'pre' : (n === 4 ? 'click' : 'post');
      if (n === 4 && trg) trg.click();
      samp(t0);
      n++;
      if (n < 40) requestAnimationFrame(tick);
      else window.__ARM = 1;
    }
    requestAnimationFrame(tick);
  }
  if (M === 'read') { out.arm = window.__ARM || 0; out.log = window.__LOG; }
  if (M === 'readClose') { out.log = window.__CLOSE || null; }

  /* ---- ②b 关态采样（看「闪一下就不见」是不是回落） ---- */
  if (M === 'armClose') {
    var m2 = q('.td-mod-menu'), t2 = q('[data-td-add]');
    var lg = []; var k = 0;
    window.__CLOSE = lg;
    function s2(tag) {
      var c = getComputedStyle(m2); var bb = m2.getBoundingClientRect();
      lg.push([k, tag, c.opacity, c.visibility, c.translate, c.scale,
        Math.round(bb.left * 100) / 100, Math.round(bb.top * 100) / 100,
        m2.hasAttribute('hidden') ? 0 : 1, /giencoder-popup-open/.test(m2.className) ? 1 : 0]);
    }
    function t2f() {
      if (k === 4 && t2) t2.click();          /* 先开 */
      if (k === 16 && t2) t2.click();         /* 再关 */
      s2(k < 4 ? 'pre' : (k < 16 ? 'open' : 'close'));
      k++;
      if (k < 34) requestAnimationFrame(t2f); else window.__ARM2 = 1;
    }
    requestAnimationFrame(t2f);
  }

  /* ---- ① 真实鼠标拖选之后：浮条在不在 ---- */
  if (M === 'selRead') {
    var sb = q('.td-selbar');
    out.selbarExists = !!sb;
    out.selbarHidden = sb ? sb.hasAttribute('hidden') : null;
    out.selbarRect = r(sb);
    out.selbarBtns = sb ? qa('.td-selbar button').map(function (b) { return b.textContent.trim(); }) : [];
    out.selText = String(window.getSelection()).slice(0, 80);
    out.selRangeCount = window.getSelection().rangeCount;
  }
  /* ---- ① 合成选区（不依赖真实拖选）——只用来验「守卫」这一层 ---- */
  if (M === 'synthSel') {
    var host = q('.td-rv-body');
    var t = null;
    var walker = document.createTreeWalker(host, NodeFilter.SHOW_TEXT, null);
    var node;
    while ((node = walker.nextNode())) { if (node.nodeValue && node.nodeValue.trim().length > 6) { t = node; break; } }
    if (t) {
      var rg = document.createRange();
      var st = Math.min(4, t.nodeValue.length - 1);
      rg.setStart(t, st); rg.setEnd(t, Math.min(st + 12, t.nodeValue.length));
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(rg);
      out.selected = String(s).trim();
      out.hostCls = t.parentElement ? t.parentElement.className : null;
      out.inBrowse = !!(t.parentElement && t.parentElement.closest('.td-browse'));
      var tg = t.parentElement;
      tg.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
      out.dispatched = 1;
    } else { out.err = 'no text node'; }
  }

  return out;
})();
