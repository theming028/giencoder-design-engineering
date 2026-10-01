(function () {
  var tg = document.querySelector('.r93-baract[data-r93-browse]');
  if (tg && !document.querySelector('.av-browse-on')) tg.click();
  return JSON.stringify({ clicked: !!tg, on: !!document.querySelector('.av-browse-on') });
})()
