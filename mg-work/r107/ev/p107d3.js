(function () {
  var pane = document.querySelector('.td-browse');
  var ctx = pane.querySelector('.td-ctxmenu');
  function shut() {
    document.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  }
  function fire(el, label) {
    if (!el) return { label: label, miss: true };
    el.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 980, clientY: 320 }));
    var r = {
      label: label,
      open: !ctx.hasAttribute('hidden'),
      cls: ctx.className,
      items: ctx.querySelectorAll('.td-ctx-item').length,
      seps: ctx.querySelectorAll('.td-mm-line').length,
      head: ctx.querySelector('.td-ctx-head') ? ctx.querySelector('.td-ctx-head').textContent : null,
      pos: [Math.round(ctx.getBoundingClientRect().x), Math.round(ctx.getBoundingClientRect().y)]
    };
    var first = ctx.querySelector('.td-ctx-item');
    if (first) { r.item0 = first.textContent.trim(); r.item0h = getComputedStyle(first).height; }
    shut();
    r.afterShut = ctx.hasAttribute('hidden');
    return r;
  }
  var out = {};
  out.tab = fire(pane.querySelector('.td-browse-tab'), '标签');
  out.file = fire(pane.querySelector('.td-diff-h'), '审查文件头');
  out.row = fire(pane.querySelector('.td-dr'), '审查代码行');
  out.term = fire(pane.querySelector('[data-td-term]'), '终端');
  out.brwEl = fire(pane.querySelector('[data-td-el]'), '浏览器元素');
  out.brwView = fire(pane.querySelector('.td-view'), '浏览器空白');
  out.src = fire(pane.querySelector('.td-sum-src'), '摘要来源');
  out.art = fire(pane.querySelector('.td-sum-art'), '摘要产物');
  out.plan = fire(pane.querySelector('.td-sum-plan li'), '计划条目');
  /* 反例：右栏内的普通空白（模块正文）应当**不接管**右键 */
  out.blank = fire(pane.querySelector('.td-sum-body'), '摘要空白');
  /* 反例：右栏外（主对话）也不接管 */
  var outside = document.querySelector('.r93-scroll');
  outside.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 300, clientY: 300 }));
  out.outsidePrevented = false;
  out.outsideOpen = !ctx.hasAttribute('hidden');
  shut();
  return JSON.stringify(out);
})()
