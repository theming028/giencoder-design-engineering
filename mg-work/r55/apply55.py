#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 55 轮（r54 收口）：子菜单顶边对齐修正。

依据：
  · DS 契约 /.giencoder-dropdown-submenu-popup => left: calc(100% + 4px); top: 0;
    即子菜单顶边 == 父项（item）顶边，不做额外偏移。
  · 设计稿导出图 容器-171_1350-18294.png（856x924，2x）实测：
      主菜单卡片 432..795 x 46..493（图 px）→ 182 x 224 设计 px
      「打开方式」行 hover 底 y 417..482        → 项高 32 设计 px
      子菜单卡片顶边 y = 415  → 与父项顶边(417) 相差 -2 图 px ≈ -1 设计 px
    结论：子菜单 top 应 ≈ 父项 top（0 偏移）；r54 实现里的 -6 使顶边高出 6px，需去掉。

同时把左偏移的魔数 4 命名化，避免后续误改。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET = os.path.join(ROOT, 'pages', 'task-detail.html')

OLD = 'var left = r.right + 4, top = r.top - 6;'
NEW = 'var left = r.right + 4, top = r.top;   /* DS 契约 submenu-popup: left calc(100%+4px) / top 0 */'

# 第二项：气泡宽度口径修正（border-box）。
#   设计稿导出图 856x924（2x）实测边框像素（226..232 灰阶）：
#     主菜单卡片 x 432..795  → 364 图 px = 182 设计 px（含左右各 1px 边框）
#     子菜单卡片 x  60..423  → 364 图 px = 182 设计 px（同上）
#   即 border-box = 182、内容区 = 180。r54 把「180」直接写成 width（默认 border-box），
#   导致内容区只有 178：item 166（应 168）。改为 182 后 item = 168，与设计稿 hover 底实测一致。
OLD2 = '        box-sizing: border-box; min-width: 0; width: 180px; padding: 6px;'
NEW2 = '        box-sizing: border-box; min-width: 0; width: 182px; padding: 6px;'

stats = []


def chk(name, got, exp):
    ok = got == exp
    stats.append(ok)
    print(f"{'OK  ' if ok else '!!FAIL'} {name} = {got}（期望 {exp}）")
    return ok


def sub1(s, label, old, new):
    """先判 mark(=new) 再判 OLD；命中数不为 1 则该步记 FAIL。"""
    n_new, n_old = s.count(new), s.count(old)
    if n_new == 1:
        print(f'SKIP task-detail · {label}（已应用）')
        return s
    if n_old == 1:
        print(f'OK   task-detail · {label}')
        return s.replace(old, new, 1)
    print(f'!!FAIL task-detail · {label}：锚点命中 OLD={n_old} NEW={n_new}（期望恰好 1）')
    stats.append(False)
    return s


def main():
    with open(TARGET, encoding='utf-8') as f:
        s0 = f.read()
    s = s0

    s = sub1(s, '子菜单顶边对齐（-6 → 0，对齐 DS top:0）', OLD, NEW)
    s = sub1(s, '气泡宽度 180 → 182（border-box 口径）', OLD2, NEW2)

    # 标签级 / 业务锚点计数（只断言"不变"，不写死数值）
    stat0 = {k: s0.count(k) for k in ('<style', '</style>', '<script', '</script>',
                                      'class=\\"td-bf is-file', 'td-sec-head')}
    stat1 = {k: s.count(k) for k in stat0}
    print('---- 自检 ----')
    chk('OBSOLETE 残留 (r.top - 6)', s.count(OLD), 0)
    chk('NEW 锚点 top', s.count(NEW), 1)
    chk('OBSOLETE 残留 (width: 180px)', s.count(OLD2), 0)
    chk('NEW 锚点 width 182', s.count(NEW2), 1)
    for k in stat0:
        chk(f'计数不变 {k}', stat1[k], stat0[k])

    if all(stats):
        print('---- ALL PASS ----')
    else:
        print('---- 存在失败断言，未写盘 ----')
        return 1

    if s != s0:
        with open(TARGET, 'w', encoding='utf-8') as f:
            f.write(s)
        print(f'task-detail 字符 {len(s0)} → {len(s)}')
    else:
        print('task-detail 无变化（幂等）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
