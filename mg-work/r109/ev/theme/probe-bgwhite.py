# -*- coding: utf-8 -*-
u"""r109 第十一拍 · 精确定位 --color-bg-white 的浅/暗两块（用更宽的窗口判归属）。"""
import io
import re
import sys

P = u'pages/base.html'


def main():
    t = io.open(P, encoding='utf-8', newline='').read().replace(u'\r\n', u'\n')
    for tok in (u'--color-bg-white', u'--color-bg-popup', u'--color-bg-1'):
        print(u'=== %s ===' % tok)
        i = 0
        while True:
            k = t.find(tok, i)
            if k < 0:
                break
            m = re.match(re.escape(tok) + u'\\s*:\\s*([^;}]+)', t[k:k + 100])
            if m:
                head = t[max(0, k - 700):k]
                # 判归属：最近的选择器块
                lb = head.rfind(u'}')
                lc = head.rfind(u'{')
                sel = head[lb + 1:lc] if lc > lb else u'(?)'
                is_dark = u'theme=dark' in sel
                print(u'   [%s] sel=%-52s = %s' % (
                    u'暗' if is_dark else u'浅', sel.strip()[:52], m.group(1).strip()[:30]))
            i = k + len(tok)
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
