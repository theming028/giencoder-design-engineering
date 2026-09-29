#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""r84 —— 「会话历史」二级视图的四条修正。

接 r83（`mg-work/r83/apply83.py`）的落点，改动只有 4 处，全部针对 `pages/avatar.html`：

  1. `.av-hs-name` 字重 → 常规（400，原 500）。
  2. 右枚「删除会话」图标换成**设计稿真矢量**；两枚图标按钮都带 DS 观感的 tooltip。
     ★ 取证结论（本轮新发现）：设计稿结构里第 2 枚图标是一个**未被展开的 DS 组件实例**
       （`ui-component name="icon-wrapper" props={"尺寸":"14"}`），所以 mgfetch 只捞到 2 个图标
       asset（导出 + 返回），删除图标**没有**导出 SVG ⇒ 上一轮是"照 PNG 像素手搓"的，形状确实不对。
       逐像素比对（`mg-work/r83/raw/cmp_icon.png`）后确认：设计稿那枚 = 仓内 DS 的
       `assets/icons/delete.svg`（12 单位 viewBox 按 14px 渲染，×1.1667），三处关键坐标全中：
         盖 x434..445 / y91..92 、桶身竖边 x435..436 与 x443..444 、双肋 x438 / x441 、底 y100..101。
       ⇒ 直接搬仓内真矢量，不再手搓。
     同时把第 1 枚「导出」也换回真矢量 `raw/1389-18518__svg_5f4f2e22.svg`（上一轮同样是手搓近似版；
       真矢量的托盘宽 11.08、右壁中段断开让箭头穿过，与设计稿 PNG 的 x403..414 / y90..101 逐像素吻合）。
  3. **点击「删除会话」图标** → 该行图标组换成 [取消][确定删除]（邵先生 2026-09-29 定稿）。
     · 触发用纯 CSS `.av-hs-item.is-confirm`；按钮组进**布局流**（不再绝对定位）⇒
       确认态下文本自动收窄，与设计稿第 3 行"名字框变窄"一致；右侧间距按设计稿实测 8px
       （图标组是 10px，设计稿这两处本身差 2px，用 -2px 外边距对齐）。
     · 「取消」= 退出确认态（移除类即可）；点行内其他位置同样视为放弃。
  4. 首行不再默认吃 fill-2（白底）；整行铺满可点热区（`.av-hs-name::after` 铺 `inset:0`，
     图标组/按钮组用 z-index 压在热区之上，仍各自可点）。

★ 轮内修订（首版 → 定稿）：第 3 条首版实现的是「hover 整张卡片就替换」，落地后发现它与第 2 条
  **落在同一个 hover 上互斥** —— 鼠标一进卡片，两枚图标就 `display:none`，tooltip 永远弹不出来。
  邵先生随即定稿为「**点击**删除图标才替换」⇒ 两条需求各得其所（图标可 hover ⇒ tooltip 可用），
  代码里已不存在 `.is-cancel` 与 `:hover` 触发。块 id 保持 `r84-hs-*`（本轮未提交，就地修订，
  不另起一代 —— 免得"hover 方案的历史"留在仓库里误导后人）。

用法：
  python mg-work/r84/apply84.py            # 落地（幂等；复跑输出「摘 3 → 插 3」）
回滚：
  cp mg-work/r84/avatar.before.html pages/avatar.html
"""
import io
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PAGES = ['avatar.html']

VIEW_OPEN = '<!-- r84-hs-view -->'
VIEW_CLOSE = '<!-- /r84-hs-view -->'

# ⚠ 块内必须自带首尾空白：幂等自证要求「摘掉后字符数完全回到基线」。
#   返回按钮补 `data-av-tip="返回"`（图标按钮 tooltip）。
VIEW_HTML = (VIEW_OPEN + '\n'
             '      <div class="av-hs" id="av-hs">\n'
             '        <header class="av-hs-bar">\n'
             '          <button class="av-hs-back" type="button" aria-label="返回" data-av-tip="返回" data-av-hs-back="1">\n'
             '            <svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true"><path d="M3.8 6.72h9.2v1.56H3.8l3.4 3.62-1.03 1.1L1 7.5l5.17-5.5 1.03 1.1z" fill="currentColor"/></svg>\n'
             '          </button>\n'
             '          <span class="av-hs-rule" aria-hidden="true"></span>\n'
             '          <h2 class="av-hs-title">会话历史</h2>\n'
             '        </header>\n'
             '        <div class="av-hs-list" id="av-hs-list" role="list"></div>\n'
             '      </div>\n'
             '      ' + VIEW_CLOSE)


# ────────────────────────────────────────────────────────────────
# 2. CSS
#    几何数值来源：r83 的逐像素实测（设计稿 PNG 488×990，节点原点落在 PNG (3,2)）。
#    r84 新增数值来源：设计稿**结构树**（`raw/node_1389-18518.json`）+ 像素复核。
# ────────────────────────────────────────────────────────────────
HS_CSS = """
/* ★ 第 84 轮 · 「会话历史」二级视图的四条修正（承 r83 的 1389:18518 设计稿）
   r84 ① 名字常规字重 ② 删除/导出图标换真矢量 + tooltip ③ 点击删除图标 → 该行换成按钮组 ④ 首行白底 + 整卡热区 */
:root {
  --av-hs-line: #E7EBF1;               /* 表头底线，设计稿实测 rgb(231,235,241) */
  --av-hs-rule: rgb(var(--gray-4));    /* 表头竖分隔线，设计稿实测 #C9C9C9 = 灰阶 4 */
}
[giencoder-theme='dark'] {
  --av-hs-line: rgb(var(--gray-3));
}

/* ---------- 视图切换：只有 #av-chat-drawer[data-av-hs] 时才显示二级页 ---------- */
.av-hs { display: none; }
#av-chat-drawer[data-av-hs] > .td-right-inner > .av-hs {
  display: flex; flex-direction: column; flex: 1; min-height: 0;
}
#av-chat-drawer[data-av-hs] > .td-right-inner > :not(.av-hs) { display: none; }

/* ---------- 表头 ---------- */
.av-hs-bar {
  flex: none; height: 48px; box-sizing: border-box;
  display: flex; align-items: center; padding: 0 20px;
  border-bottom: 1px solid var(--av-hs-line);
}
.av-hs-back {
  flex: none; width: 24px; height: 24px; box-sizing: border-box;
  display: flex; align-items: center; justify-content: center;
  margin: 0; padding: 0; border: 0; border-radius: 4px; background: transparent;
  color: var(--color-text-1); cursor: pointer;
  transition: background-color 120ms linear;
}
.av-hs-back:hover { background: var(--color-fill-2); }
.av-hs-back svg { width: 14px; height: 14px; }
.av-hs-rule {
  flex: none; width: 1px; height: 16px;
  margin: 0 12px 0 8px;
  background: var(--av-hs-rule);
}
.av-hs-title {
  margin: 0; padding: 0; min-width: 0;
  font-size: var(--font-size-title-1); font-weight: 600; line-height: 24px;
  color: var(--color-text-1);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

/* ---------- 列表 ---------- */
.av-hs-list {
  flex: 1; min-height: 0; overflow-y: auto; overflow-x: hidden;
  padding: 20px;
  display: flex; flex-direction: column; gap: 2px;
}
/* 滚动条与设计稿一致：6px 宽、rgba(0,0,0,.16)（实测 #D6D6D6）、圆角 3 */
.av-hs-list::-webkit-scrollbar { width: 6px; }
.av-hs-list::-webkit-scrollbar-track { background: transparent; }
.av-hs-list::-webkit-scrollbar-thumb { background: rgba(0, 0, 0, .16); border-radius: 3px; }

/* ---------- 会话行 ---------- */
.av-hs-item {
  position: relative;                 /* ① 给整卡热区（::after）当定位基准 */
  flex: none; height: 56px; box-sizing: border-box;
  display: flex; align-items: center; gap: 8px;
  padding: 0 10px; border-radius: 4px; background: transparent;
  cursor: pointer;
  transition: background-color 120ms linear;
}
/* r84 ④：默认白底 —— 去掉 `.is-on`（当前会话）的 fill-2，
   ⚠ 设计稿第 1 行是 #F2F2F2，邵先生 2026-09-29 明确「默认不要浅灰底、白底即可」⇒ 以用户为准。 */
.av-hs-item:hover { background: var(--color-fill-2); }

.av-hs-txt { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.av-hs-name {
  display: block; width: 100%; margin: 0; padding: 0; border: 0; background: none;
  font-family: inherit; text-align: left; cursor: pointer;
  /* r84 ①：字重常规（原 500） */
  font-size: var(--font-size-body-3); font-weight: 400; line-height: 22px;
  color: var(--color-text-1);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
/* r84 ④：整行可点热区 —— 铺满本行的透明覆盖层，点击即落到名字按钮上（= pick） */
.av-hs-name::after { content: ''; position: absolute; inset: 0; border-radius: 4px; }
.av-hs-time {
  display: block; min-height: 16px;
  font-size: var(--font-size-body-1); line-height: 16px; color: var(--color-text-3);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

.av-hs-acts {
  flex: none; display: flex; align-items: center; gap: 8px;
  position: relative; z-index: 1;       /* r84 ④：压在整卡热区之上，图标仍可单独点 */
}
.av-hs-ibtn {
  flex: none; width: 24px; height: 24px; box-sizing: border-box; padding: 5px;
  display: flex; align-items: center; justify-content: center;
  margin: 0; border: 0; border-radius: 4px; background: transparent;
  color: var(--color-text-3); cursor: pointer;
  transition: background-color 120ms linear, color 120ms linear;
}
.av-hs-ibtn:hover { background: var(--color-fill-3); color: var(--color-text-1); }
.av-hs-ibtn svg { width: 14px; height: 14px; }

/* ---------- ③ 点击「删除会话」图标 → 该行进入确认态：图标组让位给 [取消][确定删除] ----------
   ★ 2026-09-29 邵先生定稿的交互：**点击删除图标才替换**。
     原本 r84 首版是「hover 整张卡片就替换」，但它与 ② 的图标 tooltip 落在同一个 hover 上互斥
     （鼠标一进卡片图标就被 display:none，tooltip 永远显示不出来）；改成点击触发后两者各得其所。 */
.av-hs-confirm {
  flex: none; display: none; align-items: center; gap: 8px;
  position: relative; z-index: 1;
  /* 设计稿实测：按钮组右缘距行右缘 8（图标组是 10，设计稿这两处本身差 2） */
  margin-right: -2px;
}
.av-hs-item.is-confirm .av-hs-acts { display: none; }
.av-hs-item.is-confirm .av-hs-confirm { display: flex; }
/* 确认态自持底色（设计稿确认态那行实测也是 #F2F2F2）：鼠标移出行外也不掉 */
.av-hs-item.is-confirm { background: var(--color-fill-2); }

/* 适配层：DS Button(size-mini) 收敛到设计稿的 28 高 / 左右内边距 11
   （实测 取消 48 宽、确定删除 72 宽 = 12px 字宽 + 11 × 2 内边距 + 2 × 1 描边） */
.giencoder-btn.giencoder-btn-size-mini.av-hs-btn {
  height: 28px; padding: 0 11px; border-radius: 4px;
}

/* ---------- 图标按钮 tooltip（照 DS `giencoder-tooltip-popup` 的观感，全部取 token） ---------- */
.av-tip {
  position: fixed; z-index: 9999; pointer-events: none; white-space: nowrap;
  background: var(--color-tooltip-bg); color: var(--color-white);
  font-size: var(--font-size-body-1); line-height: 16px; padding: 4px 8px;
  border-radius: calc(var(--radius) - 2px); box-shadow: var(--shadow1-down);
}
.av-tip::after {
  content: ''; position: absolute; left: 50%; transform: translateX(-50%);
  width: 0; height: 0; border: 5px solid transparent;
}
.av-tip.is-top::after { top: 100%; border-bottom: 0; border-top-color: var(--color-tooltip-bg); }
.av-tip.is-bottom::after { bottom: 100%; border-top: 0; border-bottom-color: var(--color-tooltip-bg); }
"""


# ────────────────────────────────────────────────────────────────
# 3. JS
# ────────────────────────────────────────────────────────────────
HS_JS = """
/* SHELL-AV-HS v3 —— AI 会话栏内的「会话历史」二级视图
   ⚠ 勿手改此块；落地脚本 mg-work/r84/apply84.py；设计稿 MasterGo 1389:18518。
   v2 = r84 四条：名字常规字重 / 图标真矢量 + tooltip / hover 整卡换成按钮组 / 首行白底 + 整卡热区
   v3 = ★ 交互定稿（邵先生 2026-09-29）：确认态改由**点击「删除会话」图标**触发
        （v2 的"hover 整卡替换"会吃掉图标的 hover ⇒ tooltip 显示不出来）；
        v2 那套"悬停内退出确认态"的类与监听一并撤销，不需要了。 */
(function () {
  var drawer = document.getElementById('av-chat-drawer');
  var view = document.getElementById('av-hs');
  var list = document.getElementById('av-hs-list');
  if (!drawer || !view || !list) return;
  if (drawer.__avHs) return;
  drawer.__avHs = 1;

  var ATTR = 'data-av-hs';

  /* ---------- 图标：全部搬设计稿/DS 的真矢量，只把 fill 改成 currentColor ----------
     · 导出 = raw/1389-18518__svg_5f4f2e22.svg（asset 原样；mastergo 导出时带
       matrix(0,1,1,0,.2417,-.2417) 转置 ⇒ 转置后即「托盘 ⊓ + 下箭头」；
       去掉原 clipPath（rect 0 0 14 14，路径本就在框内，留着反而产生重复 id）。
     · 删除 = assets/icons/delete.svg（DS 组件；12 单位 viewBox 按 14px 渲染 = ×1.1667）。 */
  var ICON_EXPORT = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true">' +
    '<path d="M1.45849609375,1.2168426513671875C1.45849609375,1.2168426513671875,9.04182909375,1.2168426513671875,9.04182909375,1.2168426513671875C9.04182909375,1.2168426513671875,9.04182909375,2.3835092513671876,9.04182909375,2.3835092513671876C9.04182909375,2.3835092513671876,2.62516269375,2.3835092513671876,2.62516269375,2.3835092513671876C2.62516269375,2.3835092513671876,2.62516269375,11.133508651367187,2.62516269375,11.133508651367187C2.62516269375,11.133508651367187,9.04182909375,11.133508651367187,9.04182909375,11.133508651367187C9.04182909375,11.133508651367187,9.04182909375,12.300175651367187,9.04182909375,12.300175651367187C9.04182909375,12.300175651367187,1.45849609375,12.300175651367187,1.45849609375,12.300175651367187C1.45849609375,12.300175651367187,1.45849609375,1.2168426513671875,1.45849609375,1.2168426513671875C1.45849609375,1.2168426513671875,1.45849609375,1.2168426513671875,1.45849609375,1.2168426513671875ZM9.72511669375,3.7006118513671873C9.72511669375,3.7006118513671873,12.78332909375,6.7588300513671875,12.78332909375,6.7588300513671875C12.78332909375,6.7588300513671875,9.72511669375,9.817012751367187,9.72511669375,9.817012751367187C9.72511669375,9.817012751367187,8.90016649375,8.992063051367188,8.90016649375,8.992063051367188C8.90016649375,8.992063051367188,10.55038739375,7.3418426513671875,10.55038739375,7.3418426513671875C10.55038739375,7.3418426513671875,4.91690419375,7.3418426513671875,4.91690419375,7.3418426513671875C4.91690419375,7.3418426513671875,4.91690419375,6.175175651367187,4.91690419375,6.175175651367187C4.91690419375,6.175175651367187,10.54977509375,6.175175651367187,10.54977509375,6.175175651367187C10.54977509375,6.175175651367187,8.90016649375,4.525567551367187,8.90016649375,4.525567551367187C8.90016649375,4.525567551367187,9.72511669375,3.7006118513671873,9.72511669375,3.7006118513671873C9.72511669375,3.7006118513671873,9.72511669375,3.7006118513671873,9.72511669375,3.7006118513671873Z" fill-rule="evenodd" fill="currentColor" transform="matrix(0,1,1,0,0.2416534423828125,-0.2416534423828125)"/></svg>';
  var ICON_TRASH = '<svg viewBox="0 0 12 12" width="14" height="14" fill="none" aria-hidden="true">' +
    '<path fill-rule="evenodd" clip-rule="evenodd" d="M7.463 1.125c.269 0 .487.218.487.488V2.1h2.612c.11 0 .149.011.188.033.04.02.071.052.092.092.022.04.033.079.033.187v.35c0 .11-.011.149-.033.188a.221.221 0 01-.092.092c-.04.022-.079.033-.188.033H9.9v7.313c0 .269-.218.487-.488.487H2.587a.488.488 0 01-.487-.488V3.075h-.663c-.108 0-.148-.011-.187-.033a.221.221 0 01-.092-.092c-.022-.04-.033-.079-.033-.187v-.35c0-.11.011-.149.033-.188a.221.221 0 01.092-.092c.04-.022.079-.033.187-.033H4.05v-.488c0-.269.218-.487.487-.487h2.926zm1.462 1.95h-5.85V9.9h5.85V3.075zM5.269 4.537c.134 0 .244.11.244.244v3.413c0 .134-.11.243-.244.243H4.78a.244.244 0 01-.244-.243V4.78c0-.134.11-.244.244-.244h.488zm1.95 0c.134 0 .244.11.244.244v3.413c0 .134-.11.243-.244.243H6.73a.244.244 0 01-.244-.243V4.78c0-.134.11-.244.244-.244h.488z" fill="currentColor"/></svg>';

  /* 会话数据：[标题, 时间, 是否当前会话]。文案与排序照抄设计稿。
     ⚠ 占位数据 —— 真实数据接入后只改这个数组。
     ⚠ 第 3 位只用于 aria-current 语义，**不再着色**（r84 ④：首行默认白底）。 */
  var ROWS = [
    ['银行金融科技IT开发服务AI智能体平台与IDE插件...', '', 1],
    ['SimplAI AI应用部署平台介绍', '半小时前', 0],
    ['可视化工作流编排可视化工作流编排...', '昨天 11:12', 0],
    ['成都到深圳海边性价比方案', '07/12 09:32', 0],
    ['自动任务手动触发对话创建', '07/12 09:32', 0],
    ['Git Worktree多分支并行开发', '07/12 09:32', 0],
    ['Codex自定义大模型方法', '07/12 09:32', 0]
  ];

  function rowHTML(r) {
    return '<div class="av-hs-item' + (r[2] ? ' is-on' : '') + '" role="listitem"' +
        (r[2] ? ' aria-current="true"' : '') + '>' +
      '<span class="av-hs-txt">' +
        '<button class="av-hs-name" type="button" data-av-hs-pick="1">' + r[0] + '</button>' +
        '<span class="av-hs-time">' + r[1] + '</span>' +
      '</span>' +
      '<span class="av-hs-acts">' +
        '<button class="av-hs-ibtn" type="button" aria-label="导出会话" data-av-tip="导出会话" data-av-hs-export="1">' + ICON_EXPORT + '</button>' +
        '<button class="av-hs-ibtn" type="button" aria-label="删除会话" data-av-tip="删除会话" data-av-hs-del="1">' + ICON_TRASH + '</button>' +
      '</span>' +
      '<span class="av-hs-confirm">' +
        '<button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini av-hs-btn" type="button" data-av-hs-cancel="1">取消</button>' +
        '<button class="giencoder-btn giencoder-btn-danger giencoder-btn-size-mini av-hs-btn" type="button" data-av-hs-ok="1">确定删除</button>' +
      '</span>' +
    '</div>';
  }

  if (!list.childElementCount) {
    var buf = '';
    for (var i = 0; i < ROWS.length; i++) buf += rowHTML(ROWS[i]);
    list.innerHTML = buf;
  }

  /* ---------- 轻提示：复用页面自身的 .td-dp-msg（同构造），没有就按同构造建一个 ---------- */
  var MSG_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true">' +
    '<circle cx="7" cy="7" r="6.2" fill="currentColor"/>' +
    '<path d="M4.3 7.2l1.9 1.9 3.5-3.7" stroke="var(--color-white)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function toast(text) {
    var box = document.querySelector('.td-dp-msg');
    if (!box) {
      box = document.createElement('div');
      box.className = 'td-dp-msg';
      box.innerHTML = '<div class="giencoder-message" role="status">' +
        '<span class="giencoder-message-icon" aria-hidden="true">' + MSG_SVG + '</span>' +
        '<span class="giencoder-message-content"></span></div>';
      box.hidden = true;
      document.body.appendChild(box);
    }
    var c = box.querySelector('.giencoder-message-content');
    if (!c) return;
    c.textContent = text;
    box.hidden = false;
    clearTimeout(box._t);
    box._t = setTimeout(function () { box.hidden = true; }, 2400);
  }

  /* ---------- r84 ② 图标按钮 tooltip（观感照 DS `giencoder-tooltip-popup`） ---------- */
  var tip = null;
  function ensureTip() {
    if (tip) return tip;
    tip = document.createElement('div');
    tip.className = 'av-tip';
    tip.setAttribute('role', 'tooltip');
    tip.hidden = true;
    document.body.appendChild(tip);
    return tip;
  }
  function hideTip() { if (tip) tip.hidden = true; }
  function showTip(btn) {
    var text = btn.getAttribute('data-av-tip');
    if (!text) return;
    var t = ensureTip();
    t.textContent = text;
    t.hidden = false;
    var r = btn.getBoundingClientRect(), tr = t.getBoundingClientRect();
    var above = r.top - tr.height - 4;
    var bottom = above >= 8;
    t.classList.remove('is-top', 'is-bottom');
    t.classList.add(bottom ? 'is-top' : 'is-bottom');
    t.style.top = Math.round(bottom ? above : r.bottom + 4) + 'px';
    var left = r.left + r.width / 2 - tr.width / 2;
    var max = (window.innerWidth || 0) - tr.width - 8;
    t.style.left = Math.round(Math.max(8, Math.min(left, max))) + 'px';
  }
  function tipTarget(ev) {
    var t = ev.target;
    return (t && t.closest) ? t.closest('[data-av-tip]') : null;
  }
  view.addEventListener('mouseover', function (ev) { var b = tipTarget(ev); if (b) showTip(b); });
  view.addEventListener('mouseout', function (ev) { var b = tipTarget(ev); if (b) hideTip(); });
  /* ⚠ 只走 hover：曾用 focusin 也弹一次，结果 openView() 里给返回按钮 `.focus()`
     会在每次打开视图时凭空弹出一个「返回」tooltip（实测踩到）⇒ 键盘用户的名称由 aria-label 承载。 */
  list.addEventListener('scroll', hideTip);

  /* ---------- 视图开合 ---------- */
  function isOpen() { return drawer.hasAttribute(ATTR); }
  function syncAria(open) { view.setAttribute('aria-hidden', open ? 'false' : 'true'); }

  function openView() {
    if (isOpen()) return;
    drawer.setAttribute(ATTR, '');
    syncAria(true);
    var back = view.querySelector('[data-av-hs-back]');
    if (back) back.focus();
  }
  function closeView() {
    if (!isOpen()) return;
    /* 关视图时复位确认态：下次进来不该还停在「确定删除」上 */
    var cs = list.querySelectorAll('.av-hs-item.is-confirm');
    for (var i = 0; i < cs.length; i++) cs[i].classList.remove('is-confirm');
    hideTip();
    drawer.removeAttribute(ATTR);
    syncAria(false);
    var entry = chatEntry();
    if (entry && entry.isConnected) entry.focus();
  }
  function chatEntry() {
    return drawer.querySelector('.td-right-acts [aria-label="会话历史"]');
  }

  /* ---------- 点击委托（⚠ 挂在整个视图上：返回按钮在 .av-hs-bar 里，不在列表内） ---------- */
  function brief(el) {
    var t = el ? el.textContent : '';
    return t.length > 14 ? t.slice(0, 14) + '…' : t;
  }
  view.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!t || !t.closest) return;
    hideTip();

    if (t.closest('[data-av-hs-back]')) { closeView(); return; }   /* 返回 → 回到对话视图 */

    var row = t.closest('.av-hs-item');
    if (!row) return;

    if (t.closest('[data-av-hs-cancel]')) {                        /* 取消 → 退出确认态，图标组回来 */
      row.classList.remove('is-confirm');
      return;
    }
    if (t.closest('[data-av-hs-ok]')) {                            /* 确定删除 → 真的移除该行 */
      var nm = row.querySelector('.av-hs-name');
      var txt = nm ? brief(nm) : '';
      row.parentNode.removeChild(row);
      toast('已删除「' + txt + '」');
      return;
    }
    if (t.closest('[data-av-hs-export]')) {                        /* 导出（本轮只做回执） */
      toast('已导出「' + brief(row.querySelector('.av-hs-name')) + '」');
      return;
    }
    if (t.closest('[data-av-hs-del]')) {                           /* ★ 删除图标 → 该行进确认态（一次只允许一行） */
      var cur = list.querySelector('.av-hs-item.is-confirm');
      if (cur && cur !== row) cur.classList.remove('is-confirm');
      row.classList.add('is-confirm');
      /* 键盘触发（click.detail === 0）时把焦点交给「取消」：刚被 display:none 的删除按钮
         会把焦点丢回 body，下一个 Tab 会从页面开头重来。鼠标触发则不动焦点，免得飘出光圈。 */
      if (!ev.detail) {
        var cb = row.querySelector('[data-av-hs-cancel]');
        if (cb) cb.focus();
      }
      return;
    }
    /* 确认态是个"子状态"：点行内其他位置一律视为放弃 ——
       否则会直接跳去"打开该会话 + 关视图"，对用户太意外（旧的 hover 触发没这个问题，因为鼠标一移开就复位）。 */
    if (row.classList.contains('is-confirm')) {
      row.classList.remove('is-confirm');
      return;
    }
    /* 其余：整张卡片任意位置 → 打开该会话（r84 ④ 整卡热区） */
    var on = list.querySelector('.av-hs-item.is-on');
    if (on && on !== row) on.classList.remove('is-on');
    row.classList.add('is-on');
    row.setAttribute('aria-current', 'true');
    if (on && on !== row) on.removeAttribute('aria-current');
    closeView();
  });

  /* Esc 返回上一层（优先级低于页面自己的弹层/全屏裁决：它们消费掉后不会走到这里） */
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape' && ev.key !== 'Esc') return;
    if (!isOpen()) return;
    if (document.querySelector('.td-dp-msg') && !document.querySelector('.td-dp-msg').hidden) return;
    closeView();
  }, true);

  /* 「会话历史」入口 */
  var entry = chatEntry();
  if (entry) entry.addEventListener('click', function () { openView(); });

  /* 整个 AI 会话栏关掉时，二级页要复位（下次打开回到对话视图） */
  if (window.MutationObserver) {
    new MutationObserver(function () {
      if (!document.documentElement.hasAttribute('data-av-chat-open')) closeView();
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-av-chat-open'] });
  }

  /* 入口按钮若晚于本脚本出现（外壳克隆），用观察器兜住，只绑一次 */
  if (!entry) {
    var boot = new MutationObserver(function () {
      var b = chatEntry();
      if (!b) return;
      b.addEventListener('click', function () { openView(); });
      boot.disconnect();
    });
    boot.observe(document.body, { childList: true, subtree: true });
  }

  syncAria(false);
})();
"""


# ────────────────────────────────────────────────────────────────
# 4. 装配与注入
# ────────────────────────────────────────────────────────────────
def style_block(bid, css):
    return '<style id="%s">\n%s\n</style>' % (bid, css)


def script_block(bid, js):
    return '<script id="%s">\n%s\n</script>' % (bid, js)


HS_STYLE = style_block('r84-hs-css', HS_CSS)
HS_SCRIPT = script_block('r84-hs-js', HS_JS)

# ⚠ 两条块规则必须把**尾随换行**一起吃掉 —— 注入时写的是 `块 + \n` 接下一件，
#   不带上它，幂等自证会残留字符。
# ⚠★ 同时摘 r83 与 r84 两代标记：这样 r83 与 r84 谁复跑都是「先摘后插」，
#    永远不会出现两代块并存（否则重复定义视图 id）。
PRIOR = (
    (re.compile(r'<style id="r83-hs-css">.*?</style>\n', re.S), 1),
    (re.compile(r'<script id="r83-hs-js">.*?</script>\n', re.S), 1),
    (re.compile(r'<!-- r83-hs-view -->.*?<!-- /r83-hs-view -->', re.S), 1),
    (re.compile(r'<style id="r84-hs-css">.*?</style>\n', re.S), 1),
    (re.compile(r'<script id="r84-hs-js">.*?</script>\n', re.S), 1),
    (re.compile(re.escape(VIEW_OPEN) + r'.*?' + re.escape(VIEW_CLOSE), re.S), 1),
)

ANCHOR_INNER = '<div class="td-right-inner">'
TOKENS = ['av-hs-bar', 'av-hs-back', 'av-hs-rule', 'av-hs-title',
          'av-hs-list', 'av-hs-item', 'av-hs-name', 'av-hs-time',
          'av-hs-acts', 'av-hs-ibtn', 'av-hs-confirm', 'av-hs-btn', 'av-tip']

# 本轮「被改对象」的精确断言：改前页面里必须一个都没有
NEW_TOKENS = ['r84-hs-css', 'r84-hs-js', VIEW_OPEN, 'data-av-tip', 'av-tip']


def meta_guard():
    """护身符：新块里不得出现会破坏 HTML 结构的标签字面量。"""
    common = (('</body>', 0), ('</html>', 0), ('</head>', 0), ('<body', 0), ('<html', 0), ('<head', 0))
    rules = {
        'css': common + (('</style>', 1), ('<style', 1), ('</script>', 0), ('<script', 0)),
        'js': common + (('</script>', 1), ('<script', 1), ('</style>', 0), ('<style', 0)),
    }
    for part, name, key in ((HS_STYLE, 'hs/css', 'css'), (HS_SCRIPT, 'hs/js', 'js')):
        for bad, allowed in rules[key]:
            n = part.count(bad)
            if n != allowed:
                sys.exit('!! 元守卫失败：%s 里 %r 出现 %d 次（应为 %d）' % (name, bad, n, allowed))
    if '<div' in HS_STYLE or '</div>' in HS_STYLE:
        sys.exit('!! 元守卫失败：hs/css 里出现 div 标签字面量')
    for part, name in ((HS_STYLE, 'hs/css'), (HS_SCRIPT, 'hs/js')):
        if VIEW_OPEN in part or VIEW_CLOSE in part:
            sys.exit('!! 元守卫失败：%s 里出现视图注释标记' % name)
    if VIEW_OPEN in VIEW_HTML.replace(VIEW_OPEN, '', 1) or VIEW_CLOSE in VIEW_HTML.replace(VIEW_CLOSE, '', 1):
        sys.exit('!! 元守卫失败：视图块内的注释标记重复')


def strip_all(s):
    """按 PRIOR 摘掉两代块，返回 (剩余文本, 摘掉件数)。"""
    n = 0
    for pat, want in PRIOR:
        s, k = re.subn(pat, '', s, count=want)
        n += k
    return s, n


def apply_page(fname):
    page = os.path.join(ROOT, 'pages', fname)
    with open(page, encoding='utf-8') as f:
        s0 = f.read()

    # —— 先摘旧块（r83 或 r84 两代），得到「本轮基线」 ——
    s, dropped = strip_all(s0)
    if dropped not in (0, 1, 2, 3):
        sys.exit('!! %s 旧块删除数量异常：%d' % (fname, dropped))
    for tok in ('id="r83-hs-css"', 'id="r83-hs-js"', 'id="r84-hs-css"', 'id="r84-hs-js"',
                '<!-- r83-hs-view -->', VIEW_OPEN):
        if tok in s:
            sys.exit('!! %s 摘除旧块后仍残留 %s' % (fname, tok))
    base_txt = s                       # 本轮基线（摘掉旧块后的文本）
    n_base = len(base_txt)

    # —— 锚点防呆 ——
    if s.count(ANCHOR_INNER) != 1:
        sys.exit('!! %s 的 %s 不是恰好 1 个（%d）' % (fname, ANCHOR_INNER, s.count(ANCHOR_INNER)))
    if '<div class="td-chat">' not in s:
        sys.exit('!! %s 里找不到 .td-chat（落点可能已变）' % fname)
    if s.count('</body>') != 1:
        sys.exit('!! %s 的 </body> 不是恰好 1 个（%d）' % (fname, s.count('</body>')))
    # 本轮新增标记在基线上必须为 0（否则断言口径不成立）
    for tok in NEW_TOKENS:
        if tok in base_txt:
            sys.exit('!! %s 基线上已存在本轮标记 %r' % (fname, tok))

    # —— 基线计数 ——
    base = {
        'style': s.count('<style'), 'estyle': s.count('</style>'),
        'script': s.count('<script'), 'escript': s.count('</script>'),
        'body': s.count('</body>'),
        'inner': s.count(ANCHOR_INNER),
    }

    # —— 插视图 ——
    s = s.replace(ANCHOR_INNER, ANCHOR_INNER + VIEW_HTML, 1)

    # —— 插 CSS + JS ——
    s = s.replace('</body>', HS_STYLE + '\n' + HS_SCRIPT + '\n</body>', 1)

    # —— 断言：标签级精确增减 ——
    checks = (('<style', base['style'] + 1), ('</style>', base['estyle'] + 1),
              ('<script', base['script'] + 1), ('</script>', base['escript'] + 1),
              ('</body>', base['body']))
    for tok, want in checks:
        got = s.count(tok)
        if got != want:
            sys.exit('!! %s 标签计数 %r = %d（应为 %d）' % (fname, tok, got, want))
    if s.count(ANCHOR_INNER) != base['inner']:
        sys.exit('!! %s 锚点计数变了' % fname)

    # —— 断言：被改对象的精确计数 ——
    # 判据：`av-hs-*` / `av-tip` 是本轮新造的前缀，基线里一个都没有
    #       ⇒ 全页计数 必须 == 三个块里的出现次数之和。
    blob = HS_CSS + HS_JS + VIEW_HTML
    for tok in TOKENS:
        want = blob.count(tok)
        if want == 0:
            sys.exit('!! 块内不存在 token %r' % tok)
        got = s.count(tok)
        if got != want:
            sys.exit('!! %s token %r 计数 %d（块内 %d）' % (fname, tok, got, want))
    if s.count('id="av-hs-list"') != 1 or s.count('id="av-hs"') != 1:
        sys.exit('!! %s 视图 id 计数异常' % fname)
    # 已废弃的机制必须真的清干净：`is-cancel`（v2 的"悬停内退出"）、
    # `.is-on` 的着色选择器（r84 ④ 摘掉）、`data-av-hs-confirm`（r83 的点击进入）
    # ⚠ `is-confirm` 本身现在是**在用的**（v3 点击触发），不能再当作"旧机制"来断言它的缺席。
    for gone in ('is-cancel', 'av-hs-item.is-on,', 'data-av-hs-confirm'):
        if gone in blob:
            sys.exit('!! 新块里仍残留旧机制 %r' % gone)

    # —— 幂等自证：把刚插的三块按同样规则摘掉，必须**逐字节等于本轮基线** ——
    t, dropped2 = strip_all(s)
    if dropped2 != 3:
        sys.exit('!! %s 幂等自证失败：只摘掉 %d 件（应为 3）' % (fname, dropped2))
    if t != base_txt:
        sys.exit('!! %s 幂等自证失败：摘回后 %d 字符 ≠ 基线 %d 字符' % (fname, len(t), n_base))

    with open(page, 'w', encoding='utf-8') as f:
        f.write(s)

    return n_base, len(s), dropped


def main():
    meta_guard()
    print('')
    for fname in PAGES:
        a, b, dropped = apply_page(fname)
        print('%-18s %d → %d (%+d)  视图=av-hs  （摘掉上一代块 %d 件）' % (fname, a, b, b - a, dropped))
    print('')


if __name__ == '__main__':
    main()
