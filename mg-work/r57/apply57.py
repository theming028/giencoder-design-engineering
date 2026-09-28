# -*- coding: utf-8 -*-
"""r57：两处 hover 底色深一级（fill-1 → fill-2）

用户需求：
  ① 右键菜单 item 的 hover 背景色浅了，需要深一级；
  ② 「td-browse-files」的 item 的 hover 背景色同样处理。

色阶依据（页面内联 token + DS tokens）：
  --color-fill-1 = rgb(var(--gray-1)) = rgb(247,247,247) = #F7F7F7  ← 原值
  --color-fill-2 = rgb(var(--gray-2)) = rgb(242,242,242) = #F2F2F2  ← 目标「深一级」
  （fill-2 同时是页面内外壳 DS Dropdown 组件自身 hover 的档位：hover:bg-[var(--color-fill-2)]）

改动清单（均只存在于 pages/task-detail.html，各 1 处）：
  A. .td-bf:hover                              background: fill-1 → fill-2
  B. .td-ctx .giencoder-dropdown-item:hover /
     .td-ctx .giencoder-dropdown-item.is-hover  background: fill-1 → fill-2
 注释：.td-ctx .giencoder-dropdown-item-disabled:hover { background: transparent; } 不动。

自检口径（按记忆铁律）：
  ① 标签级计数（<style>/</style>/<script>/</script>）改前改后相等；
  ② 本改动对象的精确增减量：--color-fill-1 恰好 −2、--color-fill-2 恰好 +2。
  不做「全文件关键词总数 = N」这类脆弱断言。
"""

import io
import sys

TARGET = 'pages/task-detail.html'

# ---- A：文件树行 hover ----
A_OLD = "      .td-bf:hover { background: var(--color-fill-1); }"
A_NEW = ("      /* ★ 第 57 轮：hover 底色由 fill-1 深一级到 fill-2（#F7F7F7 → #F2F2F2）。 */\n"
         "      .td-bf:hover { background: var(--color-fill-2); }")

# ---- B：右键菜单 item hover ----
B_OLD = ("      .td-ctx .giencoder-dropdown-item:hover,\n"
         "      .td-ctx .giencoder-dropdown-item.is-hover { background: var(--color-fill-1); }")
B_NEW = ("      /* ★ 第 57 轮：hover 底色由 fill-1 深一级到 fill-2（#F7F7F7 → #F2F2F2），\n"
         "         与页面内外壳 DS Dropdown 组件自身的 hover 档位一致。 */\n"
         "      .td-ctx .giencoder-dropdown-item:hover,\n"
         "      .td-ctx .giencoder-dropdown-item.is-hover { background: var(--color-fill-2); }")

stats = []


def chk(name, got, exp):
    ok = got == exp
    stats.append(ok)
    print(f"{'OK  ' if ok else '!!FAIL'} {name} = {got}（期望 {exp}）")
    return ok


def sub1(s, label, old, new, applied):
    """幂等替换：先判 new（已应用）再判 old（待应用），返回 (新串, 是否应用)"""
    n_new, n_old = s.count(new), s.count(old)
    if n_new == 1 and n_old == 0:
        print(f'SKIP {label}（已应用）')
        return s, False
    if n_new == 0 and n_old == 1:
        print(f'OK   {label}')
        return s.replace(old, new, 1), True
    print(f'!!FAIL {label}：锚点命中 new={n_new} old={n_old}（期望恰好其一为 1）')
    stats.append(False)
    return s, False


def main():
    with io.open(TARGET, encoding='utf-8') as f:
        s0 = f.read()
    s = s0

    tag_keys = ('<style', '</style>', '<script', '</script>')
    stat0 = {k: s0.count(k) for k in tag_keys}
    f1_0 = s0.count('--color-fill-1')
    f2_0 = s0.count('--color-fill-2')

    print('---- 替换 ----')
    s, ap_a = sub1(s, 'A 文件树行 .td-bf:hover', A_OLD, A_NEW, None)
    s, ap_b = sub1(s, 'B 右键菜单 item hover', B_OLD, B_NEW, None)

    if s != s0:
        with io.open(TARGET, 'w', encoding='utf-8') as f:
            f.write(s)
        print(f'已写入 {TARGET}')
    else:
        print('内容无变化，未写入')

    applied = 1 if (ap_a or ap_b) else 0

    print('---- 自检 ----')
    chk('A 目标态存在', s.count("      .td-bf:hover { background: var(--color-fill-2); }"), 1)
    chk('A 旧态残留', s.count(A_OLD), 0)
    chk('B 目标态存在',
        s.count(".td-ctx .giencoder-dropdown-item.is-hover { background: var(--color-fill-2); }"), 1)
    chk('B 旧态残留', s.count(B_OLD), 0)
    chk('disabled 行仍为 transparent（未被波及）',
        s.count('.td-ctx .giencoder-dropdown-item-disabled:hover { background: transparent; }'), 1)
    chk('--color-fill-1 精确增减量', s.count('--color-fill-1'), f1_0 - 2 * applied)
    chk('--color-fill-2 精确增减量', s.count('--color-fill-2'), f2_0 + 2 * applied)
    for k in tag_keys:
        chk(f'标签级计数不变 {k}', s.count(k), stat0[k])

    print()
    if all(stats):
        print('---- ALL PASS ----')
        return 0
    print('---- HAS FAILURE ----')
    return 1


if __name__ == '__main__':
    sys.exit(main())
