# -*- coding: utf-8 -*-
import io, re, sys
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
            out.append((css[start:j], css[start:i].strip())); i = j; start = j
        elif c == '}': i += 1; start = i
        else: i += 1
    return out
WANT = ['.td-root.is-fullscreen', '.td-ico-min', '.td-ico-max', '.td-collapsed',
        '.td-root.is-collapsed', '.td-file', '.td-ico-check', '.td-composer']
for st in re.findall(r'<style[^>]*>(.*?)</style>', s, re.S)[2:]:
    for body, sel in top_rules(st):
        if sel.startswith('@'): continue
        for w in WANT:
            if w in sel:
                print(body.strip()); print()
                break
