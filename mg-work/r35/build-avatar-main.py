# -*- coding: utf-8 -*-
"""第 35 轮第 2 项 —— 还原 pages/avatar.html 的「数字分身」主内容。

设计稿节点：1345:18487（容器 53，800×1200）；用户要求内容默认宽 **860px**。

做法（与第 34 轮第 2 项同一条路子：产物上打补丁、幂等、可升级）：
  1. **React 层**：把 bundle 里 `function Dt(){…}` 的渲染体换成
     `<div class="av-main">`（空壳）。React 对该 div 无子节点声明，
     故之后由本脚本注入的 innerHTML 不会被 React 协调覆盖。
     ‣ 原渲染体由「花括号配平」在构建期定位，不硬编码（bundle 是外部 Vite 产物）。
  2. **内容层**：完整还原标记放在 `<template id="av-main-tpl">`（惰性、不渲染），
     由注入脚本在 React 挂载后填进 `.av-main`（MutationObserver 兜底首帧时序）。
  3. **样式层**：`av-main-*` / `av-card` / `av-row` / `av-link` 为视图适配层，
     一律作用在设计系统契约类（.giencoder-card / -card-header / -card-body /
     -header-title / -header-extra / -avatar / -tag / -btn）之上，不改组件本体。

设计稿真值来源（MasterGo MCP）：
  · `get_selection_node 1345:18487` → 全部几何（mg-work/r34/design/avatar-main.txt）
  · `get_screenshot` 逐节点 PNG → 全部文案 + 字号 + 配色
    （C:/Users/Administrator/.mgmcp/resources/screenshots/193158744355579/263-06824/）
    ⚠️ `text/title` 组件在 get_selection_node 里不返回文案，卡片/行卡标题只能靠截图取；
       本脚本的 CONTENT 已按截图逐字校正（不再有推断值）。

用法：C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe mg-work/r35/build-avatar-main.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEST = os.path.join(ROOT, "pages", "avatar.html")
START = "<!-- AV-MAIN"
END = "<!-- /AV-MAIN -->"
VERSION = "v2 —— 数字分身主内容还原（设计稿 1345:18487，内容宽 860px；文案/字号/配色按截图逐项校正）"

# ══════════════════════════ 内容（逐字取自设计稿截图） ══════════════════════════
CONTENT = {
    "name": "艾迪",
    "pill": "数字分身",
    "created": "创建于 2026年06月25日",
    "desc": "学习我的聊天风格、知识库和人格画像，以结果导向、事实至上的心智模型自主执行任务，"
            "能像我一样思考、沟通和决策，同时保持人格一致性和战略对齐。",
    "edit": "编辑",
    "trigger": "通过对话完善数字分身",

    "cardA": {
        "title": "我的人格", "link": "编辑 SOUL.md", "thumb": 180,
        "para": "我作为助手的核心行事准则：以务实交付取代空话，保持独立思考与立场，凡事先自行推演、"
                "带着方案而非问题沟通，以克制的向外行动和果断的内在学习建立可信度，并始终珍视用户"
                "托付的隐私与信任；在边界上严守隐私、不擅作主张、不提交半成品、不捏造信息，"
                "准确优先于自信；气质上追求做一个有主见、有温度的协作者，该简洁时简洁，该深入时深入。",
    },
    "cardB": {
        "title": "我的画像", "link": "编辑 USER.md", "thumb": 72,
        "groups": [
            {"title": "基本信息", "lines": [
                "姓名：邵先生",
                "机构：中电金信研究院",
                "角色：覆盖产品/设计/文档/办公自动化"]},
            {"title": "沟通偏好", "lines": [
                "中文沟通",
                "文风简洁犀利幽默（Luke Wen/听风的蚕风格）",
                "结构化、直接",
                "一次问一个问题，选择题优先（提供 2-3 个选项）",
                "及时确认：每个关键理解都要确认"]},
        ],
    },
    "cardC": {
        "title": "工作风格", "link": "编辑 BEHAVIOR.md", "thumb": 180,
        "items": [
            ("先理解再行动", "复杂任务先梳理全貌，避免方向错误返工。"),
            ("说明推理过程", "重要决策时展示你的思路，让我能判断逻辑是否正确。"),
            ("权衡利弊", "有多种方案时列出各自优劣，给出你的倾向但让我做最终决定。"),
            ("指出风险", "看到潜在问题或边界情况时主动提醒，即使我没有问。"),
        ],
    },
    "cardD": {
        "title": "工作流程", "link": "打开所在文件夹", "thumb": 100,
        "items": [
            ("编码任务执行协议", "8 步主流程 + Harness 强制 5 步检查"),
            ("OADA 自我进化循环", "Observe→Analyze→Decide→Act，含快记/完整两种日志格式"),
            ("OpenSpec 主动触发工作流", "4 步 + PRD 逐章节确认 + 技能链 + 输出路径规范"),
            ("产品设计工作流程", "4 步 + PRD 逐章节确认 + 技能链 + 输出路径规范"),
        ],
    },

    "rows": [
        {"title": "长期记忆",
         "sub": "AI 的长期记忆让它能跨对话记住你，越聊越懂你，告别每次“重新介绍”的陌生感。",
         "meta": "来自 MEMORY.md，5.2 KB，最后更新于 2026/07/25 10:19",
         "links": ["查看"]},
        {"title": "知识库",
         "sub": "AI 知识库通过提供可检索的事实依据，来减少模型幻觉并提升回答准确性。",
         "meta": "12.28 MB，最后更新于 2026/07/25 10:19",
         "links": ["管理知识库", "打开所在文件夹"]},
        {"title": "存储位置",
         "sub": "数字分身「艾迪」所有意识文件的存储目录",
         "meta": "~/.geincoder-x/ai-avatar/main",
         "links": ["打开所在文件夹"]},
    ],

    "foot": "© 数字分身",
}

# ══════════════════════════ 图标 ══════════════════════════
ARROW = ('<svg class="av-link-arrow" viewBox="0 0 12 12" fill="none" aria-hidden="true">'
         '<path d="M4.5 2.5L8 6l-3.5 3.5" stroke="currentColor" stroke-width="1.2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')
PILL_ICON = ('<svg viewBox="0 0 12 12" fill="none" aria-hidden="true">'
             '<path d="M6 1.2l1.35 3.45L10.8 6 7.35 7.35 6 10.8 4.65 7.35 1.2 6l3.45-1.35z" '
             'fill="currentColor"/></svg>')
# 与 pages/task-detail.html / 第 34 轮抽屉触发器同一个图标，保证两页视觉一致
TRIGGER_ICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" class="size-3.5" aria-hidden="true">'
    '<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/>'
    '<path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/></svg>')
EDIT_ICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" class="size-3.5" aria-hidden="true">'
    '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def link(text, cls=""):
    c = ("av-link " + cls).strip()
    return '<button type="button" class="%s">%s%s</button>' % (c, esc(text), ARROW)


def card(key):
    c = CONTENT[key]
    if "para" in c:
        body = '<p class="av-para">%s</p>' % esc(c["para"])
    elif "groups" in c:
        parts = []
        for gp in c["groups"]:
            lines = "".join('<span class="av-line">%s</span>' % esc(l) for l in gp["lines"])
            parts.append('<div class="av-item"><span class="av-item-title">%s</span>'
                         '<span class="av-lines">%s</span></div>' % (esc(gp["title"]), lines))
        body = '<div class="av-list">%s</div>' % "".join(parts)
    else:
        body = '<div class="av-list">%s</div>' % "".join(
            '<div class="av-item"><span class="av-item-title">%s</span>'
            '<span class="av-item-desc">%s</span></div>' % (esc(t), esc(d)) for t, d in c["items"])
    return (
        '        <section class="giencoder-card av-card">\n'
        '          <div class="giencoder-card-header">\n'
        '            <span class="giencoder-card-header-title">%s</span>\n'
        '            <span class="giencoder-card-header-extra">%s</span>\n'
        '          </div>\n'
        '          <div class="giencoder-card-body">%s</div>\n'
        '          <span class="av-card-thumb" style="height:%dpx" aria-hidden="true"></span>\n'
        '        </section>' % (esc(c["title"]), link(c["link"]), body, c["thumb"])
    )


def row(r):
    acts = []
    for i, txt in enumerate(r["links"]):
        if i:
            acts.append('<span class="av-link-sep" aria-hidden="true"></span>')
        acts.append(link(txt))
    return (
        '        <section class="giencoder-card av-row">\n'
        '          <div class="av-row-head">\n'
        '            <div class="av-row-info">\n'
        '              <span class="av-row-title">%s</span>\n'
        '              <span class="av-row-sub">%s</span>\n'
        '            </div>\n'
        '            <span class="av-row-actions">%s</span>\n'
        '          </div>\n'
        '          <span class="av-row-bar" aria-hidden="true"></span>\n'
        '          <span class="av-row-meta">%s</span>\n'
        '        </section>' % (esc(r["title"]), esc(r["sub"]), "".join(acts), esc(r["meta"]))
    )


MAIN_HTML = (
    '  <template id="av-main-tpl">\n'
    '    <div class="av-main">\n'
    '      <header class="av-main-head">\n'
    '        <span class="giencoder-avatar giencoder-avatar-square av-main-avatar" role="img" '
    'aria-label="%s">\n'
    '          <span class="av-main-avatar-face">\U0001F383</span>\n'
    '        </span>\n'
    '        <div class="av-main-head-info">\n'
    '          <span class="av-main-name-row">\n'
    '            <h1 class="av-main-name">%s</h1>\n'
    '            <span class="giencoder-tag av-main-pill">%s%s</span>\n'
    '          </span>\n'
    '          <p class="av-main-created">%s</p>\n'
    '          <p class="av-main-desc">%s</p>\n'
    '        </div>\n'
    '        <span class="av-main-head-actions">\n'
    '          <button type="button" class="giencoder-btn giencoder-btn-secondary '
    'giencoder-btn-size-default av-main-edit">%s%s</button>\n'
    '          <button type="button" class="giencoder-btn giencoder-btn-secondary '
    'giencoder-btn-size-default" data-av-chat-toggle="1" aria-controls="av-chat-drawer" '
    'aria-expanded="false">%s%s</button>\n'
    '        </span>\n'
    '      </header>\n'
    '\n'
    '      <div class="av-main-rule" role="separator" aria-orientation="horizontal"></div>\n'
    '\n'
    '      <div class="av-main-grid">\n'
    '%s\n'
    '%s\n'
    '%s\n'
    '%s\n'
    '      </div>\n'
    '\n'
    '      <div class="av-main-rows">\n'
    '%s\n'
    '      </div>\n'
    '\n'
    '      <div class="av-main-foot">%s</div>\n'
    '    </div>\n'
    '  </template>' % (
        esc(CONTENT["name"]), esc(CONTENT["name"]), PILL_ICON, esc(CONTENT["pill"]),
        esc(CONTENT["created"]), esc(CONTENT["desc"]),
        EDIT_ICON, esc(CONTENT["edit"]),
        TRIGGER_ICON, esc(CONTENT["trigger"]),
        card("cardA"), card("cardB"), card("cardC"), card("cardD"),
        "\n".join(row(r) for r in CONTENT["rows"]),
        esc(CONTENT["foot"]),
    )
)

# ══════════════════════════ CSS（视图适配层） ══════════════════════════
CSS_TMPL = """<style id="av-main-css">
  /* ============================================================
     AV-MAIN @@VER@@

     视图适配层：一律作用在设计系统契约类（.giencoder-card / -card-header /
     -card-header-title / -card-header-extra / -card-body / -avatar / -tag / -btn）
     之上，不改组件本体；颜色·圆角·字号全部走 token 变量。

     几何 = 设计稿节点 1345:18487（容器 53，800×1200）逐项实测：
       头部 110 · 页分隔线 y130 · 卡片网格 y150（卡 292 / 列距 16 / 行距 16）
       底部三行卡 y766/900/1034（各 118 / 间距 16）· 页脚 16（y1184）· 整页 1200
       卡内：卡头 36(含 1px 底纹) · 卡体自 y56 起 · 左右内边距 20
     内容宽按用户要求 860px（设计 800）；两列卡片等比拉伸 392 → 422。

     字号/配色 = 逐节点 PNG 截图实测（scale 2，逐字形量 pitch）：
       卡头标题 14px/#1F1F1F · 卡头链接 12px/#6B6B6B
       卡体条目标题 14px/#1F1F1F · 条目描述与列表行 12px/20/#6B6B6B
       卡体段落 14px/22/#6B6B6B · 行卡标题 14px/#1F1F1F
       行卡副标题 12px/#6B6B6B · 行卡元信息 12px/#868686 · 行卡链接 14px
       姓名 20px/#1F1F1F · 创建时间 14px/#868686 · 描述 14px/22/#6B6B6B · 页脚 12px/#A9A9A9
     ============================================================ */

  /* 设计稿里这几个颜色不在 token 表内（#6B6B6B / #A9A9A9），
     与详情页的 --td-ico-gray 同值，故在适配层收敛成局部变量，避免散落硬编码。 */
  .av-main {
    --av-ink: var(--color-text-1);      /* #1F1F1F */
    --av-ink-2: #6B6B6B;                /* 设计稿次级文字（非 token） */
    --av-ink-3: var(--color-text-3);    /* #868686 */
    --av-ink-4: #A9A9A9;                /* 页脚（非 token） */

    width: 100%; max-width: 860px; margin: 0 auto; box-sizing: border-box;
    display: flex; flex-direction: column;
  }

  /* ---------- 头部（容器 34：800×110） ---------- */
  .av-main-head { position: relative; display: flex; align-items: flex-start; gap: 20px; }
  .av-main-avatar {
    width: 104px; height: 104px; padding: 8px; box-sizing: border-box; flex-shrink: 0;
    background: var(--color-bg-1); border: 1px solid var(--color-border-1);
    border-radius: var(--border-radius-large);
  }
  .av-main-avatar-face {
    width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
    background: var(--color-fill-1); border-radius: var(--border-radius-medium);
    font-size: 40px; line-height: 1;
  }
  .av-main-head-info { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: 8px; }
  .av-main-name-row { display: flex; align-items: center; gap: 8px; height: 28px; }
  .av-main-name {
    margin: 0; font-size: var(--font-size-title-2); font-weight: 600;
    line-height: 28px; color: var(--av-ink);
  }
  /* 胶囊（设计稿 组 9934：80×24 / radius 24 / 白字 12px / 品牌渐变底图） */
  .av-main-pill {
    flex-shrink: 0; height: 24px; padding: 0 8px; gap: 4px; border: none;
    border-radius: 24px; font-size: var(--font-size-body-1); font-weight: 500;
    line-height: 16px; color: #fff;
    background: linear-gradient(90deg, #8FA9F2 0%, #4F68CE 62%, #7C82C7 100%);
  }
  .av-main-pill svg { width: 12px; height: 12px; display: block; flex-shrink: 0; }
  .av-main-created { margin: 0; font-size: var(--font-size-body-3); line-height: 22px; color: var(--av-ink-3); }
  .av-main-desc { margin: 0; font-size: var(--font-size-body-3); line-height: 22px; color: var(--av-ink-2); }
  /* 动作区：设计稿两个按钮同高 32、间距 8、白底 + 1px #E5E5E5 描边、文字 14px #6B6B6B；
     顺序是「编辑」在前、「通过对话完善数字分身」在后（与设计稿截图一致）。
     DS 的 .giencoder-btn-secondary 底色是 --color-bg-5 且文字是 text-1，故在适配层收敛成设计稿值。 */
  .av-main-head-actions { position: absolute; top: 0; right: 0; display: flex; align-items: center; gap: 8px; }
  .av-main-head-actions .giencoder-btn-secondary {
    background: var(--color-bg-1); color: var(--av-ink-2); box-shadow: none;
  }
  .av-main-head-actions .giencoder-btn-secondary:hover { background: var(--color-fill-1); }

  /* ---------- 页分隔线（直线 53：y130） ---------- */
  .av-main-rule { height: 1px; background: var(--color-border-1); margin: 20px 0 19px; }

  /* ---------- 卡片网格（4 张，设计 392×292 → 2×422） ---------- */
  .av-main-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
  .av-card { position: relative; min-height: 292px; border-color: var(--color-border-1); }
  .av-card .giencoder-card-header {
    padding: 6px 20px; background: var(--color-fill-1); border-bottom-color: var(--color-border-1);
    border-radius: var(--border-radius-medium) var(--border-radius-medium) 0 0;
  }
  .av-card .giencoder-card-header-title {
    font-size: var(--font-size-body-3); line-height: 24px; font-weight: 500; color: var(--av-ink);
  }
  .av-card .giencoder-card-header-extra { align-items: center; }
  /* ⚠️ 卡体下内边距 14 = 设计值 16 − 2：DS .giencoder-card 自带 1px 上下边框共 2px，
     而设计稿的卡边框画在背景图里、不占布局 → 不减这 2px 卡片就是 294 而非 292，
     连带把网格、底部三行卡、页脚整体下推（整页 1202 vs 1200）。 */
  .av-card .giencoder-card-body { padding: 19px 20px 14px; background: var(--color-bg-1); }
  /* 卡内滚动指示条（矩形 219：6×N / rgba(0,0,0,.16) / radius 6 / x382） */
  .av-card-thumb {
    position: absolute; right: 4px; top: 40px; width: 6px;
    border-radius: var(--border-radius-circle); background: rgba(0, 0, 0, 0.16);
  }

  /* ---------- 卡内小结构 ---------- */
  .av-list { display: flex; flex-direction: column; gap: 12px; }
  .av-item { display: flex; flex-direction: column; gap: 2px; }
  .av-item-title { font-size: var(--font-size-body-3); line-height: 22px; font-weight: 500; color: var(--av-ink); }
  .av-item-desc { font-size: var(--font-size-body-1); line-height: 20px; color: var(--av-ink-2); }
  .av-lines { display: flex; flex-direction: column; }
  .av-line {
    display: flex; align-items: flex-start; gap: 12px;
    font-size: var(--font-size-body-1); line-height: 20px; color: var(--av-ink-2);
  }
  .av-line::before {
    content: ""; flex-shrink: 0; width: 4px; height: 4px; margin-top: 8px;
    border-radius: var(--border-radius-circle); background: var(--color-text-4);
  }
  .av-para {
    margin: 0; display: -webkit-box; -webkit-line-clamp: 7; -webkit-box-orient: vertical;
    overflow: hidden; font-size: var(--font-size-body-3); line-height: 22px; color: var(--av-ink-2);
  }

  /* ---------- 底部三行卡（容器 48/50/52：800×118） ---------- */
  .av-main-rows { display: flex; flex-direction: column; gap: 16px; margin-top: 16px; }
  .av-row {
    position: relative; height: 118px; box-sizing: border-box; padding: 16px 20px;
    border-color: var(--color-border-1); background: var(--color-bg-1);
  }
  .av-row-head { display: flex; align-items: flex-start; gap: 16px; }
  .av-row-info { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
  .av-row-title { font-size: var(--font-size-body-3); line-height: 24px; font-weight: 500; color: var(--av-ink); }
  .av-row-sub { font-size: var(--font-size-body-1); line-height: 16px; color: var(--av-ink-2); }
  /* 细线（矩形 219/直线 52：128×1 / #E5E5E5）实测在 y69 → 距副标题底 11 */
  .av-row-bar { display: block; width: 128px; height: 1px; background: var(--color-border-2); margin-top: 11px; }
  .av-row-meta { font-size: var(--font-size-body-1); line-height: 16px; color: var(--av-ink-3); margin-top: 12px; }
  .av-row-actions { margin-left: auto; display: inline-flex; align-items: center; gap: 12px; flex-shrink: 0; }
  .av-link-sep { width: 1px; height: 12px; background: var(--color-text-4); }

  /* ---------- 文字链接（DS Link 契约约定 root 为 <a>、无类名，视觉由适配层承载） ---------- */
  .av-link {
    display: inline-flex; align-items: center; gap: 2px; padding: 0; border: none; background: none;
    cursor: pointer; font-family: inherit; font-size: var(--font-size-body-1); line-height: 16px;
    color: var(--av-ink-2); border-radius: var(--border-radius-medium);
    transition: color var(--transition-duration-2) var(--transition-timing-function-standard);
  }
  .av-link:hover { color: var(--color-primary-6); }
  .av-link-arrow { width: 12px; height: 12px; flex-shrink: 0; }
  .av-row .av-link { font-size: var(--font-size-body-3); line-height: 24px; }
  .av-row .av-link-arrow { width: 14px; height: 14px; }

  /* ---------- 页脚（divider：240×16，© 数字分身 居中） ---------- */
  .av-main-foot {
    width: 240px; margin: 32px auto 0; height: 16px;
    display: flex; align-items: center; justify-content: center; gap: 16px;
    font-size: var(--font-size-body-1); color: var(--av-ink-4);
  }
  .av-main-foot::before,
  .av-main-foot::after { content: ""; flex: 1 1 auto; height: 1px; background: var(--color-border-2); }
</style>"""

# ══════════════════════════ JS ══════════════════════════
JS_TMPL = """<script id="av-main-js">
(function () {
  /* 把 <template> 里的还原标记填进 React 渲染出的空壳 .av-main。
     React 对 .av-main 没有子节点声明（bundle 已改为 <div class="av-main">），
     因此这里写入的 DOM 不会被 React 协调覆盖。 */
  var tpl = document.getElementById('av-main-tpl');
  if (!tpl) return;
  var HTML = tpl.innerHTML;
  function mount() {
    var host = document.querySelector('.av-main');
    if (!host) return false;
    if (host.getAttribute('data-av-main-ready') === '1') return true;
    host.innerHTML = HTML;
    host.setAttribute('data-av-main-ready', '1');
    return true;
  }
  if (!mount()) {
    /* React 首帧可能晚于本脚本 */
    var mo = new MutationObserver(function () { if (mount()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>"""

# ══════════════════════════ React bundle 补丁 ══════════════════════════
DT_NEW = ('function Dt(){return(0,j.jsx)(yt,{children:(0,j.jsx)(`div`,'
          '{className:`av-main`,id:`av-main`})})}')
DT_MARK = 'className:`av-main`,id:`av-main`'
DT_OLD_MARK = 'className:`mx-auto flex w-full max-w-3xl flex-col gap-5`'


def find_dt(src):
    """花括号配平定位 `function Dt(){…}` 整段（bundle 是外部产物，不硬编码）。"""
    i = src.find("function Dt(){")
    assert i > 0, "bundle 里找不到 function Dt(){"
    depth, k = 0, src.find("{", i)
    while k < len(src):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                break
        k += 1
    seg = src[i:k + 1]
    assert DT_OLD_MARK in seg, "Dt() 里没有预期的 max-w-3xl 容器：%s" % seg[:120]
    return i, k + 1, seg


def fill(tmpl, **kw):
    for k, v in kw.items():
        tmpl = tmpl.replace("@@%s@@" % k, v)
    return tmpl


css_block = fill(CSS_TMPL, VER=VERSION)
js_block = JS_TMPL

for nm, blk in (("CSS", css_block), ("JS", js_block), ("HTML", MAIN_HTML)):
    assert "@@" not in blk, "%s 段仍有未替换占位符：%s" % (nm, re.findall(r"@@[A-Z]+@@", blk))
assert css_block.count("/*") == css_block.count("*/"), "CSS 注释定界符不成对"

INJECT = ("  " + START + " " + VERSION + " -->\n"
          + css_block + "\n"
          + MAIN_HTML + "\n"
          + js_block + "\n"
          + "  " + END + "\n")
assert INJECT.count(START) == 1 and INJECT.count(END) == 1, "注入段标记数异常"
assert INJECT.rstrip().endswith(END), "注入段未以结束标记收尾"

# ══════════════════════════ 写入 ══════════════════════════
dst = io.open(DEST, encoding="utf-8").read()
acts = []

# (1) React bundle 补丁（幂等：已打过就跳过）
if DT_MARK in dst:
    acts.append("bundle  B: 已打补丁（跳过）")
else:
    i, j, seg = find_dt(dst)
    dst = dst[:i] + DT_NEW + dst[j:]
    acts.append("bundle  B: 替换 Dt() 渲染体 %d → %d chars" % (len(seg), len(DT_NEW)))
    assert DT_OLD_MARK not in dst, "bundle 里仍有旧的 max-w-3xl 容器未被替换"

# (2) 注入段（幂等：整块替换）
a = dst.find(START)
if a >= 0:
    b = dst.find(END, a)
    assert b > a, "有开启标记但找不到结束标记"
    b += len(END)
    while a > 0 and dst[a - 1] in " \t":
        a -= 1
    if dst[b:b + 1] == "\n":
        b += 1
    new = dst[:a] + INJECT + dst[b:]
    a2 = new.find(START)
    while a2 > 0 and new[a2 - 1] in " \t":
        a2 -= 1
    b2 = new.find(END, a2) + len(END)
    if new[b2:b2 + 1] == "\n":
        b2 += 1
    assert new[:a2] + INJECT + new[b2:] == new, "幂等自检失败：重复替换后内容发生变化"
    acts.append("inject  R: 整块替换  %+d chars（幂等自检通过）" % (len(new) - len(dst)))
else:
    idx = dst.rfind("</body>")
    assert idx > 0, "找不到 </body>"
    new = dst[:idx] + INJECT + dst[idx:]
    acts.append("inject  P: 追加注入  %+d chars" % (len(new) - len(dst)))

io.open(DEST, "w", encoding="utf-8", newline="").write(new)

print("目标      : pages/avatar.html")
for x in acts:
    print("动作      : %s" % x)
print("内容模板  : %d chars（头部 + 4 卡 + 3 行卡 + 页脚）" % len(MAIN_HTML))
print("适配层 CSS: %d chars" % len(css_block))
print("注入脚本  : %d chars" % len(js_block))
print("页面      : %d → %d chars" % (len(dst), len(new)))
