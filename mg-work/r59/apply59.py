# -*- coding: utf-8 -*-
"""
★ 第 59 轮：任务详情页标题栏「更多操作」按钮 → 下方下拉菜单

需求：任务详情页标题栏的「更多操作」按钮被点击后，在下方显示下拉菜单。
设计稿：MasterGo 966:35630（dropdown-menu，page 622:13589）

设计稿 2× 截图逐像素量测（外框 130×76 = 内容 128×74 + 1px 描边）：
  面板   内距 4 / 项间距 2 / 圆角 5（外角实测 9~10px @2×）/ 描边 1px #E5E5E5
  菜单项 120×32 / 内距 0 8px / 图标-文字 8 / 圆角 4（实测 7px @2×）/ 文字 14px #1F1F1F
  图标   16px 框（24 viewBox + stroke 2.2 ⇒ 视觉笔画 1.47px、墨迹 ≈14px）#1F1F1F
  条目   终止任务（圆圈+实心方块）/ 取消任务（圆圈+叉）
  hover  视觉稿为 fill-1(#F7F7F7)；本页取 fill-2(#F2F2F2)——与 DS 契约 dropdown.json
         「hover 背景 --color-fill-2」一致，也与第 57 轮用户明确要求的「深一级」一致。

改动：
  ① DOM：给「更多操作」按钮补 aria-haspopup / aria-expanded / aria-controls / data-td-more
  ② CSS：新增 .td-more 弹层样式块（双类提权压过外壳自带的 .giencoder-dropdown-popup）
  ③ JS：新增 bindMoreMenu()（构建 / 定位 / 开合 / 键盘 / 关闭途径）
  ④ inject() 里注册 bindMoreMenu()

幂等：先判 mark（第 59 轮标记 / data-td-more），再判 OLD；命中数不符即 FAIL。
"""
import io, sys

P = 'pages/task-detail.html'

TAG_CHANGES = []      # (old, new) 列表，用于「增量 == 预期增量」的自检
def sub1(s, label, old, new, mark, expect=1):
    if mark and mark in s:
        print('   [SKIP] %s（已含标记）' % label)
        return s, True
    n = s.count(old)
    if n != expect:
        print('   [!!FAIL] %s：OLD 命中 %d 次（期望 %d）' % (label, n, expect))
        return s, False
    TAG_CHANGES.append((old, new))
    s = s.replace(old, new)
    print('   [OK]   %s（替换 %d 处）' % (label, n))
    return s, True

ok = True
s = io.open(P, encoding='utf-8').read()
before_len = len(s)
TOKENS = ['<style>', '</style>', '<script>', '</script>',
          'class=\\"td-bf is-file', '.td-sec-head', 'td-browse-files',
          'giencoder-dropdown-item', 'giencoder-popup-open', 'tdToast',
          'data-td-browse-toggle', 'aria-label=\\"更多操作\\"',
          '.td-ctx.giencoder-dropdown-popup', 'var LEFT_KEEP_MIN = 480',
          'function bindBrowseContextMenu()', 'function bindEditTask()',
          '.td-ctx .giencoder-dropdown-item {', 'td-dp-msg']
BEFORE = {t: s.count(t) for t in TOKENS}

# ================================================================ ① DOM
OLD_DOM = 'aria-label=\\"更多操作\\">",'
NEW_DOM = ('aria-label=\\"更多操作\\" aria-haspopup=\\"menu\\" aria-expanded=\\"false\\" '
           'aria-controls=\\"td-more-menu\\" data-td-more=\\"1\\">",')
s, r = sub1(s, 'DOM: 更多操作按钮补 aria / data-td-more', OLD_DOM, NEW_DOM, 'data-td-more')
ok &= r

# ================================================================ ② CSS
OLD_CSS = "      .td-ctx .giencoder-dropdown-arrow svg { display: block; width: 14px; height: 14px; }\n"
NEW_CSS = OLD_CSS + '''      /* ================= 第 59 轮：标题栏「更多操作」下拉菜单 =================
         设计稿：节点 966:35630（MasterGo dropdown-menu）。
         2× 截图逐像素量测（外框 130×76 = 内容 128×74 + 1px 描边）：
           面板   内距 4 / 项间距 2 / 圆角 5（外角实测 9~10px @2×）/ 描边 1px #E5E5E5
           菜单项 120×32 / 内距 0 8px / 图标-文字 8 / 圆角 4（实测 7px @2×）/ 文字 14px #1F1F1F
           图标   16px 框（24 viewBox + stroke 2.2 ⇒ 视觉笔画 1.47px、墨迹 ≈14px）
           hover  视觉稿是 fill-1(#F7F7F7)；本页统一取 fill-2(#F2F2F2)——与 DS 契约
                  dropdown.json「hover 背景 --color-fill-2」一致，也与第 57 轮用户
                  明确要求的「hover 深一级」一致（与右键菜单同值）。
         ⚠️ 与 r54 同一个坑：本页产物里已有一条同名 .giencoder-dropdown-popup
            （外壳 React 组件样式：transform-origin:top / min-width:168 / padding:6 /
            animation 播完 opacity 会回落到 0）→ 必须双类提权 + 显式 animation:none。 */
      .td-more.giencoder-dropdown-popup {
        position: fixed; z-index: var(--z-index-popup);
        box-sizing: border-box; min-width: 0; width: 130px; padding: 4px;
        display: flex; flex-direction: column; gap: 2px;
        background: var(--color-bg-popup);
        border: 1px solid var(--color-border-2);
        border-radius: 5px;
        box-shadow: var(--shadow3-down);
        transform-origin: top left;
        animation: none;
        opacity: 0; visibility: hidden; translate: 0 4px; scale: 0.96;
        transition: opacity .15s cubic-bezier(0.34, 0.69, 0.1, 1),
                    translate .15s cubic-bezier(0.34, 0.69, 0.1, 1),
                    scale .15s cubic-bezier(0.34, 0.69, 0.1, 1),
                    visibility 0s .15s;
      }
      .td-more.giencoder-dropdown-popup.giencoder-popup-open {
        opacity: 1; visibility: visible; translate: 0 0; scale: 1;
        transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1),
                    translate .2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
                    scale .2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
                    visibility 0s;
      }
      .td-more .giencoder-dropdown-item {
        display: flex; align-items: center; gap: 8px; height: 32px; box-sizing: border-box;
        padding: 0 8px; border-radius: 4px;
        font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-1);
        white-space: nowrap; cursor: pointer; user-select: none; outline: none;
        transition: background 120ms var(--transition-timing-function-standard, ease);
      }
      /* 与 r54 右键菜单、r57 定稿同档：hover 底 --color-fill-2（非 fill-1） */
      .td-more .giencoder-dropdown-item:hover,
      .td-more .giencoder-dropdown-item.is-hover { background: var(--color-fill-2); }
      .td-more-ico {
        flex: none; width: 16px; height: 16px; display: inline-flex;
        align-items: center; justify-content: center; color: var(--color-text-1);
      }
      .td-more-ico svg { display: block; width: 16px; height: 16px; }
      .td-more-label { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; }
'''
s, r = sub1(s, 'CSS: 新增 .td-more 下拉菜单样式块', OLD_CSS, NEW_CSS, '.td-more.giencoder-dropdown-popup {')
ok &= r

# ================================================================ ③ JS
OLD_JS = '  function bindEditTask() {\n'
NEW_JS = '''  /* ★ 第 59 轮：标题栏「更多操作」按钮 → 下方下拉菜单
     设计稿：MasterGo 966:35630（dropdown-menu），量测数据见上方 .td-more 样式块注释。
     结构按 DS Dropdown 契约（components/dropdown.json，trigger=click 变体）组装：
       div.giencoder-dropdown-popup.td-more[role=menu]
         └ div.giencoder-dropdown-item[role=menuitem] > span.td-more-ico + span.td-more-label
     开合状态类复用 .giencoder-popup-open（与 r54 右键菜单 / Select / Popover 同一套参数）。
     关闭途径：选中任一项 / 点菜单外 / 右键 / 页面滚轮 / 窗口缩放或失焦 / Esc
              （Esc 走页尾 Esc 链：html 根上的 data-td-pop-open → td:close-popovers）。
     键盘（契约 keyboard 清单）：↑↓ 移动虚拟焦点 · Enter 选中 · Esc 关闭并归还焦点到触发器。 */
  function bindMoreMenu() {
    var btn = document.querySelector('[data-td-more]');
    if (!btn || btn.getAttribute('data-td-more-bound') === '1') return;
    btn.setAttribute('data-td-more-bound', '1');
    if (!btn.getAttribute('title')) btn.setAttribute('title', '更多操作');

    var ICONS = {
      /* 终止任务：圆圈 + 实心方块。24 viewBox + stroke 2.2 落在 16px 框里
         ⇒ 视觉笔画 1.47px、外圈墨迹 ≈14px，与设计稿 2× 量测（笔画 ≈1.5、墨迹 28px@2×）吻合。 */
      stop: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.4"/><rect x="8.25" y="8.25" width="7.5" height="7.5" rx="0.6" fill="currentColor" stroke="none"/></svg>',
      /* 取消任务：圆圈 + 叉（设计稿叉臂实测 ≈6px ⇒ 24 viewBox 里 ±4.2） */
      cancel: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.4"/><path d="M7.8 7.8 16.2 16.2"/><path d="M16.2 7.8 7.8 16.2"/></svg>'
    };
    var ITEMS = [
      { id: 'stop',   label: '终止任务', svg: ICONS.stop },
      { id: 'cancel', label: '取消任务', svg: ICONS.cancel }
    ];

    var menu = null, rows = [], open = false, cur = -1;

    function build() {
      var box = document.createElement('div');
      box.className = 'giencoder-dropdown-popup td-more';
      box.id = 'td-more-menu';
      box.setAttribute('role', 'menu');
      ITEMS.forEach(function (it) {
        var row = document.createElement('div');
        row.className = 'giencoder-dropdown-item';
        row.setAttribute('role', 'menuitem');
        row.setAttribute('tabindex', '-1');
        row.setAttribute('data-more-id', it.id);
        row.innerHTML = '<span class="td-more-ico" aria-hidden="true">' + it.svg + '</span>' +
                        '<span class="td-more-label"></span>';
        row.querySelector('.td-more-label').textContent = it.label;
        box.appendChild(row);
      });
      return box;
    }

    function ensure() {
      if (menu) return;
      menu = build();
      menu.style.display = 'none';
      document.body.appendChild(menu);
      rows = Array.prototype.slice.call(menu.querySelectorAll('.giencoder-dropdown-item'));
      menu.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
      menu.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.giencoder-dropdown-item') : null;
        if (row) run(row.getAttribute('data-more-id'));
      });
    }

    /* 契约：弹层贴在触发器下方 4px，左对齐；越界向另一侧翻 */
    function place() {
      var r = btn.getBoundingClientRect();
      menu.style.display = 'flex';
      menu.style.visibility = 'hidden';
      var w = menu.offsetWidth, h = menu.offsetHeight;
      var left = r.left, top = r.bottom + 4;
      if (left + w > window.innerWidth - 8) left = Math.max(8, window.innerWidth - 8 - w);
      if (top + h > window.innerHeight - 8) top = Math.max(8, r.top - 4 - h);
      menu.style.left = Math.round(left) + 'px';
      menu.style.top = Math.round(top) + 'px';
      menu.style.visibility = '';
    }

    function flag(on) { document.documentElement.toggleAttribute('data-td-pop-open', on); }

    function show() {
      ensure();
      /* 与同页其它弹层互斥：先派发关闭信号（此刻 open 仍为 false，本监听会自行让位） */
      document.dispatchEvent(new CustomEvent('td:close-ctx'));
      document.dispatchEvent(new CustomEvent('td:close-popovers'));
      place();
      void menu.offsetHeight;                 /* 强制回流，让开合过渡生效 */
      menu.classList.add('giencoder-popup-open');
      open = true; cur = -1;
      rows.forEach(function (r) { r.classList.remove('is-hover'); });
      btn.setAttribute('aria-expanded', 'true');
      flag(true);
    }

    function close() {
      if (!open) return;
      open = false; cur = -1;
      menu.classList.remove('giencoder-popup-open');
      rows.forEach(function (r) { r.classList.remove('is-hover'); });
      btn.setAttribute('aria-expanded', 'false');
      setTimeout(function () { if (!open && menu) menu.style.display = 'none'; }, 200);
      flag(false);
    }

    function focusRow(i) {
      if (!rows.length) return;
      cur = (i + rows.length) % rows.length;
      rows.forEach(function (r, k) { r.classList.toggle('is-hover', k === cur); });
    }

    /* 结果回执一律走 DS Message（第 19 轮全局约定），不另造提示 */
    function run(id) {
      var t = document.querySelector('.td-title');
      var name = t && t.textContent ? t.textContent.trim() : '当前任务';
      close();
      if (id === 'stop') { tdToast('已终止任务：' + name); return; }
      if (id === 'cancel') { tdToast('已取消任务：' + name); return; }
    }

    btn.addEventListener('click', function () { if (open) close(); else show(); });

    /* ---- 关闭途径（契约 clickOutsideClose / escClose） ---- */
    document.addEventListener('pointerdown', function (e) {
      if (!open) return;
      if (menu.contains(e.target) || btn.contains(e.target)) return;
      close();
    }, true);
    document.addEventListener('contextmenu', function () { if (open) close(); });
    document.addEventListener('wheel', function () { if (open) close(); }, { passive: true });
    document.addEventListener('td:close-popovers', close);
    document.addEventListener('td:close-ctx', close);
    window.addEventListener('blur', close);
    window.addEventListener('resize', close);

    /* ---- 键盘（契约 keyboard 清单） ----
       Esc 走**捕获段**：页面尾部的 Esc 链注册更早、且在冒泡段读根上的 data-td-pop-open
       再自己派发 td:close-popovers —— 那段已经会收菜单，但不会归还焦点。这里在捕获段
       先一步收掉并 stopPropagation，避免链继续往下跑（既归还焦点，也不会误跳回看板）。 */
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !open) return;
      e.preventDefault();
      e.stopPropagation();
      close();
      btn.focus();
    }, true);
    btn.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;   /* Enter/Space 走原生 click */
      e.preventDefault();
      if (!open) show();
      focusRow(e.key === 'ArrowDown' ? 0 : rows.length - 1);
    });
    document.addEventListener('keydown', function (e) {
      if (!open || e.key === 'Escape') return;
      if (e.key === 'ArrowDown') { e.preventDefault(); focusRow(cur + 1); return; }
      if (e.key === 'ArrowUp') { e.preventDefault(); focusRow(cur - 1); return; }
      if (e.key === 'Home') { e.preventDefault(); focusRow(0); return; }
      if (e.key === 'End') { e.preventDefault(); focusRow(rows.length - 1); return; }
      if (e.key === 'Tab') { close(); return; }
      if ((e.key === 'Enter' || e.key === ' ') && cur >= 0) {
        e.preventDefault();
        run(rows[cur].getAttribute('data-more-id'));
      }
    });
  }
  function bindEditTask() {
'''
s, r = sub1(s, 'JS: 新增 bindMoreMenu()', OLD_JS, NEW_JS, 'function bindMoreMenu()'); ok &= r

# ================================================================ ④ 注册
OLD_INJ = '    bindBrowseContextMenu();\n    bindEditTask();\n'
NEW_INJ = '    bindBrowseContextMenu();\n    bindMoreMenu();\n    bindEditTask();\n'
s, r = sub1(s, 'JS: inject() 内注册 bindMoreMenu', OLD_INJ, NEW_INJ, 'bindMoreMenu();'); ok &= r

# ================================================================ 自检
print('-' * 60)
def cnt(t):
    return s.count(t)

# ① 每个 token 的增量必须恰好等于「替换串增量」
for tok in TOKENS:
    exp = sum(n.count(tok) for _, n in TAG_CHANGES) - sum(o.count(tok) for o, _ in TAG_CHANGES)
    got = cnt(tok) - BEFORE[tok]
    good = (got == exp)
    if not good:
        ok = False
    print('   [%s] %-30s 增量 %+d（期望 %+d，改后 %d）'
          % ('OK  ' if good else 'FAIL', tok, got, exp, cnt(tok)))

# ② 关键新结构必须各就各位
for name, got, exp in [
    ('.td-more.giencoder-dropdown-popup（基础态）', cnt('.td-more.giencoder-dropdown-popup {'), 1),
    ('function bindMoreMenu()', cnt('function bindMoreMenu()'), 1),
    ('inject() 调用 bindMoreMenu();', cnt('    bindMoreMenu();\n'), 1),
    ("box.id = 'td-more-menu'", cnt("box.id = 'td-more-menu'"), 1),
    ('ITEMS 两条（终止/取消）', cnt("label: '终止任务'") + cnt("label: '取消任务'"), 2),
]:
    if got != exp:
        ok = False
    print('   [%s] %s = %d（期望 %d）' % ('OK  ' if got == exp else 'FAIL', name, got, exp))

# ③ 未动的既有锚点（改前改后必须相等；不写死数值，避免把注释里的合法出现算成破坏）
for guard in ['.td-ctx.giencoder-dropdown-popup', 'var LEFT_KEEP_MIN = 480',
              'function bindBrowseContextMenu()', 'function bindEditTask()',
              '.td-ctx .giencoder-dropdown-item {', 'td-dp-msg']:
    got = cnt(guard) - BEFORE.get(guard, 0)
    if got != 0:
        ok = False
    print('   [%s] 既有锚点 %-34s 增量 %+d' % ('OK  ' if got == 0 else 'FAIL', guard, got))
assert cnt('data-td-more-bound') == 2, 'data-td-more-bound 次数异常'

if not ok:
    print('\n>>> FAIL：未写盘')
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('\n>>> ALL PASS：已写盘 %s（%d → %d 字节，+%d）' % (P, before_len, len(s), len(s) - before_len))
