(function () {
  /* 悬停 tooltip 探针：调用前必须已用 agent-browser `hover` 把鼠标停在
     `.av-hs-list .av-hs-item:nth-child(3) [data-av-hs-del]` 上。
     ★★ v3 的核心验收点：r84 首版（hover 整卡替换）下这枚图标会被 display:none，
        鼠标够不到 ⇒ tooltip 永远出不来；改成点击触发后必须能出来。 */
  var out = {};
  var del = document.querySelector('.av-hs-list .av-hs-item:nth-child(3) [data-av-hs-del]');
  var exp = document.querySelector('.av-hs-list .av-hs-item:nth-child(3) [data-av-hs-export]');
  var t = document.querySelector('.av-tip');

  out.delExists = !!del;
  out.delHovered = del ? del.matches(':hover') : null;
  out.delVisible = del ? getComputedStyle(del).display : null;
  out.expVisible = exp ? getComputedStyle(exp).display : null;

  out.tipExists = !!t;
  out.tipHidden = t ? t.hidden : null;
  out.tipText = t ? t.textContent : null;
  out.tipClass = t ? t.className : null;
  out.tipFont = t ? getComputedStyle(t).fontSize : null;
  out.tipPad = t ? [getComputedStyle(t).paddingTop, getComputedStyle(t).paddingLeft] : null;
  out.tipBg = t ? getComputedStyle(t).backgroundColor : null;
  out.tipColor = t ? getComputedStyle(t).color : null;
  out.tipRadius = t ? getComputedStyle(t).borderRadius : null;

  /* 间隙 + tooltip / 图标的绝对矩形（给裁剪截图用） */
  if (t && del) {
    var a = del.getBoundingClientRect(), b = t.getBoundingClientRect();
    out.tipGap = Math.round(a.top - b.bottom);
    out.delRect = [Math.round(a.left), Math.round(a.top), Math.round(a.width), Math.round(a.height)];
    out.tipRect = [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)];
  }
  var dr = document.getElementById('av-chat-drawer');
  if (dr) {
    var r = dr.getBoundingClientRect();
    out.drawerRect = [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)];
  }
  return JSON.stringify(out);
})()
