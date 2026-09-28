"""r65 量测：取消任务 / 终止任务 模态弹窗设计稿（2x 截图 → CSS px）

映射：img_x = 48 + css_x*2 ；img_y = 32 + css_y*2（由 alpha 通道切边实测）
"""
from PIL import Image

R = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'
OX, OY, SC = 48.0, 32.0, 2.0


def load(n):
    im = Image.open(R + n)
    b = Image.new('RGB', im.size, (255, 255, 255))
    b.paste(im, (0, 0), im)
    return b


def CX(x):
    return round((x - OX) / SC, 1)


def CY(y):
    return round((y - OY) / SC, 1)


def alpha_bounds(n):
    a = Image.open(R + n).getchannel('A')
    W, H = a.size
    mid = H // 2
    L = next(x for x in range(W) if a.getpixel((x, mid)) > 200)
    Rr = next(x for x in range(W - 1, -1, -1) if a.getpixel((x, mid)) > 200)
    c = W // 2
    T = next(y for y in range(H) if a.getpixel((c, y)) > 200)
    B = next(y for y in range(H - 1, -1, -1) if a.getpixel((c, y)) > 200)
    return L, T, Rr, B


def long_rows(im, T, B, minlen=60, thr=252):
    g = im.convert('L')
    W = im.width
    out = []
    prev = None
    x0 = int(OX)
    for y in range(T, B + 1):
        segs = []
        s = None
        for x in range(x0, W):
            hit = g.getpixel((x, y)) < thr
            if hit and s is None:
                s = x
            elif not hit and s is not None:
                segs.append((s, x - 1))
                s = None
        if s is not None:
            segs.append((s, W - 1))
        longs = [(p, q) for p, q in segs if (q - p + 1) / SC > minlen]
        if longs:
            key = tuple((round(CX(p), 1), round(CX(q), 1)) for p, q in longs)
            if key != prev:
                out.append((CY(y), key))
                prev = key
        else:
            prev = None
    return out


def ink(im, cx0, cy0, cx1, cy1, thr=200):
    x0 = int(round(OX + cx0 * SC))
    x1 = int(round(OX + cx1 * SC))
    y0 = int(round(OY + cy0 * SC))
    y1 = int(round(OY + cy1 * SC))
    g = im.convert('L')
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if g.getpixel((x, y)) < thr:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return (CX(min(xs)), CY(min(ys)), CX(max(xs)), CY(max(ys)))


def corner_radius(im, cx, cy, side, span=20):
    """从外框左上角(cx,cy)起，逐行找首个"覆盖>50%"的 x，首次回到 x0 的竖向跨度 ≈ R"""
    g = im.convert('L')
    x0 = int(round(OX + cx * SC))
    y0 = int(round(OY + cy * SC))
    prof = []
    for dy in range(0, int(span * SC)):
        row = None
        for dx in range(0, int(span * SC)):
            x = x0 + dx if side == 'l' else x0 - dx
            if g.getpixel((x, y0 + dy)) < 250:
                row = dx
                break
        prof.append(row)
    base = prof[-1]
    for dy, off in enumerate(prof):
        if off is not None and base is not None and off <= base:
            return round(dy / SC, 2), round((base) / SC, 2)
    return None


if __name__ == '__main__':
    import sys
    for name, label in [('容器-165_1350-18230.png', '取消任务'), ('容器-171_1350-18236.png', '终止任务')]:
        im = load(name)
        L, T, Rr, B = alpha_bounds(name)
        print('=' * 74)
        print(f'### {label}  面板 CSS {(Rr - L + 1) / SC} x {(B - T + 1) / SC}')
        print('  --- 长横线/边框行（横段 > 60 CSS px）---')
        for y, key in long_rows(im, T, B):
            print(f'    y={y:7.1f}  segs(CSS x)={key}')
