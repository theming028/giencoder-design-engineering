# -*- coding: utf-8 -*-
"""r87-b · 全局界面字号机制（邵先生 r87 第 1 条）

方案 = 「变量等比缩放」（用户确认「使用你推荐的方式」）：
  · `--ui-fs` 是**唯一旋钮**（当前界面基准字号，px 无单位；14 = 默认档）
  · 11 个 DS 字号 token 全部由它 `calc()` 派生 ⇒ 改一处，全站文字等比缩放
    （覆盖：页面自绘模块 + 全站 DS 组件；默认档 ratio=1 时派生值 = 原值 ⇒ 零几何回归）
  · 行高：对「自身声明了 token 字号」的规则，把 `line-height:Npx` / `height:Npx`
    机械派生为 calc（避免字大了行高不变而**裁字**）
  · 外壳（React 渲染的顶栏/侧栏）：它用的是**尾风 px 类**（`text-sm{font-size:14px}`，
    不是 rem ⇒ `html{font-size}` 这根常规杠杆在本工程**不成立**），故逐条覆盖；
    全站实测只用 6 种，列在下面
  · 文字控件高度跟随（只列真正会「字挤爆盒」的），**图标盒与布局盒不跟随**
  · `<head>` 引导脚本读 localStorage 并写成 `<html>` 内联样式 ⇒ 首帧即生效、无闪烁
  · 所有覆盖规则统一加 `body` 前缀 ⇒ 特异性高于任何后置的普通规则，**与脚本执行顺序无关**

用法：
  python mg-work/r87/apply87b-fontsize.py            # 应用（幂等：先摘块 → 还原 → 再派生）
  python mg-work/r87/apply87b-fontsize.py --revert   # 回滚
  python mg-work/r87/apply87b-fontsize.py --dry
"""
import argparse
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
PAGES = sorted(glob.glob(os.path.join(REPO, 'pages', '*.html')))

CSS_ID = 'r87-ui-css'
JS_ID = 'r87-ui-js'
LS_KEY = 'gi-ui-fs'

RATIO = 'var(--ui-fs-ratio)'

# ---------------------------------------------------------------- 派生工具


def sc(px):
    """把 Npx 派生成 calc(Npx * var(--ui-fs-ratio))。"""
    return 'calc(%spx * %s)' % (px, RATIO)


RE_SCALED_LH = re.compile(r'line-height:\s*calc\((\d+(?:\.\d+)?)px \* var\(--ui-fs-ratio\)\)')
RE_SCALED_H2 = re.compile(r'(?<![-\w])height:\s*calc\((\d+(?:\.\d+)?)px \* var\(--ui-fs-ratio\)\);\s*'
                          r'min-height:\s*calc\(\1px \* var\(--ui-fs-ratio\)\)')
RE_SCALED_MH = re.compile(r'min-height:\s*calc\((\d+(?:\.\d+)?)px \* var\(--ui-fs-ratio\)\)')
RE_RAW_LH = re.compile(r'line-height:\s*(\d+(?:\.\d+)?)px')
RE_RAW_H = re.compile(r'(?<![-\w])height:\s*(\d+(?:\.\d+)?)px')
RE_RAW_MH = re.compile(r'(?<![-\w])min-height:\s*(\d+(?:\.\d+)?)px')
RE_HAS_FS = re.compile(r'var\(--font-size-[a-z0-9-]+\)')


def unscale(css):
    """把已派生过的行高/高度还原成裸 px（幂等第一步）。"""
    css = RE_SCALED_H2.sub(lambda m: 'height:%spx' % m.group(1), css)
    css = RE_SCALED_MH.sub(lambda m: 'min-height:%spx' % m.group(1), css)
    css = RE_SCALED_LH.sub(lambda m: 'line-height:%spx' % m.group(1), css)
    return css


def scale_block(body):
    """一个规则体：含 token 字号时，行高与固定高一并派生。"""
    if not RE_HAS_FS.search(body):
        return body
    body = RE_RAW_LH.sub(lambda m: 'line-height:%s' % sc(m.group(1)), body)
    body = RE_RAW_H.sub(lambda m: 'height:%s;min-height:%s' % (sc(m.group(1)), sc(m.group(1))), body)
    return body


RE_RULE = re.compile(r'\{([^{}]*)\}')

RE_OWN_STYLE = re.compile(r'(<style id="%s">)(.*?)(</style>)' % CSS_ID, re.S)


def scale_css(css):
    return RE_RULE.sub(lambda m: '{' + scale_block(m.group(1)) + '}', css)


def converge(css):
    """幂等收敛：unscale → scale，但**本代注入的样式块原样跳过**。

    ⚠ 必须有这一步：本块每次都是按 build_css() 逐字重建的，里面既有
    `line-height:calc(...)`（尾风覆盖）也有裸 `min-height:calc(...)`（高度跟随）。
    若把它一起交给 unscale()，这两类会被还原成字面 px，而 scale_block 又只对
    「自身声明了 token 字号」的规则重派生 ⇒ 它们**永久损毁**（r87 踩过：
    尾风 line-height 与 .giencoder-select-view 的 min-height 双双被吃掉）。
    """
    saved = []

    def stash(m):
        saved.append(m.group(2))
        return m.group(1) + '\x00OWNBLOCK%d\x00' % (len(saved) - 1) + m.group(3)

    css = RE_OWN_STYLE.sub(stash, css)
    css = scale_css(unscale(css))
    for i, blk in enumerate(saved):
        css = css.replace('\x00OWNBLOCK%d\x00' % i, blk)
    return css


def strip_blocks(src):
    """摘掉本代注入的两个块（幂等的第二步）。"""
    src = re.sub(r'<style id="%s">.*?</style>\n?' % CSS_ID, '', src, flags=re.S)
    src = re.sub(r'<script id="%s">.*?</script>\n?' % JS_ID, '', src, flags=re.S)
    return src


# ---------------------------------------------------------------- 注入内容

TAILWIND_OVERRIDES = [
    ('.text-xs', 12, 16),
    ('.text-sm', 14, 20),
    ('.text-lg', 18, 28),
    ('.text-2xl', 24, 32),
]
TAILWIND_PX_ONLY = [(r'.text-\[13px\]', 13), (r'.text-\[11px\]', 11)]

# 文字控件高度跟随（只列真正会「字挤爆盒」的；图标盒 / 布局盒刻意不跟随）
CONTROL_HEIGHTS = [
    ('.giencoder-btn-size-large', 'height', 36),
    ('.giencoder-btn-size-default', 'height', 32),
    ('.giencoder-btn-size-small', 'height', 28),
    ('.giencoder-btn-size-mini', 'height', 24),
    ('.giencoder-input-wrapper', 'height', 32),
    ('.giencoder-input-wrapper[data-size="mini"]', 'height', 24),
    ('.giencoder-input-wrapper[data-size="small"]', 'height', 28),
    ('.giencoder-input-wrapper[data-size="medium"]', 'height', 32),
    ('.giencoder-input-wrapper[data-size="large"]', 'height', 36),
    ('.giencoder-select-view', 'min-height', 32),
    ('.r85-navi', 'height', 36),
    ('.r85-back', 'height', 32),
    ('.r85-btn', 'height', 32),
    ('.r85-seg > button', 'height', 40),
    ('.r85-slider', 'height', 36),
    ('.r85-sl-lbls', 'height', 16),
]


def build_css():
    L = []
    L.append('/* r87 · 全局界面字号（唯一旋钮 = --ui-fs）')
    L.append('   --ui-fs = 当前界面基准字号（px，无单位）；14 = 默认档。')
    L.append('   11 个 DS 字号 token 全部由它派生 ⇒ 改一处，全站文字等比缩放。')
    L.append('   ratio = 1（默认档）时全部派生值 = 原值 ⇒ 零几何回归。')
    L.append('   本块覆盖规则一律加 body 前缀，特异性高于任何后置的普通规则，与脚本执行顺序无关。')
    L.append('   ⚠ --ui-fs / --ui-fs-ratio 只允许在 :root 声明一次（否则会盖掉 <html> 上的内联值）。 */')
    L.append(':root{')
    L.append('  --ui-fs:14;')
    L.append('  --ui-fs-ratio:calc(var(--ui-fs) / 14);')
    for name, px in [('body', 14), ('body-1', 12), ('body-2', 13), ('body-3', 14), ('caption', 12),
                     ('title-1', 16), ('title-2', 20), ('title-3', 24),
                     ('display-1', 36), ('display-2', 48), ('display-3', 56)]:
        L.append('  --font-size-%s:%s;' % (name, sc(px)))
    L.append('}')
    L.append('/* 外壳（React 渲染）用尾风 px 类，不吃 token ⇒ 逐条覆盖；全站实测只用这 6 种。')
    L.append('   新增文字类时需同步补在此处。 */')
    for cls, fs, lh in TAILWIND_OVERRIDES:
        L.append('body %s{font-size:%s;line-height:%s}' % (cls, sc(fs), sc(lh)))
    for cls, fs in TAILWIND_PX_ONLY:
        L.append('body %s{font-size:%s}' % (cls, sc(fs)))
    L.append('/* 文字控件高度跟随（图标盒与布局盒刻意不跟随 —— 本设置只缩放「文字相关」尺寸）。 */')
    for sel, prop, px in CONTROL_HEIGHTS:
        L.append('body %s{%s:%s}' % (sel, prop, sc(px)))
    return '<style id="%s">\n%s\n</style>\n' % (CSS_ID, '\n'.join(L))


def build_js():
    return (
        '<script id="%s">\n'
        '(function () {\n'
        '  /* r87：首帧前把用户选定的界面字号写成 <html> 内联样式，避免闪一下再变大/变小。 */\n'
        '  var OK = { 13: 1, 14: 1, 16: 1, 18: 1, 20: 1, 24: 1 };\n'
        '  var v = null;\n'
        '  try { v = localStorage.getItem(%r); } catch (e) {}\n'
        '  if (v !== null && OK[v * 1] === 1) {\n'
        '    document.documentElement.style.setProperty("--ui-fs", String(v * 1));\n'
        '  }\n'
        '})();\n'
        '</script>\n' % (JS_ID, LS_KEY))


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revert', action='store_true')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    forward = not a.revert
    tag = '应用' if forward else '回滚'
    fail = 0

    for p in PAGES:
        name = os.path.basename(p)
        src = io.open(p, encoding='utf-8').read()

        if not forward and ('id="%s"' % CSS_ID) not in src:
            print('   %-20s 未应用过，跳过' % name)
            continue

        out = strip_blocks(src)          # 1) 摘块
        out = unscale(out)               # 2) 还原派生值
        if forward:
            out = scale_css(out)         # 3) 按规则重新派生
            # 4) 注入到 </head> 之前
            if '</head>' not in out:
                print('!! %-20s 找不到 </head>' % name); fail += 1; continue
            out = out.replace('</head>', build_css() + build_js() + '</head>', 1)
        else:
            out = unscale(out)
            out = re.sub(r'\n?<style id="%s">.*?</style>' % CSS_ID, '', out, flags=re.S)
            out = re.sub(r'\n?<script id="%s">.*?</script>' % JS_ID, '', out, flags=re.S)

        if out == src:
            print('   %-20s 已是目标态（无改动）' % name)
            continue
        if not a.dry:
            io.open(p, 'w', encoding='utf-8').write(out)
        print('%-20s %s   %+d 字符' % (name, tag, len(out) - len(src)))

    if fail:
        print('\n❌ 有 %d 个文件未达预期，已中止' % fail)
        sys.exit(1)
    print('\n✅ r87-b 完成（%s）' % tag)


if __name__ == '__main__':
    main()
