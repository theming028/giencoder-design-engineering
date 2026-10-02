# -*- coding: utf-8 -*-
"""r109 第四拍（裁决③）· 逐状态亮面审计 —— 汇总/过滤

输入：mg-work/r109/raw/state4/*.json（scan-state.sh 产物，eval 输出是 JSON 套 JSON）
输出：每页 total / 去白名单后的「非已知」条目明细

★ 白名单（已知假阳性）——**判据是「本来就该亮」**，与暗色适配无关，逐条给理由：
  1. `size-3 rounded-full`   → 模拟 macOS 窗口的三个交通灯按钮（#FF5F57 / #FEBC2E / #28C840）
                               OS 窗口装饰，色值本身即品牌固定色，不属于页面配色。
  2. `r85-sl-`               → settings 主题分组里的**滑杆轨道刻度**，亮色是设计意图。
  3. `giencoder-switch-handle` → 开关钮的**白色滑块**（DS 规范：开启态滑块恒白）。
  4. `r93-adot`              → 待办卡左侧的**状态圆点**，亮色是状态语义。
"""
import io, json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'raw', 'state4')
OUT = os.path.abspath(OUT)

WHITE = [
    ('size-3 rounded-full', 'macOS 交通灯（OS 窗口装饰）'),
    ('r85-sl-', '主题滑杆刻度（设计意图亮）'),
    ('giencoder-switch-handle', '开关白滑块（DS 规范恒白）'),
    ('r93-adot', '待办卡状态圆点（状态语义亮）'),
]


def load_one(fp):
    raw = io.open(fp, encoding='utf-8').read().strip()
    try:
        s = json.loads(raw)
        if isinstance(s, str):
            s = json.loads(s)
    except Exception as e:
        return None, 'parse-error: %s' % e
    return s, None


def is_known(it):
    hay = (it.get('cls', '') + ' ' + it.get('sel', ''))
    for pat, _why in WHITE:
        if pat in hay:
            return pat
    return None


def main():
    only = sys.argv[1:] or None
    files = sorted(glob.glob(os.path.join(OUT, '*.json')))
    grand_total = grand_known = 0
    rows = []
    for fp in files:
        pg = os.path.basename(fp)[:-5]
        if only and pg not in only:
            continue
        d, err = load_one(fp)
        if err:
            rows.append((pg, 'ERR', 0, 0, [err]))
            continue
        items = d.get('items', [])
        unk = []
        kn = 0
        for it in items:
            m = is_known(it)
            if m:
                kn += 1
            else:
                unk.append(it)
        grand_total += len(items)
        grand_known += kn
        rows.append((pg, d.get('total', len(items)), len(items), kn, unk))

    print('== 逐状态亮面审计（暗色档，判据=面/线/发光，已扣白名单） ==')
    for pg, tot, n, kn, unk in rows:
        if tot == 'ERR':
            print('%-14s  %s' % (pg, unk[0]))
            continue
        flag = 'OK ' if not unk else '!! '
        print('%s%-14s  总 %-4s 已知 %-3s 非已知 %-3s' % (flag, pg, tot, kn, len(unk)))
    print('-' * 60)
    print('合计 总 %d / 已知 %d / 非已知 %d' % (grand_total, grand_known, grand_total - grand_known))

    print()
    print('== 非已知明细（按页） ==')
    any_unk = False
    for pg, tot, n, kn, unk in rows:
        if tot == 'ERR' or not unk:
            continue
        any_unk = True
        print('--- %s ---' % pg)
        for u in unk:
            print('  [%s] %s  %sx%s  @(%s,%s)  st=%s' % (
                u.get('k'), u.get('v'), u.get('w'), u.get('h'),
                u.get('x'), u.get('y'), (u.get('st') or '')[:70]))
            print('        sel=%s' % u.get('sel'))
            if u.get('img'):
                print('        img=%s' % u.get('img'))
            print('        state=%s' % u.get('state'))
    if not any_unk:
        print('（无）')


if __name__ == '__main__':
    main()
