"""r65 量测（四）：面板圆角(alpha) + 阴影衰减曲线"""
from PIL import Image

R = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'
SC = 2.0

for name, label in [('容器-165_1350-18230.png', '取消任务'), ('容器-171_1350-18236.png', '终止任务')]:
    im = Image.open(R + name)
    a = im.getchannel('A')
    W, H = a.size
    mid = H // 2
    L = next(x for x in range(W) if a.getpixel((x, mid)) > 200)
    Rr = next(x for x in range(W - 1, -1, -1) if a.getpixel((x, mid)) > 200)
    c = W // 2
    T = next(y for y in range(H) if a.getpixel((c, y)) > 200)
    B = next(y for y in range(H - 1, -1, -1) if a.getpixel((c, y)) > 200)
    print('=' * 70)
    print(f'### {label}  面板 img=({L},{T})-({Rr},{B})')
    # 顶行 alpha 探测的横向 extent → R = x0 - L
    top_ext = [x for x in range(W) if a.getpixel((x, T)) > 200]
    bot_ext = [x for x in range(W) if a.getpixel((x, B)) > 200]
    left_ext = [y for y in range(H) if a.getpixel((L, y)) > 200]
    print(f'  顶行 alpha 段 x=({top_ext[0]},{top_ext[-1]})  → R(水平) ≈ {(top_ext[0]-L)/SC}')
    print(f'  底行 alpha 段 x=({bot_ext[0]},{bot_ext[-1]})  → R(水平) ≈ {(bot_ext[0]-L)/SC}')
    print(f'  左列 alpha 段 y=({left_ext[0]},{left_ext[-1]})  → R(垂直) ≈ {(left_ext[0]-T)/SC}')
    print(f'  → 面板圆角 ≈ {(top_ext[0]-L)/SC} ~ {(left_ext[0]-T)/SC}')

    # 阴影 alpha 衰减（面板正下 / 正上 / 右）
    print('  下沿 alpha 衰减(CSS px):',
          [round((a.getpixel((c, B + k)) / 255) * 100, 1) for k in range(1, 25, 2)], '%')
    print('  上沿 alpha 衰减(CSS px):',
          [round((a.getpixel((c, T - k)) / 255) * 100, 1) for k in range(1, 25, 2)], '%')
    print('  右沿 alpha 衰减(CSS px):',
          [round((a.getpixel((Rr + k, mid)) / 255) * 100, 1) for k in range(1, 25, 2)], '%')
