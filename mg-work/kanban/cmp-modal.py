# -*- coding: utf-8 -*-
"""r11: 设计稿模态 vs 渲染模态 像素级比对"""
import io
from PIL import Image

def load(p):
    im = Image.open(p).convert('RGB')
    return im

D = load(r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\design-modal.png')
R = load(r'E:\GienCoder\giencoder-design-engineering\mg-work\kanban\r11\x-modal.png')
print('design %sx%s   render %sx%s' % (D.size + R.size))

def px(im, x, y):
    return im.getpixel((x, y))

def hexs(c):
    return '#%02X%02X%02X' % c

def scan_row(im, y, x0, x1, pred=None):
    """返回该行所有颜色分段 [(x_start,x_end,color,...)]"""
    out = []
    prev = None
    for x in range(x0, x1):
        c = px(im, x, y)
        if prev is None or (abs(c[0]-prev[0])+abs(c[1]-prev[1])+abs(c[2]-prev[2]) > 12):
            out.append([x, x, c])
            prev = c
        else:
            out[-1][1] = x
            prev = c
    return out

def col_runs(im, x, y0, y1, thr=10):
    out = []
    prev = None
    for y in range(y0, y1):
        c = px(im, x, y)
        if prev is None or (abs(c[0]-prev[0])+abs(c[1]-prev[1])+abs(c[2]-prev[2]) > thr):
            out.append([y, y, c]); prev = c
        else:
            out[-1][1] = y; prev = c
    return out

print('\n--- 设计稿 ---')
print('页面底(左上角外)   ', hexs(px(D, 20, 200)))
print('面板内左上         ', hexs(px(D, 120, 120)))
print('面板内右下         ', hexs(px(D, 960, 560)))
# 面板左右边界
row = scan_row(D, 300, 60, 1040)
print('y=300 分段(前12)   ', [(a, b, hexs(c)) for a, b, c in row[:12]])
print('y=300 分段(后6)    ', [(a, b, hexs(c)) for a, b, c in row[-6:]])
# 表头
print('表头底 y=132       ', hexs(px(D, 300, 132)))
col = col_runs(D, 640, 100, 460)
print('x=640 纵向分段(前16)', [(a, b, hexs(c)) for a, b, c in col[:16]])

print('\n--- 渲染 ---')
print('页面底(左上角外)   ', hexs(px(R, 20, 200)))
print('面板内左上         ', hexs(px(R, 120, 120)))
row = scan_row(R, 300, 60, 1040)
print('y=300 分段(前12)   ', [(a, b, hexs(c)) for a, b, c in row[:12]])
print('y=300 分段(后6)    ', [(a, b, c) if False else (a, b, hexs(c)) for a, b, c in row[-6:]])
print('表头底 y=132       ', hexs(px(R, 300, 132)))
col = col_runs(R, 640, 100, 460)
print('x=640 纵向分段(前16)', [(a, b, hexs(c)) for a, b, c in col[:16]])
