(function () {
  /* 默认态探针：进入「会话历史」后、未做任何 hover/点击时读一次。
     ★ v3 关键判据：图标组必须**可见**（display:flex）—— 这是"点击触发"换来的东西。 */
  var out = {};
  var v = document.getElementById('av-hs');
  var list = document.getElementById('av-hs-list');
  if (!v || !list) return JSON.stringify({ err: 'no view' });

  function cs(el, p) {
    if (!el) return null;
    var s = getComputedStyle(el), o = [];
    for (var i = 0; i < p.length; i++) o.push(s[p[i]]);
    return o;
  }

  var items = list.querySelectorAll('.av-hs-item');
  out.rows = items.length;

  /* 任选一行（第 3 行，与设计稿对照位对齐） */
  var it = items[2];
  var acts = it.querySelector('.av-hs-acts');
  var cf = it.querySelector('.av-hs-confirm');
  var del = it.querySelector('[data-av-hs-del]');
  var exp = it.querySelector('[data-av-hs-export]');

  out.actsDisplay = cs(acts, ['display']);      /* 期望 flex */
  out.confirmDisplay = cs(cf, ['display']);     /* 期望 none */
  out.rowBgDefault = cs(it, ['backgroundColor']);/* 期望 rgba(0,0,0,0) */
  out.nameW = Math.round(it.querySelector('.av-hs-name').getBoundingClientRect().width);

  out.delVisible = del ? getComputedStyle(del).display : null;   /* 期望 flex */
  out.expVisible = exp ? getComputedStyle(exp).display : null;   /* 期望 flex */
  out.delTip = del ? del.getAttribute('data-av-tip') : null;
  out.expTip = exp ? exp.getAttribute('data-av-tip') : null;

  /* 需求 4：第一张卡默认白底（ar: 语义类 is-on 保留，但不着色） */
  out.firstRowBg = cs(items[0], ['backgroundColor']);
  out.firstRowHasIsOn = items[0].classList.contains('is-on');

  /* 默认不该有任何行处于确认态 */
  out.isConfirmCount = list.querySelectorAll('.av-hs-item.is-confirm').length;

  /* tooltip 空闲态：必须不存在（r84 修掉的"凭空弹出"回归位） */
  var t = document.querySelector('.av-tip');
  out.tipExistsIdle = !!t;
  out.tipHiddenIdle = t ? t.hidden : null;

  return JSON.stringify(out);
})()
