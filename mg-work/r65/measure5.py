"""r65 量测（五）：圆角 —— 用「角部缺失面积」反推 R（R = sqrt(area / (1 - pi/4))）

抗锯齿下比"扫首行/首列"稳；面板用 alpha 通道，子容器用填充色阈值。
"""
import math
from PIL import Image

R_DIR = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'
SC = 2.0


def area_radius(im, L, T, K, inside):
    """L,T = 角点(img)  K = 采样方框边长(img px)  inside(px)->bool"""
    miss = 0
    for y in range(T, T + K):
        for x in range(L, L + K):
            if not inside(im.getpixel((x, y))):
                miss += 1
    return math.sqrt(miss / (1 - math.pi / 4))


for name, label in [('容器-165_1350-18230.png', '取消任务'), ('容器-171_1350-18236.png', '终止任务')]:
    im = Image.open(R_DIR + name)
    a = im.getchannel('A')
    W, H = a.size
    mid = H // 2
    L = next(x for x in range(W) if a.getpixel((x, mid)) > 200)
    Rr = next(x for x in range(W - 1, -1, -1) if a.getpixel((x, mid)) > 200)
    c = W // 2
    T = next(y for y in range(H) if a.getpixel((c, y)) > 200)
    B = next(y for y in range(H - 1, -1, -1) if a.getpixel((c, y)) > 200)
    print('=' * 70)
    print(f'### {label}')
    rgb = Image.new('RGB', im.size, (255, 255, 255)); rgb.paste(im, (0, 0), im)
    # 面板：alpha > 121 视为面板内
    for K in (20, 40, 60):
        r = area_radius(im, L, T, K, lambda p: p[3] > 121)
        print(f'  面板(K={K:2})  R(img)={r:5.2f} → CSS {r/SC:5.2f}')
    # 卡 / textarea / 按钮：用 "非纯白且非外色" 判定，取左上角
    for what, (cx, cy) in {'「当前任务」卡': (24, 90),
                           'textarea': (24, 248 if '165' in name else 210),
                           '「确定」按钮': (368, 398 if '165' in name else 360)}.items():
        x0 = int(round(48 + cx * SC)); y0 = int(round(32 + cy * SC))
        for K in (12, 20):
            r = area_radius(rgb, x0, y0, K, lambda p: min(p) < 252)
            print(f'  {what:12}(K={K:2})  R(img)={r:5.2f} → CSS {r/SC:5.2f}')
