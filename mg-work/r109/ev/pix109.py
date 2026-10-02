# -*- coding: utf-8 -*-
"""r109 第一拍 · 逐像素对照：邵先生的设计稿 PNG ↔ 真机渲染元素截图。

设计稿是 scale=2 导出的（稿1 748×168、稿2 748×288），真机截图是 1×（356×48 / 356×108）。
本脚本把两边都换算到**逻辑 1×、且以卡片描边外沿为原点**的坐标系，逐项量同一批地标，再对差值。

设计稿的映射（实测定标）：卡片描边外沿在 PNG 里是 (72, 28)，scale=2
  ⇒ 逻辑 x = (imgX - 72)/2 + 36，逻辑 y = (imgY - 28)/2
（+36 是因为卡片在 356 宽的弹层里从 36 起，与真机同坐标系）
真机截图：卡片描边外沿就在 (36, 0)，scale=1 ⇒ 逻辑坐标 = 图像坐标。

⚠ 设计稿 PNG 是「透明底 + 投影」，`convert('RGB')` 后透明像素变纯黑 ⇒ 一切按颜色筛的判据
  都必须**先限定在卡片内区**，否则会把画布边缘的 (0,0,0) 一起吃进来（第一版就这么假报的）。
"""
import io
import sys

from PIL import Image

RAW = 'mg-work/r109/raw/'


def load(name):
    return Image.open(RAW + name).convert('RGB')


def near(c, t, tol):
    return abs(c[0] - t[0]) <= tol and abs(c[1] - t[1]) <= tol and abs(c[2] - t[2]) <= tol


def scan(im, pred, x0, x1, y0, y1):
    px = im.load()
    W, H = im.size
    xs, ys = [], []
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            if pred(px[x, y]):
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1)   # 半开区间


class Frame(object):
    """图像坐标 ⇄「逻辑 1× · 卡片描边外沿为原点」坐标。"""

    def __init__(self, tag, name, card_img_x, card_img_y, scale):
        self.tag, self.im = tag, load(name)
        self.cx, self.cy, self.s = card_img_x, card_img_y, scale

    def P(self, lx, ly):
        """逻辑（卡内）坐标 → 图像像素坐标（左上角）。"""
        return (int(round(self.cx + lx * self.s)), int(round(self.cy + ly * self.s)))

    def region(self, lx0, ly0, lx1, ly1):
        x0, y0 = self.P(lx0, ly0)
        x1, y1 = self.P(lx1, ly1)
        return (x0, y0, max(x1, x0 + 1), max(y1, y0 + 1))

    def L(self, b):
        if b is None:
            return None
        return (round((b[0] - self.cx) / float(self.s), 1), round((b[1] - self.cy) / float(self.s), 1),
                round((b[2] - self.cx) / float(self.s), 1), round((b[3] - self.cy) / float(self.s), 1))

    def find(self, t, tol, lx0, ly0, lx1, ly1):
        x0, y0, x1, y1 = self.region(lx0, ly0, lx1, ly1)
        return self.L(scan(self.im, lambda c: near(c, t, tol), x0, x1, y0, y1))

    def findp(self, pred, lx0, ly0, lx1, ly1):
        x0, y0, x1, y1 = self.region(lx0, ly0, lx1, ly1)
        return self.L(scan(self.im, pred, x0, x1, y0, y1))

    def at(self, lx, ly):
        return self.im.getpixel(self.P(lx, ly))


BORDER = lambda c: near(c, (229, 229, 229), 6)
BLUE = lambda c: near(c, (55, 112, 247), 12)
DISABLED = lambda c: near(c, (218, 228, 254), 12)
PLACEHOLDER = lambda c: 130 < c[0] < 215 and abs(c[0] - c[1]) < 8 and abs(c[1] - c[2]) < 8
DARK = lambda c: c[0] < 90 and c[1] < 90 and c[2] < 90


def dump(title, pairs):
    print('=' * 96)
    print(title)
    print('  %-24s %-27s %-27s %-24s %s' % ('地标（卡内逻辑 px）', '设计稿', '真机', '差值(真机−设计)', ''))
    for label, d, m in pairs:
        if d is None or m is None:
            print('  %-24s %-27s %-27s %s' % (label, d, m, '——'))
            continue
        dl = tuple(round(m[i] - d[i], 1) for i in range(len(d)))
        flag = 'OK' if all(abs(v) <= 1 for v in dl) else '★ 超 1px'
        print('  %-24s %-27s %-27s %-24s %s' % (label, str(d), str(m), str(dl), flag))


def main():
    D1 = Frame('稿1', 'design1-initial.png', 72, 28, 2)
    M1 = Frame('真机1', 'a-note-empty.png', 36, 0, 1)
    D2 = Frame('稿2', 'design2-typing.png', 72, 28, 2)
    M2 = Frame('真机2', 'b-note-typing.png', 36, 0, 1)

    print('########## 稿1（1409:18319 · 初始态 356×48）##########')
    dump('稿1 空态', [
        ('卡片（#E5E5E5 描边外框）', D1.findp(BORDER, 0, 0, 320, 48), M1.findp(BORDER, 0, 0, 320, 48)),
        ('「添加」禁用钮（#DAE4FE）', D1.findp(DISABLED, 200, 0, 320, 48), M1.findp(DISABLED, 200, 0, 320, 48)),
        ('占位墨迹（#A9A9A9）', D1.findp(PLACEHOLDER, 5, 5, 250, 43), M1.findp(PLACEHOLDER, 5, 5, 250, 43)),
    ])
    print('  取样：设计「添加」底 %s / 真机 %s ；设计占位墨 %s / 真机 %s'
          % (D1.at(285, 24), M1.at(284, 24), D1.at(20, 23), M1.at(20, 23)))

    print()
    print('########## 稿2（1204:18467 · 输入态 356×108）##########')
    dump('稿2 输入态', [
        ('卡片（#E5E5E5 描边外框）', D2.findp(BORDER, 0, 0, 320, 12), M2.findp(BORDER, 0, 0, 320, 12)),
        ('正文第 1 行墨迹（#1F1F1F）', D2.findp(DARK, 5, 5, 319, 33), M2.findp(DARK, 5, 5, 319, 33)),
        ('正文第 2 行墨迹（#1F1F1F）', D2.findp(DARK, 5, 34, 319, 57), M2.findp(DARK, 5, 34, 319, 57)),
        ('底行提示墨迹（#A9A9A9）', D2.findp(PLACEHOLDER, 5, 66, 200, 100), M2.findp(PLACEHOLDER, 5, 66, 200, 100)),
        ('「取消」次钮（#E5E5E5 描边）', D2.findp(BORDER, 190, 60, 258, 104), M2.findp(BORDER, 190, 60, 258, 104)),
        ('「添加」主钮（#3770F7）', D2.findp(BLUE, 258, 60, 319, 104), M2.findp(BLUE, 258, 60, 319, 104)),
    ])
    print('  取样：设计「添加」底 %s / 真机 %s ；设计正文 %s / 真机 %s ；设计提示 %s / 真机 %s'
          % (D2.at(284, 82), M2.at(284, 82), D2.at(20, 23), M2.at(20, 23),
             D2.at(17, 82), M2.at(17, 82)))

    print()
    print('########## 稿2 的 Ctrl 态（设计稿没有这一帧，看「只改该改的」）##########')
    M2C = Frame('真机2c', 'c-note-ctrl.png', 36, 0, 1)
    print('  主钮文案区（#FFFFFF 字） %s' % (M2C.findp(lambda c: c[0] > 240 and c[1] > 240 and c[2] > 240, 258, 60, 319, 104),))
    print('  主钮尺寸            %s' % (M2C.findp(BLUE, 258, 60, 319, 104),))
    print('  提示前半句墨迹        %s（应与稿2 一致）'
          % (M2C.findp(PLACEHOLDER, 5, 66, 100, 100),))
    print('  提示后半句墨迹        %s（应落在 #3770F7）'
          % (M2C.findp(BLUE, 100, 66, 200, 100),))


if __name__ == '__main__':
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith('gbk'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
