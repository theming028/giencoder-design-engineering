# -*- coding: utf-8 -*-
"""round12b: 补 3 处（JSON 字符串内需用转义引号匹配）+ JS 挂载 main"""
import io, sys

P = r'E:\GienCoder\giencoder-design-engineering\pages\kanban.html'
s = io.open(P, encoding='utf-8').read()
orig = len(s)
log = []

# ---- 3b. FAB 图标（JSON 转义形式）----
OLD_ICON = ('<svg viewBox=\\"0 0 20 20\\" fill=\\"none\\"><rect x=\\"2.5\\" y=\\"4.5\\" width=\\"13\\" height=\\"11\\" rx=\\"3\\" '
            'stroke=\\"currentColor\\" stroke-width=\\"1.3\\"/><path d=\\"M6.5 9.5v1.5M10 9.5v1.5\\" stroke=\\"currentColor\\" '
            'stroke-width=\\"1.3\\" stroke-linecap=\\"round\\"/><path d=\\"M14.5 2.5l.6 1.4 1.4.6-1.4.6-.6 1.4-.6-1.4-1.4-.6 1.4-.6.6-1.4Z\\" '
            'fill=\\"currentColor\\"/></svg>')
NEW_ICON = ('<svg viewBox=\\"0 0 20 20\\" fill=\\"none\\" aria-hidden=\\"true\\">'
            '<path d=\\"M9 4.2C9.36 7.5 12.3 10.44 15.6 10.8C12.3 11.16 9.36 14.1 9 17.4C8.64 14.1 5.7 11.16 2.4 10.8'
            'C5.7 10.44 8.64 7.5 9 4.2Z\\" fill=\\"currentColor\\"/>'
            '<path d=\\"M16.2 1.2C16.35 2.55 17.55 3.75 18.9 3.9C17.55 4.05 16.35 5.25 16.2 6.6C16.05 5.25 14.85 4.05 13.5 3.9'
            'C14.85 3.75 16.05 2.55 16.2 1.2Z\\" fill=\\"currentColor\\"/></svg>')
if 'M9 4.2C9.36 7.5' in s:
    log.append('[3b] FAB 图标已替换，跳过')
elif OLD_ICON in s:
    s = s.replace(OLD_ICON, NEW_ICON, 1)
    log.append('[3b] FAB 图标替换为 AI 四角星')
else:
    log.append('[3b] !! 仍未命中'); sys.exit(1)

# ---- 4c. 列宽（JSON 转义形式）----
CL_OLD = ('<colgroup><col style=\\"width:52px\\"><col style=\\"width:132px\\"><col>'
          '<col style=\\"width:96px\\"><col style=\\"width:110px\\"><col style=\\"width:170px\\"></colgroup>')
CL_NEW = ('<colgroup><col style=\\"width:56px\\"><col style=\\"width:115px\\"><col>'
          '<col style=\\"width:100px\\"><col style=\\"width:120px\\"><col style=\\"width:184px\\"></colgroup>')
if CL_OLD in s:
    s = s.replace(CL_OLD, CL_NEW, 1)
    log.append('[4c] 列宽对齐设计稿')
elif 'width:115px' in s:
    log.append('[4c] 列宽已是新值，跳过')
else:
    log.append('[4c] !! 仍未命中'); sys.exit(1)

# ---- 4d. JS：模态挂到 main 下 ----
JS_OLD = """  function bindCoopModal(root) {
    var modal = root.querySelector('.kb-coop');
    var trigger = root.querySelector('.kb-stat--coop');
    if (!modal || !trigger) return;"""
if 'host.appendChild(modal)' in s:
    log.append('[4d] JS 已处理，跳过')
elif JS_OLD in s:
    s = s.replace(JS_OLD, JS_OLD + """
    /* r12: 面板只覆盖 main —— 把模态节点从 .kb-panel 内提到 <main> 下，
       否则绝对定位基准会是 .kb-panel（position:absolute）而非 main */
    var host = document.querySelector('main');
    if (host) {
      host.classList.add('kb-main-rel');
      if (modal.parentElement !== host) host.appendChild(modal);
    }""", 1)
    log.append('[4d] JS 模态提到 main 下')
else:
    log.append('[4d] !! bindCoopModal 锚点未找到'); sys.exit(1)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
for l in log:
    print(l)
print('DONE  %d -> %d chars' % (orig, len(s)))
