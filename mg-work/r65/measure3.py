"""r65 量测（三）：圆角 / 阴影 / 按钮内部色 —— 设计稿 2x 截图 → CSS px"""
from PIL import Image
from measure import load, OX, OY, SC

R = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'


def profile(im, cx, cy, span=22, outside=250):
    """从 (cx,cy) 起向下逐行，返回每行首个"非外色"像素相对 x 的偏移（CSS px）"""
    g = im.convert('L')
    x0 = int(round(OX + cx * SC)); y0 = int(round(OY + cy * SC))
    out = []
    for dy in range(0, int(span * SC) + 1):
        off = None
        for dx in range(0, int(span * SC) + 1):
            if g.getpixel((x0 + dx, y0 + dy)) < outside:
                off = dx; break
        out.append((round(dy / SC, 2), None if off is None else round(off / SC, 2)))
    return out


def radius_from(prof):
    """首次回到最小偏移（=直线段起点）的 dy ≈ R"""
    vals = [v for _, v in prof if v is not None]
    if not vals:
        return None
    base = min(vals)
    for dy, v in prof:
        if v is not None and v <= base:
            return dy
    return None


for name, label in [('容器-165_1350-18230.png', '取消任务'), ('容器-171_1350-18236.png', '终止任务')]:
    im = load(name)
    print('=' * 74); print('###', label)
    for what, (cx, cy) in {'面板外框': (0, 0), '「当前任务」卡': (24, 90),
                           'textarea': (24, 248 if '165' in name else 210),
                           '「确定」按钮': (368, 398 if '165' in name else 360)}.items():
        p = profile(im, cx, cy)
        print(f'  {what:14} R ≈ {radius_from(p)}   profile前6: {p[:6]}')

print()
print('=== 按钮内部取色（取消任务稿）===')
im = load('容器-165_1350-18230.png')
def px(cx, cy, im=im):
    return im.getpixel((int(round(OX + cx * SC)), int(round(OY + cy * SC))))
for k, (cx, cy) in {
    '次要按钮 底': (305, 405), '次要按钮 描边(左)': (300.1, 414),
    '次要按钮 文字': (330, 413.5),
    '危险按钮 底': (372, 402), '危险按钮 文字(空)': (0, 0),
}.items():
    if cx == 0: continue
    print(f'  {k:18} rgb={px(cx, cy)}')
print('  危险按钮 底色(多处):', px(380, 405), px(440, 420), px(410, 412))
print('  危险按钮 文字笔画(最深):', min((px(x, 413.5) for x in range(390, 440)), key=sum))
print()
print('=== 面板阴影采样（面板正下方 y=面板底+2..+14）===')
a = Image.open(R + '容器-165_1350-18230.png').getchannel('A')
W, H = a.size
c = W // 2
T = next(y for y in range(H) if a.getpixel((c, y)) > 200)
B = next(y for y in range(H - 1, -1, -1) if a.getpixel((c, y)) > 200)
im2 = Image.open(R + '容器-165_1350-18230.png')
base = Image.new('RGB', im2.size, (255, 255, 255)); base.paste(im2, (0, 0), im2)
print('  下沿外:', [base.getpixel((c, B + k))[0] for k in range(1, 16)])
print('  右沿外:', [base.getpixel((1007 + k, 500))[0] for k in range(1, 16)])
print('  上沿外:', [base.getpixel((c, T - k))[0] for k in range(1, 16)])
