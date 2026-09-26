# -*- coding: utf-8 -*-
"""
第 9 轮修复
1) 需求看板搜索框内字号统一 -> --font-size-body-3 (14px)
2) 基础工作台工作空间切换时图标联动（8 个页面公共外壳）
   - 下拉项 onSelect 传整个 workspace 对象（原来是 name，重名时无法区分）
   - On 的 state 由 name 改为对象
   - 触发器 mn/Vt/... 图标由硬编码紫色 glyph 改为按选中空间的 logoColor/logoIconPaths/logoViewBox/logoIconPos 渲染（20px = 32px * 0.625）
3) settings.html “返回”按钮移入左栏、置于 flex flex-col gap-1 之上（间隔 12px）、与 main 顶对齐，文案改为“返回”，图标改为 arrow-left
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)

ok = 0
fail = 0


def rep(s, old, new, tag, count=None):
    global ok, fail
    n = s.count(old)
    if n == 0:
        print('FAIL', tag)
        fail += 1
        return s
    if count is not None and n != count:
        print('WARN', tag, 'count=', n, 'expected', count)
    print('OK  ', tag, '(x%d)' % n)
    ok += 1
    return s.replace(old, new)


def resub(s, pat, new, tag, count=None):
    global ok, fail
    n = len(re.findall(pat, s))
    if n == 0:
        print('FAIL', tag)
        fail += 1
        return s
    if count is not None and n != count:
        print('WARN', tag, 'count=', n, 'expected', count)
    print('OK  ', tag, '(x%d)' % n)
    ok += 1
    return re.sub(pat, new, s)


# ---------------------------------------------------------------- 1) 搜索框字号
print('=== 1) req-kanban search font-size ===')
p = 'pages/req-kanban.html'
s = open(p, encoding='utf-8').read()
s = rep(s,
        r'\"giencoder-input\" placeholder=\"搜索需求\" style=\"font-size:13px;\"',
        r'\"giencoder-input\" placeholder=\"搜索需求\" style=\"font-size:var(--font-size-body-3);\"',
        'req-kanban rq-search input font-size -> body-3')
open(p, 'w', encoding='utf-8').write(s)

# ------------------------------------------------- 2) 工作空间图标联动（8 页）
print()
print('=== 2) workspace icon sync (all pages) ===')
for p in sorted(glob.glob('pages/*.html')):
    s = open(p, encoding='utf-8').read()
    m = re.search(r'(\w+)=\[\{id:`paa-team`', s)
    if not m:
        print('SKIP', p, '(no workspace list)')
        continue
    arr = m.group(1)
    print('---', p, 'wsList =', arr)
    before = s

    # 2a) 触发器函数：注入 workspaceItem 参数 + 计算 wsIco
    head_pat = re.compile(
        r'(function \w+\(\{onClick:e,onToggleSidebar:t,asideOpen:n=!0,active:r=!1,'
        r'workspaceName:i=`PAA团队工作空间`)'
        r'\}\)\{return\(0,(\w)\.jsxs\)\(`div`,\{className:`relative`,style:\{position:`relative`,'
        r'width:`fit-content`,maxWidth:360,height:26,'
    )
    head_new = (
        r'\g<1>,workspaceItem:wsSrc}){let wsI=wsSrc||' + arr + r'[0],wsK=.625,'
        r'wsIco={bg:wsI.logoColor,vb:wsI.logoViewBox,w:wsI.logoIconPos.w*wsK,'
        r'h:wsI.logoIconPos.h*wsK,x:wsI.logoIconPos.x*wsK,y:wsI.logoIconPos.y*wsK,'
        r'p:wsI.logoIconPaths};return(0,\g<2>.jsxs)(`div`,{className:`relative`,'
        r'style:{position:`relative`,width:`fit-content`,maxWidth:360,height:26,'
    )
    s = resub(s, head_pat, head_new, 'trigger head + wsIco', 1)

    # 2b) 触发器内的 20x20 图标：硬编码 -> 数据驱动
    icon_pat = re.compile(
        r'\(0,(\w)\.jsxs\)\(`div`,\{style:\{width:20,height:20,position:`relative`,flexShrink:0\},'
        r'children:\[\(0,\1\.jsx\)\(`div`,\{className:`absolute`,style:\{left:0,top:0,width:20,'
        r'height:20,borderRadius:4,background:`#9E67E1`,position:`absolute`\}\}\),'
        r'\(0,\1\.jsx\)\(`svg`,\{className:`absolute`,viewBox:`-0\.04 -0\.22 11\.33 10\.5`,'
        r'width:11\.25,height:9\.84,style:\{left:4\.375,top:5,display:`block`,position:`absolute`,'
        r'overflow:`visible`\},children:(\w+)\.map\(\(e,t\)=>\(0,\1\.jsx\)\(`path`,'
        r'\{d:e\.d,fill:e\.fill\},t\)\)\}\)\]\}\)'
    )
    icon_new = (
        r'(0,\g<1>.jsxs)(`div`,{style:{width:20,height:20,position:`relative`,flexShrink:0},'
        r'children:[(0,\g<1>.jsx)(`div`,{className:`absolute`,style:{left:0,top:0,width:20,'
        r'height:20,borderRadius:4,background:wsIco.bg,position:`absolute`}}),'
        r'(0,\g<1>.jsx)(`svg`,{className:`absolute`,viewBox:wsIco.vb,width:wsIco.w,'
        r'height:wsIco.h,style:{left:wsIco.x,top:wsIco.y,display:`block`,position:`absolute`,'
        r'overflow:`visible`},children:wsIco.p.map((e,t)=>(0,\g<1>.jsx)(`path`,'
        r'{d:e.d,fill:e.fill},t))})]})'
    )
    s = resub(s, icon_pat, icon_new, 'trigger icon -> data driven', 1)

    # 2c) 触发器的调用：传 workspaceName(p.name) + workspaceItem(p)
    s = rep(s, 'asideOpen:t,active:l,workspaceName:p,onClick:',
            'asideOpen:t,active:l,workspaceName:p.name,workspaceItem:p,onClick:',
            'trigger call props')

    # 2d) 下拉项 onSelect 传整个 item
    s = rep(s, 'onClick:()=>t?.(e.name)', 'onClick:()=>t?.(e)',
            'dropdown item onSelect -> item')

    # 2e) state: name -> workspace 对象
    s = resub(s,
              r'(\[\w+,\w+\]=\w+\.useState\()' + '`PAA团队工作空间`' + r'\)',
              r'\g<1>' + arr + r'[0])', 'state -> workspace object', 1)

    # 2f) 下拉 selectedName 传 name
    s = rep(s, 'selectedName:p,onSelect:', 'selectedName:p.name,onSelect:',
            'Tn selectedName -> p.name')

    if s == before:
        print('NOCHANGE', p)
    else:
        open(p, 'w', encoding='utf-8').write(s)

# ------------------------------------------------------------- 3) settings.html
print()
print('=== 3) settings 返回按钮 ===')
p = 'pages/settings.html'
s = open(p, encoding='utf-8').read()

# 3a) 新增 arrow-left 图标组件（复用 bundle 里的 lucide 工厂 w）
s = rep(s, 'var he=w(me),ge={name:`plus`,',
        'var he=w(me),heBack=w({name:`arrow-left`,size:24,node:['
        '[`path`,{d:`m12 19-7-7 7-7`,key:`r9al1`}],'
        '[`path`,{d:`M19 12H5`,key:`r9al2`}]]}),ge={name:`plus`,',
        'define arrow-left icon (heBack)')

# 3b) 从 main 内容里移除原“返回基础工作台”按钮
s = rep(s,
        r'(0,j.jsx)(`div`,{className:`flex flex-col gap-3`,children:(0,j.jsxs)(Tt,{to:`/`,'
        r'className:`flex w-fit items-center gap-1.5 rounded-md px-2 py-1 text-sm '
        r'[color:var(--color-text-3)] hover:bg-black/[0.05] hover:[color:var(--color-text-1)]`,'
        r'children:[(0,j.jsx)(he,{className:`size-4`}),`返回基础工作台`]})}),',
        r'',
        'remove old back-link from main')

# 3c) 左栏 settings 分支：在 flex flex-col gap-1 之上插入“返回”按钮容器
BRANCH_HEAD = (r':(0,j.jsx)(j.Fragment,{children:(0,j.jsx)(`div`,'
               r'{className:`flex-1 overflow-y-auto pt-0 pb-2 pr-3`,')
BTN = (r'(0,j.jsx)(`div`,{className:`mb-3 shrink-0`,children:(0,j.jsxs)(Tt,{to:`/`,'
       r'className:`flex w-fit items-center gap-1.5 rounded-md px-2 py-1 text-sm '
       r'[color:var(--color-text-3)] hover:bg-black/[0.05] hover:[color:var(--color-text-1)]`,'
       r'children:[(0,j.jsx)(heBack,{className:`size-4`}),`返回`]})}),')

s = rep(s,
        BRANCH_HEAD + r'children:(0,j.jsx)(`div`,{className:`flex flex-col gap-1`,children:yn.map(',
        r':(0,j.jsx)(j.Fragment,{children:(0,j.jsxs)(`div`,'
        r'{className:`flex-1 overflow-y-auto pt-0 pb-2 pr-3`,children:[' + BTN +
        r'(0,j.jsx)(`div`,{className:`flex flex-col gap-1`,children:yn.map(',
        'insert back btn into sidebar')

# 3d) 补上 children 数组的右中括号
s = rep(s, r'},e.title))})})}),', r'},e.title))})})]}),',
        'close children array in sidebar branch')

open(p, 'w', encoding='utf-8').write(s)

print()
print('OK =', ok, ' FAIL =', fail)
