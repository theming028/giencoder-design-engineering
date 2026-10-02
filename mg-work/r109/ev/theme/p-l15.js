(function () {
  /* r109 第十五拍验收探针 —— 四条：
     ① 批注模块恢复（新版标记 + 结构 + 工具条文案）
     ② `.r93-todocard` 缩进归零
     ③ 「任务产物」卡可点开右栏浏览
     ④ 不同文件 → 独立页签
     另附：`td-page-blank` 已删、`.td-annot-bar` 贴顶。 */
  function q(s, r) { return (r || document).querySelector(s); }
  function qa(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function cs(el, p) { return el ? getComputedStyle(el).getPropertyValue(p) : null; }
  var out = {};

  /* ---------- ② .r93-todocard 缩进 ---------- */
  out.todocard = qa('.r93-todocard').map(function (el) {
    var r = el.getBoundingClientRect();
    var pr = el.parentElement.getBoundingClientRect();
    return {
      w: Math.round(r.width), pw: Math.round(pr.width),
      ml: cs(el, 'margin-left'), relX: Math.round(r.left - pr.left)
    };
  });

  /* ---------- 另：td-page-blank 已删 + 标注条贴顶 ---------- */
  out.blankInDom = !!q('.td-page-blank');
  out.blankCssRule = (function () {
    for (var i = 0; i < document.styleSheets.length; i++) {
      var ss = document.styleSheets[i], rs;
      try { rs = ss.cssRules; } catch (e) { continue; }
      if (!rs) continue;
      for (var j = 0; j < rs.length; j++) {
        if (rs[j].selectorText === '.td-page-blank') return rs[j].cssText;
      }
    }
    return null;
  })();
  var ab = q('.td-annot-bar');
  out.annotBar = ab ? { pos: cs(ab, 'position'), top: cs(ab, 'top'), bottom: cs(ab, 'bottom') } : null;

  /* ---------- ① 批注模块（新版） ---------- */
  out.brw = (function () {
    var brw = q('.td-brw');
    if (!brw) return null;
    var view = q('[data-td-view]', brw);
    return {
      hasView: !!view,
      annotBtnLabel: (function () { var b = q('.td-url-annot span', brw); return b ? b.textContent : null; })(),
      /* 新版结构 = 运行期由 JS 建的气泡；静态页面上此时应有 [hidden] 的 .td-elnote + 子件 */
      elnoteInDom: !!q('.td-elnote', brw),
      pin: !!q('.td-elnote-pin', brw),
      card: !!q('.td-elnote-card', brw),
      input: !!q('.td-elnote-input', brw),
      hint: !!q('.td-elnote-hint', brw),
      acts: !!q('.td-elnote-acts', brw),
      okBtn: !!q('[data-td-elnote-ok]', brw),
      cancelBtn: !!q('[data-td-elnote-cancel]', brw),
      oldTitle: !!q('.td-elnote-t', brw),
      oldFoot: !!q('.td-elnote-f', brw)
    };
  })();

  /* ---------- ③④ 页签 ---------- */
  out.arts = qa('.td-sum-art').map(function (el) {
    return {
      name: (q('.td-sum-artt b', el) || {}).textContent,
      hasArtAttr: el.hasAttribute('data-td-art'),
      cursor: cs(el, 'cursor')
    };
  });
  var tabs0 = qa('.td-browse-tabs [data-td-tab]').map(function (t) {
    return { mod: t.getAttribute('data-td-mod'), file: t.getAttribute('data-td-file'),
             name: (q('.td-tab-name', t) || {}).textContent,
             active: t.classList.contains('is-active') };
  });
  out.tabsBefore = tabs0;

  /* 真点一下产物卡 A（不派发 click 到按钮，直接点卡本身） */
  var artA = qa('.td-sum-art')[0], artB = qa('.td-sum-art')[1];
  function fireArt(el) {
    if (!el) return;
    var r = el.getBoundingClientRect();
    el.dispatchEvent(new MouseEvent('click', {
      bubbles: true, cancelable: true,
      clientX: Math.round(r.left + 4), clientY: Math.round(r.top + r.height / 2)
    }));
  }
  fireArt(artA);
  out.tabsAfterA = qa('.td-browse-tabs [data-td-tab]').map(function (t) {
    return { mod: t.getAttribute('data-td-mod'), file: t.getAttribute('data-td-file'),
             name: (q('.td-tab-name', t) || {}).textContent,
             active: t.classList.contains('is-active') };
  });
  out.paneAfterA = (function () {
    var p = q('#av-browse-pane-preview');
    if (!p) return null;
    return { hidden: p.hasAttribute('hidden'),
             name: (q('[data-td-prev-name]', p) || {}).textContent,
             meta: (q('[data-td-prev-meta]', p) || {}).textContent,
             kind: (function () {
               var b = qa('[data-td-prev-kind]', p).filter(function (x) { return !x.hasAttribute('hidden'); });
               return b.length ? b[0].getAttribute('data-td-prev-kind') : null;
             })() };
  })();

  fireArt(artB);
  out.tabsAfterB = qa('.td-browse-tabs [data-td-tab]').map(function (t) {
    return { mod: t.getAttribute('data-td-mod'), file: t.getAttribute('data-td-file'),
             name: (q('.td-tab-name', t) || {}).textContent,
             active: t.classList.contains('is-active') };
  });
  out.paneAfterB = (function () {
    var p = q('#av-browse-pane-preview');
    if (!p) return null;
    return { hidden: p.hasAttribute('hidden'),
             name: (q('[data-td-prev-name]', p) || {}).textContent,
             kind: (function () {
               var b = qa('[data-td-prev-kind]', p).filter(function (x) { return !x.hasAttribute('hidden'); });
               return b.length ? b[0].getAttribute('data-td-prev-kind') : null;
             })() };
  })();

  /* 点回 A 的页签 —— 内容应切回 A 自己的 */
  var tabA = qa('.td-browse-tabs [data-td-tab][data-td-file]').filter(function (t) {
    return t.getAttribute('data-td-file') === (artA ? q('.td-sum-artt b', artA).textContent : '');
  })[0];
  if (tabA) tabA.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  out.paneBackToA = (function () {
    var p = q('#av-browse-pane-preview');
    if (!p) return null;
    return { name: (q('[data-td-prev-name]', p) || {}).textContent,
             activeTab: (qa('.td-browse-tabs [data-td-tab].is-active').map(function (t) {
               return t.getAttribute('data-td-file') || t.getAttribute('data-td-mod');
             })) };
  })();

  /* ---------- ① 真开批注态：点工具条「标注」 ---------- */
  out.annotFlow = (function () {
    var brw = q('.td-brw'); if (!brw) return null;
    var btn = q('.td-url-annot', brw);
    var res = { clicked: !!btn };
    if (btn) btn.click();
    res.afterOn = {
      cls: brw.classList.contains('is-annotating'),
      barHidden: q('.td-annot-bar', brw) ? q('.td-annot-bar', brw).hasAttribute('hidden') : null,
      label: (q('.td-url-annot span', brw) || {}).textContent
    };
    /* 点页面里一个可批注元素 */
    var el = q('[data-td-el]', brw);
    if (el) {
      var r = el.getBoundingClientRect();
      el.dispatchEvent(new MouseEvent('click', {
        bubbles: true, cancelable: true,
        clientX: Math.round(r.left + 20), clientY: Math.round(r.top + 10)
      }));
    }
    var note = q('.td-elnote', brw);
    res.note = note ? {
      hidden: note.hasAttribute('hidden'),
      left: note.style.left, top: note.style.top,
      hasText: q('.td-elnote-card', note) ? q('.td-elnote-card', note).classList.contains('has-text') : null,
      okDisabled: q('[data-td-elnote-ok]', note) ? q('[data-td-elnote-ok]', note).disabled : null,
      okText: (q('[data-td-elnote-ok]', note) || {}).textContent
    } : null;
    res.clickPoint = el ? { x: Math.round(r.left + 20), y: Math.round(r.top + 10) } : null;
    return res;
  })();

  return JSON.stringify(out, null, 1);
})()
