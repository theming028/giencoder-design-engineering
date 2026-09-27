# -*- coding: utf-8 -*-
"""清点 task-detail.html 内联 CSS 里，与「AI 对话栏模块」相关的全部顶层规则。"""
import io, re, json, collections

s = io.open('pages/task-detail.html', encoding='utf-8').read()

def top_rules(css):
    out, i, n, start = [], 0, len(css), 0
    while i < n:
        c = css[i]
        if c == '{':
            depth, j = 1, i + 1
            while j < n and depth:
                if css[j] == '{': depth += 1
                elif css[j] == '}': depth -= 1
                j += 1
            out.append((css[start:j], css[start:i].strip()))
            i = j; start = j
        elif c == '}':
            i += 1; start = i
        else:
            i += 1
    return out

styles = re.findall(r'<style[^>]*>(.*?)</style>', s, re.S)
print("style 块数:", len(styles), [len(x) for x in styles])

PREF = ['.td-right', '.td-chat', '.td-msg-', '.td-ai-', '.td-composer', '.td-add-', '.td-skill',
        '.td-round-btn', '.td-sep', '.td-collapsed', '.td-file', '.avatar-', '.td-ico-md',
        '.td-ico-check', '.td-ico-max', '.td-ico-min', '.td-bar', '.td-root', '.td-left',
        '.td-attr-link', '.select-view-ghost']

seen = collections.OrderedDict()
for bi, st in enumerate(styles):
    for body, sel in top_rules(st):
        if not sel or sel.startswith('@media') or sel.startswith('@keyframes'): continue
        for p in PREF:
            if p in sel:
                key = re.sub(r'\s+', ' ', sel)
                if key not in seen:
                    seen[key] = (bi, len(body), len(re.findall(r'\{', body)) - 1)
                break

print("\n命中规则数:", len(seen))
by_prefix = collections.Counter()
for k in seen: 
    for p in PREF:
        if p in k: by_prefix[p] += 1; break
for p in PREF:
    print("  %-20s %d" % (p, by_prefix[p]))
print("\n--- 明细 ---")
for k, v in seen.items():
    print("  blk%d len=%-6d nested=%d  %s" % (v[0], v[1], v[2], k[:180]))
