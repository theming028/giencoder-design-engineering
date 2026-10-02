# -*- coding: utf-8 -*-
u"""r109 第八拍 · 「规则级」硬编码审计器（只读）。

与 audit-hard.py 的差别：
  audit-hard 按「文本位置」扫，把**选择器里的 hex**（如已废弃的尾风类名
  `.bg-\\[\\#E9ECEE\\]`）也算成一处 —— 那类命中是**死的类名文本**，不渲染任何像素。
  本器把每一块 `<style>` 拆成 `selector { body }` 规则，分别统计：
    · VALUE  —— `{ }` 之内的色值字面（**真正渲染**的那些）
    · SEL    —— 选择器里的 hex（类名残留，需与「文档里还有没有这个类」交叉判定）
    · EXEMPT —— 命中豁免（mask / 阴影 / 变量定义 / 纯黑纯白透明 / logo）

判定「死的尾风类」：选择器含 `#XXXXXX` 且该**未转义类名**在文档正文里 0 次出现。

输出：每条规则一行（块 id / 页数 / 选择器 / 值 / 族），供裁决。
"""
import io, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PAGES = os.path.join(REPO, 'pages')
ALL = [u'base', u'avatar', u'automation', u'skills', u'settings',
       u'conversation', u'dev', u'kanban', u'req-kanban', u'task-detail']

RE_ANY = re.compile(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\s*\([^()]*\)')
RE_OPEN = re.compile(r'<(style|script)([^>]*)>')

# 一眼可判的「不是设计选择」
RE_TRANSPARENT = re.compile(r'^#[0-9a-fA-F]{0,8}$')          # 只对 #0000 家族有用
PURE = {u'#000', u'#0000', u'#000000', u'#00000000', u'#fff', u'#ffffff', u'#ffffff00'}


def rd(p):
    b = io.open(p, 'rb').read()
    return b.decode('utf-8').replace(u'\r\n', u'\n')


def blocks(t):
    pos = 0
    while True:
        m = RE_OPEN.search(t, pos)
        if not m:
            return
        tag = m.group(1)
        end = t.find(u'</' + tag + u'>', m.end())
        if end < 0:
            return
        idm = re.search(r'id="([^"]+)"', m.group(2))
        bid = idm.group(1) if idm else u'(anon)'
        yield bid, tag, m.end(), end, t[m.end():end]
        pos = end + len(tag) + 3


def fam(prop):
    p = (prop or u'').lower()
    if not p:
        return u'(?)'
    if 'shadow' in p:
        return u'阴影'
    if p in (u'background', u'background-color', u'background-image', u'fill', u'bg'):
        return u'面'
    if p in (u'color',):
        return u'字'
    if 'border' in p or p in (u'stroke', u'outline'):
        return u'线'
    if 'filter' in p:
        return u'滤镜'
    if 'mask' in p:
        return u'mask'
    return u'其它(%s)' % p


def strip_comments(s):
    s = re.sub(r'<style id="r109-dark-css">.*?</style>', u'', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', u'', s, flags=re.S)
    s = re.sub(r'/\*.*?\*/', u'', s, flags=re.S)
    return s


# 规则切分：以 `}` 为界，向前找最近的 `{`
def rules(css):
    i = 0
    n = len(css)
    while True:
        b = css.find(u'{', i)
        if b < 0:
            return
        e = css.find(u'}', b)
        if e < 0:
            return
        # 选择器 = 上一个 `}` 之后到 `{`
        s = css.rfind(u'}', 0, b)
        s = 0 if s < 0 else s + 1
        sel = css[s:b].strip()
        body = css[b + 1:e]
        yield sel, body
        i = e + 1


def main():
    per_rule = collections.defaultdict(lambda: collections.Counter())   # (bid,sel,lit,fam) -> pages
    killed = collections.Counter()
    for pg in ALL:
        t = strip_comments(rd(PAGES + os.sep + pg + u'.html'))
        # 文档正文（去掉**所有 `<style>` 块**、保留 `<script>` 与静态 HTML）
        # 用于判「类名是否还活着」
        # ★ 踩过：只保留静态 HTML 会把**由 JS 生成**的类名误判成 dead
        #   （实测：交通灯 `bg-[#28C840]` 写在 React 的 className 模板串里，
        #    只扫 HTML ⇒ 误报 dead；保留 script ⇒ 正确判活）。
        # 判据：**只在 `<style>` 里出现** ⇒ dead。
        live = list(t)
        for bid, tag, s, e, body in blocks(t):
            if tag != u'style':
                continue
            for k in range(s, min(e + len(u'</style>'), len(live))):
                live[k] = u'\0'
        live = u''.join(live)
        for bid, tag, s, e, body in blocks(t):
            if tag != u'style':
                continue
            for sel, decl in rules(body):
                hits = [(m.group(0), decl[max(0, m.start() - 40):m.start()]) for m in RE_ANY.finditer(decl)]
                hits = [(v, pre) for v, pre in hits if u'var(' not in
                        decl[max(0, decl.find(v) - 0):decl.find(v)]]
                # 重新取（上面过滤写法易错，改为逐 m 判）
                hits = []
                for m in RE_ANY.finditer(decl):
                    v = m.group(0)
                    inner = v[v.find(u'(') + 1:v.rfind(u')')] if u'(' in v else u''
                    if u'var(' in inner:
                        continue
                    prop = u''
                    pm = re.findall(r'([a-zA-Z-]{2,30})\s*:\s*$', decl[:m.start()])
                    if pm:
                        prop = pm[-1]
                    hits.append((v.lower(), prop))
                if hits:
                    for v, prop in hits:
                        per_rule[(bid, sel[:110], v, fam(prop))][pg] += 1
                # 选择器里的 hex
                for m in RE_ANY.finditer(sel):
                    hx = m.group(0)
                    # 未转义形式：去掉反斜杠
                    plain = hx
                    # 找它所属的尾风类 token
                    # 取选择器里的尾风类 token（未转义形式用于在正文里查存活）
                    # ★ 踩过：原先用 `\s*[:{\s]` 收尾，而**选择器串本身就是整个 className**
                    #   （如 `.bg-\[\#28C840\]`）⇒ 串尾无终止符 ⇒ 正则回溯到底、返回 []，
                    #   于是所有类名都被判成 dead。改用 lookahead 允许串尾。
                    cls = re.findall(r'\.((?:\\.|[^\s.,:{>~])+)\s*(?=[:{\s]|$)', sel)
                    alive = 0
                    for c in cls:
                        cplain = c.replace(u'\\', u'')
                        if cplain and cplain in live:
                            alive += 1
                    killed[(hx.lower(), sel[:80], u'alive' if alive else u'dead')] += 1
    print(u'===== 规则级 VALUE 命中（{} 条规则×值）====='.format(len(per_rule)))
    byfam = collections.defaultdict(list)
    for (bid, sel, v, f), pages in per_rule.items():
        byfam[f].append((v, bid, sel, sum(pages.values()), len(pages)))
    for f in sorted(byfam, key=lambda k: -sum(x[3] for x in byfam[k])):
        rows = sorted(byfam[f], key=lambda x: -x[3])
        print(u'\n── %s：%d 组 / %d 处 ──' % (f, len(rows), sum(x[3] for x in rows)))
        for v, bid, sel, n, npg in rows:
            print(u'  %-28s ×%-3d [%d页] %-9s %s' % (v, n, npg, bid[:9], sel))
    print(u'\n===== 选择器里的 hex（死/活 尾风类名）=====')
    for (hx, sel, st), n in sorted(killed.items(), key=lambda kv: -kv[1]):
        print(u'  %-12s %-5s ×%-3d %s' % (hx, st, n, sel))


if __name__ == '__main__':
    main()
