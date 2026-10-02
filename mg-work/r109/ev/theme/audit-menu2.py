# -*- coding: utf-8 -*-
"""r109 第八拍补测 · 下拉菜单项「浅/暗双档」精确矩阵审计。

区别于 audit-menu.py（只看单条规则）：本器把每条规则判为**浅色档**或**暗色档**
（暗色档 = 选择器以 html[giencoder-theme='dark'] 开头），再按「目标选择器」配对，
输出「同一目标的浅色值 vs 暗色值」，从而直接看出：
  ① 暗色档有没有被显式统一（覆盖）
  ② 暗色档最终值是否 == 基准（.perm-menu-item 的暗色值）

基准（邵先生指定）：基础工作台对话框「默认权限」下拉的暗色配色 = .perm-menu-item 的暗色 hover。
"""
import io, os, re, sys, collections

PAGES = ['base', 'conversation', 'avatar', 'automation', 'skills',
         'dev', 'kanban', 'req-kanban', 'settings', 'task-detail']
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

DARK_PREFIX = re.compile(r"^html\[giencoder-theme='dark'\]\s*", re.I)
# 「下拉菜单项」判据
TARGET = re.compile(r'(?:menu-item|dropdown-item|select-option|submenu-title|popup-btn|menu-item)\b')
RE_BG = re.compile(r'background(?:-color)?\s*:\s*([^;}]+)')


def styles(t):
    out = []
    for m in re.finditer(r'<style\b[^>]*>', t):
        e = t.find('</style>', m.end())
        if e > 0:
            out.append(t[m.end():e])
    return out


def rules(css):
    nc = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    i = 0
    while True:
        b = nc.find('{', i)
        if b < 0:
            break
        e = nc.find('}', b)
        if e < 0:
            break
        sel = ' '.join(nc[i:b].split())
        if sel and not sel.startswith('@'):
            yield sel, ' '.join(nc[b + 1:e].split())
        i = e + 1


def main():
    # key = (page, target_sel) -> {'light':[vals], 'dark':[vals]}
    mat = collections.OrderedDict()
    for pg in PAGES:
        p = os.path.join(ROOT, 'pages', pg + '.html')
        if not os.path.exists(p):
            continue
        t = io.open(p, encoding='utf-8', newline='').read()
        for css in styles(t):
            for sel, body in rules(css):
                if ':hover' not in sel:
                    continue
                if '--' in sel and 'var(' not in sel:
                    continue
                isdark = bool(DARK_PREFIX.match(sel))
                tgt = DARK_PREFIX.sub('', sel).strip()
                # 提取「目标里的类名」判据
                if not TARGET.search(tgt):
                    continue
                vals = [v.strip() for v in RE_BG.findall(body) if v.strip()
                        and 'none' not in v and v.strip() != '0 0']
                if not vals:
                    continue
                k = (pg, tgt)
                d = mat.setdefault(k, {'light': [], 'dark': []})
                d['dark' if isdark else 'light'].extend(vals)

    def ishard(v):
        return re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(\s*\d', v) and not re.search(r'var\(', v)

    print('=' * 118)
    print('下拉菜单项 hover · 浅/暗双档矩阵   （基准 = .perm-menu-item → --color-fill-2）')
    print('=' * 118)
    print('%-11s %-52s %-30s %-30s %s' % ('页', '目标选择器', '浅色档值', '暗色档值', '判定'))
    print('-' * 118)
    hard = []
    for (pg, tgt), d in mat.items():
        L = ' / '.join(dict.fromkeys(d['light'])) or '（继承基础规则）'
        D = ' / '.join(dict.fromkeys(d['dark'])) or '（继承基础规则）'
        verdict = 'OK'
        if any(ishard(v) for v in d['light'] + d['dark']):
            verdict = '★硬编码'
            hard.append((pg, tgt, L, D))
        print('%-11s %-52s %-30s %-30s %s' % (pg, tgt[:52], L[:30], D[:30], verdict))
    print()
    print('硬编码条数 =', len(hard))


if __name__ == '__main__':
    sys.exit(main())
