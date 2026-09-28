"""r65 像素回归：页面 2× 截图 vs 设计稿 2× 截图

对齐：设计稿面板左上角 img(48,32)；页面面板左上角 img=(left*2, top*2)（由运行时探针给出）
判据：
  · 容差 ±TOL /通道 —— 设计稿导出图的面板底是 253~254（其底图是 rgba(255,255,255,.95)），
    页面是 255；严格相等会把这些 1~2 级噪声全判成"不同"（首轮实测 93% 假阳性）
  · 只比「面板内部」：x 16..464（跳过左上/右上 16px 圆角弧），
    圆角本身已由 SSD 反查单独定值为 16
  · 纵向对齐：本页任务标题 1 行、设计稿样本文案 2 行；且「卡片↔分隔线」间距
    本实现取 24（取消稿）/ 设计稿终止稿是 8 ⇒ 卡片以下整体错位 16，比对时按 shift 补偿
"""
from PIL import Image

DES_DIR = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'
EV = '/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r65/ev/'
SC, TOL = 2, 4
DX, DY = 48, 32
PAGE = {'cancel': ('20-cancel-2x.png', 480, 234), 'stop': ('21-stop-2x.png', 480, 234)}
DES = {'cancel': '容器-165_1350-18230.png', 'stop': '容器-171_1350-18236.png'}
PAD = 16          # 跳过圆角弧


def design(key):
    im = Image.open(DES_DIR + DES[key])
    b = Image.new('RGB', im.size, (255, 255, 255))
    b.paste(im, (0, 0), im)
    return b


def stat(des, pg, cx, cy, w, h, shift=0):
    """比对 CSS 区 (cx,cy,w,h)；页面侧整体下移 shift"""
    n = d = 0
    mx = 0
    sad = 0
    for y in range(cy * SC, (cy + h) * SC):
        for x in range(cx * SC, (cx + w) * SC):
            a = des.getpixel((DX + x, DY + y))
            b = pg.getpixel((PX + x, PY + y + shift * SC))
            n += 1
            da = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
            sad += da
            if da > mx:
                mx = da
            if max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2])) > TOL:
                d += 1
    return d, n, mx, sad * 1.0 / n


REGIONS = {
    'cancel': [
        ('A 顶部区 标题/副标题/关闭', 0, 0, 480, 90, 0),
        ('A2 卡片上沿+标签', 24, 88, 432, 40, 0),
    ],
    'stop': [
        ('A 顶部区 标题/副标题/关闭', 0, 0, 480, 90, 0),
        ('A2 卡片上沿+标签', 24, 88, 432, 40, 0),
        ('C1 分隔线区', 16, 170, 448, 40, 16),
        ('C2 输入框区', 16, 208, 448, 96, 16),
        ('C3 辅助文字', 16, 300, 448, 32, 16),
        ('C4 页脚按钮区', 16, 352, 448, 48, 16),
    ],
}

for key in ('stop', 'cancel'):
    fn, pl, pt = PAGE[key]
    pg = Image.open(EV + fn).convert('RGB')
    PX, PY = pl * SC, pt * SC
    des = design(key)
    print('=' * 80)
    print(f'### {key}   页面原点 img=({PX},{PY})  设计稿 img=({DX},{DY})   容差 ±{TOL}/通道')
    for label, x, y, w, h, shift in REGIONS[key]:
        # 跳过左右 16px 圆角弧
        if x < PAD:
            w -= (PAD - x); x = PAD
        d, n, mx, mad = stat(des, pg, x, y, w, h, shift)
        flag = '✅' if d * 100.0 / n < 2.0 else ('⚠️' if d * 100.0 / n < 8.0 else '❌')
        print(f'  {flag} {label:26} {w}x{h}  不同 {d:>6}/{n} = {d*100.0/n:5.2f}%   最大差 {mx:>4}   平均 {mad:5.2f}')
    print()
