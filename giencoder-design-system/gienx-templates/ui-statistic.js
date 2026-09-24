/* ═══════════════════════════════════════════════════════════════
 * ui-kits 共享 Statistic 数值滚动动效交互
 * 来源：组件标准实现（giencoder/preview/component-statistic.html），
 *       与组件规范页行为一致，供模板页统计数值复用
 * 能力：
 *   1. 页面加载/刷新：所有 .giencoder-statistic-value 从 0 滚动到目标值
 *   2. 数值变化：window.giencoderStatistic.update(el, text) 从当前位滚到新值
 *   3. 重播入场：点击任意 [data-statistic-replay] 元素，本页所有
 *      .giencoder-statistic-value 从 0 重新滚动（如「刷新数据」按钮）
 * 依赖：ui-statistic.css + components.css
 * ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 渲染滚轮结构：数字位 .yd-digit（内部 0-9 垂直列）+ 静态字符 .yd-digit__sep
  function ensureDigits(el) {
    var raw = (el.getAttribute('data-value') || el.textContent || '').trim();
    el.setAttribute('data-value', raw);
    if (el.dataset.built === '1') return raw;
    el.innerHTML = '';
    Array.prototype.forEach.call(raw, function (ch) {
      if (/[0-9]/.test(ch)) {
        var wrap = document.createElement('span');
        wrap.className = 'yd-digit';
        wrap.dataset.cur = '0';
        var roll = document.createElement('span');
        roll.className = 'yd-digit__roll';
        for (var d = 0; d <= 9; d++) {
          var item = document.createElement('span');
          item.className = 'yd-digit__item';
          item.textContent = d;
          roll.appendChild(item);
        }
        wrap.appendChild(roll);
        el.appendChild(wrap);
      } else {
        var sep = document.createElement('span');
        sep.className = 'yd-digit__sep';
        sep.textContent = ch;
        el.appendChild(sep);
      }
    });
    el.dataset.built = '1';
    return raw;
  }

  // 布局兼容性：字符数相同且数字/静态字符位置一致 → 可原位滚动；否则重建（从 0 重滚）
  function sameLayout(a, b) {
    if (a.length !== b.length) return false;
    for (var i = 0; i < a.length; i++) {
      if ((/[0-9]/.test(a[i])) !== (/[0-9]/.test(b[i]))) return false;
    }
    return true;
  }

  // 滚动到目标值：先停帧在当前位（旧值），再过渡到目标位（新值）→ 刷新=从0滚、更新=从旧位滚
  function rollValue(el, targetText) {
    var raw = ensureDigits(el);
    if (!sameLayout(raw, targetText)) {
      el.dataset.built = '';
      el.setAttribute('data-value', targetText); // 重建前先指向目标值，确保渲染出新布局
      raw = ensureDigits(el);
    }
    el.setAttribute('data-value', targetText);

    var digits = el.querySelectorAll('.yd-digit');
    var targets = [], cur = [], ti = 0;
    Array.prototype.forEach.call(targetText, function (ch) {
      if (/[0-9]/.test(ch)) {
        targets.push(parseInt(ch, 10));
        cur.push(parseInt(digits[ti].dataset.cur, 10));
        ti++;
      }
    });

    var n = digits.length;
    for (var i = 0; i < n; i++) {           // 停帧到旧位
      var roll = digits[i].querySelector('.yd-digit__roll');
      roll.style.transition = 'none';
      roll.style.transitionDelay = '0ms';
      roll.style.transform = 'translateY(' + (-cur[i]) + 'em)';
    }
    void el.offsetWidth;                    // reflow 确保停帧生效
    requestAnimationFrame(function () {     // 下一帧开始过渡（错峰波浪）
      requestAnimationFrame(function () {
        for (var j = 0; j < n; j++) {
          var r = digits[j].querySelector('.yd-digit__roll');
          r.style.transition = reduceMotion ? 'none' : '';
          r.style.transitionDelay = (j * 45) + 'ms';
          r.style.transform = 'translateY(' + (-targets[j]) + 'em)';
          digits[j].dataset.cur = String(targets[j]);
        }
      });
    });
  }

  // 页面加载/刷新：所有 value 从 0 滚动到目标值
  document.querySelectorAll('.giencoder-statistic-value').forEach(function (el) {
    rollValue(el, (el.getAttribute('data-value') || el.textContent || '').trim());
  });

  // 对外更新接口：数字发生变化时调用，从当前位滚动到新值
  window.giencoderStatistic = {
    update: function (el, text) { rollValue(el, String(text)); },
    // 重播入场动效：从 0 重新滚动到当前目标值（用于「刷新数据」等场景）
    replay: function (el) {
      var text = el.getAttribute('data-value') || el.textContent || '';
      el.dataset.built = '';
      rollValue(el, text.trim());
    }
  };

  // 通用绑定：点击 [data-statistic-replay]，本页所有统计值从 0 重滚
  document.querySelectorAll('[data-statistic-replay]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.giencoder-statistic-value').forEach(function (el) {
        window.giencoderStatistic.replay(el);
      });
    });
  });
})();
