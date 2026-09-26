# -*- coding: utf-8 -*-
"""第22轮补丁：作用在 mg-work/r21/build-detail.py 上，然后重新构建 pages/task-detail.html。

需求（用户 12 项）：
 1 详情页归属研发工作台 -> 无左侧菜单栏 aside
 2 td-gutter 固定，两栏间距固定 8px
 3 td-main : td-side = 8 : 2，td-side 最小宽度 280px
 4 td-side 左侧补纵向线条
 5 header.td-bar 补底部线条
 6 h1.td-title 容器补浅灰底色 + 底部线条
 7 底部输入框完全复用基础工作台（pages/base.html）的对话框模块
 8 「展开全文」支持展开/收起
 9 左栏 / 右栏补容器边框
10 td-right-bar 三个图标加大两号，图标还原（新会话 / 会话历史 / 全屏）
"""
import io
import re

SRC = "mg-work/r21/build-detail.py"
RAW = "mg-work/r22/composer.raw.html"

s = io.open(SRC, encoding="utf-8").read()
raw = io.open(RAW, encoding="utf-8").read()


def svg_of(label):
    m = re.search(r'<button[^>]*aria-label="' + re.escape(label) + r'"[^>]*>(.*?)</button>',
                  raw, re.S)
    if not m:
        raise SystemExit("icon not found: " + label)
    sv = re.search(r"<svg.*?</svg>", m.group(1), re.S).group(0)
    return re.sub(r"\s+", " ", sv).strip()


ICO_PLUS = svg_of("添加")
ICO_WRENCH = svg_of("技能")
ICO_AVATAR = svg_of("数字分身")
ICO_WAND = svg_of("优化提示词")
ICO_SEND = svg_of("发送")
ICO_CHEV = ('<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
            'stroke-width="1.4" stroke-linecap="round"><path d="M2.6 4.6L6 8l3.4-3.4"/></svg>')

# lucide 图标（detail 页右栏头部：新会话 / 会话历史 / 全屏）
LUCIDE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
          'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
          'stroke-linejoin="round" class="lucide lucide-%s" aria-hidden="true">%s</svg>')
ICO_NEW = LUCIDE % ("plus", '<path d="M5 12h14"/><path d="M12 5v14"/>')
ICO_HIST = LUCIDE % ("history",
                     '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
                     '<path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>')
ICO_FULL = LUCIDE % ("maximize",
                     '<path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/>'
                     '<path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/>')

BTN_ROUND = ('class="flex size-8 items-center justify-center rounded-full border '
             'border-[var(--color-border-1)] text-[var(--color-text-2)] transition-colors '
             'hover:bg-[var(--color-fill-1)] hover:[color:var(--color-text-1)]"')

# ---------------------------------------------------------------- 复用的对话框模块
COMPOSER = """        <!-- 复用基础工作台的对话框模块（pages/base.html，结构与类名一致） -->
        <div class="td-composer">
          <div class="relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors" style="border-color: var(--color-border-2); box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);">
            <textarea rows="1" placeholder="描述你的任务，/ 调用技能，@引用文件" aria-label="输入消息" class="min-w-0 resize-none bg-transparent text-sm leading-[22px] [color:var(--color-text-1)] outline-none placeholder:[color:var(--color-text-3)] min-h-[96px]"></textarea>
            <div class="mt-auto flex items-center justify-between">
              <div class="flex items-center gap-[8px]">
                <div class="giencoder-select" style="flex-direction: row; align-items: flex-start; position: relative;">
                  <button type="button" aria-label="添加" aria-haspopup="menu" aria-expanded="false" %(btn)s>%(plus)s</button>
                  <div role="menu" aria-label="添加内容"></div>
                </div>
                <button type="button" aria-label="技能" aria-haspopup="listbox" aria-expanded="false" %(btn)s>%(wrench)s</button>
                <div class="avatar-wrap relative flex items-center">
                  <button type="button" aria-label="数字分身" aria-pressed="true" class="flex h-8 items-center gap-[2px] rounded-full px-3 py-[5px] text-[14px] leading-[19px] transition-colors" style="background: rgb(236, 242, 255); color: rgb(55, 112, 247); border: 1px solid rgb(211, 226, 255);">%(avatar)s艾迪</button>
                  <div role="tooltip" class="avatar-tooltip">停用数字分身</div>
                </div>
                <div class="giencoder-select" style="width: 96px; flex-shrink: 0;">
                  <div class="giencoder-select-view select-view-ghost" tabindex="0" role="combobox" aria-haspopup="listbox" aria-expanded="false" style="height: 32px; min-height: 32px; border: 1px solid var(--color-border-1); border-radius: 32px; background-color: transparent; box-shadow: none; padding: 5px 12px; gap: 4px;">
                    <div class="giencoder-select-selection" style="gap: 4px;"><span class="giencoder-select-view-text">标准模式</span></div>
                    <span class="giencoder-select-suffix">%(chev)s</span>
                  </div>
                  <div class="giencoder-select-popup" style="display: none;">
                    <ul class="giencoder-select-option-list" role="listbox">
                      <li class="giencoder-select-option giencoder-select-option-selected" role="option" aria-selected="true">标准模式</li>
                      <li class="giencoder-select-option" role="option" aria-selected="false">专家模式</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <div class="giencoder-select" style="width: fit-content; max-width: 200px; flex-shrink: 0; margin-left: auto;">
                  <div class="giencoder-select-view select-view-ghost" tabindex="0" role="combobox" aria-haspopup="listbox" aria-expanded="false" style="height: 32px; min-height: 32px; border: none; border-radius: 32px; gap: 2px; padding: 0 12px;">
                    <div class="giencoder-select-selection" style="gap: 2px;"><span class="giencoder-select-view-text">DeepSeek-V4-Pro</span></div>
                    <span class="giencoder-select-suffix">%(chev)s</span>
                  </div>
                  <div class="giencoder-select-popup" style="display: none;">
                    <ul class="giencoder-select-option-list" role="listbox" aria-label="大模型选择">
                      <li class="giencoder-select-option giencoder-select-option-selected" role="option" aria-selected="true">DeepSeek-V4-Pro</li>
                      <li class="giencoder-select-option" role="option" aria-selected="false">GLM-5.2-公司共用</li>
                    </ul>
                  </div>
                </div>
                <button type="button" aria-label="优化提示词" class="flex size-8 items-center justify-center rounded-full transition-colors hover:bg-[var(--color-fill-1)]" style="background: rgb(255, 255, 255);">%(wand)s</button>
                <button type="button" aria-label="发送" disabled class="flex shrink-0 !size-8 !rounded-full !p-0 items-center justify-center transition-colors" style="background: var(--color-fill-3); cursor: not-allowed; opacity: 0.5;">%(send)s</button>
              </div>
            </div>
          </div>
        </div>""" % {"btn": BTN_ROUND, "plus": ICO_PLUS, "wrench": ICO_WRENCH,
                      "avatar": ICO_AVATAR, "chev": ICO_CHEV, "wand": ICO_WAND, "send": ICO_SEND}

# ---------------------------------------------------------------- 描述区折叠 + 内容加长
DESC_OLD = """        <div class="td-desc">
          <p>第二步：定义状态流转规则（启动整个流程）</p>
          <p>状态标识采用“交通灯”模式，方便直观管理：</p>
          <ul>
            <li>未开始：任务尚未启动。</li>
            <li>进行中：任务已启动，正在执行。</li>
            <li>已完成：任务成功完成并通过质量门禁。</li>
            <li>阻塞/异常：任务执行受阻，需要人工介入处理。</li>
          </ul>
          <div class="td-expand">"""

DESC_NEW = """        <div class="td-desc">
          <div class="td-desc-body" id="td-desc-body" data-td-desc="1">
            <p>第一步：梳理端到端交付链路</p>
            <p>从业务方原始需求进入系统开始，到最终交付物归档为止，完整链路包含需求澄清、方案设计、任务拆分、开发实现、自测验证、联调验收、灰度发布与交付归档共 8 个阶段。每个阶段都需要明确输入、输出、责任人与准入准出条件，避免出现“任务已发起但无人认领”或“交付物缺失但流程已关闭”的情况。</p>
            <p>第二步：定义状态流转规则（启动整个流程）</p>
            <p>状态标识采用“交通灯”模式，方便直观管理：</p>
            <ul>
              <li>未开始：任务尚未启动。</li>
              <li>进行中：任务已启动，正在执行。</li>
              <li>已完成：任务成功完成并通过质量门禁。</li>
              <li>阻塞/异常：任务执行受阻，需要人工介入处理。</li>
            </ul>
            <p>第三步：设定交付物标准</p>
            <p>每类任务需产出对应交付物并登记到任务详情：需求类任务产出需求说明与验收标准；设计类任务产出概要设计与接口定义；开发类任务产出代码与单元测试报告；验证类任务产出测试用例与缺陷清单。所有交付物需带版本号与责任人，便于回溯。</p>
            <p>第四步：明确质量门禁</p>
            <p>进入“已完成”前必须通过三项门禁检查：交付物齐全且可访问、关键路径有自动化验证覆盖、遗留缺陷已评估且不影响验收。任一门禁未通过，任务自动回退到“进行中”并通知责任人。</p>
          </div>
        </div>
        <div class="td-expand">"""

EXPAND_OLD = ('<span class="td-expand-line"></span>'
              '<button class="giencoder-btn giencoder-btn-text giencoder-btn-size-small td-expand-btn" '
              'type="button">展开全文</button><span class="td-expand-line"></span></div>\n        </div>')
EXPAND_NEW = ('<span class="td-expand-line"></span>'
              '<button class="giencoder-btn giencoder-btn-text giencoder-btn-size-small td-expand-btn" '
              'type="button" aria-expanded="false" aria-controls="td-desc-body" '
              'data-td-desc-toggle="1">展开全文</button><span class="td-expand-line"></span></div>')

# ---------------------------------------------------------------- 右栏头部三图标
ACTS_OLD = """          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini giencoder-btn-icon td-round-btn" type="button" aria-label="历史会话"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2.6 8a5.4 5.4 0 1 0 1.7-3.9"/><path d="M2.4 2.6v2.6h2.6"/><path d="M8 5.4V8l1.8 1.2"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini giencoder-btn-icon td-round-btn" type="button" aria-label="新建会话"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M8 3.4v9.2M3.4 8h9.2"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini giencoder-btn-icon td-round-btn" type="button" aria-label="更多"><svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><circle cx="3.6" cy="8" r="1.2"/><circle cx="8" cy="8" r="1.2"/><circle cx="12.4" cy="8" r="1.2"/></svg></button>"""

ACTS_NEW = """          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn" type="button" aria-label="新会话">%(new)s</button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn" type="button" aria-label="会话历史">%(hist)s</button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn" type="button" aria-label="全屏">%(full)s</button>""" % {
    "new": ICO_NEW, "hist": ICO_HIST, "full": ICO_FULL}

# ---------------------------------------------------------------- 旧输入框整块替换
COMPOSER_OLD = """      <div class="td-composer">
        <textarea class="td-composer-input" placeholder="提问、创建、搜索或@协作者" aria-label="输入消息"></textarea>
        <div class="td-composer-row">
          <button class="giencoder-btn giencoder-btn-secondary td-pill" type="button">__FILEICO__艾迪</button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round" type="button" aria-label="附件"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M10.6 5.4l-4.8 4.8a1.9 1.9 0 0 0 2.7 2.7l5-5a3.2 3.2 0 0 0-4.5-4.5l-5 5a4.5 4.5 0 0 0 6.4 6.4"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round" type="button" aria-label="更多设置"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M3 8h10M8 3v10"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary td-pill td-rightslot" type="button">DeepSeek-V4-Pro<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M2.6 4.6L6 8l3.4-3.4"/></svg></button>
        </div>
      </div>"""

# ---------------------------------------------------------------- CSS 替换
CSS_COMPOSER_OLD = """      /* -------------------- 底部输入区 -------------------- */
      .td-composer {
        flex: none; box-sizing: border-box; margin: 8px 20px 20px; height: 112px;
        display: flex; flex-direction: column; padding: 12px;
        border: 1px solid var(--color-border-2); border-radius: var(--border-radius-large);
        background: var(--color-bg-1);
      }
      .td-composer:hover { border-color: var(--color-border-3); }
      .td-composer-input {
        flex: 1; min-height: 0; width: 100%; box-sizing: border-box;
        border: none; outline: none; resize: none; padding: 0; background: transparent;
        font-family: var(--font-family); font-size: var(--font-size-body-3);
        line-height: 22px; color: var(--td-strong);
      }
      .td-composer-input::placeholder { color: var(--color-text-3); }
      .td-composer-row { flex: none; height: 32px; display: flex; align-items: center; gap: 4px; }
      /* 适配层：DS Button(secondary + size-default) → 胶囊描边 / 设计稿 32 高 */
      .td-pill { box-sizing: border-box; height: 32px; gap: 4px; border-radius: 32px; color: var(--td-ink-2); }
      .td-pill svg { width: 14px; height: 14px; flex: none; }
      .td-composer-row .td-rightslot { margin-left: auto; }
      /* 适配层：DS Button(secondary + size-default + icon) → 设计稿 32×32 圆形 */
      .td-round {
        box-sizing: border-box; width: 32px; padding: 0; border-radius: 32px;
        color: var(--td-ink-2); line-height: 0;
      }
"""

CSS_COMPOSER_NEW = """      /* -------------------- 底部输入区（复用基础工作台对话框模块） -------------------- */
      /* 模块本体来自 pages/base.html，本页只负责外层定位；不新增同义类 */
      .td-composer { flex: none; margin: 8px 20px 20px; }
      /* 补齐 base 页使用、本页 Tailwind 产物未包含的 3 个任意值类 */
      .td-composer .min-h-\\[96px\\] { min-height: 96px; }
      .td-composer .gap-\\[2px\\] { gap: 2px; }
      .td-composer .bg-\\[var\\(--color-fill-3\\)\\] { background: var(--color-fill-3); }
"""

SHELL_CSS = """      /* -------------------- 归属研发工作台：无左侧菜单栏 -------------------- */
      /* 详情页是研发工作台的下一级页面，隐藏 shell 侧栏，main 占满
         （1440 = 8 + 936 + 8 + 480 + 8，与设计稿一致） */
      body:has(.td-wrap) div:has(> main) > aside { display: none; }
      body:has(.td-wrap) div:has(> main) { padding-left: 8px; }
      body:has(.td-wrap) main { border: none; border-radius: 0; }
"""

# ---------------------------------------------------------------- JS
JS_OLD = """    var gutter = wrap.querySelector('[data-td-gutter]');"""
JS_NEW = """    /* 描述区：展开全文 / 收起 */
    var descBody = wrap.querySelector('[data-td-desc]');
    var descBtn = wrap.querySelector('[data-td-desc-toggle]');
    if (descBody && descBtn) {
      descBtn.addEventListener('click', function () {
        var open = descBody.classList.toggle('is-open');
        descBtn.textContent = open ? '收起' : '展开全文';
        descBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    var gutter = wrap.querySelector('[data-td-gutter]');"""

# ---------------------------------------------------------------- 应用
EDITS = [
    ("tokens", "        --td-gap: 24px;              /* 两栏间隙，同时是拖动热区（设计稿 936+24+480=1440） */\n",
     "        --td-gap: 8px;               /* 两栏间隙固定 8px（第22轮）；拖动热区由 ::before 外扩 */\n"
     "        --td-side-min: 280px;        /* 信息列最小宽度（第22轮） */\n"),
    ("left-border", "        background: var(--color-bg-1); border-radius: 8px;\n      }\n      .td-bar {",
     "        background: var(--color-bg-1); border: 1px solid var(--color-border-2); border-radius: 8px;\n      }\n      .td-bar {"),
    ("bar-line", "        display: flex; align-items: center; gap: 8px; padding: 0 20px;\n        background: var(--color-bg-1);\n      }\n",
     "        display: flex; align-items: center; gap: 8px; padding: 0 20px;\n"
     "        background: var(--color-bg-1); border-bottom: 1px solid var(--color-border-2);\n      }\n"),
    ("main-ratio", "        flex: 1 1 0; min-width: 0; overflow: auto; padding: 0 0 32px;\n",
     "        flex: 8 1 0; min-width: 0; overflow: auto; padding: 0 0 32px;  /* 主体 : 信息列 = 8 : 2 */\n"),
    ("title-bg", "        background: var(--color-bg-2);                        /* #FAFAFA 标题区 */\n",
     "        background: var(--color-fill-1);                      /* 浅灰标题区（设计稿 #FAFAFA） */\n"
     "        border-bottom: 1px solid var(--color-border-2);\n"),
    ("desc-collapse", "      .td-expand { display: flex; align-items: center; gap: 16px; margin-top: 12px; }\n",
     "      /* 描述区折叠：默认限高（设计稿 374），点「展开全文」展开 */\n"
     "      .td-desc-body { max-height: 374px; overflow: hidden; }\n"
     "      .td-desc-body.is-open { max-height: none; }\n"
     "      .td-expand { display: flex; align-items: center; gap: 16px; margin: 12px 40px 0; }\n"),
    ("side-ratio", "        flex: none; width: 240px; box-sizing: border-box; overflow: auto;\n"
                   "        padding: 20px 20px 32px 0; display: flex; flex-direction: column; gap: 24px;\n",
     "        flex: 2 1 0; min-width: var(--td-side-min); box-sizing: border-box; overflow: auto;\n"
     "        padding: 20px; display: flex; flex-direction: column; gap: 24px;\n"
     "        border-left: 1px solid var(--color-border-2);\n"),
    ("gutter-hit", "      .td-gutter-bar {\n",
     "      /* 间隙仅 8px，用 ::before 把拖动热区向两侧各扩 8px（视觉仍为 8px） */\n"
     "      .td-gutter::before { content: ''; position: absolute; left: -8px; right: -8px; top: 0; bottom: 0; }\n"
     "      .td-gutter-bar {\n"),
    ("right-border", "        background: var(--color-bg-1); border-radius: 8px;\n      }\n"
                     "      .td-right-inner { flex: 1; min-height: 0; display: flex; flex-direction: column; }",
     "        background: var(--color-bg-1); border: 1px solid var(--color-border-2); border-radius: 8px;\n      }\n"
     "      .td-right-inner { flex: 1; min-height: 0; display: flex; flex-direction: column; }"),
    ("round-btn-32", "      .td-round-btn { box-sizing: border-box; width: 24px; padding: 0; border-color: transparent; line-height: 0; }",
     "      .td-round-btn { box-sizing: border-box; width: 32px; padding: 0; border-color: transparent; line-height: 0; }"),
    ("composer-css", CSS_COMPOSER_OLD, CSS_COMPOSER_NEW),
    ("shell-css", "    </style>\"\"\"", SHELL_CSS + "    </style>\"\"\""),
    ("desc-html", DESC_OLD, DESC_NEW),
    ("expand-btn", EXPAND_OLD, EXPAND_NEW),
    ("acts-html", ACTS_OLD, ACTS_NEW),
    ("composer-html", COMPOSER_OLD, COMPOSER),
    ("js-toggle", JS_OLD, JS_NEW),
]

for name, old, new in EDITS:
    n = s.count(old)
    if n != 1:
        raise SystemExit("PATCH FAIL [%s] count=%d" % (name, n))
    s = s.replace(old, new)
    print("OK  %-14s" % name)

io.open(SRC, "w", encoding="utf-8").write(s)
print("PATCHED", SRC, len(s), "chars")
