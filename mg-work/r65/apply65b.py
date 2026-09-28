# -*- coding: utf-8 -*-
"""r65b：模态弹窗几何收敛（首轮实测 vs 设计稿的 4 处偏差）

1) 头部实际高 28（关闭按钮撑高）→ 副标题 margin-top 4 变成"叠在 28 之后"，
   整条内容下移 4px。改为 margin: 0（副标题紧贴头部底边 = 设计稿 y48，正好比标题底 y44 低 4）。
2) 「当前任务」卡：DS 式 `border-box + 1px 描边` 让 16px 内距得到 80 高，设计稿 78
   （设计稿把描边算在框内 ⇒ 有效内距 15）。改 padding 15px 20px ⇒ 78，且标签/正文墨迹同时对齐。
3) 按钮：`.giencoder-btn` 的 `0 16px` 内距 + 1px 描边 ⇒ 62/90，设计稿 60/88。改 `0 15px`。
4) 关闭后焦点没回到「更多」按钮（run() 里先 close() 菜单，此时 activeElement 已是菜单行）。
   改为 open(key, trigger) 显式传入触发按钮。
"""
import io
import sys

PATH = 'pages/task-detail.html'
NEW = 'r65b'

SUBS = [
    ('① 副标题 margin',
     "      .td-modal-desc { margin: 4px 0 0;",
     "      .td-modal-desc { margin: 0;",
     ".td-modal-desc { margin: 0;"),

    ('② 当前任务卡内距',
     "        box-sizing: border-box; margin-top: 20px; padding: 16px 20px;\n        background: var(--color-fill-1);",
     "        box-sizing: border-box; margin-top: 20px; padding: 15px 20px;   /* 15 = 设计稿 78 高框内含 1px 描边 */\n        background: var(--color-fill-1);",
     "15 = 设计稿 78 高框内含 1px 描边"),

    ('③ 页脚按钮内距',
     "      .td-modal .giencoder-btn { border-radius: 6px; }",
     "      /* 页脚按钮：DS 默认 0 16px 内距 + 1px 描边 ⇒ 62/90，设计稿 60/88 ⇒ 收 1px（描边在设计稿里算在框内） */\n      .td-modal .giencoder-btn { padding: 0 15px; border-radius: 6px; }",
     "设计稿 60/88 ⇒ 收 1px"),

    ('④ open() 记录触发按钮',
     "    function open(key) {\n      if (cur || !CFG[key]) return;",
     "    function open(key, trigger) {\n      if (cur || !CFG[key]) return;",
     "function open(key, trigger)"),

    ('⑤ open() 赋值 back',
     "      back = document.activeElement;\n      cur = { key: key, root: root };",
     "      /* 触发按钮显式传入：更多菜单的 run() 会先 close() 菜单，此时 activeElement 已不是触发按钮 */\n      back = trigger || document.querySelector('[data-td-more]') || document.activeElement;\n      cur = { key: key, root: root };",
     "back = trigger || document.querySelector('[data-td-more]')"),

    ('⑥ run() 传入 btn',
     "      if (tdTaskModal) tdTaskModal.open(id);",
     "      if (tdTaskModal) tdTaskModal.open(id, btn);",
     "tdTaskModal.open(id, btn);"),
]


def main():
    s = io.open(PATH, encoding='utf-8').read()
    b0 = len(s.encode('utf-8'))
    tag0 = {t: s.count(t) for t in ['<style>', '</style>', '<script>', '</script>']}
    log = []
    for label, old, new, mark in SUBS:
        if mark in s:
            log.append('SKIP  ' + label + '（已应用）')
            continue
        n = s.count(old)
        if n != 1:
            log.append('!!FAIL ' + label + ' 锚点命中 ' + str(n) + ' 次（期望 1）')
            print('\n'.join(log)); sys.exit(1)
        s = s.replace(old, new, 1)
        log.append('OK    ' + label)
    tag1 = {t: s.count(t) for t in tag0}
    ok = True
    for t, v in tag0.items():
        if tag1[t] != v:
            log.append('!!FAIL 标签 ' + t + ' ' + str(v) + ' → ' + str(tag1[t])); ok = False
    if not ok:
        print('\n'.join(log)); sys.exit(1)
    io.open(PATH, 'w', encoding='utf-8').write(s)
    b1 = len(s.encode('utf-8'))
    log.append('写入完成  ' + str(b0) + ' → ' + str(b1) + ' 字节  (+' + str(b1 - b0) + ')')
    log.append('ALL PASS')
    print('\n'.join(log))


main()
