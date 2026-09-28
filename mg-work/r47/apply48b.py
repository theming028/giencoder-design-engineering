#!/usr/bin/env python3
# 第 47 轮第 2 项修复：代码块里 `&&` 被 esc_h 二次转义（&amp;amp; → 应为一层 &amp;）
import os, sys

F = '/Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html'
s = open(F, encoding='utf-8').read()
before = s.count('&amp;amp;')
if before == 0:
    print('无需修复（已是正确转义）')
else:
    s = s.replace('&amp;amp;', '&amp;')
    open(F, 'w', encoding='utf-8').write(s)
    print('已修复 %d 处二次转义' % before)

s = open(F, encoding='utf-8').read()
ok = s.count('&amp;amp;') == 0 and s.count('&amp;&amp;') == 1   # 全文件只有 1 处 `&&`
print('OK' if ok else 'FAIL: &amp;amp;=%d &amp;&amp;=%d' % (s.count('&amp;amp;'), s.count('&amp;&amp;')))
sys.exit(0 if ok else 1)
