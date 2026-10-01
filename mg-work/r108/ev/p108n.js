(function () {
  var M = window.__M;
  var r = { phase: M };
  function R(e) { if (!e) return null; var b = e.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; }
  function S(e) { return e ? getComputedStyle(e) : null; }

  if (M === 'fix') {
    /* ② 标题图标应已删净 */
    var hs = document.querySelectorAll('.td-sum-h');
    r.sumHCount = hs.length;
    r.sumHSvg = document.querySelectorAll('.td-sum-h svg').length;
    r.sumHText = [].map.call(hs, function (h) { return h.textContent.trim(); });
    /* ③ diff 折叠图标：正文色 + 13px */
    var cv = document.querySelector('.td-diff-cv');
    var c = S(cv);
    r.diffCv = c ? { color: c.color, w: c.width, h: c.height, rect: R(cv) } : null;
    /* ① 摘要卡基态边框 */
    var sec = document.querySelector('.td-sum-sec');
    r.sumSecBorder = sec ? S(sec).borderTopColor : null;
    r.sumSecRect = R(sec);
    /* ④ 产物卡：data 应在卡片上、按钮上应没有；卡片 cursor 应为 pointer */
    var art = document.querySelector('.td-sum-art');
    r.artHasData = art ? art.hasAttribute('data-td-art') : null;
    r.artCursor = art ? S(art).cursor : null;
    r.artRect = R(art);
    var btn = art ? art.querySelector('.td-diff-btn') : null;
    r.artBtnHasData = btn ? btn.hasAttribute('data-td-art') : null;
    r.artBtnRect = R(btn);
  }

  if (M === 'hover0' || M === 'hover1') {
    var s2 = document.querySelector('.td-sum-sec');
    r.secBorder = s2 ? S(s2).borderTopColor : null;
    r.secHover = s2 ? s2.matches(':hover') : null;
    r.secRect = R(s2);
  }

  if (M === 'art') {
    var pv = document.querySelector('[data-td-prev]');
    r.pvHidden = pv ? pv.hasAttribute('hidden') : null;
    r.pvRect = R(pv);
    var nm = pv ? pv.querySelector('[data-td-prev-name]') : null;
    r.pvName = nm ? nm.textContent : null;
    var mt = pv ? pv.querySelector('[data-td-prev-meta]') : null;
    r.pvMeta = mt ? mt.textContent : null;
    var bd = pv ? pv.querySelector('[data-td-prev-kind]:not([hidden])') : null;
    r.pvKind = bd ? bd.getAttribute('data-td-prev-kind') : null;
  }

  if (M === 'zd0') {
    var host = document.getElementById('av-zd-status');
    var main = document.querySelector('main');
    r.hostInMain = !!(host && main && host.parentNode === main);
    r.mainRect = R(main);
    r.hostRect = R(host);
    r.hostPE = host ? S(host).pointerEvents : null;
    var card = host ? host.querySelector('[data-zd-card]') : null;
    var c2 = S(card);
    r.cardRect = R(card);
    r.card = c2 ? { border: c2.borderTopColor, radius: c2.borderTopLeftRadius, bg: c2.backgroundColor, maxH: c2.maxHeight, w: c2.width, pe: c2.pointerEvents } : null;
    r.secs = host ? host.querySelectorAll('[data-zd-sec]').length : 0;
    r.secTitles = host ? [].map.call(host.querySelectorAll('.zd-sec-t'), function (t) { return t.textContent.trim(); }) : [];
    r.secX = host ? [].map.call(host.querySelectorAll('.zd-sec-x'), function (t) { return t.textContent.trim(); }) : [];
    r.rows = host ? [].map.call(host.querySelectorAll('.zd-row'), function (w) { return w.textContent.replace(/\s+/g, ' ').trim(); }) : [];
    r.its = host ? [].map.call(host.querySelectorAll('.zd-it'), function (w) { return w.textContent.replace(/\s+/g, ' ').trim(); }) : [];
    r.todoAll = host ? host.querySelectorAll('.zd-todo li').length : 0;
    r.todoDone = host ? host.querySelectorAll('.zd-todo li.is-done').length : 0;
    r.todoDoing = host ? host.querySelectorAll('.zd-todo li.is-doing').length : 0;
    var mini = host ? host.querySelector('[data-zd-mini]') : null;
    r.miniHidden = mini ? mini.hasAttribute('hidden') : null;
    var b0 = host ? host.querySelector('.zd-sec .zd-sec-b') : null;
    r.secBodyDisplay = b0 ? S(b0).display : null;
    /* 与顶栏/右栏的关系：面板应整体落在 main 内（不越界） */
    r.panelRightGap = (host && main) ? (R(main)[0] + R(main)[2]) - (R(card)[0] + R(card)[2]) : null;
    r.panelTopGap = (host && main) ? R(card)[1] - R(main)[1] : null;
  }

  if (M === 'zd1') {
    var s3 = document.querySelector('[data-zd-sec="git"]');
    r.closed = s3 ? s3.classList.contains('is-closed') : null;
    var b3 = s3 ? s3.querySelector('.zd-sec-b') : null;
    r.bodyDisplay = b3 ? S(b3).display : null;
    var t3 = s3 ? s3.querySelector('.zd-sec-t') : null;
    r.aria = t3 ? t3.getAttribute('aria-expanded') : null;
    r.cardRect = R(document.querySelector('[data-zd-card]'));
  }

  if (M === 'zd2') {
    var card2 = document.querySelector('[data-zd-card]');
    var mini2 = document.querySelector('[data-zd-mini]');
    r.cardHidden = card2 ? card2.hasAttribute('hidden') : null;
    r.cardDisplay = card2 ? S(card2).display : null;
    r.miniHidden = mini2 ? mini2.hasAttribute('hidden') : null;
    r.miniDisplay = mini2 ? S(mini2).display : null;
    r.miniRect = R(mini2);
    r.miniText = mini2 ? mini2.textContent.replace(/\s+/g, ' ').trim() : null;
    r.cardBodyDisplay = card2 && card2.querySelector('.zd-body') ? S(card2.querySelector('.zd-body')).display : null;
  }

  return JSON.stringify(r);
})()
