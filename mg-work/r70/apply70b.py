#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 70 轮补丁 b：抽屉收起态把 border-width 收成 0

背景：`.td-right` 加 1px 描边后，`box-sizing: border-box` 下 `width: 0` 的**实际箱宽**
      最小等于左右描边之和 = 2px → 抽屉收起时白占 2px 布局（元素本身 opacity:0 看不见）。
做法：收起态 border-width: 0、展开态 1px，并把 border-width 一并放进 transition，
      这样「展开」时描边随宽度一起长出来、「收起」时随宽度一起收回去，全程有描边可看。
"""
import os
import re
import sys
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, 'pages', 'avatar.html')
BACKUP = '/tmp/r70-backup/avatar.html'

F1_OLD = """  .av-chat-drawer {
    flex: none; width: 0; margin: 0; align-self: stretch;
    height: auto; min-height: 0; z-index: 1;
    overflow: hidden; opacity: 0; visibility: hidden;
    transition: width 240ms var(--av-chat-ease), opacity 180ms var(--av-chat-ease),
                visibility 0s linear 240ms;
  }"""
F1_NEW = """  .av-chat-drawer {
    flex: none; width: 0; margin: 0; align-self: stretch;
    height: auto; min-height: 0; z-index: 1;
    overflow: hidden; opacity: 0; visibility: hidden;
    /* ★ 第 70 轮第 1c 项：收起态把描边宽度收成 0 —— 否则 border-box 下
       箱宽最小等于左右描边之和（2px），静止时会白占 2px 布局。 */
    border-width: 0;
    transition: width 240ms var(--av-chat-ease), opacity 180ms var(--av-chat-ease),
                border-width 240ms var(--av-chat-ease),
                visibility 0s linear 240ms;
  }"""

F2_OLD = """  html[data-av-chat-open] .av-chat-drawer {
    width: var(--av-chat-w); opacity: 1; visibility: visible;
    transition: width 240ms var(--av-chat-ease), opacity 180ms var(--av-chat-ease), visibility 0s;
  }"""
F2_NEW = """  html[data-av-chat-open] .av-chat-drawer {
    width: var(--av-chat-w); opacity: 1; visibility: visible;
    border-width: 1px;
    transition: width 240ms var(--av-chat-ease), opacity 180ms var(--av-chat-ease),
                border-width 240ms var(--av-chat-ease), visibility 0s;
  }"""

JOBS = [
    ('F1 收起态 border-width:0', F1_OLD, F1_NEW, '★ 第 70 轮第 1c 项'),
    ('F2 展开态 border-width:1px', F2_OLD, F2_NEW, F2_NEW),
]

TAG_TOKENS = ['<style', '</style>', '<script', '</script>']


def main():
    s0 = open(PATH, encoding='utf-8').read()
    if not os.path.exists(BACKUP):
        os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
        shutil.copy2(PATH, BACKUP)
    s = s0
    applied, skipped = [], []
    for jn, old, new, mk in JOBS:
        if mk and mk in s:
            skipped.append(jn)
            continue
        c = s.count(old)
        if c != 1:
            print(f'!! {jn}: OLD 命中 {c} 次（应为 1）')
            sys.exit(1)
        s = s.replace(old, new, 1)
        applied.append(jn)

    errs = []
    if applied:
        for tk in TAG_TOKENS:
            d = s.count(tk) - s0.count(tk)
            if d != 0:
                errs.append(f'{tk} 计数变了 {d:+d}')
    errs += [lbl for lbl, ok in [
        ('border-width 过渡未成对', s.count('border-width 240ms var(--av-chat-ease)') == 2),
        ('收起态未收描边宽', '.av-chat-drawer {\n    flex: none; width: 0;' in s and
         'border-width: 0;' in s.split('.av-chat-drawer {\n    flex: none; width: 0;')[1][:400]),
        ('展开态未给描边宽', 'border-width: 1px;\n    transition: width 240ms var(--av-chat-ease)' in s),
        ('描边色仍在 .td-right 上', s.count('border: 1px solid var(--td-panel-line);') == 2),
    ] if not ok]
    if errs:
        print('!! 自检失败：')
        for e in errs:
            print('   ✗', e)
        sys.exit(1)

    if applied:
        open(PATH, 'w', encoding='utf-8').write(s)
    print(f'[avatar.html] 应用: {len(applied)} 项 | 跳过: {len(skipped)} 项  ({len(s0)} → {len(s)} B)')
    for j in applied:
        print('   应用:', j)
    for j in skipped:
        print('   跳过:', j)


if __name__ == '__main__':
    main()
