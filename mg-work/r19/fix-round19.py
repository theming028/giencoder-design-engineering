# -*- coding: utf-8 -*-
"""Round 19 补丁：kanban.html 5 项调整
1) 校验提示改用 DS Message 组件（giencoder-message + icon/content anatomy）
2) 五张统计卡等宽（.kb-create 由固定 184px 改为弹性）
3) 附件区按设计稿 1343:18391 实现「上传中 / 已上传」两种卡片
4) .kb-crt-aside 最小宽度 320px
5) 六个字段可视框宽度统一（修 date-picker 与其他 select 宽度不一致）
"""
import io
import re
import sys

PAGE = "pages/kanban.html"
s = io.open(PAGE, encoding="utf-8").read()
orig_len = len(s)


def sub_once(old, new, label):
    """整段唯一替换，否则中止。"""
    global s
    n = s.count(old)
    if n != 1:
        print("[FAIL] %s —— 命中 %d 次（期望 1）" % (label, n))
        sys.exit(1)
    s = s.replace(old, new, 1)
    print("[ OK ] %s" % label)


# ───────────────────────── 1. Message 组件化 ─────────────────────────
OLD_MSG_CSS = """      .kb-crt-msg {
        display: flex; align-items: center; gap: 8px; height: 32px; padding: 0 16px;
        background: var(--color-bg-2); border-radius: var(--border-radius-medium);
        box-shadow: var(--shadow2-down); font-size: var(--font-size-body-3); white-space: nowrap;
      }
      .kb-crt-msg[hidden] { display: none; }
      .kb-crt-msg-ico { display: inline-flex; color: var(--color-danger-6); }
      .kb-crt-msg-tx { color: var(--color-danger-6); }"""

NEW_MSG_CSS = """      /* 校验提示直接采用 DS Message 组件：尺寸/白底/圆角/阴影/内边距全部由
         .giencoder-message 提供，此处仅保留视图适配层（error 语义图标色 + hidden 支持） */
      .kb-crt-msgs .giencoder-message { white-space: nowrap; }
      .kb-crt-msgs .giencoder-message-icon { display: inline-flex; flex: none; color: var(--color-danger-6); }"""

sub_once(OLD_MSG_CSS, NEW_MSG_CSS, "1a Message CSS 改为 DS 契约")


def msg_html(err_key, text):
    return (
        '        "      <div class=\\"giencoder-message\\" data-component=\\"message\\"'
        ' data-variant=\\"error\\" data-state=\\"default\\" role=\\"status\\"'
        ' data-err=\\"%s\\" hidden>",\n'
        '        "        <span class=\\"giencoder-message-icon\\"><svg viewBox=\\"0 0 16 16\\"'
        ' width=\\"14\\" height=\\"14\\" fill=\\"none\\" stroke=\\"currentColor\\"'
        ' stroke-width=\\"1.5\\" stroke-linecap=\\"round\\"><circle cx=\\"8\\" cy=\\"8\\" r=\\"6.5\\"/>'
        '<path d=\\"M5.6 5.6l4.8 4.8M10.4 5.6l-4.8 4.8\\"/></svg></span>",\n'
        '        "        <span class=\\"giencoder-message-content\\">%s</span>",'
        % (err_key, text)
    )


for key, text in (("type", "「任务类型」不能为空"), ("title", "「任务标题」不能为空")):
    old_cls = 'class=\\"giencoder-message kb-crt-msg\\"'
    i = s.find('data-err=\\"%s\\"' % key)
    if i == -1:
        print("[FAIL] 找不到 message 节点 %s" % key)
        sys.exit(1)
    # 取该节点整段（上一行开头到今天这一行结束）
    start = s.rfind('        "      <div class=\\"giencoder-message', 0, i)
    end = s.find('</span>",', i) + len('</span>",')
    block_old = s[start + len('        "'):end - 1]
    # 直接用已知旧块文本替换
    old_block = (
        '      <div class=\\"giencoder-message kb-crt-msg\\" data-component=\\"message\\"'
        ' data-variant=\\"error\\" data-state=\\"default\\" role=\\"alert\\"'
        ' data-err=\\"%s\\" hidden>",\n'
        '        "        <span class=\\"kb-crt-msg-ico\\"><svg viewBox=\\"0 0 16 16\\"'
        ' width=\\"14\\" height=\\"14\\" fill=\\"none\\" stroke=\\"currentColor\\"'
        ' stroke-width=\\"1.5\\" stroke-linecap=\\"round\\"><circle cx=\\"8\\" cy=\\"8\\" r=\\"6.5\\"/>'
        '<path d=\\"M5.6 5.6l4.8 4.8M10.4 5.6l-4.8 4.8\\"/></svg></span>",\n'
        '        "        <span class=\\"kb-crt-msg-tx\\">%s</span>",' % (key, text)
    )
    sub_once(old_block, msg_html(key, text), "1b message 节点 %s" % key)

# ───────────────────────── 2. 五张统计卡等宽 ─────────────────────────
OLD_CREATE = """      .kb-create {
        position: relative; flex: none; width: 184px; height: 64px;"""
NEW_CREATE = """      /* 与 .kb-stat 同为弹性等宽：5 张卡（创建/待协作/待评审/已延期/已取消）按比例均分 */
      .kb-create {
        position: relative; flex: 1 1 0; min-width: 0; height: 64px;"""
sub_once(OLD_CREATE, NEW_CREATE, "2 .kb-create 改弹性等宽")

# ───────────────────────── 3. 附件区：上传中 / 已上传 ─────────────────────────
OLD_UP_CSS = """      .kb-crt-uplist { margin: 8px 0 0; padding: 0; list-style: none; }
      .kb-crt-upitem { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-1); color: var(--color-text-2); }
      .kb-crt-upname { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .kb-crt-uprm { display: inline-flex; align-items: center; justify-content: center; width: 16px; height: 16px; flex: none; border: none; background: none; cursor: pointer; color: var(--color-text-3); padding: 0; line-height: 0; }
      .kb-crt-uprm:hover { color: var(--color-text-1); }"""

NEW_UP_CSS = """      /* 附件列表：设计稿 1343:18391 —— 卡 256x56 / 底 fill-1 / 圆角 8 / 三栏均分 gap 8
         卡内：40x40 白底文件图标（border fill-2, 圆角 4）；右侧 14x14 移除图标 */
      .kb-crt-uplist {
        margin: 12px 0 0; padding: 0; list-style: none;
        display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;
      }
      .kb-crt-uplist[hidden] { display: none; }
      .kb-crt-uplist .kb-crt-upitem {
        position: relative; box-sizing: border-box; height: 56px; min-width: 0;
        display: flex; align-items: center; gap: 8px; padding: 0 8px;
        background: var(--color-fill-1); border-radius: var(--border-radius-large);
      }
      .kb-crt-upfile {
        flex: none; width: 40px; height: 40px; box-sizing: border-box;
        display: flex; align-items: center; justify-content: center;
        background: var(--color-bg-1); border: 1px solid var(--color-fill-2);
        border-radius: var(--border-radius-medium); color: var(--color-text-2); line-height: 0;
      }
      .kb-crt-upfile svg { width: 18px; height: 18px; }
      .kb-crt-upinfo { flex: 1 1 0; min-width: 0; padding-right: 22px; display: flex; flex-direction: column; gap: 4px; }
      .kb-crt-upname { font-size: var(--font-size-body-3); line-height: 16px; color: var(--color-text-1); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .kb-crt-upmeta { display: flex; align-items: center; gap: 6px; font-size: var(--font-size-body-2); line-height: 16px; color: var(--color-text-3); }
      .kb-crt-updot { flex: none; width: 3px; height: 3px; border-radius: 50%; background: rgb(var(--gray-4)); }
      .kb-crt-upprog { flex: none; width: 150px; max-width: 100%; height: 4px; border-radius: 2px; background: var(--color-fill-3); overflow: hidden; }
      .kb-crt-upprog i { display: block; height: 100%; border-radius: 2px; background: var(--color-primary-6); }
      .kb-crt-uprm { position: absolute; right: 12px; top: 16px; width: 14px; height: 14px; display: inline-flex; align-items: center; justify-content: center; flex: none; border: none; background: none; cursor: pointer; color: var(--color-text-3); padding: 0; line-height: 0; }
      .kb-crt-uprm:hover { color: var(--color-text-1); }"""

sub_once(OLD_UP_CSS, NEW_UP_CSS, "3a 附件列表 CSS")

FILE_ICON = (
    '<svg viewBox=\\"0 0 18 18\\" width=\\"18\\" height=\\"18\\" fill=\\"none\\"'
    ' stroke=\\"currentColor\\" stroke-width=\\"1.4\\" stroke-linecap=\\"round\\"'
    ' stroke-linejoin=\\"round\\"><path d=\\"M10.2 2.2H5.4a1.6 1.6 0 0 0-1.6 1.6v10.4a1.6'
    ' 1.6 0 0 0 1.6 1.6h7.2a1.6 1.6 0 0 0 1.6-1.6V6.4z\\"/><path d=\\"M10.2 2.2v4.2h4.2\\"/>'
    '<path d=\\"M6.9 10.6h4.2M6.9 13.2h2.6\\"/></svg>'
)
CLOSE_ICON = (
    '<svg viewBox=\\"0 0 14 14\\" width=\\"14\\" height=\\"14\\" fill=\\"none\\"'
    ' stroke=\\"currentColor\\" stroke-width=\\"1.3\\" stroke-linecap=\\"round\\">'
    '<path d=\\"M3.2 3.2l7.6 7.6M10.8 3.2l-7.6 7.6\\"/></svg>'
)


def li_item(name, meta_html):
    return (
        '        "            <li class=\\"giencoder-upload-list-item kb-crt-upitem\\">",\n'
        '        "              <span class=\\"kb-crt-upfile\\">%s</span>",\n'
        '        "              <span class=\\"kb-crt-upinfo\\">",\n'
        '        "                <span class=\\"kb-crt-upname\\">%s</span>",\n'
        '%s\n'
        '        "              </span>",\n'
        '        "              <button class=\\"kb-crt-uprm\\" type=\\"button\\" aria-label=\\"移除\\">%s</button>",\n'
        '        "            </li>",' % (FILE_ICON, name, meta_html, CLOSE_ICON)
    )


PROG = ('        "                <span class=\\"kb-crt-upprog\\" role=\\"progressbar\\"'
        ' aria-valuenow=\\"66\\" aria-valuemin=\\"0\\" aria-valuemax=\\"100\\">'
        '<i style=\\"width:53%\\"></i></span>",')
META = ('        "                <span class=\\"kb-crt-upmeta\\">DOCX'
        '<span class=\\"kb-crt-updot\\"></span>256KB</span>",')

OLD_UP_HTML = """        "            <ul class=\\"kb-crt-uplist\\" hidden></ul>","""
NEW_UP_HTML = "\n".join([
    '        "            <ul class=\\"kb-crt-uplist\\">",',
    li_item("业务方原始需求文档", PROG),
    li_item("结构化的 PRD 产品需求文档", META),
    li_item("结构化的 PRD 产品需求文档", META),
    '        "            </ul>",',
])
sub_once(OLD_UP_HTML, NEW_UP_HTML, "3b 附件列表 HTML（1 上传中 + 2 已上传）")

# ───────────────────────── 4. aside 最小宽度 320 ─────────────────────────
OLD_ASIDE = """      .kb-crt-aside {
        flex: 1 1 20%; box-sizing: border-box; min-width: 0;"""
NEW_ASIDE = """      .kb-crt-aside {
        flex: 1 1 20%; box-sizing: border-box; min-width: 320px;"""
sub_once(OLD_ASIDE, NEW_ASIDE, "4 aside min-width: 320px")

# ───────────────────────── 5. 六个字段可视框宽度统一 ─────────────────────────
OLD_DATE_W = """      .kb-crt-date, .kb-crt-date .giencoder-input-wrapper { width: auto; min-width: 0; }"""
NEW_DATE_W = """      /* 六个字段的可视框宽度一律由 .kb-crt-fld 决定，避免 date-picker 与 select 出现宽度差 */
      .kb-crt-fld > .giencoder-select-view,
      .kb-crt-date .giencoder-input-wrapper { width: 100%; box-sizing: border-box; }"""
sub_once(OLD_DATE_W, NEW_DATE_W, "5 date-picker 宽度统一")

io.open(PAGE, "w", encoding="utf-8", newline="").write(s)
print("\nDONE  %d -> %d chars" % (orig_len, len(s)))
