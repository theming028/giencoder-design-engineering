# -*- coding: utf-8 -*-
"""
r54 补丁：四项
  1) .giencoder-popover-title 字重 600/400 → 500（DS 源 + 页面内联 + 转派浮窗视图覆盖）
  2) 对话框容器激活态（task-detail / avatar，取值与 pages/base.html 完全同款）
  3) .td-browse 展开/收起微动效 → 从右边推出来 / 向右收回去（新增 .td-browse-slot 裁剪窗口）
  4) 文件树行 + 代码预览区右键菜单（DS Dropdown contextMenu 契约 + 「打开方式」二级菜单）

幂等：每条先判 NEW 标记，再判 OLD；自检见文件末尾（标签级计数 + 被改对象精确增减量）。
"""
import os
import re
import sys

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
TD = os.path.join(ROOT, 'pages/task-detail.html')
AV = os.path.join(ROOT, 'pages/avatar.html')
DS = os.path.join(ROOT, 'giencoder-design-system/components.css')
BLOBS = os.path.expanduser('~/.mgmcp/artifacts/blobs/sha256')

report = []


def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def wr(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def sub1(s, label, old, new, mark=None, cnt=1):
    """幂等精确替换：mark（默认 = new）已存在则整条跳过。"""
    key = mark if mark is not None else new
    if key in s:
        report.append('SKIP %s（已应用）' % label)
        return s
    n = s.count(old)
    if n != cnt:
        report.append('!!FAIL %s：OLD 命中 %d 次（期望 %d）' % (label, n, cnt))
        return None
    report.append('OK   %s' % label)
    return s.replace(old, new)


# ============================================================ 图标素材
def blob(sha):
    with open(os.path.join(BLOBS, sha), encoding='utf-8') as f:
        return f.read()


def strip_svg(svg, colorize=False):
    inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
    inner = re.sub(r'<defs>.*?</defs>', '', inner, flags=re.S)
    inner = re.sub(r'\s*clip-path="[^"]*"', '', inner)
    if colorize:                      # 单色图标改 currentColor，不写死 hex
        inner = re.sub(r'fill="#[0-9A-Fa-f]{3,8}"', '', inner)
        inner = re.sub(r'\s{2,}', ' ', inner)
    return inner.strip()


BRAND = {
    'giencoder': strip_svg(blob('bb/bbffb766691b26fc4e466f56272ade36ecdd6d8641182b816288f6f4a2d13077'), True),
    'vscode': strip_svg(blob('87/87eb80d062e10b4685ff0fbd24bee85b7614fb1715f400c3e2903d9311b20a7b')),
    'trae': strip_svg(blob('8a/8a4e9194bb6c959c2d5345f2e1673c3f691212142740e46ba017c19d8826e5f5')),
    'chrome': strip_svg(blob('be/be2051fc0fe856cd11679c4e7e75c51ca6a0c55fc88476e5dae724ad8412a0c4')),
    'edge': strip_svg(blob('4b/4b0ef2e52ec16ff4a03f8fd2fab34356d90579524bc67de76dfa589f22264618')),
    'notes': strip_svg(blob('ea/eaee95c956ee42db7a45d276514d315ef6a70019319265d84175c9f57763e56b')),
    'explorer': strip_svg(blob('9d/9ddebd2b6bfd15408f20a95018189bb5e325138e39eef493b8720312beb4883e')),
}

LINE_ICONS = {
    'file': '<path d="M15.6 3.2H5.6a2 2 0 0 0-2 2v13.6a2 2 0 0 0 2 2h12.8a2 2 0 0 0 2-2V8.4z"/>'
            '<path d="M8.6 10.8h7.6"/><path d="M8.6 14.6h4.2"/>',
    'folder': '<path d="M4.1 3.8H9.2a1.6 1.6 0 0 1 1.6 1.6v0.8h8.5a1.6 1.6 0 0 1 1.6 1.6v11.5'
              'a1.6 1.6 0 0 1-1.6 1.6H4.1a1.6 1.6 0 0 1-1.6-1.6V5.4a1.6 1.6 0 0 1 1.6-1.6Z"/>'
              '<path d="M2.5 11.3h18.9"/>',
    'message': '<path d="M4 21.2V12.2A8.2 8.2 0 0 1 12.2 4h1.6a8.2 8.2 0 0 1 8.2 8.2v0.8'
               'a8.2 8.2 0 0 1-8.2 8.2z"/>'
               '<path d="M8 11.5h8"/><path d="M8 15.3h4"/>',
    'copy': '<path d="M6.5 6.8V5.7a2.6 2.6 0 0 1 2.6-2.6h9.4a2.6 2.6 0 0 1 2.6 2.6v9.4'
            'a2.6 2.6 0 0 1-2.6 2.6h-0.8"/>'
            '<rect x="2.3" y="6.5" width="14.6" height="14.6" rx="2.6"/>',
    'apps': '<rect x="3.65" y="3.65" width="6.55" height="6.55" rx="1.6"/>'
            '<rect x="13.8" y="3.65" width="6.55" height="6.55" rx="1.6"/>'
            '<rect x="3.65" y="13.8" width="6.55" height="6.55" rx="1.6"/>'
            '<rect x="13.8" y="13.8" width="6.55" height="6.55" rx="1.6"/>',
    'right': '<path d="M9.5 5.6 15.9 12l-6.4 6.4"/>',
}


def line_icon(name):
    return ('<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor"'
            ' stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            + LINE_ICONS[name] + '</svg>')


def brand_icon(name):
    return ('<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true">'
            + BRAND[name] + '</svg>')


def jsstr(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


# ============================================================ 目标 2：对话框激活态
COMPOSER_ANCHOR = '      .td-composer { flex: none; margin: 8px 20px 20px; }\n'

COMPOSER_CSS = """
      /* ★ 第 54 轮第 2 项：AI 对话框「激活态」。
         用户开始点击输入（焦点进入对话框内任意控件）时描边变蓝 + 外发光，
         取值与「基础工作台」pages/base.html 里同一个对话框模块的聚焦态**完全一致**
         （base 页是 Vite 产物，那里由 React 的 onFocus/onBlur 切行内 style，只能作真值参考）：
             常态 border-color: var(--color-border-2)  / box-shadow: 0 1px 4px rgba(0,0,0,.04)
             激活 border-color: #A0BAF7              / box-shadow: 0 0 0 3px rgba(55,112,247,.12)
         这两条原先写在元素行内 style 上 —— 行内优先级高于任何类选择器，激活态压不住，
         故改由 .td-composer-field 类承载；transition-colors 继续负责描边色过渡（与 base 同）。
         数字分身（pages/avatar.html）里同一个模块同步同款。 */
      .td-composer-field { border-color: var(--color-border-2); box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.04); }
      .td-composer-field:focus-within { border-color: #A0BAF7; box-shadow: 0px 0px 0px 3px rgba(55, 112, 247, 0.12); }
"""

TD_COMPOSER_OLD = ('        "          <div class=\\"relative flex w-full flex-col rounded-[16px] border bg-white '
                   'p-3 transition-colors\\" style=\\"border-color: var(--color-border-2); '
                   'box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);\\">",')
TD_COMPOSER_NEW = ('        "          <div class=\\"td-composer-field relative flex w-full flex-col '
                   'rounded-[16px] border bg-white p-3 transition-colors\\">",')

AV_COMPOSER_OLD = ('          <div class="relative flex w-full flex-col rounded-[16px] border bg-white '
                   'p-3 transition-colors" style="border-color: var(--color-border-2); '
                   'box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);">')
AV_COMPOSER_NEW = ('          <div class="td-composer-field relative flex w-full flex-col '
                   'rounded-[16px] border bg-white p-3 transition-colors">')

# ============================================================ 目标 3：browse 动效
NEW_BROWSE_CSS = """      /* ★ 第 54 轮第 3 项：预览栏展开/收起微动效 —— 改为「从右边推出来 / 关闭时向右收回去」。
         r53 用的是 clip-path 从左往右「抹开」，方向感不对（像被擦出来，不像被推出来）。
         现改为整栏横向位移：开 = translateX(100%) → 0；关 = 0 → translateX(100%)。
         ⚠️ 必须套一层裁剪窗口 .td-browse-slot：.td-root 是 overflow:visible
            （第 24 轮为放两栏投影特意放开的），直接给 .td-browse 加 translateX
            会让整栏溢出到外壳右侧、撑出横向滚动条。
            slot 与面板同尺寸、透明无样式，不改动任何既有几何（树宽 / 代码区 / 分栏条全不动）。
         收起仍走 .is-closing：先播 220ms 移出动画，随后由 setOpen 摘掉 is-browse（见 JS 段）。 */
      .td-browse-slot { display: none; flex: 1 1 auto; min-width: 0; overflow: hidden; }
      .td-root.is-browse .td-browse-slot { display: flex; }
      @keyframes tdBrowseIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
      }
      @keyframes tdBrowseOut {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
      }
      .td-root.is-browse .td-browse {
        animation: tdBrowseIn 280ms var(--transition-timing-function-enter, cubic-bezier(0.16, 1, 0.3, 1)) both;
      }
      .td-root.is-browse .td-browse.is-closing {
        animation: tdBrowseOut 220ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1)) both;
      }
      @media (prefers-reduced-motion: reduce) {
        .td-root.is-browse .td-browse,
        .td-root.is-browse .td-browse.is-closing { animation: none; }
      }
"""

# ============================================================ 目标 4：右键菜单 CSS
CTX_CSS = """      /* ================= 第 54 轮第 4 项：文件右键菜单 =================
         设计稿：主菜单 = 节点 1350:18294 里的 836:28993；「打开方式」二级菜单 = 836:28935。
         结构一律按 DS Dropdown 契约组装（components/dropdown.json，trigger=contextMenu 变体）：
           div.giencoder-dropdown-popup[role=menu]
             ├ div.giencoder-dropdown-item[role=menuitem] > svg + span
             ├ div.giencoder-dropdown-divider[role=separator]
             └ div.giencoder-dropdown-item.giencoder-dropdown-submenu[aria-haspopup=menu]
                 └ div.giencoder-dropdown-popup.giencoder-dropdown-submenu-popup[role=menu]
         设计稿 2× 截图逐像素量测（主菜单 180×224 / 子菜单 180×214）：
           面板   内距 6 / 项间距 2 / 圆角 8 / 描边 1px #E5E5E5 / 投影 0 8px 20px rgba(0,0,0,.12)
           菜单项 内距 5px 8px / 图标-文字 8 / 圆角 4 / 14px-22px / 文字 #1F1F1F
           图标   14px（单色 #1F1F1F）；「打开方式」右向箭头 14px #868686
           分隔线 140×1 #E5E5E5，上下各留 4（实测：与内容盒左对齐，右侧留白 26）
           hover  底色 #F7F7F7 = --color-fill-1（实测；DS 契约 dropdown.json 写的是
                  --color-fill-2，与视觉稿差一档 —— 以视觉稿为准）
         ⚠️ 本页产物里已有一条同名 .giencoder-dropdown-popup（外壳 React 组件样式：
            transform-origin:top / min-width:168 / padding:6 / animation:giencoder-popup-in），
            其 animation 播完 opacity 会回落到 0（菜单"闪一下就不见"）。
            故这里用 .td-ctx 双类提高优先级并显式 animation:none，开合改走契约状态类
            .giencoder-popup-open（与 Select / Popover 弹层同一套参数）。 */
      .td-ctx.giencoder-dropdown-popup {
        position: fixed; z-index: var(--z-index-popup);
        box-sizing: border-box; min-width: 0; width: 180px; padding: 6px;
        display: flex; flex-direction: column; gap: 2px;
        background: var(--color-bg-popup);
        border: 1px solid var(--color-border-2);
        border-radius: 8px;
        box-shadow: var(--shadow3-down);
        transform-origin: top left;
        animation: none;
        opacity: 0; visibility: hidden; translate: 0 4px; scale: 0.96;
        transition: opacity .15s cubic-bezier(0.34, 0.69, 0.1, 1),
                    translate .15s cubic-bezier(0.34, 0.69, 0.1, 1),
                    scale .15s cubic-bezier(0.34, 0.69, 0.1, 1),
                    visibility 0s .15s;
      }
      .td-ctx.giencoder-dropdown-popup.giencoder-popup-open {
        opacity: 1; visibility: visible; translate: 0 0; scale: 1;
        transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1),
                    translate .2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
                    scale .2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
                    visibility 0s;
      }
      .td-ctx .giencoder-dropdown-item {
        display: flex; align-items: center; gap: 8px;
        padding: 5px 8px; border-radius: 4px;
        font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-1);
        white-space: nowrap; cursor: pointer; user-select: none; outline: none;
        transition: background 120ms var(--transition-timing-function-standard, ease);
      }
      .td-ctx .giencoder-dropdown-item:hover,
      .td-ctx .giencoder-dropdown-item.is-hover { background: var(--color-fill-1); }
      .td-ctx .giencoder-dropdown-item-disabled { color: var(--color-text-4); cursor: not-allowed; }
      .td-ctx .giencoder-dropdown-item-disabled:hover { background: transparent; }
      .td-ctx-ico {
        flex: none; width: 14px; height: 14px; display: inline-flex;
        align-items: center; justify-content: center; color: var(--color-text-1);
      }
      .td-ctx-ico svg { display: block; width: 14px; height: 14px; }
      .td-ctx-label { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; }
      .td-ctx .giencoder-dropdown-arrow {
        flex: none; width: 14px; height: 14px; display: inline-flex;
        align-items: center; justify-content: center; color: var(--color-text-3);
      }
      .td-ctx .giencoder-dropdown-arrow svg { display: block; width: 14px; height: 14px; }
      .td-ctx .giencoder-dropdown-divider {
        flex: none; width: 140px; height: 1px; margin: 4px 0; background: var(--color-border-2);
      }
"""

# ============================================================ 目标 4：右键菜单 JS
CTX_JS = r"""  /* ---------- 文件目录 / 代码预览 → 鼠标右键菜单（★ 第 54 轮第 4 项） ----------
     设计稿：主菜单 = 节点 1350:18294 里的 836:28993（180 宽 / 内距 6 / 项间距 2 / 圆角 8 /
     描边 #E5E5E5 / 投影 0 8px 20px 12%）；「打开方式」二级菜单 = 节点 836:28935（同规格 6 项）。
     结构按 DS Dropdown 契约（components/dropdown.json，trigger=contextMenu 变体）组装，
     不自造同义结构；开合沿用契约状态类 .giencoder-popup-open（与 Select / Popover 同参数）。
     ⚠️ 图标来源：设计稿里 6 个 ui-icon 走的是 MasterGo 官方图标库（MCP 只给组件名、拿不到 path），
        故按设计稿 2× 截图逐像素量测后自绘（24 格 / 描边 2.2 / 圆头圆角）；
        品牌类图标（GienCoder / VS Code / Trae / Chrome / Edge / Notes / 文件资源管理器）
        直接取设计稿导出的 SVG 素材，单色的一律改 currentColor（配色不写死 hex）。
     触发目标：① 文件树任意行 .td-bf ② 代码预览区 .td-browse-pre（"里的文字"）。
     关闭途径：选中任一项 / 点菜单外 / 页面滚动 / 窗口缩放或失焦 / Esc
              （Esc 走页尾 Esc 链：html 根上的 data-td-ctx-open → td:close-ctx）。
     键盘（契约 keyboard 清单）：↑↓ 移动虚拟焦点 · Enter 选中 · → 展开子菜单 · ← 收起 · Esc 关闭。 */
  function bindBrowseContextMenu() {
    var root = document.querySelector('.td-root');
    if (!root || root.getAttribute('data-td-ctx-bound') === '1') return;
    root.setAttribute('data-td-ctx-bound', '1');

    var ICON = {
      file: @@IFILE@@,
      folder: @@IFOLDER@@,
      message: @@IMESSAGE@@,
      brand: @@IBRAND@@,
      copy: @@ICOPY@@,
      apps: @@IAPPS@@,
      right: @@IRIGHT@@
    };
    var OPEN_WITH = [
      { id: 'vscode',   label: 'VS Code',         svg: @@BVSCODE@@ },
      { id: 'trae',     label: 'Trae',            svg: @@BTRAE@@ },
      { id: 'chrome',   label: 'Google Chrome',   svg: @@BCHROME@@ },
      { id: 'edge',     label: 'Microsoft Edge',  svg: @@BEDGE@@ },
      { id: 'notes',    label: 'Notes',           svg: @@BNOTES@@ },
      { id: 'explorer', label: '文件资源管理器',    svg: @@BEXPLORER@@ }
    ];
    var MENU = [
      { id: 'open',     label: '打开',            svg: ICON.file },
      { id: 'reveal',   label: '打开所在文件夹',    svg: ICON.folder },
      { id: 'chat',     label: '添加到对话',       svg: ICON.message },
      { id: 'brand',    label: '添加到 GienCoder', svg: ICON.brand },
      { id: 'path',     label: '复制路径',         svg: ICON.copy },
      { divider: true },
      { id: 'openwith', label: '打开方式',         svg: ICON.apps, children: OPEN_WITH }
    ];

    var tree = root.querySelector('.td-browse-files');
    var pre = root.querySelector('.td-browse-pre');
    var crumb = root.querySelector('.td-browse-crumb-path');
    if (!tree && !pre) return;

    var menu = null, sub = null, subRow = null, open = false, cur = -1, rows = [], target = null;

    function build(items) {
      var box = document.createElement('div');
      box.className = 'giencoder-dropdown-popup td-ctx';
      box.setAttribute('role', 'menu');
      items.forEach(function (it) {
        if (it.divider) {
          var d = document.createElement('div');
          d.className = 'giencoder-dropdown-divider';
          d.setAttribute('role', 'separator');
          box.appendChild(d);
          return;
        }
        var row = document.createElement('div');
        row.className = 'giencoder-dropdown-item' + (it.children ? ' giencoder-dropdown-submenu' : '');
        row.setAttribute('role', 'menuitem');
        row.setAttribute('tabindex', '-1');
        row.setAttribute('data-ctx-id', it.id);
        if (it.children) row.setAttribute('aria-haspopup', 'menu');
        row.innerHTML = '<span class="td-ctx-ico" aria-hidden="true">' + it.svg + '</span>' +
                        '<span class="td-ctx-label"></span>' +
                        (it.children
                          ? '<span class="giencoder-dropdown-arrow" aria-hidden="true">' + ICON.right + '</span>'
                          : '');
        row.querySelector('.td-ctx-label').textContent = it.label;
        box.appendChild(row);
      });
      return box;
    }

    function ensure() {
      if (menu) return;
      menu = build(MENU);
      menu.style.display = 'none';
      document.body.appendChild(menu);
      sub = build(OPEN_WITH);
      sub.classList.add('giencoder-dropdown-submenu-popup');
      sub.style.display = 'none';
      document.body.appendChild(sub);
      rows = Array.prototype.slice.call(menu.querySelectorAll('.giencoder-dropdown-item'));

      menu.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
      menu.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.giencoder-dropdown-item') : null;
        if (!row) return;
        if (row.getAttribute('data-ctx-id') === 'openwith') { toggleSub(row); return; }
        run(row.getAttribute('data-ctx-id'));
      });
      /* 悬停切换：主菜单里移到别的项就收子菜单；指向「打开方式」本身或子菜单则保留 */
      menu.addEventListener('pointerover', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.giencoder-dropdown-item') : null;
        if (!row) return;
        if (row.getAttribute('data-ctx-id') === 'openwith') { openSub(row); return; }
        if (subRow && subRow !== row) closeSub();
      });
      sub.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
      sub.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.giencoder-dropdown-item') : null;
        if (row) run(row.getAttribute('data-ctx-id'));
      });
      sub.addEventListener('pointerover', function () { if (subRow) subRow.classList.add('is-hover'); });
      sub.addEventListener('pointerleave', function () { closeSub(); });
    }

    function openSub(row) {
      ensure();
      if (subRow === row && sub.classList.contains('giencoder-popup-open')) return;
      closeSub();
      subRow = row;
      row.classList.add('is-hover');
      var r = row.getBoundingClientRect();
      sub.style.display = 'flex';
      sub.style.visibility = 'hidden';
      var w = sub.offsetWidth, h = sub.offsetHeight;
      var left = r.right + 4, top = r.top - 6;
      if (left + w > window.innerWidth - 8) left = Math.max(8, r.left - 4 - w);
      if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - 8 - h);
      if (top < 8) top = 8;
      sub.style.left = left + 'px';
      sub.style.top = top + 'px';
      sub.style.visibility = '';
      sub.classList.add('giencoder-popup-open');
    }

    function closeSub() {
      if (!sub || !subRow) { return; }
      subRow.classList.remove('is-hover');
      subRow = null;
      cur = -1;
      sub.classList.remove('giencoder-popup-open');
      setTimeout(function () {
        if (!subRow && sub) sub.style.display = 'none';
      }, 200);
    }

    function toggleSub(row) {
      if (subRow === row && sub.classList.contains('giencoder-popup-open')) closeSub();
      else openSub(row);
    }

    /* 结果回执一律走 DS Message（第 19 轮全局约定），不另造提示 */
    function run(id) {
      var name = (target && target.name) || '';
      var path = (target && target.path) || '';
      close();
      if (id === 'path') {
        try { if (navigator.clipboard && path) navigator.clipboard.writeText(path); } catch (er) {}
        tdToast(path ? '已复制路径：' + path : '已复制路径');
        return;
      }
      var plain = { open: '打开', reveal: '打开所在文件夹', chat: '添加到对话', brand: '添加到 GienCoder' };
      if (plain[id]) { tdToast(plain[id] + '：' + name); return; }
      for (var i = 0; i < OPEN_WITH.length; i++) {
        if (OPEN_WITH[i].id === id) { tdToast('已用 ' + OPEN_WITH[i].label + ' 打开：' + name); return; }
      }
    }

    function flag(on) {
      if (on) document.documentElement.setAttribute('data-td-ctx-open', '');
      else document.documentElement.removeAttribute('data-td-ctx-open');
    }

    function place(x, y) {
      menu.style.display = 'flex';
      menu.style.visibility = 'hidden';
      var w = menu.offsetWidth, h = menu.offsetHeight;
      var left = x, top = y;
      if (left + w > window.innerWidth - 8) left = Math.max(8, window.innerWidth - 8 - w);
      if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - 8 - h);
      menu.style.left = left + 'px';
      menu.style.top = top + 'px';
      /* 缩放原点落在光标上 —— 契约的「轻微位移展开」就有了方向感 */
      menu.style.transformOrigin = (x - left) + 'px ' + (y - top) + 'px';
      menu.style.visibility = '';
    }

    function show(x, y, t) {
      ensure();
      closeSub();
      target = t;
      place(x, y);
      void menu.offsetHeight;                 /* 强制回流，让开合过渡生效 */
      menu.classList.add('giencoder-popup-open');
      open = true;
      cur = -1;
      rows.forEach(function (r) { r.classList.remove('is-hover'); });
      flag(true);
    }

    function close() {
      if (!menu || !open) return;
      open = false;
      closeSub();
      menu.classList.remove('giencoder-popup-open');
      setTimeout(function () { if (!open && menu) menu.style.display = 'none'; }, 200);
      flag(false);
    }

    function focusRow(i) {
      if (!rows.length) return;
      cur = (i + rows.length) % rows.length;
      rows.forEach(function (r, k) { r.classList.toggle('is-hover', k === cur); });
      if (rows[cur].getAttribute('data-ctx-id') === 'openwith') openSub(rows[cur]);
      else if (subRow) closeSub();
    }

    /* ---- 触发：树行 / 代码预览区 ---- */
    function hit(e) {
      var t = e.target;
      if (!t || !t.closest) return null;
      var base = crumb ? crumb.textContent.replace(/\s*\/\s*/g, '/').replace(/\/[^/]*$/, '') : '';
      var row = t.closest('.td-bf');
      if (row && tree && tree.contains(row)) {
        var nm = row.querySelector('.td-bf-name');
        var name = nm ? nm.textContent : '';
        return { name: name, path: (base ? base + '/' : '') + name };
      }
      if (pre && pre.contains(t)) {
        var p = crumb ? crumb.textContent.replace(/\s*\/\s*/g, '/') : '';
        return { name: p.split('/').pop() || 'index.html', path: p };
      }
      return null;
    }

    root.addEventListener('contextmenu', function (e) {
      if (!root.classList.contains('is-browse')) return;
      var t = hit(e);
      if (!t) return;
      e.preventDefault();
      var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
      if (row && row.classList.contains('is-file')) {
        var old = root.querySelector('.td-bf.is-active');
        if (old) { old.classList.remove('is-active'); old.setAttribute('aria-selected', 'false'); }
        row.classList.add('is-active');
        row.setAttribute('aria-selected', 'true');
      }
      show(e.clientX, e.clientY, t);
    });

    /* ---- 关闭途径（契约 clickOutsideClose / escClose） ---- */
    document.addEventListener('pointerdown', function (e) {
      if (!open) return;
      if (e.button === 2) return;                       /* 右键交给 contextmenu 分支重开 */
      if (menu.contains(e.target) || sub.contains(e.target)) return;
      close();
    }, true);
    window.addEventListener('blur', close);
    window.addEventListener('resize', close);
    root.addEventListener('scroll', function () { if (open) close(); }, true);
    document.addEventListener('wheel', function () { if (open) close(); }, { passive: true });
    document.addEventListener('td:close-ctx', close);
    document.addEventListener('td:close-popovers', close);

    /* ---- 键盘（契约 keyboard 清单） ---- */
    document.addEventListener('keydown', function (e) {
      if (!open) return;
      if (e.key === 'Escape') { e.stopPropagation(); close(); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); focusRow(cur + 1); return; }
      if (e.key === 'ArrowUp') { e.preventDefault(); focusRow(cur - 1); return; }
      if (e.key === 'ArrowRight') {
        if (cur >= 0 && rows[cur].getAttribute('data-ctx-id') === 'openwith') {
          e.preventDefault(); openSub(rows[cur]);
        }
        return;
      }
      if (e.key === 'ArrowLeft') { if (subRow) { e.preventDefault(); closeSub(); } return; }
      if (e.key === 'Enter' || e.key === ' ') {
        if (cur < 0) return;
        e.preventDefault();
        var id = rows[cur].getAttribute('data-ctx-id');
        if (id === 'openwith') toggleSub(rows[cur]); else run(id);
      }
    });
  }

"""


def build_ctx_js():
    out = CTX_JS
    tokens = {
        '@@IFILE@@': jsstr(line_icon('file')),
        '@@IFOLDER@@': jsstr(line_icon('folder')),
        '@@IMESSAGE@@': jsstr(line_icon('message')),
        '@@IBRAND@@': jsstr(brand_icon('giencoder')),
        '@@ICOPY@@': jsstr(line_icon('copy')),
        '@@IAPPS@@': jsstr(line_icon('apps')),
        '@@IRIGHT@@': jsstr(line_icon('right')),
        '@@BVSCODE@@': jsstr(brand_icon('vscode')),
        '@@BTRAE@@': jsstr(brand_icon('trae')),
        '@@BCHROME@@': jsstr(brand_icon('chrome')),
        '@@BEDGE@@': jsstr(brand_icon('edge')),
        '@@BNOTES@@': jsstr(brand_icon('notes')),
        '@@BEXPLORER@@': jsstr(brand_icon('explorer')),
    }
    for k, v in tokens.items():
        if k not in out:
            report.append('!!FAIL 图标占位缺失: %s' % k)
            return None
        out = out.replace(k, v)
    leftover = re.findall(r'@@\w+@@', out)
    if leftover:
        report.append('!!FAIL 未替换占位: %s' % leftover)
        return None
    return out


# ============================================================ 执行
def main():
    # --- DS 源 ---
    s = rd(DS)
    old = ('.giencoder-popover-title { padding: 10px 16px 0; font-size: var(--font-size-body-3); '
           'font-weight: 600; color: var(--color-text-1); }')
    r = sub1(s, 'DS components.css · popover-title 600→500', old,
             old.replace('font-weight: 600;', 'font-weight: 500;'))
    if r is None:
        print('\n'.join(report)); return 2
    wr(DS, r)

    # --- task-detail ---
    s = rd(TD)
    n0 = len(s)
    stat0 = {k: s.count(k) for k in ('<style', '</style>', '<script', '</script>',
                                     'class=\\"td-bf is-file', 'td-sec-head')}

    for label, old, new, mark in [
        ('task-detail · 内联 popover-title 600→500',
         '.giencoder-popover-title { padding: 10px 16px 0; font-size: var(--font-size-body-3); '
         'font-weight: 600; color: var(--color-text-1); }',
         '.giencoder-popover-title { padding: 10px 16px 0; font-size: var(--font-size-body-3); '
         'font-weight: 500; color: var(--color-text-1); }', None),
        ('task-detail · .td-dp 浮窗标题 400→500',
         '.td-dp .giencoder-popover-title { padding: 15px 15px 0; font-size: 14px; '
         'line-height: 22px; font-weight: 400; }',
         '.td-dp .giencoder-popover-title { padding: 15px 15px 0; font-size: 14px; '
         'line-height: 22px; font-weight: 500; }', None),
        ('task-detail · 对话框激活态 CSS', COMPOSER_ANCHOR, COMPOSER_ANCHOR + COMPOSER_CSS,
         '.td-composer-field:focus-within'),
        ('task-detail · 对话框容器类名', TD_COMPOSER_OLD, TD_COMPOSER_NEW, None),
        ('task-detail · .td-browse-slot 开始标签',
         '        "<aside class=\\"td-browse\\" aria-label=\\"文件预览\\">",',
         '        "<div class=\\"td-browse-slot\\">",\n'
         '        "<aside class=\\"td-browse\\" aria-label=\\"文件预览\\">",', None),
        ('task-detail · .td-browse-slot 结束标签',
         '        "    </section>",\n        "  </div>",\n        "</aside>",\n        "</div>",',
         '        "    </section>",\n        "  </div>",\n        "</aside>",\n        "</div>",\n        "</div>",', None),
        ('task-detail · setOpen 收起时长 200→240',
         'pane._browseT = setTimeout(done, 200);', 'pane._browseT = setTimeout(done, 240);', None),
        ('task-detail · setOpen 注释同步',
         '收起先播 180ms 的 .is-closing 移出动画，再摘 is-browse ——',
         '收起先播 220ms 的 .is-closing 移出动画，再摘 is-browse ——', None),
        ('task-detail · 右键菜单调用',
         '    bindDispatchPicker();\n    bindCoop();',
         '    bindDispatchPicker();\n    bindCoop();\n    bindBrowseContextMenu();', None),
    ]:
        r = sub1(s, label, old, new, mark)
        if r is None:
            print('\n'.join(report)); return 2
        s = r

    # 动效 CSS 整块替换（用标记定位，避免超长字面量）
    if 'tdBrowseIn 280ms' in s:
        report.append('SKIP task-detail · browse 动效 CSS（已应用）')
    else:
        i0 = s.find('      /* ★ 第 53 轮第 1 项：预览栏展开/收起补微动效。')
        i1 = s.find('      /* ★ 第 50 轮第 2 项：浏览态（文件预览栏展示时）AI 对话框固定为')
        if i0 < 0 or i1 < 0 or i1 <= i0:
            report.append('!!FAIL browse 动效 CSS 锚点')
            print('\n'.join(report)); return 2
        s = s[:i0] + NEW_BROWSE_CSS + CTX_CSS + s[i1:]
        report.append('OK   task-detail · browse 动效 CSS 替换 + 右键菜单 CSS')

    # 右键菜单 JS 函数体
    ctx_js = build_ctx_js()
    if ctx_js is None:
        print('\n'.join(report)); return 2
    anchor = ('  /* ---------- 顶栏「协作」→ 分步模态弹窗'
              '（★ 第 32 轮第 5 项，设计稿节点 622:20081） ----------')
    r = sub1(s, 'task-detail · 右键菜单 JS', anchor, ctx_js + anchor,
             mark='function bindBrowseContextMenu()')
    if r is None:
        print('\n'.join(report)); return 2
    s = r

    # Esc 链
    old_esc = ("        if (document.documentElement.hasAttribute('data-td-pop-open')) {\n"
               "          document.dispatchEvent(new CustomEvent('td:close-popovers'));\n"
               "          return;\n"
               "        }")
    new_esc = ("        /* ★ 第 54 轮第 4 项：文件右键菜单打开时，Esc 先收菜单"
               "（见 bindBrowseContextMenu）。 */\n"
               "        if (document.documentElement.hasAttribute('data-td-ctx-open')) {\n"
               "          document.dispatchEvent(new CustomEvent('td:close-ctx'));\n"
               "          return;\n"
               "        }\n") + old_esc
    r = sub1(s, 'task-detail · Esc 链加右键菜单分支', old_esc, new_esc)
    if r is None:
        print('\n'.join(report)); return 2
    s = r

    stat1 = {k: s.count(k) for k in stat0}
    report.append('task-detail 字符 %d → %d' % (n0, len(s)))
    wr(TD, s)

    # --- avatar ---
    a = rd(AV)
    a0 = len(a)
    astat0 = {k: a.count(k) for k in ('<style', '</style>', '<script', '</script>')}
    for label, old, new, mark in [
        ('avatar · 对话框激活态 CSS', COMPOSER_ANCHOR, COMPOSER_ANCHOR + COMPOSER_CSS,
         '.td-composer-field:focus-within'),
        ('avatar · 对话框容器类名', AV_COMPOSER_OLD, AV_COMPOSER_NEW, None),
    ]:
        r = sub1(a, label, old, new, mark)
        if r is None:
            print('\n'.join(report)); return 2
        a = r
    astat1 = {k: a.count(k) for k in astat0}
    report.append('avatar 字符 %d → %d' % (a0, len(a)))
    wr(AV, a)

    # ---------------------------------------------------------- 自检
    print('\n'.join(report))
    print('---- 自检 ----')
    ok = True

    def chk(name, got, exp):
        nonlocal ok
        good = got == exp
        if not good:
            ok = False
        print('%s %s = %s（期望 %s）' % ('OK  ' if good else 'FAIL', name, got, exp))

    for f, name in ((TD, 'task-detail'), (AV, 'avatar')):
        t = rd(f)
        chk('%s .td-composer-field:focus-within 规则数' % name, t.count('.td-composer-field:focus-within'), 1)
        chk('%s .td-composer-field 声明块' % name, t.count('.td-composer-field { border-color'), 1)

    t = rd(TD)
    chk('task-detail .td-composer-field 标记', t.count('td-composer-field relative'), 1)
    chk('task-detail tdBrowseIn 出现次数（定义+引用）', t.count('tdBrowseIn'), 2)
    chk('task-detail tdBrowseOut 出现次数（定义+引用）', t.count('tdBrowseOut'), 2)
    chk('task-detail tdBrowseContentIn 残留', t.count('tdBrowseContentIn'), 0)
    chk('task-detail browse-slot 标记', t.count('class=\\"td-browse-slot\\"'), 1)
    chk('task-detail .td-ctx 面板规则（基态+开态）', t.count('.td-ctx.giencoder-dropdown-popup'), 2)
    chk('task-detail bindBrowseContextMenu 定义+调用', t.count('bindBrowseContextMenu'), 3)
    chk('task-detail Esc 链 ctx 分支', t.count("hasAttribute('data-td-ctx-open')"), 1)
    chk('task-detail .giencoder-popover-title 权重 500', t.count(
        '.giencoder-popover-title { padding: 10px 16px 0; font-size: var(--font-size-body-3); '
        'font-weight: 500; color: var(--color-text-1); }'), 1)
    chk('task-detail .td-dp 权重 500', t.count(
        '.td-dp .giencoder-popover-title { padding: 15px 15px 0; font-size: 14px; '
        'line-height: 22px; font-weight: 500; }'), 1)
    for k in stat0:
        chk('task-detail 计数不变 %s' % k, stat1[k], stat0[k])

    a = rd(AV)
    for k in astat0:
        chk('avatar 计数不变 %s' % k, astat1[k], astat0[k])

    d = rd(DS)
    chk('DS popover-title 权重 500', d.count(
        '.giencoder-popover-title { padding: 10px 16px 0; font-size: var(--font-size-body-3); '
        'font-weight: 500; color: var(--color-text-1); }'), 1)
    print('---- %s ----' % ('ALL PASS' if ok else 'HAS FAILURE'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
