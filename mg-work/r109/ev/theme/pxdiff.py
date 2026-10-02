# -*- coding: utf-8 -*-
"""像素级 diff：对同一页同一档的两张整屏截图做逐像素比对。

用法:
    python pxdiff.py <dirA> <dirB> [dirA2 dirB2 ...]

对每一对目录，按文件名配对 PNG，输出:
  - 有差异像素数 / 总像素数
  - Δ 的最大值
  - Δ 分桶直方图 (0, 1-2, 3-5, 6-10, 11-20, 21-40, 41-80, >80)
  - Top-N 差异最大的颜色对 (原色 -> 新色, 出现次数)
"""
import sys, os, collections
from PIL import Image

BUCKETS = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 20), (21, 40), (41, 80), (81, 255)]


def bucket(d):
    for lo, hi in BUCKETS:
        if lo <= d <= hi:
            return '%d-%d' % (lo, hi)
    return '>80'


def diff_pair(pa, pb, topn=12):
    a = Image.open(pa).convert('RGB')
    b = Image.open(pb).convert('RGB')
    if a.size != b.size:
        return {'error': 'size %s vs %s' % (a.size, b.size)}
    ha, hb = a.load(), b.load()
    w, h = a.size
    total = w * h
    diffpx = 0
    maxd = 0
    hist = collections.Counter()
    pairs = collections.Counter()
    for y in range(h):
        for x in range(w):
            ca, cb = ha[x, y], hb[x, y]
            d = max(abs(ca[0] - cb[0]), abs(ca[1] - cb[1]), abs(ca[2] - cb[2]))
            if d:
                diffpx += 1
                hist[bucket(d)] += 1
                if d > maxd:
                    maxd = d
                pairs[(ca, cb)] += 1
    return {
        'total': total,
        'diffpx': diffpx,
        'pct': 100.0 * diffpx / total,
        'maxd': maxd,
        'hist': dict(hist),
        'top': pairs.most_common(topn),
    }


def main():
    args = sys.argv[1:]
    for i in range(0, len(args) - 1, 2):
        da, db = args[i], args[i + 1]
        print('=' * 78)
        print('DIFF  %s  ->  %s' % (da, db))
        print('=' * 78)
        names = sorted(f for f in os.listdir(da) if f.endswith('.png'))
        agg = collections.Counter()
        for n in names:
            pb = os.path.join(db, n)
            if not os.path.exists(pb):
                print('  %-26s (missing in B)' % n)
                continue
            r = diff_pair(os.path.join(da, n), pb)
            if 'error' in r:
                print('  %-26s %s' % (n, r['error']))
                continue
            for k, v in r['hist'].items():
                agg[k] += v
            print('  %-26s diff=%7d/%d (%.2f%%)  maxΔ=%3d  %s'
                  % (n, r['diffpx'], r['total'], r['pct'], r['maxd'],
                     ' '.join('%s:%d' % (b, r['hist'][b])
                              for b in [('%d-%d' % t) for t in BUCKETS]
                              if b in r['hist'])))
            if r['diffpx'] > 3000:
                print('      TOP pairs:')
                for (ca, cb), cnt in r['top']:
                    print('        #%02X%02X%02X -> #%02X%02X%02X   x%d  (Δ%d)'
                          % (ca[0], ca[1], ca[2], cb[0], cb[1], cb[2], cnt,
                             max(abs(ca[i] - cb[i]) for i in range(3))))
        print('  AGG hist: %s' % ' '.join('%s:%d' % (b, agg[b])
                                          for b in [('%d-%d' % t) for t in BUCKETS]
                                          if b in agg))
    print('done')


if __name__ == '__main__':
    main()
