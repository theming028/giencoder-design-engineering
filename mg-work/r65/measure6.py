"""r65 量测（六）：圆角定值 —— 设计稿角部区块 与 标定图各半径角部 逐像素 SSD 比对，取最优

标定图 mg-work/r65/calib-2x.png 是 2x DPR 截图，红块/容器块半径分别为 2,4,5,6,7,8,10,12,14,16。
"""
from PIL import Image

CAL = Image.open('calib-2x.png') if __import__('os').path.exists('calib-2x.png') \
    else Image.open('/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r65/calib-2x.png')

R_DIR = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'
DES = Image.open(R_DIR + '容器-165_1350-18230.png')
DES_A = DES.getchannel('A')

XS = {2: 24, 4: 166, 5: 307, 6: 449, 7: 590, 8: 732, 10: 874, 12: 1015, 14: 1157, 16: 1298}
ROWS = {'red': 268, 'box': 48}      # img y


def crop(im, x, y, k):
    p = im.crop((x, y, x + k, y + k)).convert('RGB')
    return list(p.getdata())


def ssd(a, b):
    return sum((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2 for p, q in zip(a, b))


def best(kind, dx, dy, k, label):
    ref = crop(DES, dx, dy, k)
    scores = []
    for r, x in XS.items():
        c = crop(CAL, 2 * x, ROWS[kind], k)
        scores.append((ssd(ref, c), r))
    scores.sort()
    print(f'  {label:22} K={k:3}  →  最优 R={scores[0][1]:2}  (SSD={scores[0][0]:,})'
          f'   次优 R={scores[1][1]:2} (SSD={scores[1][0]:,})')


print('=== 设计稿角部 vs 标定图角部（SSD 最小者为半径真值）===')
print('  设计稿原点：面板 img(48,32) / 卡 img(96,212) / 按钮 img(784,828)')
best('red', 784, 828, 24, '「确定」按钮 左上角')
best('red', 784, 828, 44, '「确定」按钮 左上角')
best('box', 96, 212, 32, '「当前任务」卡 左上角')
best('box', 96, 212, 56, '「当前任务」卡 左上角')
best('box', 96, 496, 32, 'textarea 左上角')

print()
print('=== 面板：用 alpha 通道比对（标定图无 alpha，改比对亮度梯度）===')
# 面板角部用 alpha 作为灰度
pa = DES_A.crop((48, 32, 48 + 80, 32 + 80))
print('  面板角部 alpha 前 5 行:', [[pa.getpixel((x, y)) for x in range(0, 40, 4)] for y in range(0, 10, 2)])
