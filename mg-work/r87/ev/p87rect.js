(function () {
  function R(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.right), Math.round(b.bottom)]; }
  function rowByText(t) {
    var rows = [].slice.call(document.querySelectorAll('.r85-row'));
    for (var i = 0; i < rows.length; i++) {
      var s = rows[i].querySelector('.r85-t');
      if (s && s.textContent.trim() === t) return R(rows[i]);
    }
    return null;
  }
  var out = {
    viewport: [innerWidth, innerHeight],
    page: R(document.querySelector('.r85-page')),
    aside: R(document.querySelector('aside')),
    navCur: R(document.querySelector('.r85-navi[aria-current="true"]')),
    rows: {
      'Agent 预设': rowByText('Agent 预设'),
      '权限': rowByText('权限'),
      '语言': rowByText('语言'),
      '字号': rowByText('字号'),
      '外观': rowByText('外观'),
      '版本更新': rowByText('版本更新'),
      '账号': rowByText('账号')
    },
    r85ctl0: R(document.querySelector('.r85-ctl > .giencoder-select')),
    seg0: R(document.querySelector('.r85-seg > button')),
    slider: R(document.querySelector('.r85-slider')),
    btnLog: R((function () { var b = [].slice.call(document.querySelectorAll('.r85-btn')); return b[0]; })()),
    btnOut: R((function () { var b = [].slice.call(document.querySelectorAll('.r85-btn')); return b[b.length - 1]; })())
  };
  return JSON.stringify(out, null, 1);
})()
