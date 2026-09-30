# -*- coding: utf-8 -*-
import os, collections
from PIL import Image
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
im = Image.open(os.path.join(REPO,'mg-work','r88','raw','arch@2x_rgb.png')).convert('RGB')
px = im.load()

def hist(x0,y0,x1,y1,label,dark=8):
    cnt = collections.Counter()
    for y in range(y0,y1):
        for x in range(x0,x1):
            cnt[px[x,y]] += 1
    # 只报最暗的若干（文字/图标墨迹）
    items = sorted(cnt.items(), key=lambda kv: sum(kv[0]))[:dark]
    print('  %-14s' % label, ' '.join('#%02X%02X%02X(%d)' % (c[0],c[1],c[2],n) for c,n in items))

hist(42, 300, 420, 330, '行2 标题')
hist(42, 350, 500, 380, '行2 元信息')
hist(300, 350, 380, 380, '行2 归档于')
hist(386, 350, 480, 380, '行2 时间')
hist(1528, 330, 1552, 360, '默认钮 图标')
hist(1440, 626, 1496, 656, 'hover钮 文字')
hist(2, 10, 160, 46, '页标题')
hist(2, 66, 590, 96, '页副标题')
hist(1488, 44, 1656, 74, '清空按钮 文字')
hist(1305, 176, 1334, 206, '下拉 文件夹图标')
hist(22, 178, 46, 204, '搜索 放大镜图标')
