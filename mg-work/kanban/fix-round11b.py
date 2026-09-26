# -*- coding: utf-8 -*-
"""round11b: 修正 bindCoopModal 的脚本作用域
fix-round11.py 用 s.index('})();\n</script>') 取到了文件里第一个 IIFE 结尾（script#2），
导致 bindCoopModal 定义落在了 skills-popup 那个 IIFE 里，而 inject() 在 script#4，
调用时 ReferenceError → 绑定不执行 → 点击不动。
本脚本把定义搬到 KB 脚本（含 var KB_HTML 的那个）的 IIFE 内。
幂等：若已位于正确位置则跳过。
"""
import io

P = r'E:\GienCoder\giencoder-design-engineering\pages\kanban.html'
s = io.open(P, encoding='utf-8').read()
orig = len(s)

HEAD = '  /* ===== r11: 待协作任务模态'
TAIL = '  }\n'          # 函数体收尾
CLOSE = '})();\n</script>'

kb_idx = s.index('var KB_HTML')

# --- 1. 取出错位的那段 JS ---
start = s.index(HEAD)
# 该段之后紧跟的第一个 IIFE 收尾
seg_end = s.index(CLOSE, start)
body = s[start:seg_end]                 # HEAD ... '  }\n'
assert body.rstrip().endswith('}'), repr(body[-80:])
assert 'function bindCoopModal' in body

# 判断它现在落在哪个 script：KB 脚本的 IIFE 结尾下标
kb_close = s.index(CLOSE, kb_idx)
misplaced = start < kb_idx               # 在 KB 之前 => 错位

if not misplaced:
    print('[scope] already correct, skip')
else:
    # 删除错位定义（连同其前面的一个空行）
    cut_from = start
    if s[cut_from - 1] == '\n' and s[cut_from - 2] == '\n':
        cut_from -= 1
    s = s[:cut_from] + s[seg_end:]
    # 重新定位 KB 脚本的 IIFE 结尾并插入
    kb_close = s.index(CLOSE, s.index('var KB_HTML'))
    s = s[:kb_close] + body + s[kb_close:]
    print('[scope] moved definition into KB script IIFE')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('DONE  %d -> %d chars' % (orig, len(s)))
