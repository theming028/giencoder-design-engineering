/* r109 第十二拍 · 四条真机取证
   ① .r93-bar 背景色（浅/暗两档，含 backdrop-filter）
   ② .r93-att 附件卡可点链路
   ③ .r93-card--ctx 内间距
   ④ .zd-sec-h 整行点击折展（含右侧 .zd-sec-x 死区是否已通）
   输出：JSON（由 scan-l12.sh 落到 raw/l12/*.json） */
(function () {
  var r = {};
  function cs(el, p) { return el ? getComputedStyle(el)[p] : null; }

  /* ---- ① 标题栏 ---- */
  var bar = document.querySelector('.r93-bar');
  r.bar = {
    exist: !!bar,
    bg: cs(bar, 'backgroundColor'),
    bf: cs(bar, 'backdropFilter') || cs(bar, 'webkitBackdropFilter'),
    h: bar ? bar.getBoundingClientRect().height : null
  };

  /* ---- ③ 上下文卡内距 ---- */
  var ctx = document.querySelector('.r93-card--ctx');
  r.ctx = {
    exist: !!ctx,
    pad: cs(ctx, 'padding'),
    padT: cs(ctx, 'paddingTop'),
    minH: cs(ctx, 'minHeight'),
    maxH: cs(ctx, 'maxHeight')
  };

  /* ---- ② 附件卡 ---- */
  var atts = [].slice.call(document.querySelectorAll('.r93-att[data-r93-att-file]'));
  r.att = atts.map(function (el) {
    var b = el.getBoundingClientRect();
    return {
      file: el.getAttribute('data-r93-att-file'),
      role: el.getAttribute('role'),
      tabindex: el.getAttribute('tabindex'),
      cursor: cs(el, 'cursor'),
      borderColor: cs(el, 'borderTopColor'),
      w: Math.round(b.width), h: Math.round(b.height)
    };
  });
  r.attCount = atts.length;

  /* ---- ④ 分区整行可点 ---- */
  var secs = [].slice.call(document.querySelectorAll('[data-zd-sec]'));
  r.secs = secs.map(function (s) {
    var h = s.querySelector('.zd-sec-h');
    var x = s.querySelector('.zd-sec-x');
    var hb = h ? h.getBoundingClientRect() : null;
    var tb = h && h.querySelector('.zd-sec-t') ? h.querySelector('.zd-sec-t').getBoundingClientRect() : null;
    return {
      key: s.getAttribute('data-zd-sec'),
      closed: s.classList.contains('is-closed'),
      cursor: cs(h, 'cursor'),
      rowW: hb ? Math.round(hb.width) : null,
      titleW: tb ? Math.round(tb.width) : null,
      deadRightPx: (hb && tb) ? Math.round(hb.width - tb.width) : null
    };
  });

  /* ---- 动作：点右侧死区，看是否折起来 ---- */
  window.__l12 = {
    /* 点第 i 个分区的**右侧空白**（死区），返回该分区之前/之后的 closed 态 */
    tapRight: function (i) {
      var s = secs[i]; if (!s) return 'no-sec';
      var h = s.querySelector('.zd-sec-h');
      var b = h.getBoundingClientRect();
      var before = s.classList.contains('is-closed');
      /* 点在行右缘往内 6px（一定落在 .zd-sec-x 上，不在标题按钮上） */
      var ev = new MouseEvent('click', {
        bubbles: true, cancelable: true, view: window,
        clientX: b.right - 6, clientY: b.top + b.height / 2
      });
      var target = document.elementFromPoint(b.right - 6, b.top + b.height / 2);
      (target || h).dispatchEvent(ev);
      return { key: s.getAttribute('data-zd-sec'), before: before,
               after: s.classList.contains('is-closed'),
               hit: target ? (target.className || target.tagName) : null };
    },
    /* 点标题按钮本身，检查是否只 toggle 一次（不是被行重复处理两次而"没反应"） */
    tapTitle: function (i) {
      var s = secs[i]; if (!s) return 'no-sec';
      var t = s.querySelector('.zd-sec-t');
      var before = s.classList.contains('is-closed');
      t.click();
      return { key: s.getAttribute('data-zd-sec'), before: before,
               after: s.classList.contains('is-closed') };
    },
    /* 点附件卡，驱动右栏预览 */
    tapAtt: function (i) {
      var el = atts[i]; if (!el) return 'no-att';
      el.click();
      return el.getAttribute('data-r93-att-file');
    },
    /* 读右栏预览页签状态 */
    prev: function () {
      var p = document.querySelector('#av-browse-pane-preview');
      var t = document.querySelector('[data-td-tab][data-td-mod="preview"]');
      var body = p ? p.querySelector('[data-td-prev-kind]:not([hidden])') : null;
      return {
        paneHidden: p ? p.hasAttribute('hidden') : null,
        tabName: t && t.querySelector('.td-tab-name') ? t.querySelector('.td-tab-name').textContent : null,
        tabExist: !!t,
        name: p && p.querySelector('[data-td-prev-name]') ? p.querySelector('[data-td-prev-name]').textContent : null,
        meta: p && p.querySelector('[data-td-prev-meta]') ? p.querySelector('[data-td-prev-meta]').textContent : null,
        kind: body ? body.getAttribute('data-td-prev-kind') : null,
        browseOn: (function () {
          var s = document.getElementById('av-browse-slot');
          return s && s.parentElement ? s.parentElement.classList.contains('av-browse-on') : null;
        })()
      };
    }
  };
  return JSON.stringify(r);
})();
