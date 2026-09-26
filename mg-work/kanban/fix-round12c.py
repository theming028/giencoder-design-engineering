# -*- coding: utf-8 -*-
"""round12c: 模态内层收尾
a) table-layout: fixed —— 让 colgroup 生效（auto 布局下浏览器按内容分配，把「创建时间」压到 132px 截断）
b) 序号列 56 → 48（设计稿实测）
c) 表头 padding 5.75px → 32px
d) 关闭键：打开时聚焦对话框本身（而非关闭键）避免默认焦点环；补 :focus-visible 主题环
幂等。
"""
import io, sys

P = r'E:\GienCoder\giencoder-design-engineering\pages\kanban.html'
s = io.open(P, encoding='utf-8').read()
orig = len(s)
log = []

# a) table-layout: fixed
OLD = "      .kb-coop-tbl { width: 100%; border-collapse: collapse; font-size: var(--font-size-body-3); }"
NEW = ("      /* table-layout:fixed —— 让 <colgroup> 列宽成为权威值；\n"
       "         auto 布局会按内容分配宽度，把「创建时间」压窄到放不下 yyyy/mm/dd hh:mm 而截断 */\n"
       "      .kb-coop-tbl { width: 100%; table-layout: fixed; border-collapse: collapse; font-size: var(--font-size-body-3); }")
if 'table-layout: fixed' in s:
    log.append('[a] table-layout 已设置，跳过')
elif OLD in s:
    s = s.replace(OLD, NEW, 1)
    log.append('[a] table-layout: fixed 写入')
else:
    log.append('[a] !! .kb-coop-tbl 锚点未找到'); sys.exit(1)

# b) 序号列 48
if '<col style=\\"width:56px\\"><col style=\\"width:115px\\"><col>' in s:
    s = s.replace('<col style=\\"width:56px\\"><col style=\\"width:115px\\"><col>',
                  '<col style=\\"width:48px\\"><col style=\\"width:115px\\"><col>', 1)
    log.append('[b] 序号列 56 → 48')
elif '<col style=\\"width:48px\\"><col style=\\"width:115px\\"><col>' in s:
    log.append('[b] 序号列已为 48，跳过')
else:
    log.append('[b] !! colgroup 锚点未找到（继续）')

# c) 表头 5.5 → 5.75
if 'padding: 5.5px 12px; line-height: 20px;' in s:
    s = s.replace('padding: 5.5px 12px; line-height: 20px;', 'padding: 5.75px 12px; line-height: 20px;', 1)
    log.append('[c] 表头内距 5.75px')
elif 'padding: 5.75px 12px; line-height: 20px;' in s:
    log.append('[c] 表头内距已是 5.75，跳过')
else:
    log.append('[c] !! 表头内距锚点未找到（继续）')

# d) 关闭键焦点环
OLD_CLOSE = "      .kb-coop-close:hover { background: var(--color-fill-2); color: var(--color-text-1); }"
NEW_CLOSE = (OLD_CLOSE + "\n"
             "      /* 打开时聚焦的是对话框本身；关闭键仅在键盘 Tab 到达时给主题焦点环，避免露出系统默认轮廓 */\n"
             "      .kb-coop-close:focus { outline: none; }\n"
             "      .kb-coop-close:focus-visible { outline: none; box-shadow: 0 0 0 2px var(--color-primary-light-2); }\n"
             "      .kb-coop-dialog:focus { outline: none; }")
if '.kb-coop-close:focus-visible' in s:
    log.append('[d] 关闭键焦点样式已存在，跳过')
elif OLD_CLOSE in s:
    s = s.replace(OLD_CLOSE, NEW_CLOSE, 1)
    log.append('[d] 关闭键焦点样式写入')
else:
    log.append('[d] !! 关闭键 hover 锚点未找到'); sys.exit(1)

OLD_FOCUS = """      var first = modal.querySelector('.kb-coop-close');
      if (first) first.focus({ preventScroll: true });"""
NEW_FOCUS = """      var dlg = modal.querySelector('.kb-coop-dialog');
      if (dlg) dlg.focus({ preventScroll: true });"""
if OLD_FOCUS in s:
    s = s.replace(OLD_FOCUS, NEW_FOCUS, 1)
    log.append('[d2] open() 改为聚焦对话框')
elif 'dlg.focus(' in s:
    log.append('[d2] 已聚焦对话框，跳过')
else:
    log.append('[d2] !! open() 聚焦锚点未找到（继续）')

# d3) 对话框加 tabindex，保证可编程聚焦
if 'class=\\"giencoder-modal kb-coop-dialog\\" role=\\"dialog\\" aria-modal=\\"true\\" aria-label=\\"待协作任务\\"' in s:
    s = s.replace('class=\\"giencoder-modal kb-coop-dialog\\" role=\\"dialog\\" aria-modal=\\"true\\" aria-label=\\"待协作任务\\"',
                  'class=\\"giencoder-modal kb-coop-dialog\\" role=\\"dialog\\" aria-modal=\\"true\\" tabindex=\\"-1\\" aria-label=\\"待协作任务\\"', 1)
    log.append('[d3] 对话框 tabindex=-1')
elif 'tabindex=\\"-1\\" aria-label=\\"待协作任务\\"' in s:
    log.append('[d3] tabindex 已存在，跳过')
else:
    log.append('[d3] !! dialog 锚点未找到（继续）')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
for l in log:
    print(l)
print('DONE  %d -> %d chars' % (orig, len(s)))
