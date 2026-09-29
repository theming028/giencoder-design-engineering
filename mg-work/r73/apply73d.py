# -*- coding: utf-8 -*-
"""
第 73 轮 · 补丁 d（需求 3：顶栏 tablist 的 tab 切换「跨页接力滑动」，9 页）

【背景取证】
  顶栏只有 2 个页签：`base`（基础工作台）/ `dev`（研发工作台）。
  外壳组件 On() 里滑块 `span[aria-hidden]` 的几何：
     useLayoutEffect → h(activeTab) → { left: btn.offsetLeft, width: btn.offsetWidth }
     内联样式：transition: left .2s cubic-bezier(.34,1.56,.64,1), width .2s 同曲线
  ⇒ **同页内本来就有弹簧滑动**。但它在 file:// 下永远播不出来：
     页尾「页签跳转兜底」在 document **捕获阶段** stopPropagation() + location.href 直接跳页，
     React 的 onClick（内含 setTimeout(navigate,200)「先滑再跳」）根本收不到事件。
     用户看到的「没有动效」= 目标页冷启动时滑块直接**出现在终点**。

【⚠️ 关键教训（本轮踩到的坑，务必记住）】
  第一次排查时我读的是 `span.style.left`（**内联**值），得出「task-detail 滑块错位」的结论 —— **错的**。
  task-detail.html 里另有一条上一轮留下的 CSS：
      body:has(.td-wrap) [role="tablist"] > span[aria-hidden] { left:62px !important; width:124px !important }
  它用 !important 把滑块**钉**在 dev 位（同时另两条钉了文字色），
  所以 React 内联值虽然停在 2px，**渲染位置其实一直是对的**。
  ⇒ 结论：判断视觉位置必须看 `getBoundingClientRect()` / `getComputedStyle()`，
    **不能看 `element.style.*`**（内联样式可能被 !important 规则压掉）。
  因此本块**不做任何「纠偏/对齐」**，只加动效。

【做法 —— 跨页接力，用 translate 叠加，不跟 !important 抢 left/width】
  ① 出发页（window 捕获，早于 document 捕获的跳转兜底）：把滑块的**渲染矩形** left/width
     与当前选中页签 key 存进 sessionStorage（带时间戳，10s 内有效）。
  ② 到达页：算出「出发位置 - 当前目标位置」的位移 dx，先 `transition:none` + `translate: dx 0`
     把滑块**摆到出发位置**，隔两帧把过渡交还并 `translate: 0 0` ⇒ 滑块从上一个页签滑过来。
  ③ 为什么用 translate 而不是改 left/width：
     task-detail 的 `left/width` 被 `!important` 钉死，内联值写不动它（!important 压内联）。
     而 translate 不在那些规则里 ⇒ **同一套逻辑在 9 页都成立**，也不用去动上一轮留下的钉位规则。

【为什么用 sessionStorage】
  file:// 下 `origin` 是 "file://"，实测 sessionStorage 可读写，且**跨页面导航保持**
  （agent-browser 实测：base.html 写入 → dev.html 读到）。http://127.0.0.1 预览同源同样可用；
  不可用时 try/catch 静默降级为「无接力」（= 现状，不报错）。

【不动 React】React 的 style 对象是 {left,width,transform,transition,opacity}，**不含 translate**，
  所以本块写的 translate 不会被 React 回写；但 transition 必须交还（React 认为值没变不会重写），
  否则之后的 left/width 变化将失去弹簧过渡。

幂等三要素：MARK 命中即 SKIP；锚点 `</body>` 必须恰好 1 次；跑完立刻复跑验幂等。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r73d-backup'
PAGES = 'pages'

MARK = '<script id="r73-tab-relay">'
ANCHOR = '</body>'

NEW = (
    '<script id="r73-tab-relay">\n'
    '/* SHELL-TAB-RELAY v1 —— 顶栏页签「跨页接力滑动」（勿手改此块）\n'
    '   出发页记下滑块的渲染位置 → 到达页先用 translate 摆回旧位置、再滑到目标。\n'
    '   用 translate 叠加而非改 left/width：本仓库 task-detail 的滑块位置被一条\n'
    '   !important 规则钉死，内联 left/width 写不动它，translate 不在其管辖范围内。 */\n'
    '(function () {\n'
    '  var KEY = "r73-tab-relay";\n'
    '  var TLS = \'[role="tablist"][aria-label="工作台切换"]\';\n'
    '  var SPRING = "cubic-bezier(.34,1.56,.64,1)";\n'
    '  var TRANS = "left .2s " + SPRING + ", width .2s " + SPRING + ", translate .2s " + SPRING;\n'
    '  var TTL = 10000;\n'
    '\n'
    '  function pick() {\n'
    '    var tl = document.querySelector(TLS);\n'
    '    if (!tl) return null;\n'
    '    var sp = tl.querySelector("span[aria-hidden]");\n'
    '    var cur = tl.querySelector(\'[data-tab][aria-selected="true"]\');\n'
    '    if (!sp || !cur) return null;\n'
    '    return { tl: tl, sp: sp, key: cur.getAttribute("data-tab") };\n'
    '  }\n'
    '\n'
    '  /* ---------- A. 出发页：记下滑块的**渲染**几何 ---------- */\n'
    '  window.addEventListener("click", function (e) {\n'
    '    var t = e.target;\n'
    '    var btn = t && t.closest ? t.closest(TLS + " [data-tab]") : null;\n'
    '    if (!btn) return;\n'
    '    var o = pick();\n'
    '    if (!o) return;\n'
    '    if (btn.getAttribute("data-tab") === o.key) return; /* 点的是当前页签：不记 */\n'
    '    var r = o.sp.getBoundingClientRect();\n'
    '    if (!(r.width > 0)) return;\n'
    '    try {\n'
    '      sessionStorage.setItem(KEY, JSON.stringify({\n'
    '        from: o.key, left: r.left, width: r.width, t: Date.now()\n'
    '      }));\n'
    '    } catch (err) { /* 存储不可用则静默：退化为无接力 */ }\n'
    '  }, true);\n'
    '\n'
    '  /* ---------- B. 到达页：摆回出发位置，再滑到目标 ---------- */\n'
    '  var from = null;\n'
    '  try {\n'
    '    var raw = sessionStorage.getItem(KEY);\n'
    '    if (raw) { sessionStorage.removeItem(KEY); from = JSON.parse(raw); }\n'
    '  } catch (e) { from = null; }\n'
    '  if (from && (!(from.width > 0) || Date.now() - from.t > TTL)) from = null;\n'
    '  if (!from) return;\n'
    '\n'
    '  var booted = false;\n'
    '  function boot() {\n'
    '    if (booted) return true;\n'
    '    var o = pick();\n'
    '    if (!o) return false;\n'
    '    booted = true;\n'
    '    if (o.key === from.from) return true;          /* 刷新 / 点的就是当前页签：不接力 */\n'
    '    var now = o.sp.getBoundingClientRect();\n'
    '    if (!(now.width > 0)) return true;\n'
    '    var dx = Math.round((from.left - now.left) * 100) / 100;\n'
    '    if (Math.abs(dx) < 1) return true;             /* 位置一样：无位移可演 */\n'
    '\n'
    '    o.sp.style.transition = "none";\n'
    '    o.sp.style.translate = dx + "px 0px";          /* ① 摆到出发页签的位置（不带动画）*/\n'
    '    requestAnimationFrame(function () {\n'
    '      requestAnimationFrame(function () {\n'
    '        o.sp.style.transition = TRANS;             /* ② 交还过渡 */\n'
    '        o.sp.style.translate = "0px 0px";          /*    并滑回自己的目标位 */\n'
    '      });\n'
    '    });\n'
    '    return true;\n'
    '  }\n'
    '\n'
    '  /* 外壳是 React 异步挂载：先直接试，未就绪则等滑块出现 */\n'
    '  function schedule() {\n'
    '    requestAnimationFrame(function () {\n'
    '      if (boot()) return;\n'
    '      var mo = new MutationObserver(function () { if (boot()) mo.disconnect(); });\n'
    '      mo.observe(document.body, { childList: true, subtree: true });\n'
    '    });\n'
    '  }\n'
    '  if (document.readyState === "loading") {\n'
    '    document.addEventListener("DOMContentLoaded", schedule);\n'
    '  } else {\n'
    '    schedule();\n'
    '  }\n'
    '})();\n'
    '</script>\n'
)

# 自检唯一片段
U1 = 'var KEY = "r73-tab-relay";'
U2 = 'sessionStorage.setItem(KEY, JSON.stringify({'
U3 = 'o.sp.style.translate = dx + "px 0px";'
U4 = 'o.sp.style.translate = "0px 0px";'
U5 = 'if (document.readyState === "loading") {'
U6 = 'var TRANS = "left .2s " + SPRING + ", width .2s " + SPRING + ", translate .2s " + SPRING;'
U7 = 'var r = o.sp.getBoundingClientRect();'


def files():
    return [f for f in sorted(os.listdir(os.path.join(ROOT, PAGES))) if f.endswith('.html')]


def load(name):
    with io.open(os.path.join(ROOT, PAGES, name), encoding='utf-8') as f:
        return f.read()


def save(name, s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    src = os.path.join(ROOT, PAGES, name)
    dst = os.path.join(BACKUP, name)
    if not os.path.exists(dst):
        with io.open(src, encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(src, 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    for bad in ('</body', '</html'):
        if bad in payload:
            sys.exit('!! 元守卫失败：%s 载荷含 %s' % (label, bad))
    if payload.count('<script') != 1 or payload.count('</scr' + 'ipt>') != 1:
        sys.exit('!! 元守卫失败：%s 载荷的 script 标签不是一进一出' % label)


def main():
    guard('接力块', NEW)

    applied, skipped, failed = [], [], []
    for name in files():
        s = load(name)
        if MARK in s:
            skipped.append(name)
            continue
        n = s.count(ANCHOR)
        if n != 1:
            failed.append('%s: %s 命中 %d 次' % (name, ANCHOR, n))
            continue
        before = s
        s = s.replace(ANCHOR, NEW + ANCHOR)
        for tag in ('<script', '</script>', '<style', '</style>'):
            d = s.count(tag) - before.count(tag)
            expect = 1 if tag in ('<script', '</script>') else 0
            if d != expect:
                failed.append('%s: 标签计数 %s Δ%d（期望 Δ%d）' % (name, tag, d, expect))
                break
        else:
            save(name, s)
            applied.append(name)

    print('应用: %d 页 | 跳过: %d 页 | 失败: %d 页' % (len(applied), len(skipped), len(failed)))
    if applied:
        print('  已改: ' + ', '.join(applied))
    if skipped:
        print('  已就位: ' + ', '.join(skipped))
    for f in failed:
        print('  ✗ ' + f)
    if failed:
        sys.exit(1)

    # ================= 自检 =================
    print('\n--- 自检 ---')
    checks = []
    for name in files():
        t = load(name)
        checks.append(('%s: 本块恰好 1 个' % name, t.count(MARK) == 1))
        checks.append(('%s: 接力键名在位' % name, t.count(U1) == 1))
        checks.append(('%s: 出发页记录在位' % name, t.count(U2) == 1))
        checks.append(('%s: 出发位置取渲染矩形' % name, t.count(U7) == 1))
        checks.append(('%s: 到达页位移摆位在位' % name, t.count(U3) == 1))
        checks.append(('%s: 到达页滑回目标在位' % name, t.count(U4) == 1))
        checks.append(('%s: 就绪分支在位' % name, t.count(U5) == 1))
        checks.append(('%s: 过渡串在位' % name, t.count(U6) == 1))
        checks.append(('%s: 锚点仍唯一' % name, t.count(ANCHOR) == 1))
        body = t.split(MARK, 1)[1].split('</scr' + 'ipt>', 1)[0]
        checks.append(('%s: 块内无重复闭合标签' % name, body.count('</scr' + 'ipt') == 0))
        checks.append(('%s: 未擅自改渲染位置（不写内联 left）' % name, 'style.left =' not in body))
    ok = 0
    for nm, cond in checks:
        if cond:
            ok += 1
        else:
            print('  ✗ %s' % nm)
    print('自检：%d/%d 通过' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
