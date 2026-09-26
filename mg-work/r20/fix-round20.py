# -*- coding: utf-8 -*-
"""Round 20 补丁：kanban.html 5 项调整
1) 弹窗出现瞬间边缘黑边：非整数像素坐标导致边缘抗锯齿半透明，补 1px 同色 spread 覆盖
2) 附件「上传中」卡：标题与进度条间距 4px -> 6px
3) 附件卡 hover：背景加深一级（fill-1 -> fill-2）
4) .kb-crt-editor 容器边框加深一级（border-1 -> border-2）
5) 「创建任务」卡补 hover 态
"""
import io
import sys

PAGE = "pages/kanban.html"
s = io.open(PAGE, encoding="utf-8").read()
orig = len(s)


def sub_once(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print("[FAIL] %s —— 命中 %d 次（期望 1）" % (label, n))
        sys.exit(1)
    s = s.replace(old, new, 1)
    print("[ OK ] %s" % label)


# ───────── 1. 弹窗边缘黑边 ─────────
OLD_SHADOW = """        background: var(--color-bg-1); border-radius: 0 0 12px 12px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
        opacity: 0; transform-origin: top center;"""
NEW_SHADOW = """        background: var(--color-bg-1); border-radius: 0 0 12px 12px;
        /* 首帧黑边修复：left:50%+translateX(-50%) 会落在 .203 这类非整数像素上，
           边缘 1px 被抗锯齿混成半透明、透出深色遮罩，动画期间即一道黑边。
           首位补 1px 同背景色 spread，把半透明边缘填实成纯色。 */
        box-shadow: 0 0 0 1px var(--color-bg-1), 0 1px 2px rgba(0, 0, 0, 0.08);
        opacity: 0; transform-origin: top center;"""
sub_once(OLD_SHADOW, NEW_SHADOW, "1 弹窗边缘黑边")

# ───────── 2. 上传中卡：标题与进度条间距 ─────────
OLD_GAP = """      .kb-crt-upinfo { flex: 1 1 0; min-width: 0; padding-right: 22px; display: flex; flex-direction: column; gap: 4px; }"""
NEW_GAP = """      .kb-crt-upinfo { flex: 1 1 0; min-width: 0; padding-right: 22px; display: flex; flex-direction: column; gap: 6px; }"""
sub_once(OLD_GAP, NEW_GAP, "2 标题/进度条间距 4->6px")

# ───────── 3. 附件卡 hover ─────────
OLD_UP_BG = """      .kb-crt-upfile {
        flex: none; width: 40px; height: 40px; box-sizing: border-box;"""
NEW_UP_BG = """      .kb-crt-uplist .kb-crt-upitem { transition: background-color 120ms var(--transition-timing-function-standard); }
      .kb-crt-uplist .kb-crt-upitem:hover { background: var(--color-fill-2); }
      .kb-crt-upfile {
        flex: none; width: 40px; height: 40px; box-sizing: border-box;"""
sub_once(OLD_UP_BG, NEW_UP_BG, "3 附件卡 hover 加深一级")

# ───────── 4. 编辑器容器边框加深一级 ─────────
OLD_EDGE = """      /* 富文本编辑器：设计稿 880x320，1px #F2F2F2 + 圆角 8；高度可随窗口收缩 */
      .kb-crt-editor {
        margin-top: 20px; width: 100%;
        flex: 1 1 320px; min-height: 140px; max-height: 320px;
        display: flex; flex-direction: column;
        border: 1px solid var(--color-border-1); border-radius: var(--border-radius-large);"""
NEW_EDGE = """      /* 富文本编辑器：设计稿 880x320，1px #E5E5E5（--color-border-2）+ 圆角 8；高度可随窗口收缩 */
      .kb-crt-editor {
        margin-top: 20px; width: 100%;
        flex: 1 1 320px; min-height: 140px; max-height: 320px;
        display: flex; flex-direction: column;
        border: 1px solid var(--color-border-2); border-radius: var(--border-radius-large);"""
sub_once(OLD_EDGE, NEW_EDGE, "4 编辑器边框 border-1 -> border-2")

# ───────── 5. 创建任务卡 hover ─────────
OLD_CREATE = """      [giencoder-theme='dark'] .kb-create { background: rgba(var(--giencoderblue-6), 0.16); border-color: rgba(var(--giencoderblue-6), 0.32); }"""
NEW_CREATE = """      [giencoder-theme='dark'] .kb-create { background: rgba(var(--giencoderblue-6), 0.16); border-color: rgba(var(--giencoderblue-6), 0.32); }
      /* hover：底色与边框各深一级 + 投影，与相邻 .kb-stat 的抬升手感一致 */
      .kb-create { transition: background-color 120ms var(--transition-timing-function-standard), border-color 120ms var(--transition-timing-function-standard), box-shadow 120ms var(--transition-timing-function-standard); }
      .kb-create:hover {
        background: rgb(var(--giencoderblue-2)); border-color: rgb(var(--giencoderblue-3));
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06);
      }
      [giencoder-theme='dark'] .kb-create:hover { background: rgba(var(--giencoderblue-6), 0.24); border-color: rgba(var(--giencoderblue-6), 0.44); }"""
sub_once(OLD_CREATE, NEW_CREATE, "5 创建任务卡 hover")

io.open(PAGE, "w", encoding="utf-8", newline="").write(s)
print("\nDONE  %d -> %d chars" % (orig, len(s)))
