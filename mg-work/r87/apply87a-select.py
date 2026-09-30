# -*- coding: utf-8 -*-
"""r87-a · 全站 select 组件三项改动（邵先生 r87 第 2 条）

  ① 去掉 `--select-ring`：它是 `.giencoder-select-view` 内部声明的**局部变量**
     （不是 token），作用是把「表面层」外扩 1px 同色 spread 补齐 —— 去掉变量与该 spread 项，
     保留那条极淡的 `0 1px 2px` 轻投影。
  ② 圆角：`.giencoder-select-view` 的 `border-radius` 由 4px（`--border-radius-medium`）
     改为 8px（`--border-radius-large`）。
  ③ 宽度自适应：`.giencoder-select` 由 `width: 100%` 改为 `width: auto` + `max-width: 100%`
     （`display:inline-flex` ⇒ 按内容收缩）。
  ④ 页面级适配层统一：另有 4 条**页面级**规则把同一个触发框写死成 6px（kanban 3 + req-kanban 1），
     邵先生「三项全部全站」⇒ 一并抬到 8px（含与 select 共用一条规则的日期输入框）。
     ⚠ 刻意**不动** `.select-view-ghost` 胶囊芯片（内联写死 32px，是另一种有意变体，邵先生已确认保留）。

作用面 = 「全站」= 三份 DS 样式源 + 9 个页面：
  · `giencoder-design-system/components.css`               （主源）
  · `giencoder-design-system/gienx-templates/_shared/components.css`（模板层副本）
  · `pages/*.html` 内联副本（构建产物，token 已内联成字面量）
  · `giencoder-design-system/components/select.json`      （契约里消费的 token 名）

⚠ 页面内联副本是**构建产物**（已被 PostCSS 把 token 内联成字面量，如 `border-radius:4px`），
  与 DS 源码写法不同（源码是 `var(--border-radius-medium)`）⇒ 两套替换串各自独立。

用法：
  python mg-work/r87/apply87a-select.py            # 应用（幂等）
  python mg-work/r87/apply87a-select.py --revert   # 回滚到改前
  python mg-work/r87/apply87a-select.py --dry      # 只报告
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
DS_CSS = os.path.join(REPO, 'giencoder-design-system', 'components.css')
# ⚠ DS 的组件样式在仓库里有**两份**源：
#   · giencoder-design-system/components.css                —— 主源
#   · giencoder-design-system/gienx-templates/_shared/components.css —— 模板层副本（build.py 复用它）
# 页面 bundle 内联的是第三份（构建产物）。「全站」三者都要一致，漏一处就会回潮。
SH_CSS = os.path.join(REPO, 'giencoder-design-system', 'gienx-templates', '_shared', 'components.css')
DS_JSON = os.path.join(REPO, 'giencoder-design-system', 'components', 'select.json')

# ---------------------------------------------------------------- 页面（构建副本，压缩形态）

# .giencoder-select-view 的整块（务必整块匹配：`border-radius:4px` 在别处也大量出现）
PV_OLD_RING_VAR = '--select-ring:var(--color-bg-2);'
PV_OLD_RING_USE = ', 0 0 0 1px var(--select-ring)'
PV_OLD_VIEW_HEAD = '.giencoder-select-view{background:var(--color-bg-2);'
PV_RADIUS_OLD = 'border-radius:4px'
PV_RADIUS_NEW = 'border-radius:8px'

# ---------------------------------------------------------------- DS 源（美化形态）

DS_OLD_RING_VAR = '  --select-ring: var(--color-bg-2);\n'
DS_OLD_RING_USE = ', 0 0 0 1px var(--select-ring)'
DS_RADIUS_OLD = 'border: 1px solid var(--color-border-2); border-radius: var(--border-radius-medium); cursor: pointer;'
DS_RADIUS_NEW = 'border: 1px solid var(--color-border-2); border-radius: var(--border-radius-large); cursor: pointer;'
DS_WIDTH_OLD = ('  display: inline-flex; flex-direction: column; position: relative; font-size: var(--font-size-body-3);\n'
                '  color: var(--color-text-1); width: 100%;\n')
DS_WIDTH_NEW = ('  display: inline-flex; flex-direction: column; position: relative; font-size: var(--font-size-body-3);\n'
                '  /* r87：宽度自适应（按内容收缩），不再强制撑满容器；容器需要撑满时由外部给定 width */\n'
                '  color: var(--color-text-1); width: auto; max-width: 100%;\n')
DS_COMMENT_OLD = (
    '  /* Secondary 按钮同款表面层机制：外扩 1px 同色 spread 补齐表面 + 轻投影抬升；\n'
    '     hover 背景向浅灰档过渡（fill-1）、投影加深；按压/展开收起 spread → 表面内缩 1px 下沉 */\n')
DS_COMMENT_NEW = (
    '  /* r87：去掉「表面层外扩 1px 同色 spread」那一圈（原先由局部变量承载）—— 它会让边框视觉加粗；\n'
    '     仅保留极淡的 1px 轻投影；hover 背景向浅灰档过渡（fill-1） */\n')

# ------------------------------------------------ 模板层副本（_shared/components.css）

SH_OLD_RING_VAR = '  --select-ring: var(--color-bg-2);\n'
SH_OLD_RING_USE = ', 0 0 0 1px var(--select-ring)'
SH_COMMENT_OLD = (
    '  /* Secondary 按钮同款表面层机制：外扩 1px 同色 spread 补齐表面 + 轻投影抬升；\n'
    '     hover 背景向浅灰档过渡（fill-1）、投影加深；按压/展开收起 spread → 表面内缩 1px 下沉 */\n')
SH_COMMENT_NEW = (
    '  /* r87：去掉「表面层外扩 1px 同色 spread」那一圈（原先由局部变量承载）—— 它会让边框视觉加粗；\n'
    '     仅保留极淡的 1px 轻投影；hover 背景向浅灰档过渡（fill-1） */\n')
SH_RADIUS_OLD = 'border: 1px solid var(--color-border-2); border-radius: 4px; cursor: pointer;'
SH_RADIUS_NEW = 'border: 1px solid var(--color-border-2); border-radius: var(--border-radius-large); cursor: pointer;'
SH_WIDTH_OLD = '  color: var(--color-text-1); width: 100%;\n}'
SH_WIDTH_NEW = ('  /* r87：宽度自适应（按内容收缩），不再强制撑满容器；容器需要撑满时由外部给定 width */\n'
                '  color: var(--color-text-1); width: auto; max-width: 100%;\n}')


def patch_shared_css(src, forward):
    out = src
    log = []
    if forward:
        if SH_OLD_RING_VAR in out:
            out = out.replace(SH_OLD_RING_VAR, '', 1); log.append('删 --select-ring 变量')
        if SH_OLD_RING_USE in out:
            out = out.replace(SH_OLD_RING_USE, '', 1); log.append('删 ring spread 项')
        if SH_COMMENT_OLD in out:
            out = out.replace(SH_COMMENT_OLD, SH_COMMENT_NEW, 1); log.append('更新表面层注释')
        if SH_RADIUS_OLD in out:
            out = out.replace(SH_RADIUS_OLD, SH_RADIUS_NEW, 1); log.append('圆角 → --border-radius-large')
        if SH_WIDTH_OLD in out:
            out = out.replace(SH_WIDTH_OLD, SH_WIDTH_NEW, 1); log.append('宽度 100% → auto/max-width 100%')
        if '--select-ring:' in out or 'var(--select-ring)' in out:
            return None, ['_shared 副本仍残留 select-ring 用法']
    else:
        out = out.replace(SH_COMMENT_NEW, SH_COMMENT_OLD, 1)
        out = out.replace(SH_WIDTH_NEW, SH_WIDTH_OLD, 1)
        out = out.replace(SH_RADIUS_NEW, SH_RADIUS_OLD, 1)
        if 'select-ring' not in out:
            out = out.replace(
                '  min-height: 32px; padding: 0 12px; background: var(--color-bg-2);\n',
                '  min-height: 32px; padding: 0 12px; background: var(--color-bg-2);\n'
                '  --select-ring: var(--color-bg-2);\n', 1)
            out = out.replace('box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);',
                              'box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 0 0 1px var(--select-ring);', 1)
            log.append('还原 --select-ring')
    return out, log


# ------------------------------------------------ ④ 页面级适配层：6px → 8px
#
# DS 本体改到 8px 后，仍有 4 条**页面级适配规则**把同一个触发框写死成 6px
# （它们是各页当初按设计稿逐页定的，不是 DS 本体）。邵先生 r87 明确「三项全部全站」，
# 故一并统一为 8px。
#   ⚠ kanban 有一条是 `select-view` 与「日期输入框」**共用同一条规则**；
#     邵先生已拍板「输入框同改」⇒ 直接把共用规则的 6px 抬到 8px（保证同行两控件圆角一致）。
# 选择器一律用**精确正则锚定**（页面 bundle 是单行压缩产物，不能用宽松匹配 —— 会误伤
# `.kb-radio` / `.kb-stat-tile` / `.rounded-[6px]` 等一大批与 select 无关的 6px 圆角）。
ADAPTER_FIXUPS = [
    ('kanban.html',
     re.escape('.kb-boardhead .giencoder-select[data-size="small"] .giencoder-select-view')),
    ('kanban.html',
     re.escape('.kb-coop-sel .giencoder-select-view') + r',\s*'
     + re.escape('.kb-coop-date .giencoder-input-wrapper')),
    ('kanban.html',
     re.escape('.kb-coop-pageopt .giencoder-select-view')),
    ('req-kanban.html',
     re.escape('.rq-bh-filters .giencoder-select[data-size="small"] .giencoder-select-view')),
]


def patch_adapters(src, forward, name):
    """把 4 条页面级适配规则里的圆角在 6px ↔ 8px 之间切换。"""
    out = src
    log = []
    for fname, sel_re in ADAPTER_FIXUPS:
        if fname != name:
            continue
        pat = re.compile(sel_re + r'(\s*\{)([^{}]*)(\})')
        hits = list(pat.finditer(out))
        if not hits:
            return None, ['适配层选择器未命中：%s' % sel_re[:60]]
        if len(hits) != 1:
            return None, ['适配层选择器命中 %d 次（预期 1）：%s' % (len(hits), sel_re[:60])]
        m = hits[0]
        body = m.group(2)
        if forward:
            nb = re.sub(r'border-radius:\s*6px', 'border-radius: 8px', body)
            if nb == body and 'border-radius: 8px' not in body:
                return None, ['适配层圆角不在预期形态：%s' % sel_re[:60]]
        else:
            nb = re.sub(r'border-radius:\s*8px', 'border-radius: 6px', body)
            if nb == body and 'border-radius: 6px' not in body:
                return None, ['适配层圆角不在预期形态（回滚）：%s' % sel_re[:60]]
        if nb != body:
            out = out[:m.start(2)] + nb + out[m.end(2):]
            log.append('适配层 6px ↔ 8px：%s' % sel_re[:52].replace('\\', ''))
    return out, log



def patch_page(src, forward, name):
    """对单个页面的内联 select 副本做改动；forward=False 表示回滚。"""
    out = src
    log = []

    # ---- ④ 页面级适配层（6px ↔ 8px）
    out2, log2 = patch_adapters(out, forward, name)
    if out2 is None:
        return None, log2
    out = out2
    log += log2

    # ---- ② 圆角（只在 .giencoder-select-view 块内改）
    m = re.search(r'\.giencoder-select-view\{([^}]*)\}', out)
    if not m:
        return None, ['找不到 .giencoder-select-view 规则']
    body = m.group(1)
    if forward:
        if PV_RADIUS_NEW in body:
            log.append('圆角已是 8px')
        elif PV_RADIUS_OLD in body:
            nb = body.replace(PV_RADIUS_OLD, PV_RADIUS_NEW, 1)
            out = out[:m.start(1)] + nb + out[m.end(1):]
            log.append('圆角 4px → 8px')
        else:
            return None, ['圆角属性不在预期形态']
    else:
        m2 = re.search(r'\.giencoder-select-view\{([^}]*)\}', out)
        if PV_RADIUS_NEW in m2.group(1):
            nb = m2.group(1).replace(PV_RADIUS_NEW, PV_RADIUS_OLD, 1)
            out = out[:m2.start(1)] + nb + out[m2.end(1):]
            log.append('圆角 8px → 4px')

    # ---- ① 去 ring
    if forward:
        if PV_OLD_RING_VAR in out:
            if out.count(PV_OLD_RING_VAR) != 1:
                return None, ['--select-ring 变量出现 %d 次（预期 1）' % out.count(PV_OLD_RING_VAR)]
            out = out.replace(PV_OLD_RING_VAR, '', 1)
            log.append('删 --select-ring 变量')
        if PV_OLD_RING_USE in out:
            if out.count(PV_OLD_RING_USE) != 1:
                return None, ['ring spread 出现 %d 次（预期 1）' % out.count(PV_OLD_RING_USE)]
            out = out.replace(PV_OLD_RING_USE, '', 1)
            log.append('删 ring spread 项')
        if '--select-ring:' in out or 'var(--select-ring)' in out:
            return None, ['仍残留 select-ring 用法']
        # 全局兜底：任何「选择器含 .giencoder-select-view」的规则都不许再写死 6px
        for mm in re.finditer(r'(?P<sel>[^{}]{0,300}?)\{(?P<b>[^{}]{0,400}?)\}', out):
            if '.giencoder-select-view' not in mm.group('sel'):
                continue
            if re.search(r'border-radius\s*:\s*6px', mm.group('b')):
                return None, ['仍有 select-view 规则写死 6px：%s' % mm.group('sel').strip()[-60:]]
    else:
        if 'select-ring' not in out:
            # 还原：把变量加回 select-view 块首，把 spread 项加回 box-shadow
            mb = re.search(r'\.giencoder-select-view\{([^}]*)\}', out)
            nb = mb.group(1)
            nb = nb.replace('background:var(--color-bg-2);',
                            'background:var(--color-bg-2);' + PV_OLD_RING_VAR, 1)
            nb = nb.replace('box-shadow:0 1px 2px #0f172a0a;',
                            'box-shadow:0 1px 2px #0f172a0a' + PV_OLD_RING_USE + ';', 1)
            out = out[:mb.start(1)] + nb + out[mb.end(1):]
            log.append('还原 --select-ring')

    return out, log


def patch_ds_css(src, forward):
    out = src
    log = []
    if forward:
        if DS_OLD_RING_VAR in out:
            out = out.replace(DS_OLD_RING_VAR, '', 1); log.append('删 --select-ring 变量')
        if DS_OLD_RING_USE in out:
            out = out.replace(DS_OLD_RING_USE, '', 1); log.append('删 ring spread 项')
        if DS_COMMENT_OLD in out:
            out = out.replace(DS_COMMENT_OLD, DS_COMMENT_NEW, 1); log.append('更新表面层注释')
        if DS_RADIUS_OLD in out:
            out = out.replace(DS_RADIUS_OLD, DS_RADIUS_NEW, 1); log.append('圆角 → --border-radius-large')
        if DS_WIDTH_OLD in out:
            out = out.replace(DS_WIDTH_OLD, DS_WIDTH_NEW, 1); log.append('宽度 100% → auto/max-width 100%')
        if '--select-ring:' in out or 'var(--select-ring)' in out:
            return None, ['DS 源仍残留 select-ring 用法']
    else:
        out = out.replace(DS_COMMENT_NEW, DS_COMMENT_OLD, 1)
        out = out.replace(DS_WIDTH_NEW, DS_WIDTH_OLD, 1)
        out = out.replace(DS_RADIUS_NEW, DS_RADIUS_OLD, 1)
        if 'select-ring' not in out:
            out = out.replace(
                '  min-height: 32px; padding: 0 12px; background: var(--color-bg-2);\n',
                '  min-height: 32px; padding: 0 12px; background: var(--color-bg-2);\n'
                '  --select-ring: var(--color-bg-2);\n', 1)
            out = out.replace('box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);',
                              'box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 0 0 1px var(--select-ring);', 1)
            log.append('还原 --select-ring')
    return out, log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revert', action='store_true')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    forward = not a.revert
    tag = '应用' if forward else '回滚'
    fail = 0

    for p in PAGES:
        src = io.open(p, encoding='utf-8').read()
        name = os.path.basename(p)
        out, log = patch_page(src, forward, name)
        if out is None:
            print('!! %-20s %s' % (name, ' / '.join(log))); fail += 1; continue
        if out == src:
            print('   %-20s 已是目标态（无改动）' % name); continue
        if not a.dry:
            io.open(p, 'w', encoding='utf-8').write(out)
        print('%-20s %s   %+d 字符' % (name, tag, len(out) - len(src)))
        for l in log:
            print('        · ' + l)

    for path, fn in ((DS_CSS, patch_ds_css), (SH_CSS, patch_shared_css)):
        src = io.open(path, encoding='utf-8').read()
        out, log = fn(src, forward)
        name = os.path.relpath(path, REPO)
        if out is None:
            print('!! %-20s %s' % (name, ' / '.join(log))); fail += 1; continue
        if not a.dry and out != src:
            io.open(path, 'w', encoding='utf-8').write(out)
        print('%-20s %s   %+d 字符' % (name, tag, len(out) - len(src)))
        for l in log:
            print('        · ' + l)

    # 契约文件：消费的 token 名 4 → 8
    if os.path.exists(DS_JSON):
        src = io.open(DS_JSON, encoding='utf-8').read()
        if forward and '--border-radius-medium' in src:
            out = src.replace('--border-radius-medium', '--border-radius-large')
            if not a.dry:
                io.open(DS_JSON, 'w', encoding='utf-8').write(out)
            print('%-20s %s   · token --border-radius-medium → large' % ('components/select.json', tag))
        elif not forward and '--border-radius-large' in src:
            out = src.replace('--border-radius-large', '--border-radius-medium')
            if not a.dry:
                io.open(DS_JSON, 'w', encoding='utf-8').write(out)
            print('%-20s %s   · token --border-radius-large → medium' % ('components/select.json', tag))

    if fail:
        print('\n❌ 有 %d 个文件未达预期，已中止' % fail)
        sys.exit(1)
    print('\n✅ r87-a 完成（%s）' % tag)


if __name__ == '__main__':
    main()
