# -*- coding: utf-8 -*-
"""r53 补丁：task-detail.html 七项（第 4 项待用户确认口径，暂不动）。

幂等铁律（r52 踩坑）：**先判 NEW 标记，再判 OLD**。
NEW 串常是 OLD 串的「前缀超集」，若先判 OLD 会重复追加。

自检铁律：只允许 ① 标签级计数 ② 针对被改对象的精确增减量。
禁止「全文件关键词总数不变」这类断言。
"""
import re, sys, os

PAGE = 'pages/task-detail.html'
DS_CSS = 'giencoder-design-system/components.css'

s = open(PAGE, encoding='utf-8').read()
bef = len(s)

# ---------------------------------------------------------------- 1 微动效
OLD1 = '.td-root.is-browse .td-browse { display: flex; }\n'
NEW1 = '''.td-root.is-browse .td-browse { display: flex; }
      /* ★ 第 53 轮第 1 项：预览栏展开/收起补微动效。
         原来靠 display:none ↔ flex 硬切（不可过渡）—— 这就是「生硬」的根源。
         这里用 clip-path 从右向左「抹开」+ 淡入：不改盒模型、不产生任何溢出，
         比 translateX 安全（.td-browse 右缘已贴到外壳内缘，右移会被裁）。
         clip-path 带上 round 8px，否则会把右侧圆角切成直角。
         收起的 .is-closing 由 setOpen 延迟 180ms 再摘 is-browse（见 JS 段）。 */
      @keyframes tdBrowseIn {
        from { opacity: 0; clip-path: inset(0 0 0 28px round 0 8px 8px 0); }
        to { opacity: 1; clip-path: inset(0 0 0 0 round 0 8px 8px 0); }
      }
      @keyframes tdBrowseOut {
        from { opacity: 1; clip-path: inset(0 0 0 0 round 0 8px 8px 0); }
        to { opacity: 0; clip-path: inset(0 0 0 28px round 0 8px 8px 0); }
      }
      .td-root.is-browse .td-browse {
        animation: tdBrowseIn 260ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1)) both;
      }
      .td-root.is-browse .td-browse.is-closing {
        animation: tdBrowseOut 180ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1)) both;
      }
      @media (prefers-reduced-motion: reduce) {
        .td-root.is-browse .td-browse,
        .td-root.is-browse .td-browse.is-closing { animation: none; }
      }
'''
MARK1 = '@keyframes tdBrowseIn {'

# ---------------------------------------------------------------- 1' JS
OLD1J = """        function setOpen(on) {
          root.classList.toggle('is-browse', on);
          btn.setAttribute('aria-pressed', on ? 'true' : 'false');
          if (on) { setRight(curRight, false); setTree(curTree, false); }
        }
"""
NEW1J = """        /* ★ 第 53 轮第 1 项：展开/收起补微动效。
           收起先播 180ms 的 .is-closing 移出动画，再摘 is-browse ——
           否则 display:none 会让整栏瞬间消失（原来的「生硬」正来自这里）。
           定时器挂在 pane 上，收起途中又点开时可取消，避免动画被半路摘掉。 */
        function setOpen(on) {
          var isOn = root.classList.contains('is-browse');
          if (on === isOn && !pane.classList.contains('is-closing')) return;
          if (on) {
            if (pane._browseT) { clearTimeout(pane._browseT); pane._browseT = null; }
            pane.classList.remove('is-closing');
            root.classList.add('is-browse');
            btn.setAttribute('aria-pressed', 'true');
            setRight(curRight, false); setTree(curTree, false);
            return;
          }
          if (pane.classList.contains('is-closing')) return;
          var done = function () {
            pane._browseT = null;
            pane.classList.remove('is-closing');
            root.classList.remove('is-browse');
            btn.setAttribute('aria-pressed', 'false');
          };
          pane.classList.add('is-closing');
          pane._browseT = setTimeout(done, 200);
          pane.addEventListener('animationend', function onEnd(e) {
            if (e.target !== pane) return;
            clearTimeout(pane._browseT);
            pane.removeEventListener('animationend', onEnd);
            done();
          });
        }
"""
MARK1J = 'pane._browseT = setTimeout(done, 200);'

# ---------------------------------------------------------------- 2 底部渐隐
OLD2 = """      .td-desc-body {
        max-height: 374px; overflow: hidden;
        transition: max-height 320ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1));
      }
      .td-desc-body.is-open { max-height: none; }
"""
NEW2 = """      .td-desc-body {
        max-height: 374px; overflow: hidden;
        /* ★ 第 53 轮第 2 项：折叠态底部渐隐。
           实测 scrollHeight 845 > clientHeight 374 —— 确为硬截断，不是「看起来只剩一行」。
           用 mask 而不是盖一层渐变 ::after：后者展开后还得额外隐藏，且会挡住正文交互。
           渐隐高度走变量，展开时归零，与 max-height 同曲线过渡（calc 两端结构一致可插值）。 */
        --td-desc-fade: 56px;
        -webkit-mask-image: linear-gradient(to bottom, #000 calc(100% - var(--td-desc-fade)), transparent 100%);
        mask-image: linear-gradient(to bottom, #000 calc(100% - var(--td-desc-fade)), transparent 100%);
        transition: max-height 320ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1)),
                    mask-image 320ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1));
      }
      .td-desc-body.is-open { max-height: none; --td-desc-fade: 0px; }
"""
MARK2 = '--td-desc-fade: 0px;'

# ---------------------------------------------------------------- 3 状态点 6px
OLD3 = '.giencoder-badge-status-dot{border-radius:50%;width:8px;height:8px}'
NEW3 = '.giencoder-badge-status-dot{border-radius:50%;width:6px;height:6px}'
MARK3 = 'giencoder-badge-status-dot{border-radius:50%;width:6px;height:6px}'

# ---------------------------------------------------------------- 5 顶栏导航图标 14px
OLD5 = '.td-bar-nav { flex: none; display: flex; align-items: center; gap: 4px; }\n'
NEW5 = ('.td-bar-nav { flex: none; display: flex; align-items: center; gap: 4px; }\n'
        '      /* ★ 第 53 轮第 5 项：上一个/下一个的**图标本身** 14px（容器 .td-iconbtn 尺寸不动）。\n'
        '         与第 52 轮 td-right-acts 同口径：只缩 svg，不缩外框。 */\n'
        '      .td-bar-nav .td-iconbtn svg { width: 14px; height: 14px; }\n')
MARK5 = '.td-bar-nav .td-iconbtn svg { width: 14px; height: 14px; }'

# ---------------------------------------------------------------- 6 下拉右对齐 + 7 日历补齐
OLD6 = '.kb-crt-date .giencoder-date-picker-popup { left: auto; right: 0; }\n'
NEW6 = '''.kb-crt-date .giencoder-date-picker-popup { left: auto; right: 0; }
      /* ★ 第 53 轮第 6 项：任务属性里的下拉弹层 min-width 200 > 字段宽 191，
         默认 left:0（与触发器左对齐）→ 右缘冲出字段 9px。改为与 .kb-crt-fld 右对齐。
         注意：这是**另一处**选择器（不在 .td-composer 里），r52 那条覆盖不到。 */
      .kb-crt-fld > .giencoder-select-popup { left: auto; right: 0; }
      /* ★ 第 53 轮第 7 项：补齐 DatePicker 面板 + 日历样式。
         根因：本页只内联了 Select 的弹层 CSS，DatePicker 整块缺失
         （DS 源：giencoder-design-system/gienx-templates/ui-controls.css），
         实测展开后 padding / border-radius 均为 0，日历塌成一行纯文本。
         以下按 DS 源逐条补齐；唯一偏差：投影取产品编译产物的 var(--shadow3-down)
         （0 8px 20px），与同页 Select 弹层一致 —— DS 源里标的 --shadow1-down 是遗留偏差。 */
      .giencoder-date-picker { position: relative; display: inline-block; }
      .giencoder-date-picker-popup {
        position: absolute; top: calc(100% + 4px); left: 0; z-index: 10;
        background: var(--color-bg-popup);
        border: 1px solid var(--color-border-2);
        border-radius: var(--border-radius-large);
        box-shadow: var(--shadow3-down);
        padding: var(--spacing-6);
        opacity: 0; visibility: hidden;
        transform: scale(0.97) translateY(4px);
        transform-origin: top right;
        transition: opacity var(--transition-duration-2) var(--transition-timing-function-standard),
                    transform var(--transition-duration-2) var(--transition-timing-function-spring),
                    visibility var(--transition-duration-2) var(--transition-timing-function-standard);
      }
      .giencoder-date-picker-popup.giencoder-panel-open {
        opacity: 1; visibility: visible; transform: scale(1) translateY(0);
      }
      .giencoder-date-picker-panels { display: flex; gap: var(--spacing-9); }
      .giencoder-calendar { width: 224px; }
      .giencoder-calendar-header {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: var(--spacing-4);
      }
      .giencoder-calendar-title {
        font-size: var(--font-size-body-3); font-weight: 600; color: var(--color-text-1);
      }
      .giencoder-calendar-nav {
        border: none; background: none; cursor: pointer; color: var(--color-text-3);
        width: 24px; height: 24px; border-radius: var(--border-radius-small);
        display: inline-flex; align-items: center; justify-content: center; padding: 0;
      }
      .giencoder-calendar-nav:hover { background: var(--color-fill-1); color: var(--color-text-1); }
      .giencoder-calendar-weekdays,
      .giencoder-calendar-grid { display: grid; grid-template-columns: repeat(7, 32px); gap: 0; }
      .giencoder-calendar-weekdays span {
        width: 32px; height: 28px; display: inline-flex; align-items: center; justify-content: center;
        font-size: var(--font-size-body-1); color: var(--color-text-3);
      }
      .giencoder-calendar-cell {
        width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center;
        border-radius: 50%; font-size: var(--font-size-body-2); color: var(--color-text-1);
        cursor: pointer; box-sizing: border-box;
      }
      .giencoder-calendar-cell:hover { background: var(--color-fill-1); }
      .giencoder-calendar-cell-other { color: var(--color-text-4); }
      .giencoder-calendar-cell-today { border: 1px solid var(--color-primary-6); color: var(--color-primary-6); }
      .giencoder-calendar-cell-selected { background: var(--color-primary-6); color: var(--color-white); }
      .giencoder-calendar-cell-in-range { background: var(--color-primary-1); border-radius: 0; }
      .giencoder-calendar-cell-range-start,
      .giencoder-calendar-cell-range-end {
        background: var(--color-primary-6); color: var(--color-white); border-radius: 50%;
      }
      .giencoder-calendar-cell-empty { visibility: hidden; }
'''
MARK6 = '.kb-crt-fld > .giencoder-select-popup { left: auto; right: 0; }'
MARK7 = '.giencoder-calendar-cell-empty { visibility: hidden; }'

# ---------------------------------------------------------------- 8 文件树 item 圆角
OLD8 = """      .td-bf {
        position: relative; display: flex; align-items: center; height: 28px; box-sizing: border-box;
        font-size: var(--font-size-body-2); color: var(--color-text-1);
        white-space: nowrap; overflow: hidden; cursor: pointer;
      }
"""
NEW8 = """      .td-bf {
        position: relative; display: flex; align-items: center; height: 28px; box-sizing: border-box;
        font-size: var(--font-size-body-2); color: var(--color-text-1);
        white-space: nowrap; overflow: hidden; cursor: pointer;
        /* ★ 第 53 轮第 8 项：行本体补 4px 圆角。
           此前只有激活态的 ::before 带圆角，hover 底色是直角，两态不一致。 */
        border-radius: 4px;
      }
"""
MARK8 = '/* ★ 第 53 轮第 8 项：行本体补 4px 圆角。'

PAIRS = [
    ('1 预览栏微动效 CSS', OLD1, NEW1, MARK1),
    ('1 预览栏微动效 JS',  OLD1J, NEW1J, MARK1J),
    ('2 描述区底部渐隐',    OLD2, NEW2, MARK2),
    ('3 状态点 6px',       OLD3, NEW3, MARK3),
    ('5 顶栏导航图标 14px', OLD5, NEW5, MARK5),
    ('6 下拉右对齐+7 日历', OLD6, NEW6, MARK6),
    ('8 文件树行圆角 4px',  OLD8, NEW8, MARK8),
]

applied, skipped = [], []
for label, old, new, mark in PAIRS:
    if mark in s:
        skipped.append(label)
    elif s.count(old) == 1:
        s = s.replace(old, new, 1)
        applied.append(label)
    else:
        sys.exit('!! 【%s】锚点匹配数 = %d（应为 1）' % (label, s.count(old)))

open(PAGE, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- 自检
def cnt(p):
    return len(re.findall(p, s))

checks = [
    # 标签级（全页基线：3 / 3 / 9 / 9）
    ('<style 3', cnt(r'<style'), 3),
    ('</style> 3', cnt(r'</style>'), 3),
    ('<script 9', cnt(r'<script'), 9),
    ('</script> 8', cnt(r'</script>'), 8),
    # 1
    ('@keyframes tdBrowseIn 1', cnt(re.escape('@keyframes tdBrowseIn')), 1),
    ('@keyframes tdBrowseOut 1', cnt(re.escape('@keyframes tdBrowseOut')), 1),
    ('tdBrowseIn 260ms 1', cnt(re.escape('tdBrowseIn 260ms')), 1),
    ('tdBrowseOut 180ms 1', cnt(re.escape('tdBrowseOut 180ms')), 1),
    ('.td-browse.is-closing 2', cnt(re.escape('.td-root.is-browse .td-browse.is-closing {')), 2),
    ('JS _browseT 出现 6 次', cnt(re.escape('_browseT')), 6),
    ("JS contains('is-closing') 2", cnt(re.escape("pane.classList.contains('is-closing')")), 2),
    # 2
    ('--td-desc-fade: 56px 1', cnt(re.escape('--td-desc-fade: 56px')), 1),
    ('--td-desc-fade: 0px 1', cnt(re.escape('--td-desc-fade: 0px')), 1),
    ('mask-image 2', cnt(re.escape('mask-image: linear-gradient')), 2),
    # 3
    ('dot 6px 1', cnt(re.escape('giencoder-badge-status-dot{border-radius:50%;width:6px;height:6px}')), 1),
    ('dot 8px 0', cnt(re.escape('giencoder-badge-status-dot{border-radius:50%;width:8px;height:8px}')), 0),
    # 5
    ('bar-nav svg 规则 1', cnt(re.escape('.td-bar-nav .td-iconbtn svg { width: 14px; height: 14px; }')), 1),
    # 6
    ('kb-crt-fld > popup 1', cnt(re.escape('.kb-crt-fld > .giencoder-select-popup { left: auto; right: 0; }')), 1),
    ('r52 那条仍在 1', cnt(re.escape('.td-composer .mt-auto .flex.items-center.gap-2 > .giencoder-select > .giencoder-select-popup { left: auto; right: 0; }')), 1),
    # 7
    ('date-picker-popup 规则 1', cnt(re.escape('.giencoder-date-picker-popup {\n        position: absolute')), 1),
    ('panel-open 1', cnt(re.escape('.giencoder-date-picker-popup.giencoder-panel-open {')), 1),
    ('calendar-cell 1', cnt(re.escape('.giencoder-calendar-cell {')), 1),
    ('calendar-grid 1', cnt(re.escape('.giencoder-calendar-grid { display: grid')), 1),
    ('calendar-cell-empty 1', cnt(re.escape('.giencoder-calendar-cell-empty { visibility: hidden; }')), 1),
    # 8
    ('td-bf 行圆角 1', cnt(re.escape('/* ★ 第 53 轮第 8 项：行本体补 4px 圆角。')), 1),
    # 不得误伤
    ('td-right-acts svg 14px 仍在 1', cnt(re.escape('.td-right-acts .td-round-btn svg { width: 14px; height: 14px; }')), 1),
    ('td-browse-add 28px 仍在 1', cnt(re.escape('.td-browse-bar .td-browse-ico { width: 28px; height: 28px; }')), 1),
    ('td-panel-line 仍在', cnt(re.escape('--td-panel-line: #DAE3ED;')), 1),
]

bad = []
for label, got, want in checks:
    if got != want:
        bad.append('   ✗ %-28s 实测 %s，期望 %s' % (label, got, want))

print('应用: %d 项 | 跳过(已应用): %d 项' % (len(applied), len(skipped)))
if applied:
    print('  应用:', '、'.join(applied))
if skipped:
    print('  跳过:', '、'.join(skipped))
print('')
if bad:
    print('!! 自检未通过 %d 条：' % len(bad))
    print('\n'.join(bad))
    sys.exit(1)
print('✅ 全部自检通过，文件 %d 字符（%d 字节，Δ%+d 字符）' % (
    len(s), len(s.encode('utf-8')), len(s) - bef))
