# -*- coding: utf-8 -*-
"""按块提取设计稿里每个 text/text ui-component 的文案（含换行）与框尺寸。"""
import io, re

S = io.open('design-1393-18748.html', encoding='utf-8').read()

# 找到所有顶层内容块（left:164px）的起点
tops = []
for m in re.finditer(r'data-node-id="(\d+:\d+)"\s*\n?\s*data-name="([^"]*)"\s*\n?\s*style="width: 840px; height: (\d+)px; position: absolute; left: 164px; top: (\d+)px[^"]*"', S):
    tops.append((m.start(), m.group(1), m.group(2), int(m.group(4)), int(m.group(3))))
tops.sort()

for i, (pos, nid, name, top, h) in enumerate(tops):
    end = tops[i + 1][0] if i + 1 < len(tops) else len(S)
    seg = S[pos:end]
    print('=' * 78)
    print('块 %s %s  top=%d h=%d' % (nid, name, top, h))
    # 折叠头文字（span 14/22）
    for m in re.finditer(r'data-name="(深度思考|上下文注入|Bash|网页搜索|需求采访|更新任务清单|文件写入|SKILL|Tool call|搜索资料|未知 surface 事件|调用 5 个工具|压缩上下文|上下文已压缩|模型已切换)"', seg):
        pass
    for m in re.finditer(r'<span\s*\n?\s*data-node-id="[^"]*"\s*\n?\s*data-name="([^"]*)"\s*\n?\s*style="color: (#[0-9A-Fa-f]{6}); font-size: (\d+)px; font-family: [A-Za-z ]+; line-height: (\d+)px[^"]*"[^>]*>\s*([^<]{0,80})', seg):
        nm, col, fs, lh, txt = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5).strip()
        print('  span %-14s %s %s/%s  %r' % (nm, col, fs, lh, txt))
    # ui-component text props
    for m in re.finditer(r'<ui-component([^>]*?)>', seg, re.S):
        blob = m.group(1)
        w = re.search(r'width:\s*(\d+)px', blob)
        hh = re.search(r'height:\s*(\d+)px', blob)
        tp = re.search(r"text='(\{.*?\})'", blob, re.S)
        if tp:
            t = tp.group(1)
            t = t.replace('\\n', '⏎')
            print('  ui  %sx%s  %s' % (w.group(1) if w else '?', hh.group(1) if hh else '?', t[:300]))
