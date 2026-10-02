(function () {
  /* 测试台：把拖动标记复位（`_tdMoved` 是内部实现细节，真机上由「拖过 ⇒ 下一次 click 被吃掉」驱动）。
     只在探针里用，页面代码零依赖。 */
  var a = document.querySelector('.td-anchor');
  var before = a ? a._tdMoved : null;
  if (a) a._tdMoved = false;
  return 'reset _tdMoved: ' + before + ' -> ' + (a ? a._tdMoved : null);
})()
