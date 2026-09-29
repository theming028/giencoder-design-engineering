(function () {
  /* ★ v3 交互链探针（纯程序化 click，不依赖鼠标 hover）：
       ① 点「删除会话」→ 该行进确认态
       ② 点「取消」→ 复原
       ③ 点 A 行删除、再点 B 行删除 → A 行自动复位（一次只允许一行）
       ④ 确认态下点行内其他地方 → 只是放弃，**不打开会话**
       ⑤ 点「确定删除」→ 行真的消失 + 轻提示（放在最后，因为会改 DOM）      */
  var out = {};
  var list = document.getElementById('av-hs-list');
  if (!list) return JSON.stringify({ err: 'no list' });
  var drawer = document.getElementById('av-chat-drawer');

  /* 开局先清干净（上一步的截图流程可能留下了确认态） */
  var cs0 = list.querySelectorAll('.av-hs-item.is-confirm');
  for (var z = 0; z < cs0.length; z++) cs0[z].classList.remove('is-confirm');

  var items = list.querySelectorAll('.av-hs-item');
  var r3 = items[2], r5 = items[4];

  /* ⚠ 行上有 `transition: background-color 120ms`：不掐掉的话 add 类之后立刻读
     拿到的是过渡第一帧 rgba(0,0,0,0)，不是终值。 */
  r3.style.transition = 'none';
  r5.style.transition = 'none';

  function d(el) { return el ? getComputedStyle(el).display : null; }
  function snap(it) {
    return {
      isConfirm: it.classList.contains('is-confirm'),
      acts: d(it.querySelector('.av-hs-acts')),
      confirm: d(it.querySelector('.av-hs-confirm')),
      bg: getComputedStyle(it).backgroundColor,
      nameW: Math.round(it.querySelector('.av-hs-name').getBoundingClientRect().width)
    };
  }
  function rel(el, host) {
    var a = el.getBoundingClientRect(), b = host.getBoundingClientRect();
    return [Math.round(a.left - b.left), Math.round(a.top - b.top), Math.round(a.width), Math.round(a.height)];
  }

  out["1_before"] = snap(r3);

  /* ① 点删除图标 */
  r3.querySelector('[data-av-hs-del]').click();
  out["2_afterClickDel"] = snap(r3);
  var cb = r3.querySelector('[data-av-hs-cancel]'), ok = r3.querySelector('[data-av-hs-ok]');
  out.cancelRect = rel(cb, r3);
  out.okRect = rel(ok, r3);
  out.gapBetween = Math.round(ok.getBoundingClientRect().left - cb.getBoundingClientRect().right);
  out.confirmRight = Math.round(r3.getBoundingClientRect().right - ok.getBoundingClientRect().right);
  out.cancelStyle = [
    getComputedStyle(cb).height, getComputedStyle(cb).paddingLeft, getComputedStyle(cb).fontSize,
    getComputedStyle(cb).backgroundColor, getComputedStyle(cb).borderTopColor, getComputedStyle(cb).borderRadius
  ];
  out.okStyle = [
    getComputedStyle(ok).height, getComputedStyle(ok).paddingLeft, getComputedStyle(ok).fontSize,
    getComputedStyle(ok).backgroundColor, getComputedStyle(ok).color, getComputedStyle(ok).borderRadius
  ];

  /* ② 取消 → 复原 */
  cb.click();
  out["3_afterCancel"] = snap(r3);

  /* ③ 一次只允许一行 */
  r3.querySelector('[data-av-hs-del]').click();
  out["4_reopened"] = snap(r3);
  r5.querySelector('[data-av-hs-del]').click();
  out["5_twoRows"] = { row3: snap(r3), row5: snap(r5) };

  /* ④ 确认态下点名字 → 只放弃，不打开会话（视图必须还开着） */
  r5.querySelector('.av-hs-name').click();
  out["6_afterClickNameInConfirm"] = snap(r5);
  out.viewStillOpen = drawer ? drawer.hasAttribute('data-av-hs') : null;

  /* ⑤ 确定删除（放最后，会移除 DOM） */
  var n0 = list.querySelectorAll('.av-hs-item').length;
  var nm = r3.querySelector('.av-hs-name').textContent;
  r3.querySelector('[data-av-hs-del]').click();
  r3.querySelector('[data-av-hs-ok]').click();
  var n1 = list.querySelectorAll('.av-hs-item').length;
  var box = document.querySelector('.td-dp-msg');
  out["7_afterOk"] = {
    rowsBefore: n0, rowsAfter: n1,
    removedName: nm.length > 18 ? nm.slice(0, 18) + '…' : nm,
    toastShown: box ? !box.hidden : false,
    toastText: box ? box.textContent.replace(/\s+/g, ' ').trim() : null
  };

  /* 复位（截图前） */
  r3.style.transition = ''; r5.style.transition = '';
  return JSON.stringify(out);
})()
