#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""页面产物语法自检：抽取内联 <script> 与 <style>，分别交给 node/简单规则校验。

用法:
    python mg-work/check-syntax.py pages/dev.html pages/kanban.html ...
    python mg-work/check-syntax.py pages/*.html          # 由 shell 展开

退出码 0 = 全部 ALL_OK；非 0 = 有问题清单。
只读，不修改任何文件。
"""
import os
import re
import subprocess
import sys
import tempfile

NODE = r'C:\Users\Administrator\.workbuddy\binaries\node\versions\22.22.2-3\node.exe'

SCRIPT_RE = re.compile(r'<script\b([^>]*)>(.*?)</script\s*>', re.S | re.I)
STYLE_RE = re.compile(r'<style\b([^>]*)>(.*?)</style\s*>', re.S | re.I)
SRC_RE = re.compile(r'\bsrc\s*=', re.I)


def check_file(path, tmpdir):
    with open(path, 'r', encoding='utf-8') as fh:
        html = fh.read()

    problems = []
    base = os.path.basename(path)
    stem = base.replace('.html', '').replace('.', '_')

    # --- JS ---
    js_count = 0
    for i, m in enumerate(SCRIPT_RE.finditer(html)):
        attrs, body = m.group(1), m.group(2)
        if SRC_RE.search(attrs):
            continue                      # 外链脚本跳过
        js_count += 1
        tmp = os.path.join(tmpdir, '%s_s%d.js' % (stem, i))
        with open(tmp, 'w', encoding='utf-8') as fh:
            fh.write(body)
        p = subprocess.run([NODE, '--check', tmp], capture_output=True, text=True)
        if p.returncode != 0:
            msg = (p.stderr or p.stdout).strip().splitlines()
            problems.append('script#%d 语法错误: %s' % (i, msg[0] if msg else '?'))

    # --- CSS ---
    css_count = 0
    for i, m in enumerate(STYLE_RE.finditer(html)):
        body = m.group(2)
        css_count += 1
        if body.count('{') != body.count('}'):
            problems.append('style#%d 花括号不配对 {%d vs }%d'
                            % (i, body.count('{'), body.count('}')))

        # CSS 注释不嵌套：注释里再出现 /* 只是普通文本，**无害**（如 "pages/*.html"）。
        # 真正的危险是「多余的 */」——它会提前闭合注释、把后面的规则吐出来。
        # 判据：顺序扫描，若某个 */ 找不到配对的 /*，即为真问题。
        stack = 0
        orphan = False
        for m in re.finditer(r'/\*|\*/', body):
            if m.group(0) == '/*':
                stack += 1
            elif stack:
                stack -= 1
            else:
                orphan = True
                break
        if orphan:
            problems.append('style#%d 出现无配对的 */（会提前闭合注释）' % i)

    return js_count, css_count, problems


def main():
    files = sys.argv[1:]
    if not files:
        print('用法: python mg-work/check-syntax.py <页面.html> ...')
        return 1

    bad = 0
    with tempfile.TemporaryDirectory(prefix='synchk_') as tmpdir:
        for path in files:
            if not os.path.exists(path):
                print('!! 文件不存在: %s' % path)
                bad += 1
                continue
            js_c, css_c, problems = check_file(path, tmpdir)
            if problems:
                bad += 1
                print('FAIL %-18s script=%d style=%d' % (os.path.basename(path), js_c, css_c))
                for p in problems:
                    print('     - %s' % p)
            else:
                print('ALL_OK %-16s script=%d style=%d' % (os.path.basename(path), js_c, css_c))

    print('---')
    print('结果：%d/%d 通过' % (len(files) - bad, len(files)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
