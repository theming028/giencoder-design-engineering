(function () {
  var sc = document.querySelector('.r93-scroll');
  var rl = document.querySelector('.r93-rateline');
  sc.scrollTop = rl.offsetTop - 200;
  return JSON.stringify({ scrollTop: sc.scrollTop, ratelineTop: rl.getBoundingClientRect().top });
})();
