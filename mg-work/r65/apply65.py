# -*- coding: utf-8 -*-
"""r65：任务详情页「取消任务 / 终止任务」模态弹窗（设计稿 1350:18230 / 1350:18236）

幂等：每条替换先判 MARK，命中即 SKIP；再判 OLD 必须恰好命中 expect 次。
自检：① 标签级计数（<style>/</style>/<script>/</script>）改前改后相等
      ② 声明 token 的「增量 == 插入串增量 − 被替换串增量」
      ③ 未被触碰的结构计数（.td-sec-head / .td-file / .td-more ）不变
"""
import io
import re
import sys

PATH = 'pages/task-detail.html'
NEW = 'r65'

CSS_MARK = '★ 第 65 轮：「取消任务 / 终止任务」模态弹窗'
JS_MARK = 'var tdTaskModal = null;'
RUN_MARK = '改为先收起菜单、再打开对应的模态弹窗'
REG_MARK = '    bindTaskModals();'

CSS_OLD = "      .td-more-label { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; }\n"

CSS_NEW = CSS_OLD + r"""      /* ★ 第 65 轮：「取消任务 / 终止任务」模态弹窗
         设计稿 1350:18230（取消任务）/ 1350:18236（终止任务），面板 480 宽。
         数值全部由 2× 设计稿截图实测（alpha 通道切边定面板矩形 + 角部区块 SSD 反查圆角，
         并先用浏览器渲染已知半径的控件做过偏差标定）：
           · 面板 480 / 圆角 16 / 内距 20 24 24 / 阴影 --shadow3-down / 遮罩 --color-mask-bg
           · 标题 16 · 600 · 行高 24 · text-1；副标题 14 · 行高 22 · gray-7
           · 关闭按钮 28×28（X 墨迹 10×10，色 gray-7）
           · 当前任务卡：内距 16/20、圆角 8、底 fill-1、描边 border-2（1 行卡高 78 / 2 行 100）
           · 分隔线：高 22，两侧 flex:1 的 1px 线(border-2)，gap 16
           · 输入框 432×88 / 内距 10 12 / 圆角 8 / 描边 border-2
           · 页脚按钮高 32、间距 8；圆角设计稿实测 6（DS .giencoder-btn 为 4 → 此处局部覆盖）
         注：设计稿两稿「卡片 ↔ 分隔线」间距不一致（取消稿 24 / 终止稿 8），本实现统一取 24。 */
      .td-modal { position: fixed; inset: 0; z-index: var(--z-index-modal); display: flex; align-items: center; justify-content: center; }
      .td-modal[hidden] { display: none; }
      .td-modal-mask { position: absolute; inset: 0; background: var(--color-mask-bg); opacity: 0; transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1); }
      .td-modal.is-open .td-modal-mask { opacity: 1; }
      .td-modal-panel {
        position: relative; box-sizing: border-box; overflow: auto;
        width: 480px; max-width: calc(100vw - 32px); max-height: calc(100vh - 32px);
        padding: 20px 24px 24px; outline: none;
        background: var(--color-bg-2); border-radius: 16px; box-shadow: var(--shadow3-down);
        opacity: 0; transform: translateY(4px) scale(.96);
        transition: opacity .15s cubic-bezier(0.34, 0.69, 0.1, 1), transform .15s cubic-bezier(0.34, 0.69, 0.1, 1);
      }
      .td-modal.is-open .td-modal-panel {
        opacity: 1; transform: translateY(0) scale(1);
        transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1), transform .2s var(--transition-timing-function-spring, cubic-bezier(0.34, 1.56, 0.64, 1));
      }
      .td-modal-head { display: flex; align-items: flex-start; justify-content: space-between; }
      .td-modal-title { flex: 1; min-width: 0; margin: 0; font-size: var(--font-size-title-1); line-height: 24px; font-weight: 600; color: var(--color-text-1); }
      .td-modal-close {
        flex: none; width: 28px; height: 28px; margin: 0; padding: 0; border: 0;
        display: inline-flex; align-items: center; justify-content: center;
        border-radius: var(--border-radius-medium); background: none; color: rgb(var(--gray-7)); cursor: pointer;
        transition: background 80ms, color 80ms;
      }
      .td-modal-close:hover { background: var(--color-fill-2); color: var(--color-text-2); }
      .td-modal-desc { margin: 4px 0 0; font-size: var(--font-size-body-3); line-height: 22px; color: rgb(var(--gray-7)); }
      .td-modal-task {
        box-sizing: border-box; margin-top: 20px; padding: 16px 20px;
        background: var(--color-fill-1); border: 1px solid var(--color-border-2);
        border-radius: var(--border-radius-large);
      }
      .td-modal-task-lbl { display: block; font-size: var(--font-size-body-1); line-height: 16px; color: var(--color-text-3); }
      .td-modal-task-tx { margin: 8px 0 0; font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-1); }
      .td-modal-sep { margin-top: 24px; height: 22px; display: flex; align-items: center; gap: 16px; font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-1); }
      .td-modal-sep::before, .td-modal-sep::after { content: ''; flex: 1; height: 1px; background: var(--color-border-2); }
      .td-modal-input {
        display: block; box-sizing: border-box; width: 100%; height: 88px; margin-top: 12px; padding: 10px 12px;
        border: 1px solid var(--color-border-2); border-radius: var(--border-radius-large); background: var(--color-bg-2);
        font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-1);
        outline: none; resize: none; transition: border-color var(--transition-duration-1);
      }
      .td-modal-input::placeholder { color: var(--color-text-3); }
      .td-modal-input:hover { border-color: var(--color-border-3); }
      .td-modal-input:focus { border-color: var(--color-primary-6); box-shadow: 0 0 0 2px var(--color-primary-light-2); }
      .td-modal-note { margin: 8px 0 0; font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-3); }
      .td-modal-foot { margin-top: 32px; display: flex; justify-content: flex-end; gap: 8px; }
      .td-modal .giencoder-btn { border-radius: 6px; }
      html.td-modal-lock, html.td-modal-lock body { overflow: hidden; }
"""

# ---------- JS：新增 bindTaskModals ----------
JS_OLD = "  function bindMoreMenu() {"

JS_NEW = r"""  /* ★ 第 65 轮：「取消任务 / 终止任务」模态弹窗
     两稿共用一套骨架，只有标题/说明/分隔文案/确认按钮文案不同。
     行为对齐 DS modal 契约：role=dialog + aria-modal、遮罩点击关闭、Esc 关闭、
     焦点锁在弹窗内（Tab 循环）、打开时锁定 body 滚动、关闭后焦点归还触发按钮。 */
  var tdTaskModal = null;
  function bindTaskModals() {
    var CFG = {
      cancel: {
        title: '取消任务',
        desc: '任务取消后将被标记为“已取消”状态，历史信息与本次原因会保留。',
        sep: '取消原因',
        note: '取消原因将被写入任务动态，保存后不可删除。',
        ok: '确定取消',
        done: '已取消任务：'
      },
      stop: {
        title: '终止任务',
        desc: '任务终止后将被标记为“已终止”状态，请说明停止推进的原因。',
        sep: '终止原因',
        note: '终止原因将被写入任务动态，保存后不可删除。',
        ok: '确定终止',
        done: '已终止任务：'
      }
    };
    /* 与 r59 下拉菜单同一套图标口径（viewBox 24 + stroke 2.2 放进 16px 框），
       端点 5.7..18.3 使 X 墨迹 ≈10px，与设计稿一致。 */
    var X_SVG = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M5.7 5.7 18.3 18.3"/><path d="M18.3 5.7 5.7 18.3"/></svg>';
    var boxes = {}, cur = null, back = null;

    function build(key) {
      var c = CFG[key];
      var root = document.createElement('div');
      root.className = 'td-modal';
      root.hidden = true;
      root.setAttribute('data-td-modal', key);
      root.innerHTML =
        '<div class="td-modal-mask"></div>' +
        '<div class="td-modal-panel" role="dialog" aria-modal="true" tabindex="-1" aria-labelledby="td-modal-t-' + key + '">' +
          '<div class="td-modal-head">' +
            '<h2 class="td-modal-title" id="td-modal-t-' + key + '">' + c.title + '</h2>' +
            '<button class="td-modal-close" type="button" aria-label="关闭">' + X_SVG + '</button>' +
          '</div>' +
          '<p class="td-modal-desc">' + c.desc + '</p>' +
          '<div class="td-modal-task">' +
            '<span class="td-modal-task-lbl">当前任务</span>' +
            '<p class="td-modal-task-tx"></p>' +
          '</div>' +
          '<div class="td-modal-sep"><span>' + c.sep + '</span></div>' +
          '<textarea class="td-modal-input" placeholder="请输入" aria-label="' + c.sep + '"></textarea>' +
          '<p class="td-modal-note">' + c.note + '</p>' +
          '<div class="td-modal-foot">' +
            '<button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default td-modal-no" type="button">取消</button>' +
            '<button class="giencoder-btn giencoder-btn-danger giencoder-btn-size-default td-modal-yes" type="button">' + c.ok + '</button>' +
          '</div>' +
        '</div>';
      root._panel = root.querySelector('.td-modal-panel');
      root._input = root.querySelector('.td-modal-input');
      root._tx = root.querySelector('.td-modal-task-tx');
      root._mask = root.querySelector('.td-modal-mask');
      root._close = root.querySelector('.td-modal-close');
      root._yes = root.querySelector('.td-modal-yes');
      root._no = root.querySelector('.td-modal-no');
      document.body.appendChild(root);

      root._mask.addEventListener('click', close);
      root._close.addEventListener('click', close);
      root._no.addEventListener('click', close);
      root._yes.addEventListener('click', confirm);
      root.addEventListener('keydown', function (e) {
        if (e.key !== 'Tab') return;
        var list = Array.prototype.filter.call(
          root._panel.querySelectorAll('button, textarea, [href], [tabindex]:not([tabindex="-1"])'),
          function (el) { return !el.disabled && el.offsetParent !== null; });
        if (!list.length) return;
        var first = list[0], last = list[list.length - 1], act = document.activeElement;
        if (e.shiftKey && (act === first || act === root._panel)) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && act === last) { e.preventDefault(); first.focus(); }
      });
      return root;
    }

    function open(key) {
      if (cur || !CFG[key]) return;
      var root = boxes[key] || (boxes[key] = build(key));
      var t = document.querySelector('.td-title');
      root._tx.textContent = (t && t.textContent ? t.textContent : '当前任务').trim() || '当前任务';
      root._input.value = '';
      back = document.activeElement;
      cur = { key: key, root: root };

      root.hidden = false;
      void root.offsetHeight;                 /* 先落定初始样式，再加类才有过渡 */
      root.classList.add('is-open');
      document.documentElement.classList.add('td-modal-lock');
      try { root._panel.focus({ preventScroll: true }); } catch (e) {}
      setTimeout(function () { if (cur && cur.root === root) { try { root._input.focus(); } catch (e) {} } }, 190);
    }

    function close() {
      if (!cur) return;
      var root = cur.root;
      cur = null;
      root.classList.remove('is-open');
      document.documentElement.classList.remove('td-modal-lock');
      setTimeout(function () { if (!cur) root.hidden = true; }, 220);
      var b = back; back = null;
      if (b && b.focus) { try { b.focus({ preventScroll: true }); } catch (e) {} }
    }

    function confirm() {
      if (!cur) return;
      var c = CFG[cur.key];
      var t = document.querySelector('.td-title');
      var name = (t && t.textContent ? t.textContent : '当前任务').trim() || '当前任务';
      var reason = cur.root._input.value.trim();
      close();
      tdToast(c.done + name + (reason ? '（原因：' + reason + '）' : ''));
    }

    /* Esc：捕获段最优先，关完就 stopPropagation，避免页尾 Esc 链继续处理其它浮层 */
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !cur) return;
      e.preventDefault();
      e.stopPropagation();
      close();
    }, true);

    tdTaskModal = { open: open, close: close, isOpen: function () { return !!cur; } };
  }

  function bindMoreMenu() {"""

# ---------- JS：run() 改为打开弹窗 ----------
RUN_OLD = """    function run(id) {
      var t = document.querySelector('.td-title');
      var name = t && t.textContent ? t.textContent.trim() : '当前任务';
      close();
      if (id === 'stop') { tdToast('已终止任务：' + name); return; }
      if (id === 'cancel') { tdToast('已取消任务：' + name); return; }
    }
"""

RUN_NEW = """    function run(id) {
      /* ★ 第 65 轮：选中「终止任务 / 取消任务」后不再直接弹提示，
         改为先收起菜单、再打开对应的模态弹窗（设计稿 1350:18236 / 1350:18230）。
         弹窗确认后才写提示，文案与 r59 保持一致。 */
      close();
      if (tdTaskModal) tdTaskModal.open(id);
    }
"""

REG_OLD = "    bindMoreMenu();\n"
REG_NEW = "    bindMoreMenu();\n" + REG_MARK + "\n"

TOKENS = ['td-modal', 'tdTaskModal', 'bindTaskModals', 'td-modal-lock', 'data-td-modal', 'td-modal-yes']


def main():
    s = io.open(PATH, encoding='utf-8').read()
    before_bytes = len(s.encode('utf-8'))
    tag_before = {t: s.count(t) for t in ['<style>', '</style>', '<script>', '</script>']}
    struct_before = {t: s.count(t) for t in ['.td-sec-head', '.td-file', '.td-more', 'giencoder-dropdown-item']}
    tok_before = {t: s.count(t) for t in TOKENS}
    log = []
    applied = []

    def sub1(label, old, new, mark):
        nonlocal s
        if mark in s:
            log.append('SKIP  ' + label + '（已应用）')
            return
        n = s.count(old)
        if n != 1:
            log.append('!!FAIL ' + label + ' 锚点命中 ' + str(n) + ' 次（期望 1）')
            log.append('DONE_FAIL')
            print('\n'.join(log))
            sys.exit(1)
        s = s.replace(old, new, 1)
        applied.append((old, new))
        log.append('OK    ' + label)

    sub1('CSS 弹窗样式块', CSS_OLD, CSS_NEW, CSS_MARK)
    sub1('JS bindTaskModals()', JS_OLD, JS_NEW, JS_MARK)
    sub1('JS run() 改为开弹窗', RUN_OLD, RUN_NEW, RUN_MARK)
    sub1('inject() 注册', REG_OLD, REG_NEW, REG_MARK)

    # --- 自检 ---
    ok = True
    tag_after = {t: s.count(t) for t in tag_before}
    for t, v in tag_before.items():
        if tag_after[t] != v:
            log.append('!!FAIL 标签 ' + t + ' 计数 ' + str(v) + ' → ' + str(tag_after[t]))
            ok = False
    struct_after = {t: s.count(t) for t in struct_before}
    for t, v in struct_before.items():
        if struct_after[t] != v:
            log.append('!!FAIL 结构 ' + t + ' 计数 ' + str(v) + ' → ' + str(struct_after[t]))
            ok = False
    # 声明增量：每条「已实际应用」的替换的「插入串 − 被替换串」之和
    pairs = [(old, new) for old, new in applied]
    for t in TOKENS:
        exp = sum(new.count(t) - old.count(t) for old, new in pairs)
        got = s.count(t) - tok_before[t]
        if got != exp:
            log.append('!!FAIL token ' + t + ' 增量 ' + str(got) + ' ≠ 声明 ' + str(exp))
            ok = False
        else:
            log.append('ok    token ' + t + ' 增量 ' + str(got) + ' == 声明')
    if not ok:
        log.append('DONE_FAIL')
        print('\n'.join(log))
        sys.exit(1)

    io.open(PATH, 'w', encoding='utf-8').write(s)
    after_bytes = len(s.encode('utf-8'))
    log.append('写入完成  ' + str(before_bytes) + ' → ' + str(after_bytes) + ' 字节  (+' + str(after_bytes - before_bytes) + ')')
    log.append('ALL PASS')
    print('\n'.join(log))


main()
