# -*- coding: utf-8 -*-
"""r109 第八拍补测 · 全站「下拉菜单家族」静态普查。

目的（对应邵先生指令 A）：
  「全局所有的下拉菜单的暗色模式没有统一，全部以基础工作台对话框『默认权限』的下拉菜单的暗色模式的配色为准。」
要证明「全部」被覆盖，先把全站每个下拉的**三态**取值枚举出来：
  ① 面板底（容器）  ② 选项 hover   ③ 选项选中
判据：任一取值若为**绝对字面色**（非 var）⇒ 暗色档不会翻转 ⇒ 违规；若全是 var ⇒ 自然随档翻转。

输出：按「页 × 家族」的分组表 + 违规清单。
"""
import io, os, re, sys

PAGES = ['base', 'conversation', 'avatar', 'automation', 'skills',
         'dev', 'kanban', 'req-kanban', 'settings', 'task-detail']
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

# 家族关键词：出现即认为是「下拉/菜单」类规则
FAMILY_KW = ['menu-item', 'select-option', 'dropdown', 'popup', 'menu',
             'item-hover', 'option', 'trigger', 'suggest']
# 三态判定
RE_HOVER = re.compile(r':hover[^{]*\{', re.S)
RE_SELECTED = re.compile(r'(-selected|\.is-selected|\[aria-selected)[^{]*\{', re.S)
RE_BG = re.compile(r'background(?:-color)?\s*:\s*([^;}]+)')
# 绝对字面色（排除 var()/transparent/inherit/currentColor/0 0/none/rgb(var(...))
RE_HARD = re.compile(r'(#[0-9a-fA-F]{3,8}\b|rgba?\(\s*\d)')
RE_VAR = re.compile(r'var\(\s*--')


def blocks(t):
    """产出 (block_id, tag, start, end, body)"""
    out, i, n = [], 0, 0
    for m in re.finditer(r'<(style|script)\b[^>]*>', t):
        tag = m.group(1)
        e = t.find('</' + tag + '>', m.end())
        if e < 0:
            continue
        out.append((n, tag, m.end(), e, t[m.end():e]))
        n += 1
    return out


def rules(css):
    """产出 (selector, body) —— 朴素按 } 切，够用（无嵌套）"""
    i = 0
    while True:
        b = css.find('{', i)
        if b < 0:
            break
        e = css.find('}', b)
        if e < 0:
            break
        sel = css[i:b].strip()
        # 丢掉 @media / @keyframes 之类的前导
        if sel and not sel.startswith('@'):
            yield sel, css[b + 1:e]
        i = e + 1


def main():
    rows = []          # (page, kind, selector, prop_value)
    hard = []          # 违规
    for pg in PAGES:
        p = os.path.join(ROOT, 'pages', pg + '.html')
        if not os.path.exists(p):
            continue
        t = io.open(p, encoding='utf-8', newline='').read()
        for bid, tag, s, e, body in blocks(t):
            if tag != 'style':
                continue
            for sel, rb in rules(body):
                low = sel.lower()
                if not any(k in low for k in FAMILY_KW):
                    continue
                if '--' in sel:            # 变量定义块，跳过
                    continue
                # 真下拉规则的判据：selector 里带 popup/menu/option/dropdown 且是类选择器
                if not re.search(r'\.(?:giencoder-|r\d+-)?[a-z-]*(?:popup|menu|option|dropdown|item)', low):
                    continue
                for m in RE_BG.finditer(rb):
                    val = m.group(1).strip()
                    kind = ('hover' if ':hover' in sel
                            else 'selected' if re.search(r'-selected|aria-selected|is-selected', sel)
                            else 'base')
                    rows.append((pg, kind, sel.replace('\n', ' ')[:90], val[:60]))
                    if RE_HARD.search(val) and not RE_VAR.search(val):
                        hard.append((pg, kind, sel.replace('\n', ' ')[:90], val[:60]))

    # 汇总：面板底（base & 选择器含 popup/menu 容器）
    print('=' * 78)
    print('A. 面板容器底（base 态，选择器含 popup / dropdown / menu 且非 item/option）')
    print('=' * 78)
    seen = set()
    for pg, kind, sel, val in rows:
        if kind != 'base':
            continue
        if not re.search(r'(popup|dropdown|menu)(?:[.\s]|$)', sel):
            continue
        if re.search(r'(item|option)', sel):
            continue
        k = re.sub(r'\s+', ' ', sel)
        if k in seen:
            continue
        seen.add(k)
        print('%-12s %-58s %s' % (pg, sel[:58], val))

    print()
    print('=' * 78)
    print('B. 选项 hover 底（全部）')
    print('=' * 78)
    seen = set()
    for pg, kind, sel, val in rows:
        if kind != 'hover':
            continue
        k = re.sub(r'\s+', ' ', sel)
        if k in seen:
            continue
        seen.add(k)
        print('%-12s %-58s %s' % (pg, sel[:58], val))

    print()
    print('=' * 78)
    print('C. 选项选中底（全部）')
    print('=' * 78)
    seen = set()
    for pg, kind, sel, val in rows:
        if kind != 'selected':
            continue
        k = re.sub(r'\s+', ' ', sel)
        if k in seen:
            continue
        seen.add(k)
        print('%-12s %-58s %s' % (pg, sel[:58], val))

    print()
    print('=' * 78)
    print('D. ★ 违规：取值是绝对字面色（非 var）⇒ 暗色档不翻转')
    print('=' * 78)
    if not hard:
        print('（无）')
    for pg, kind, sel, val in hard:
        print('%-12s %-10s %-50s %s' % (pg, kind, sel[:50], val))

    print()
    print('统计：规则取值 %d 条，绝对字面 %d 条' % (len(rows), len(hard)))
    return 1 if hard else 0


if __name__ == '__main__':
    sys.exit(main())
