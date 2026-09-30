(function () {
  var g = document.querySelector('.r93-seg');
  var sl = g.querySelector('.giencoder-radio-button-slider');
  var on = g.querySelector('.giencoder-radio-button-checked');
  var lb = g.querySelectorAll('[data-r93-tab]');
  var out = {
    label0: lb[0].offsetWidth, label1: lb[1].offsetWidth,
    lb1left: lb[1].offsetLeft,
    sliderW: sl.offsetWidth, sliderTX: getComputedStyle(sl).transform,
    checkedIs: on.getAttribute('data-r93-tab')
  };
  return JSON.stringify(out);
})()
