#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 56 轮（r54 收口）：Esc 让位 —— 右键菜单打开时不得连带收起文件浏览侧栏。

问题（r54 验收时暴露）：
  pages/task-detail.html 里早有一处「浏览态下按 Esc 收起侧栏」的**独立** keydown 监听：
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && root.classList.contains('is-browse')) setOpen(false);
      });
  它不参与页尾那条 Esc 优先级链，所以 r54 给链加的
      if (html.hasAttribute('data-td-ctx-open')) { dispatch('td:close-ctx'); return; }
  挡不住它 → 表现为：**右键菜单打开时按 Esc，菜单收了，整个文件侧栏也一起被收起**。

⚠️ 关键坑（前两版修法都失败的原因，务必看懂）：
  1) 链条与浏览侧栏监听**都在 document 冒泡段**，执行顺序＝注册顺序；
     浏览侧栏的监听是**首次打开侧栏时**才注册的 → 它必然晚于链条。
  2) 链条是第一个跑的：它 `dispatch('td:close-ctx')` → 菜单侧 `close()` → `flag(false)`
     **同步摘掉** `data-td-ctx-open`；随后 ctx 自己的 keydown 因 `open===false` 提前 return。
  3) 于是浏览侧栏监听无论「读状态位」还是「读菜单侧打的标记」都拿不到信息 → 照旧收侧栏。
  ⇒ 结论：**标记必须由链条自己打**（链条是最先决策的一环），而不是等菜单侧去补。

修法（与监听顺序无关）：
  · 链条 ctx 分支：`ev.__tdCtxHandled = true;` 放在 `dispatch` **之前**
  · 菜单侧 keydown（链条对 INPUT/TEXTAREA 会提前 return，这条是兜底）：同样先打标记
  · 浏览侧栏监听：`!e.__tdCtxHandled && !hasAttribute('data-td-ctx-open')`
  三条路径都不成立时才收起侧栏 ⇒ 菜单没开时 Esc 行为完全不变。

验证（agent-browser，file:// 直开）：
  开侧栏 → 树行 contextmenu → 派发 Escape →
  期望：菜单 opacity 0、`.td-browse` 宽度仍 944、`.td-browse-pre` rect 非零、HTML 状态位已摘。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET = os.path.join(ROOT, 'pages', 'task-detail.html')

# ---- ① 菜单侧 keydown：先打标记再 close()（行级锚点，注释保持原样）----
A_OLD = "if (e.key === 'Escape') { e.stopPropagation(); close(); return; }"
A_NEW = "if (e.key === 'Escape') { e.__tdCtxHandled = true; e.stopPropagation(); close(); return; }"

# ---- ② 浏览侧栏 keydown：加一条「事件已被菜单消费」的判断（行级插入）----
B_OLD = "              && !document.documentElement.hasAttribute('data-td-ctx-open')) setOpen(false);"
B_NEW = ("              && !e.__tdCtxHandled\n"
         "              && !document.documentElement.hasAttribute('data-td-ctx-open')) setOpen(false);")

# ---- ③ 页尾 Esc 链：先打标记再派发（关键的一环）----
C_OLD = "          document.dispatchEvent(new CustomEvent('td:close-ctx'));"
C_NEW = ("          /* ★ 必须**先打标记再派发**：链条注册最早、最先跑并会摘掉 data-td-ctx-open，\n"
         "             而浏览侧栏的 Esc 监听注册晚于链条 —— 只读状态位它会读到 false 而连带收侧栏。 */\n"
         "          ev.__tdCtxHandled = true;\n"
         "          document.dispatchEvent(new CustomEvent('td:close-ctx'));")

stats = []


def chk(name, got, exp):
    ok = got == exp
    stats.append(ok)
    print(f"{'OK  ' if ok else '!!FAIL'} {name} = {got}（期望 {exp}）")
    return ok


def sub1(s, label, old, new):
    """行级/块级锚点：先判 mark(=new) 再判 OLD；命中数不为 1 记 FAIL。"""
    n, o = s.count(new), s.count(old)
    if n == 1:
        print(f'SKIP task-detail · {label}')
        return s
    if o == 1:
        print(f'OK   task-detail · {label}')
        return s.replace(old, new, 1)
    print(f'!!FAIL task-detail · {label}：OLD={o} NEW={n}（期望恰好 1）')
    stats.append(False)
    return s


def main():
    with open(TARGET, encoding='utf-8') as f:
        s0 = f.read()
    s = s0

    s = sub1(s, '① 菜单侧 Esc 打标记', A_OLD, A_NEW)
    s = sub1(s, '② 浏览侧栏 Esc 让位', B_OLD, B_NEW)
    s = sub1(s, '③ Esc 链先打标记', C_OLD, C_NEW)

    stat0 = {k: s0.count(k) for k in ('<style', '</style>', '<script', '</script>',
                                      'class=\\"td-bf is-file', 'td-sec-head')}
    stat1 = {k: s.count(k) for k in stat0}
    print('---- 自检 ----')
    chk('标记写入点（菜单侧 + 链条）', s.count('__tdCtxHandled = true'), 2)
    chk('浏览侧栏读标记', s.count('&& !e.__tdCtxHandled'), 1)
    chk('链条派发点仍为 1', s.count("CustomEvent('td:close-ctx')"), 1)
    chk('状态位判断总数', s.count("hasAttribute('data-td-ctx-open')"), 2)
    for k in stat0:
        chk(f'计数不变 {k}', stat1[k], stat0[k])

    if not all(stats):
        print('---- 存在失败断言，未写盘 ----')
        return 1
    print('---- ALL PASS ----')

    if s != s0:
        with open(TARGET, 'w', encoding='utf-8') as f:
            f.write(s)
        print(f'task-detail 字符 {len(s0)} → {len(s)}')
    else:
        print('task-detail 无变化（幂等）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
