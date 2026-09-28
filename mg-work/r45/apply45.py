#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r45 · 六处修正
  task-detail.html
   1) .td-bar 底部线加深一级：--td-hairline(#F2F2F2) → --color-border-2(#E5E5E5)
   2) 去掉 header 右侧 `flex w-60 items-center justify-end gap-1` 模块的内容（保留 240px 空容器以稳定布局）
  avatar.html
   3) 「当前用户」按钮圆角 rounded-full(9999px) → rounded-md(8px)；「设置」按钮实测已是 8px，不动
   4) .av-main-avatar-face 底色 --color-fill-1(#F7F7F7) → --color-fill-2(#F2F2F2)（DS 填充阶深一级）
   5) .td-right-title 与右侧按钮间距 → 由 .td-right-bar gap 8px 提到 48px（≥48px 下限）
   6) .td-composer 总高 154 → 128px（输入区 min-height 96 → 70；70+32工具条+12×2内距+1×2边框=128）
幂等：重复执行输出「已应用」。
"""
import sys, os, shutil, re

BK = '/tmp/r45-backup'
os.makedirs(BK, exist_ok=True)

def backup(path, name):
    p = os.path.join(BK, name)
    if not os.path.exists(p):
        shutil.copy2(path, p)
    return open(p, encoding='utf-8').read()

# ============ 1) task-detail.html ============
TD = 'pages/task-detail.html'
td_old = backup(TD, 'task-detail.html')
td = open(TD, encoding='utf-8').read()

E1_OLD = 'background: var(--color-bg-1); border-bottom: 1px solid var(--td-hairline);'
E1_NEW = 'background: var(--color-bg-1); border-bottom: 1px solid var(--color-border-2);'

# 2) 清空 header 右侧模块内容 —— 用「children 数组起点 + 末按钮 tail」定界，
#    避免正则被数组内 `[color:…]` 的方括号误伤
MODKEY = 'className:`flex w-60 items-center justify-end gap-1`,children:['
MODTAIL = '`A`})]'

def clear_module(s):
    if MODKEY + ']' in s:            # 已清空 → 幂等
        return s, 0
    i = s.find(MODKEY)
    if i < 0:
        return s, 0
    j = s.find(MODTAIL, i)
    if j < 0:
        raise SystemExit('!! 找不到模块收尾锚点')
    return s[:i] + MODKEY + ']' + s[j + len(MODTAIL):], 1

td2, n_mod = clear_module(td)

applied = 0
for old, new, cnt, marker in [(E1_OLD, E1_NEW, 1, E1_NEW)]:
    if marker in td2:                # 幂等：以新串存在为已应用标志
        continue
    if td2.count(old) != cnt:
        print('!! task-detail 锚点异常 %d: %r' % (td2.count(old), old[:60])); sys.exit(1)
    td2 = td2.replace(old, new, 1); applied += 1

if td2 != td or n_mod:
    open(TD, 'w', encoding='utf-8').write(td2)
print('  task-detail.html  线色 %d 项 / 模块清空 %d 处' % (applied, n_mod))

# ============ 2) avatar.html ============
AV = 'pages/avatar.html'
av_old_txt = backup(AV, 'avatar.html')
av = open(AV, encoding='utf-8').read()

E3_OLD = 'flex size-7 items-center justify-center rounded-full [background-color:var(--color-text-1)]'
E3_NEW = 'flex size-7 items-center justify-center rounded-md [background-color:var(--color-text-1)]'
E4_OLD = 'background: var(--color-fill-1); border-radius: var(--border-radius-medium);'
E4_NEW = 'background: var(--color-fill-2); border-radius: var(--border-radius-medium);'
E5_OLD = r'.td-composer .min-h-\[96px\] { min-height: 96px; }'
E5_NEW = r'.td-composer .min-h-\[96px\] { min-height: 70px; }'
E6_OLD = '.td-right-head { min-width: 0; flex: 1; }'
E6_NEW = ('/* \u2605 第 45 轮：标题与右侧按钮留白 \u2265 48px（原承 .td-right-bar{gap:8px}，标题紧贴按钮） */\n'
          '.td-right-bar { gap: 48px; }\n'
          '.td-right-head { min-width: 0; flex: 1; }')

applied = 0
# 幂等标志 marker 单独给出：E6_OLD 是 E6_NEW 的子串，不能用「新在旧不在」判据
GAP48 = '.td-right-bar { gap: 48px; }'
for old, new, cnt, marker in [(E3_OLD, E3_NEW, 1, E3_NEW), (E4_OLD, E4_NEW, 1, E4_NEW),
                              (E5_OLD, E5_NEW, 1, E5_NEW), (E6_OLD, E6_NEW, 1, GAP48)]:
    if marker in av:
        continue
    if av.count(old) != cnt:
        print('!! avatar 锚点异常 %d: %r' % (av.count(old), old[:60])); sys.exit(1)
    av = av.replace(old, new, 1); applied += 1

if av != open(AV, encoding='utf-8').read():
    open(AV, 'w', encoding='utf-8').write(av)
print('  avatar.html       应用 %d 项' % applied)

# ============ 自检（只认标签级计数 + 被改对象精确增减量）============
bad = 0
td = open(TD, encoding='utf-8').read()
av = open(AV, encoding='utf-8').read()

if td.count(MODKEY + ']') != 1:
    print('!! 模块未清空或重复'); bad += 1
if E1_NEW not in td: print('!! td-bar 线色未生效'); bad += 1
if td.count('--td-hairline') != td_old.count('--td-hairline') - 1:
    print('!! --td-hairline 减少量 ≠ 1'); bad += 1
for key in ['<style', '</style>', '<script', '</script>', 'td-bar', 'td-attr-row']:
    if td.count(key) != td_old.count(key):
        print('!! task-detail 结构漂移 %s: %d → %d' % (key, td_old.count(key), td.count(key))); bad += 1

for frag in [E3_NEW, E4_NEW, E5_NEW, '.td-right-bar { gap: 48px; }']:
    if av.count(frag) != 1: print('!! avatar 新串数量异常 %d: %r' % (av.count(frag), frag[:50])); bad += 1
for frag in [E3_OLD, E4_OLD, E5_OLD, 'min-height: 96px']:
    if frag in av: print('!! avatar 旧串残留: %r' % frag[:50]); bad += 1
if av.count('--color-fill-1') != av_old_txt.count('--color-fill-1') - 1:
    print('!! --color-fill-1 减少量 ≠ 1'); bad += 1
for key in ['<style', '</style>', '<script', '</script>', 'av-main-avatar-face', 'td-composer']:
    if av.count(key) != av_old_txt.count(key):
        print('!! avatar 结构漂移 %s: %d → %d' % (key, av_old_txt.count(key), av.count(key))); bad += 1

print('ALL OK' if not bad else 'FAILED')
sys.exit(0 if not bad else 1)
