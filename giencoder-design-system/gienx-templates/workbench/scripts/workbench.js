<script>
(function () {
  'use strict';
  /* 交互清单（零依赖原生 JS，动效统一走 Token）
     1. Header 胶囊 Tabs：互斥切换 + aria-selected
     2. Menu：菜单项互斥选中；disabled 无响应；分组标题 Msg 折叠（aria-expanded）
     3. Tree：switcher 展开/折叠 0.2s 过渡、节点互斥选中、↑↓→← / Enter 键盘导航
     4. Dropdown：点击开合、Esc 关闭、点击外部关闭
     5. Composer：Enter 发送 → 追加用户气泡 → Spin 等待态 → 追加助手回复 */

  /* ---- 1. Tabs capsule ---- */
  function syncTabLabels() {
    document.querySelectorAll('.giencoder-tabs-capsule .giencoder-tabs-tab').forEach(function (t) {
      var label = t.querySelector('.wb-tab-label');
      if (!label) { return; }
      var isActive = t.classList.contains('giencoder-tabs-tab-active');
      label.textContent = isActive ? (label.getAttribute('data-full') || '') : (label.getAttribute('data-short') || '');
    });
    // 定位滑动指示条到选中 tab
    var thumb = document.querySelector('.giencoder-tabs-capsule .giencoder-tabs-thumb');
    var activeTab = document.querySelector('.giencoder-tabs-capsule .giencoder-tabs-tab-active');
    if (thumb && activeTab) {
      thumb.style.width = activeTab.offsetWidth + 'px';
      thumb.style.transform = 'translateX(' + activeTab.offsetLeft + 'px)';
    }
  }
  document.querySelectorAll('.giencoder-tabs-capsule .giencoder-tabs-tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      tab.parentElement.querySelectorAll('.giencoder-tabs-tab').forEach(function (t) {
        t.classList.remove('giencoder-tabs-tab-active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('giencoder-tabs-tab-active');
      tab.setAttribute('aria-selected', 'true');
      syncTabLabels();
    });
  });
  syncTabLabels();


  /* ---- 2. Menu ---- */
  /* 全局单选：清空左侧所有菜单项与树节点的选中态 */
  function clearAllSelections() {
    document.querySelectorAll('.giencoder-menu-item-selected').forEach(function (n) {
      n.classList.remove('giencoder-menu-item-selected');
    });
    document.querySelectorAll('.giencoder-tree-node-selected').forEach(function (n) {
      n.classList.remove('giencoder-tree-node-selected');
      n.removeAttribute('aria-selected');
      n.setAttribute('tabindex', '-1');
    });
  }
  document.querySelectorAll('.giencoder-menu-item').forEach(function (item) {
    item.addEventListener('click', function () {
      if (item.classList.contains('giencoder-menu-item-disabled')) { return; }
      clearAllSelections();
      item.classList.add('giencoder-menu-item-selected');
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); item.click(); }
    });
  });
  document.querySelectorAll('.wb-dropdown-item').forEach(function (di) {
    di.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); di.click(); }
    });
  });
  document.querySelectorAll('.giencoder-menu-submenu-title').forEach(function (title) {
    var toggle = function () {
      if (title.querySelector('.giencoder-btn')) { /* 仅含操作按钮的标题仍可折叠 */ }
      var sub = title.closest('.giencoder-menu-submenu');
      var open = sub.classList.toggle('giencoder-menu-submenu-open');
      title.setAttribute('aria-expanded', String(open));
    };
    title.addEventListener('click', function (e) {
      if (e.target.closest('.giencoder-btn')) { e.stopPropagation(); return; }
      toggle();
    });
    title.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });

  /* ---- 3. Tree ---- */
  function visibleNodes() {
    return Array.prototype.slice.call(document.querySelectorAll('.giencoder-tree-node')).filter(function (n) {
      return n.offsetParent !== null;
    });
  }
  document.querySelectorAll('.giencoder-tree').forEach(function (tree) {
    tree.querySelectorAll('.giencoder-tree-node').forEach(function (node) {
      node.setAttribute('tabindex', node.getAttribute('aria-selected') === 'true' ? '0' : '-1');
      node.addEventListener('click', function (e) {
        if (node.classList.contains('giencoder-tree-node-disabled')) { return; }
        var hasChildren = node.hasAttribute('aria-expanded');
        var onAction = e.target.closest('.giencoder-tree-node-extra .giencoder-btn, .giencoder-tree-node-extra .wb-icon-btn, .giencoder-tree-node-extra button, [data-dropdown-toggle]');
        if (hasChildren && !onAction) {
          var expanded = node.classList.toggle('giencoder-tree-node-expanded');
          node.setAttribute('aria-expanded', String(expanded));
          return;
        }
        if (onAction) { return; }
        clearAllSelections();
        node.classList.add('giencoder-tree-node-selected');
        node.setAttribute('aria-selected', 'true');
        node.setAttribute('tabindex', '0');
      });
      node.addEventListener('keydown', function (e) {
        var nodes = visibleNodes();
        var idx = nodes.indexOf(node);
        if (e.key === 'ArrowDown' && idx < nodes.length - 1) { e.preventDefault(); nodes[idx + 1].focus(); }
        else if (e.key === 'ArrowUp' && idx > 0) { e.preventDefault(); nodes[idx - 1].focus(); }
        else if (e.key === 'ArrowRight' && node.hasAttribute('aria-expanded') && node.getAttribute('aria-expanded') === 'false') {
          e.preventDefault(); node.click();
        } else if (e.key === 'ArrowLeft' && node.hasAttribute('aria-expanded') && node.getAttribute('aria-expanded') === 'true') {
          e.preventDefault(); node.click();
        } else if (e.key === 'Enter') { e.preventDefault(); node.click(); }
      });
    });
  });

  /* ---- 4. Dropdown ---- */
  document.querySelectorAll('[data-dropdown-toggle]').forEach(function (btn) {
    var wrap = btn.closest('.wb-dropdown');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = wrap.classList.toggle('wb-dropdown-open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.wb-dropdown-open').forEach(function (d) { d.classList.remove('wb-dropdown-open'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.wb-dropdown-open').forEach(function (d) { d.classList.remove('wb-dropdown-open'); });
    }
  });

  /* ---- 5. Composer ---- */
  var input = document.getElementById('wbInput');
  var stream = document.getElementById('wbStream');
  var timeNow = function () {
    return new Date().toTimeString().slice(0, 5);
  };
  var appendUser = function (text) {
    var el = document.createElement('div');
    el.className = 'wb-msg wb-msg-user';
    el.innerHTML = '<span class="wb-avatar-me">邵</span><div class="wb-msg-body">' +
      '<div class="wb-msg-meta">你 · ' + timeNow() + '</div>' +
      '<div class="wb-bubble wb-bubble-user"></div></div>';
    el.querySelector('.wb-bubble').textContent = text;
    stream.appendChild(el);
    stream.scrollTop = stream.scrollHeight;
  };
  var appendAssistant = function (text) {
    var el = document.createElement('div');
    el.className = 'wb-msg';
    el.innerHTML = '<span class="wb-avatar-ai"><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><rect x="2.5" y="3.5" width="11" height="9" rx="2"/><path d="M2.5 7h11M6.5 3.5v9"/></svg></span>' +
      '<div class="wb-msg-body"><div class="wb-msg-meta">元启助理 · ' + timeNow() + '</div>' +
      '<div class="wb-bubble wb-bubble-assistant"></div></div>';
    el.querySelector('.wb-bubble').textContent = text;
    stream.appendChild(el);
    stream.scrollTop = stream.scrollHeight;
  };
  var appendThinking = function () {
    var el = document.createElement('div');
    el.className = 'wb-msg';
    el.id = 'wbThinking';
    el.innerHTML = '<span class="wb-avatar-ai"><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><rect x="2.5" y="3.5" width="11" height="9" rx="2"/><path d="M2.5 7h11M6.5 3.5v9"/></svg></span>' +
      '<div class="wb-msg-body"><div class="wb-msg-meta">元启助理 · 正在处理</div>' +
      '<div class="wb-bubble wb-bubble-assistant" style="display:inline-flex;align-items:center;gap:8px;">' +
      '<span class="giencoder-spin-loading giencoder-spin-loading-mini" role="status"></span><span>正在执行…</span></div></div>';
    stream.appendChild(el);
    stream.scrollTop = stream.scrollHeight;
  };
  var send = function () {
    var text = input.value.trim();
    if (!text) { return; }
    appendUser(text);
    input.value = '';
    appendThinking();
    setTimeout(function () {
      var thinking = document.getElementById('wbThinking');
      if (thinking) { thinking.remove(); }
      appendAssistant('已收到指令：「' + text + '」。当前为演示数据，实际执行需接入会话服务。');
    }, 1200);
  };
  if (document.getElementById('wbSend')) {
    document.getElementById('wbSend').addEventListener('click', send);
  }
  if (input) {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
    });
  }
})();
</script>