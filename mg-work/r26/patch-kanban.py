# -*- coding: utf-8 -*-
"""第 26 轮第 8/9 项：看板两页的卡片跳转 + 移除右下角智能助手悬浮球。

第 8 项：pages/kanban.html 的卡片点击处理器原本 `if (card.classList.contains('is-dashed')) return;`
        —— 而「进行中」泳道首卡（待确认态）正好带 .is-dashed，所以唯独它点不动。
        改成「只放行带 .kb-card-title 的真实任务卡」，占位卡依然不跳。

第 9 项：移除 pages/kanban.html / pages/req-kanban.html 里 `.kb-fab`（右下角智能助手悬浮球）。
        ⚠️ 标记文字 `<!-- floating action` 必须保留 —— mg-work/req-kanban/build-table.py 用它做锚点
           （`src.find('        <!-- floating action')`），删掉锚点会导致该构建脚本 assert 失败。
        同时同步两个构建输入 _req_html.html / _kb_html.html，避免重跑生成器时按钮复活。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NOTE = '<!-- floating action（第 26 轮第 9 项：右下角「智能助手」悬浮球已按需求移除；锚点文字保留给 req-kanban 构建脚本） -->'


def strip_fab(s, label):
    """删掉 .kb-fab 悬浮球，保留 floating action 锚点注释。"""
    if 'kb-fab' not in s:
        return s, 'SKIP (no kb-fab)'
    # 转义形态：JS 字符串数组里的条目
    a = s.find('"        <!-- floating action -->"')
    if a >= 0:
        end_tok = '"        </div>",'
        b = s.find(end_tok, a)
        if b < 0:
            return s, 'FAIL (escaped form: close token missing)'
        block = s[a:b + len(end_tok)]
        if 'kb-fab' not in block or '智能助手' not in block:
            return s, 'FAIL (escaped form: unexpected block)'
        new = s[:a] + '"        %s",' % NOTE + s[b + len(end_tok):]
        return new, 'OK escaped (-%d chars)' % (len(s) - len(new))
    # 明文形态：直接是 HTML
    a = s.find('        <!-- floating action -->\n')
    if a >= 0:
        end_tok = '\n        </div>'
        b = s.find(end_tok, a)
        if b < 0:
            return s, 'FAIL (plain form: close token missing)'
        b += len(end_tok)
        # 该行可能没有结尾换行（文件末尾）
        tail = '\n' if s[b:b + 1] == '\n' else ''
        b += len(tail)
        block = s[a:b]
        if 'kb-fab' not in block or '智能助手' not in block:
            return s, 'FAIL (plain form: unexpected block)'
        new = s[:a] + '        %s%s' % (NOTE, tail) + s[b:]
        return new, 'OK plain (-%d chars)' % (len(s) - len(new))
    return s, 'FAIL (no floating-action anchor)'


def patch_card_click(s):
    """第 8 项：让虚线卡（待确认态）也能进详情页。"""
    old = "        if (card.classList.contains('is-dashed')) return;"
    new = ("        /* 第 26 轮第 8 项：虚线卡（「进行中」首卡的待确认态）也要能进详情页，\n"
           "           改为「只放行带标题的真实任务卡」，占位卡依然不跳。 */\n"
           "        if (!card.querySelector('.kb-card-title')) return;")
    if old not in s:
        return s, 'SKIP (anchor missing)'
    if s.count(old) != 1:
        return s, 'FAIL (anchor x%d)' % s.count(old)
    return s.replace(old, new, 1), 'OK'


def run(rel, do_fab=True, do_card=False):
    path = os.path.join(ROOT, rel)
    s = io.open(path, encoding='utf-8').read()
    msgs = []
    if do_card:
        s, m = patch_card_click(s)
        msgs.append('card=%s' % m)
    if do_fab:
        s, m = strip_fab(s, rel)
        msgs.append('fab=%s' % m)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    print('%-40s %s' % (rel, '  '.join(msgs)))


if __name__ == '__main__':
    run('pages/kanban.html', do_fab=True, do_card=True)
    run('pages/req-kanban.html', do_fab=True, do_card=False)
    # 构建输入（明文形态），保证重跑生成器不会让按钮复活
    run('mg-work/req-kanban/_req_html.html', do_fab=True, do_card=False)
    run('mg-work/req-kanban/_kb_html.html', do_fab=True, do_card=False)
