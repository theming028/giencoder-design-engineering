
(function () {
  var KB_HTML = [
        "<div class=\"td-root\" role=\"region\" aria-label=\"任务详情\">",
        "  <section class=\"td-left\" aria-label=\"任务详细信息\">",
        "    <header class=\"td-bar\">",
        "      <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn td-back\" type=\"button\" aria-label=\"返回任务看板\" data-td-back=\"1\">",
        "        <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9.8 3.4L5.2 8l4.6 4.6\"/></svg>",
        "      </button>",
        "      <span class=\"td-bar-title\">任务详情</span>",
        "      <div class=\"td-bar-actions\">",
        "        <button class=\"giencoder-btn giencoder-btn-primary giencoder-btn-size-small td-btn\" type=\"button\">开始任务</button>",
        "        <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn\" type=\"button\">转派</button>",
        "        <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn\" type=\"button\">协作</button>",
        "        <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn\" type=\"button\">编辑</button>",
        "        <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn\" type=\"button\" aria-label=\"更多操作\">",
        "          <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"currentColor\"><circle cx=\"3.4\" cy=\"8\" r=\"1.3\"/><circle cx=\"8\" cy=\"8\" r=\"1.3\"/><circle cx=\"12.6\" cy=\"8\" r=\"1.3\"/></svg>",
        "        </button>",
        "        <span class=\"td-bar-sep\" aria-hidden=\"true\"></span>",
        "        <div class=\"td-bar-nav\">",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn\" type=\"button\" aria-label=\"上一个任务\" data-td-prev=\"1\">",
        "            <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3.6 9.8L8 5.4l4.4 4.4\"/></svg>",
        "          </button>",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn\" type=\"button\" aria-label=\"下一个任务\" data-td-next=\"1\">",
        "            <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3.6 6.2L8 10.6l4.4-4.4\"/></svg>",
        "          </button>",
        "        </div>",
        "      </div>",
        "    </header>",
        "    <div class=\"td-left-body\">",
        "      <div class=\"td-main\">",
        "        <h1 class=\"td-title\">端到端流程初始化：用户输入业务流程并触发全链路交付</h1>",
        "        <div class=\"td-desc\">",
        "          <div class=\"td-desc-body\" id=\"td-desc-body\" data-td-desc=\"1\">",
        "            <p>第一步：梳理端到端交付链路</p>",
        "            <p>从业务方原始需求进入系统开始，到最终交付物归档为止，完整链路包含需求澄清、方案设计、任务拆分、开发实现、自测验证、联调验收、灰度发布与交付归档共 8 个阶段。每个阶段都需要明确输入、输出、责任人与准入准出条件，避免出现“任务已发起但无人认领”或“交付物缺失但流程已关闭”的情况。</p>",
        "            <p>第二步：定义状态流转规则（启动整个流程）</p>",
        "            <p>状态标识采用“交通灯”模式，方便直观管理：</p>",
        "            <ul>",
        "              <li>未开始：任务尚未启动。</li>",
        "              <li>进行中：任务已启动，正在执行。</li>",
        "              <li>已完成：任务成功完成并通过质量门禁。</li>",
        "              <li>阻塞/异常：任务执行受阻，需要人工介入处理。</li>",
        "            </ul>",
        "            <p>第三步：设定交付物标准</p>",
        "            <p>每类任务需产出对应交付物并登记到任务详情：需求类任务产出需求说明与验收标准；设计类任务产出概要设计与接口定义；开发类任务产出代码与单元测试报告；验证类任务产出测试用例与缺陷清单。所有交付物需带版本号与责任人，便于回溯。</p>",
        "            <p>第四步：明确质量门禁</p>",
        "            <p>进入“已完成”前必须通过三项门禁检查：交付物齐全且可访问、关键路径有自动化验证覆盖、遗留缺陷已评估且不影响验收。任一门禁未通过，任务自动回退到“进行中”并通知责任人。</p>",
        "          </div>",
        "        </div>",
        "        <div class=\"td-expand\"><span class=\"td-expand-line\"></span><button class=\"giencoder-btn giencoder-btn-text giencoder-btn-size-small td-expand-btn\" type=\"button\" aria-expanded=\"false\" aria-controls=\"td-desc-body\" data-td-desc-toggle=\"1\">展开全文</button><span class=\"td-expand-line\"></span></div>",
        "        <section class=\"td-sec\">",
        "          <div class=\"td-sec-head\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/><path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg>2个附件</div>",
        "          <div class=\"td-files\">",
        "            <a class=\"td-file\" href=\"#\" title=\"端到端流程初始化：用户输入业务流程并触发全链路交付.docx\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z\"/><path d=\"M9 1.8v3.4h3.8\"/></svg></span><span class=\"td-file-tx\">端到端流程初始化：用户输入业务流程并触发全链路交付.docx</span></a>",
        "            <a class=\"td-file\" href=\"#\" title=\"TaskBoard.png\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z\"/><path d=\"M9 1.8v3.4h3.8\"/></svg></span><span class=\"td-file-tx\">TaskBoard.png</span></a>",
        "          </div>",
        "        </section>",
        "        <section class=\"td-sec\">",
        "          <div class=\"td-sec-head\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/><path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg>3个 AI 产物</div>",
        "          <div class=\"td-files\">",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"prd-template.html\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z\"/><path d=\"M9 1.8v3.4h3.8\"/></svg></span><span class=\"td-file-body\"><span class=\"td-file-tx\">prd-template.html</span><span class=\"td-file-size\">128KB</span></span></a>",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"端到端初始化 - 任务分析报告.md\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z\"/><path d=\"M9 1.8v3.4h3.8\"/></svg></span><span class=\"td-file-body\"><span class=\"td-file-tx\">端到端初始化 - 任务分析报告.md</span><span class=\"td-file-size\">128KB</span></span></a>",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"spec-template.md\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z\"/><path d=\"M9 1.8v3.4h3.8\"/></svg></span><span class=\"td-file-body\"><span class=\"td-file-tx\">spec-template.md</span><span class=\"td-file-size\">128KB</span></span></a>",
        "          </div>",
        "        </section>",
        "        <section class=\"td-sec\">",
        "          <div class=\"td-sec-head\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/><path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg>文件</div>",
        "          <div class=\"td-files\">",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"概要设计-Steps.md\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z\"/><path d=\"M9 1.8v3.4h3.8\"/></svg></span><span class=\"td-file-body\"><span class=\"td-file-tx\">概要设计-Steps.md</span><span class=\"td-file-size\">17KB</span></span></a>",
        "          </div>",
        "        </section>",
        "      </div>",
        "      <aside class=\"td-side\" aria-label=\"任务属性与动态\">",
        "        <section class=\"td-side-attr\">",
        "          <h2>任务属性</h2>",
        "          <div class=\"td-attr\">",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">状态</span><span class=\"td-attr-v\"><span class=\"giencoder-badge giencoder-badge-status\"><span class=\"giencoder-badge-status-dot giencoder-badge-status-processing\"></span><span class=\"giencoder-badge-status-text\">进行中</span></span></span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">执行人</span><span class=\"td-attr-v\">邵禹铭</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">优先级</span><span class=\"td-attr-v\"><span class=\"giencoder-tag giencoder-tag-danger td-tag-prio\"><span class=\"giencoder-tag-content\">高优先级</span></span></span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">项目</span><span class=\"td-attr-v\">演练指挥系统</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">来源需求</span><span class=\"td-attr-v\"><a class=\"td-attr-link\" href=\"#\">GienX端到端初始化…<svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/><path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg></a></span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">实际开始</span><span class=\"td-attr-v\">2026/08/01 10:12</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">实际完成</span><span class=\"td-attr-v\">2026/08/12 15:27</span></div>",
        "          </div>",
        "        </section>",
        "        <section>",
        "          <h2>任务动态</h2>",
        "          <ul class=\"td-tl\">",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">Agent</span><span class=\"td-tl-what\">完成了任务开发</span></div><span class=\"td-tl-time\">刚刚</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">Agent</span><span class=\"td-tl-what\">已确认任务目标和优先级</span></div><span class=\"td-tl-time\">半小时前</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">邵禹铭</span><span class=\"td-tl-what\">状态更新为进行中</span></div><span class=\"td-tl-time\">昨天 10:02</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">邵禹铭</span><span class=\"td-tl-what\">补充了需求说明材料</span></div><span class=\"td-tl-time\">08/12 09:27</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">系统</span><span class=\"td-tl-what\">已同步最新处理进展</span></div><span class=\"td-tl-time\">08/11 16:51</span></li>",
        "          </ul>",
        "        </section>",
        "        <section class=\"td-side-foot\" aria-label=\"任务记录信息\">",
        "          <div class=\"td-attr\">",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">创建者</span><span class=\"td-attr-v\">秦怡</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">创建时间</span><span class=\"td-attr-v\">2026/08/12 15:27</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">最后更新</span><span class=\"td-attr-v\">半小时前</span></div>",
        "          </div>",
        "        </section>",
        "      </aside>",
        "    </div>",
        "  </section>",
        "  <div class=\"td-gutter\" role=\"separator\" tabindex=\"0\" aria-orientation=\"vertical\" aria-label=\"调整 AI 会话栏宽度\" aria-valuenow=\"480\" aria-valuemin=\"48\" aria-valuemax=\"1200\" data-td-gutter=\"1\"><span class=\"td-gutter-bar\"></span></div>",
        "  <aside class=\"td-right\" aria-label=\"AI 会话\">",
        "    <div class=\"td-right-inner\">",
        "      <header class=\"td-right-bar\">",
        "        <div class=\"td-right-head\">",
        "          <div class=\"td-right-title\">端到端流程初始化：用户输入业务流程并触发全链路交付</div>",
        "          <div class=\"td-right-time\">2026/08/01 11:26</div>",
        "        </div>",
        "        <div class=\"td-right-acts\">",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn\" type=\"button\" aria-label=\"新会话\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-plus\" aria-hidden=\"true\"><path d=\"M5 12h14\"/><path d=\"M12 5v14\"/></svg></button>",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn\" type=\"button\" aria-label=\"会话历史\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-history\" aria-hidden=\"true\"><path d=\"M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8\"/><path d=\"M3 3v5h5\"/><path d=\"M12 7v5l4 2\"/></svg></button>",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn\" type=\"button\" aria-label=\"全屏\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-maximize\" aria-hidden=\"true\"><path d=\"M8 3H5a2 2 0 0 0-2 2v3\"/><path d=\"M21 8V5a2 2 0 0 0-2-2h-3\"/><path d=\"M3 16v3a2 2 0 0 0 2 2h3\"/><path d=\"M16 21h3a2 2 0 0 0 2-2v-3\"/></svg></button>",
        "        </div>",
        "      </header>",
        "      <div class=\"td-chat\">",
        "        <div class=\"td-msg-user\">请帮我先分析一下这个任务</div>",
        "        <div class=\"td-msg-ai\">",
        "          <div class=\"td-ai-head\">",
        "            <span class=\"td-ai-avatar\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 2.2l1.8 4 4 1.8-4 1.8L8 13.8l-1.8-4-4-1.8 4-1.8z\"/></svg></span>",
        "            <span class=\"td-ai-name\">艾迪</span>",
        "          </div>",
        "          <div class=\"td-ai-meta\">",
        "            <a href=\"#\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/><path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg>思考过程</a>",
        "            <span class=\"td-sep\"></span>",
        "            <a href=\"#\">任务完成，耗时 28m12s</a>",
        "          </div>",
        "          <p>好的，收到您的需求。这是一个典型的“从需求到交付”的端到端流程初始化场景。我将为您设计一个完整的交付状态跟踪表，并定义启动整个流程所需的初始状态和关键节点。</p>",
        "          <p>我先把几个核心不确定性列出来，请你选择倾向，不确定的地方我会标注我的判断。</p>",
        "          <div class=\"td-ai-file\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z\"/><path d=\"M9 1.8v3.4h3.8\"/></svg></span><span class=\"td-file-body\"><span class=\"td-file-tx\">端到端初始化 - 任务分析报告.md</span><span class=\"td-file-size\">128KB</span></span></div>",
        "          <div class=\"td-ai-foot\"><span>输出完成</span><span class=\"td-sep\"></span><span>Token 速率：256/s</span></div>",
        "        </div>",
        "      </div>",
        "        <!-- 复用基础工作台的对话框模块（pages/base.html，结构与类名一致） -->",
        "        <div class=\"td-composer\">",
        "          <div class=\"relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors\" style=\"border-color: var(--color-border-2); box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);\">",
        "            <textarea rows=\"1\" placeholder=\"描述你的任务，/ 调用技能，@引用文件\" aria-label=\"输入消息\" class=\"min-w-0 resize-none bg-transparent text-sm leading-[22px] [color:var(--color-text-1)] outline-none placeholder:[color:var(--color-text-3)] min-h-[96px]\"></textarea>",
        "            <div class=\"mt-auto flex items-center justify-between\">",
        "              <div class=\"flex items-center gap-[8px]\">",
        "                <div class=\"giencoder-select\" style=\"flex-direction: row; align-items: flex-start; position: relative;\">",
        "                  <button type=\"button\" aria-label=\"添加\" aria-haspopup=\"menu\" aria-expanded=\"false\" class=\"flex size-8 items-center justify-center rounded-full border border-[var(--color-border-1)] text-[var(--color-text-2)] transition-colors hover:bg-[var(--color-fill-1)] hover:[color:var(--color-text-1)]\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-plus size-[14px]\" aria-hidden=\"true\"><path d=\"M5 12h14\"></path><path d=\"M12 5v14\"></path></svg></button>",
        "                  <div role=\"menu\" aria-label=\"添加内容\"></div>",
        "                </div>",
        "                <button type=\"button\" aria-label=\"技能\" aria-haspopup=\"listbox\" aria-expanded=\"false\" class=\"flex size-8 items-center justify-center rounded-full border border-[var(--color-border-1)] text-[var(--color-text-2)] transition-colors hover:bg-[var(--color-fill-1)] hover:[color:var(--color-text-1)]\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-wrench size-[14px]\" aria-hidden=\"true\"><path d=\"M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z\"></path></svg></button>",
        "                <div class=\"avatar-wrap relative flex items-center\">",
        "                  <button type=\"button\" aria-label=\"数字分身\" aria-pressed=\"true\" class=\"flex h-8 items-center gap-[2px] rounded-full px-3 py-[5px] text-[14px] leading-[19px] transition-colors\" style=\"background: rgb(236, 242, 255); color: rgb(55, 112, 247); border: 1px solid rgb(211, 226, 255);\"><svg viewBox=\"0 0 14 14\" width=\"14\" height=\"14\" class=\"size-[14px]\"><path d=\"M6.988754947683716,13.43000001192093C5.103876847683716,13.43000001192093,3.4284298476837156,12.17341601192093,2.9048526476837155,10.497968511920929L2.590706447683716,10.812115011920929C2.381275537683716,11.02154501192093,1.9624137876837158,11.02154501192093,1.6482674076837158,10.812115011920929C1.334121017683716,10.602683011920929,1.4388364836837158,10.183822411920929,1.6482674076837158,9.869675411920928L2.6954218476837157,8.822521011920928L2.6954218476837157,7.984796811920929C2.2765598876837156,7.670650811920929,2.067129017683716,7.147073111920929,2.067129017683716,6.623495911920929L2.067129017683716,3.586747711920929C2.067129017683716,2.539593411920929,2.9048526476837155,1.701869811920929,3.952006847683716,1.701869811920929L6.360462447683716,1.701869811920929L6.360462447683716,1.1782926319209288C6.360462447683716,0.8641463219209289,6.674608947683716,0.550000011920929,6.988754947683716,0.550000011920929C7.302901547683716,0.550000011920929,7.617047547683716,0.8641463219209289,7.617047547683716,1.1782926319209288L7.617047547683716,1.701869811920929L10.025503347683715,1.701869811920929C11.072657847683717,1.701869811920929,11.910381047683716,2.539593411920929,11.910381047683716,3.586747711920929L11.910381047683716,6.623495911920929C11.910381047683716,7.147073111920929,11.700949047683716,7.670649811920929,11.282088547683715,7.984796811920929L11.282088547683715,8.822521011920928L12.329243047683716,9.869675411920928C12.538674047683715,10.079107111920928,12.538674047683715,10.497968511920929,12.329243047683716,10.812115011920929C12.119811047683715,11.126262011920929,11.700951047683716,11.02154501192093,11.386802947683716,10.812115011920929L11.072657847683717,10.497968511920929C10.549079147683717,12.17341601192093,8.873632647683717,13.43000001192093,6.988754947683716,13.43000001192093ZM3.9520075476837158,9.13666611192093C3.9520075476837158,10.81211401192093,5.313308247683716,12.173413011920928,6.988754947683716,12.173413011920928C8.664201947683715,12.173413011920928,10.025503347683715,10.81211401192093,10.025503347683715,9.13666611192093L10.025503347683715,8.50837351192093L3.9520075476837158,8.50837351192093L3.9520075476837158,9.13666611192093ZM3.9520075476837158,3.063170711920929C3.6378612476837158,3.063170711920929,3.3237144476837157,3.2726017119209287,3.3237144476837157,3.586747911920929L3.3237144476837157,6.623495911920929C3.3237144476837157,6.937641911920929,3.6378610476837157,7.251788411920929,3.952006847683716,7.251788411920929L10.025502447683715,7.251788411920929C10.339648447683716,7.251788411920929,10.549078247683715,7.042357311920929,10.549078247683715,6.728210711920929L10.549078247683715,3.586747511920929C10.549078247683715,3.272601211920929,10.339647547683716,3.0631702119209288,10.025502447683715,3.0631702119209288L3.9520075476837158,3.063170711920929ZM8.873633647683715,6.099919111920929C8.559487547683716,6.099919111920929,8.245341047683716,5.785772111920929,8.245341047683716,5.471626611920929L8.245341047683716,4.843334011920929C8.140625747683716,4.424471911920929,8.454771747683715,4.1103256119209295,8.873633647683715,4.1103256119209295C9.292495947683715,4.1103256119209295,9.501925747683716,4.424471911920929,9.501925747683716,4.738618211920929L9.501925747683716,5.366911211920929C9.501925747683716,5.785772111920929,9.187779647683715,6.099919111920929,8.873633647683715,6.099919111920929ZM5.103877547683716,6.099919111920929C4.789731547683716,6.099919111920929,4.475585247683716,5.785772111920929,4.475585247683716,5.471626611920929L4.475585247683716,4.843334011920929C4.475585247683716,4.424471911920929,4.789731547683716,4.1103256119209295,5.103877547683716,4.1103256119209295C5.418023847683716,4.1103256119209295,5.732170347683716,4.424471911920929,5.732170347683716,4.738618211920929L5.732170347683716,5.366911211920929C5.836885647683716,5.785772111920929,5.5227391476837155,6.099919111920929,5.103877547683716,6.099919111920929Z\" fill=\"currentColor\" fill-rule=\"evenodd\"></path></svg>艾迪</button>",
        "                  <div role=\"tooltip\" class=\"avatar-tooltip\">停用数字分身</div>",
        "                </div>",
        "                <div class=\"giencoder-select\" style=\"width: 96px; flex-shrink: 0;\">",
        "                  <div class=\"giencoder-select-view select-view-ghost\" tabindex=\"0\" role=\"combobox\" aria-haspopup=\"listbox\" aria-expanded=\"false\" style=\"height: 32px; min-height: 32px; border: 1px solid var(--color-border-1); border-radius: 32px; background-color: transparent; box-shadow: none; padding: 5px 12px; gap: 4px;\">",
        "                    <div class=\"giencoder-select-selection\" style=\"gap: 4px;\"><span class=\"giencoder-select-view-text\">标准模式</span></div>",
        "                    <span class=\"giencoder-select-suffix\"><svg viewBox=\"0 0 12 12\" width=\"12\" height=\"12\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.4\" stroke-linecap=\"round\"><path d=\"M2.6 4.6L6 8l3.4-3.4\"/></svg></span>",
        "                  </div>",
        "                  <div class=\"giencoder-select-popup\" style=\"display: none;\">",
        "                    <ul class=\"giencoder-select-option-list\" role=\"listbox\">",
        "                      <li class=\"giencoder-select-option giencoder-select-option-selected\" role=\"option\" aria-selected=\"true\">标准模式</li>",
        "                      <li class=\"giencoder-select-option\" role=\"option\" aria-selected=\"false\">专家模式</li>",
        "                    </ul>",
        "                  </div>",
        "                </div>",
        "              </div>",
        "              <div class=\"flex items-center gap-2\">",
        "                <div class=\"giencoder-select\" style=\"width: fit-content; max-width: 200px; flex-shrink: 0; margin-left: auto;\">",
        "                  <div class=\"giencoder-select-view select-view-ghost\" tabindex=\"0\" role=\"combobox\" aria-haspopup=\"listbox\" aria-expanded=\"false\" style=\"height: 32px; min-height: 32px; border: none; border-radius: 32px; gap: 2px; padding: 0 12px;\">",
        "                    <div class=\"giencoder-select-selection\" style=\"gap: 2px;\"><span class=\"giencoder-select-view-text\">DeepSeek-V4-Pro</span></div>",
        "                    <span class=\"giencoder-select-suffix\"><svg viewBox=\"0 0 12 12\" width=\"12\" height=\"12\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.4\" stroke-linecap=\"round\"><path d=\"M2.6 4.6L6 8l3.4-3.4\"/></svg></span>",
        "                  </div>",
        "                  <div class=\"giencoder-select-popup\" style=\"display: none;\">",
        "                    <ul class=\"giencoder-select-option-list\" role=\"listbox\" aria-label=\"大模型选择\">",
        "                      <li class=\"giencoder-select-option giencoder-select-option-selected\" role=\"option\" aria-selected=\"true\">DeepSeek-V4-Pro</li>",
        "                      <li class=\"giencoder-select-option\" role=\"option\" aria-selected=\"false\">GLM-5.2-公司共用</li>",
        "                    </ul>",
        "                  </div>",
        "                </div>",
        "                <button type=\"button\" aria-label=\"优化提示词\" class=\"flex size-8 items-center justify-center rounded-full transition-colors hover:bg-[var(--color-fill-1)]\" style=\"background: rgb(255, 255, 255);\"><svg viewBox=\"0 0 14.08 14.06\" width=\"14\" height=\"14\" fill=\"none\"><path d=\"M9.1414957,4.6432233C8.8303785,4.9347887,8.3439808,4.9266973,8.0427332,4.6249452C7.7414865,4.3231936,7.7342105,3.8367827,8.0262985,3.5261555L9.7009659,1.8514888C10.009434,1.5430192,10.509562,1.5430192,10.818031,1.8514888C11.126502,2.1599586,11.126502,2.6600869,10.818032,2.9685569L9.1405592,4.6432233L9.1414957,4.6432233Z\" fill=\"#BEBEBE\"></path><path d=\"M11.878967,7.1103153L9.5091734,7.1103153C9.0621662,7.1256995,8.6914234,6.7674994,8.6914234,6.3202286C8.6914234,5.8729568,9.0621662,5.5147567,9.5091734,5.5301414L11.879902,5.5301414C12.326908,5.5147567,12.697651,5.8729568,12.697651,6.3202286C12.697649,6.7674994,12.326908,7.1256995,11.879902,7.1103153L11.878967,7.1103153Z\" fill=\"#BEBEBE\"></path><path d=\"M4.1137528,4.8761797C3.9033761,4.8776922,3.7011769,4.7947903,3.5524123,4.6460304L1.8777457,2.971364C1.569276,2.6628945,1.569276,2.162766,1.8777457,1.8542962C2.1862154,1.5458264,2.6863437,1.5458263,2.9948137,1.854296L4.6694798,3.5289626C4.8958349,3.7551589,4.9632897,4.0956059,4.8402843,4.3910227C4.717279,4.68644,4.4281397,4.8784089,4.1081395,4.8771148L4.1137528,4.8761797Z\" fill=\"#BEBEBE\"></path><path d=\"M6.3497601,0C6.7863712,0,7.1403146,0.35394344,7.1403146,0.79055488L7.1403146,3.1612837C7.1256599,3.5870585,6.7762556,3.9246454,6.3502278,3.9246454C5.9242005,3.9246454,5.5747943,3.5870588,5.5601397,3.1612837L5.5601397,0.79055488C5.5601397,0.35430831,5.9135146,0.00051608856,6.3497601,0Z\" fill=\"#BEBEBE\"></path><path d=\"M0.819619,5.5301414L3.1884768,5.5301414C3.6354835,5.5147562,4.0062251,5.8729568,4.0062251,6.3202286C4.0062251,6.7674994,3.6354835,7.1256995,3.1884768,7.1103153L0.81774795,7.1103153C0.37074119,7.1256995,0,6.7674994,0,6.3202286C2.5033659e-8,5.8729568,0.37074125,5.5147562,0.81774795,5.5301414L0.819619,5.5301414Z\" fill=\"#BEBEBE\"></path><path d=\"M3.5570905,7.9972339C3.8655162,7.6885071,4.3658547,7.6883845,4.6744308,7.9969606C4.9830074,8.3055372,4.9828858,8.8058758,4.6741581,9.1143007L2.9994922,10.788968C2.688375,11.08053,2.2019811,11.072435,1.9007362,10.770686C1.5994915,10.468936,1.5922134,9.9825287,1.8842953,9.6718998L3.5570905,7.9972339Z\" fill=\"#BEBEBE\"></path><path d=\"M6.3497601,8.6886187C6.7863712,8.6886187,7.1403146,9.0425615,7.1403146,9.4791737L7.1403146,11.849901C7.1256599,12.275676,6.7762556,12.613264,6.3502278,12.613264C5.9242005,12.613264,5.5747943,12.275676,5.5601397,11.849901L5.5601397,9.4791737C5.5601397,9.0429258,5.9135141,8.6891346,6.3497601,8.6886187Z\" fill=\"#BEBEBE\"></path><path d=\"M5.9540148,5.9240155C6.2626376,5.6159139,6.7624602,5.6159139,7.0710826,5.9240155L9.1424294,7.9953628L10.817097,9.6700287L13.785653,12.650749C14.077717,12.96138,14.070429,13.447771,13.769192,13.749513C13.467955,14.051255,12.981577,14.059359,12.670459,13.767816L5.9577575,7.0410843C5.6478443,6.7339692,5.6457491,6.2337155,5.9530797,5.9240155L5.9540148,5.9240155Z\" fill=\"#BEBEBE\"></path></svg></button>",
        "                <button type=\"button\" aria-label=\"发送\" disabled class=\"flex shrink-0 !size-8 !rounded-full !p-0 items-center justify-center transition-colors\" style=\"background: var(--color-fill-3); cursor: not-allowed; opacity: 0.5;\"><svg viewBox=\"8.82 10.73 14.08 11.38\" width=\"14\" height=\"14\" fill=\"none\"><path d=\"M9.028238606,34.839137L11.6378174,29.1173639C11.6825285,28.9479885,11.6825285,28.7663059,11.6378174,28.6000094L9.028238606,22.87514764C8.88469238,22.32391092,9.31768426,21.81578781,9.7224375,22.065230064L19.998936,28.4367857C20.267201,28.6030817,20.267201,29.1050444,19.998936,29.2713394L9.7224375,35.649054C9.31768426,35.898499,8.88469242,35.390374,9.028238606,34.839137Z\" fill=\"#FFFFFF\" transform=\"matrix(0,-1,1,0,-13,31)\"></path></svg></button>",
        "              </div>",
        "            </div>",
        "          </div>",
        "        </div>",
        "    </div>",
        "    <button class=\"td-collapsed\" type=\"button\" aria-label=\"展开 AI 会话\" data-td-expand=\"1\">",
        "      <span>展</span><span>开</span><span>AI</span><span>会</span><span>话</span>",
        "    </button>",
        "  </aside>",
        "</div>"
].join('\n');

  function bindDetail(wrap) {
    var root = wrap.querySelector('.td-root');
    if (!root) return;
    /* 返回任务看板 */
    var back = wrap.querySelector('[data-td-back]');
    if (back) back.addEventListener('click', function () { location.href = 'kanban.html'; });

    /* 描述区：展开全文 / 收起 */
    var descBody = wrap.querySelector('[data-td-desc]');
    var descBtn = wrap.querySelector('[data-td-desc-toggle]');
    if (descBody && descBtn) {
      descBtn.addEventListener('click', function () {
        var open = descBody.classList.toggle('is-open');
        descBtn.textContent = open ? '收起' : '展开全文';
        descBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    var gutter = wrap.querySelector('[data-td-gutter]');
    var right = wrap.querySelector('.td-right');
    if (!gutter || !right) return;

    var DEFAULT_W = 480;   /* 右栏默认宽（设计稿实测） */
    var MIN_W = 100;       /* 拖到此值以下即自动折叠（第24轮：原 320） */
    var COLLAPSED_W = 48;  /* 折叠条宽（设计稿实测 1343:18532 = 48×844） */
    var LEFT_MIN = 320;    /* 左栏保底 */
    var dragging = false, curW = DEFAULT_W;

    function setWidth(w) {
      curW = w;
      root.style.setProperty('--td-right-w', w + 'px');
      gutter.setAttribute('aria-valuenow', String(Math.round(w)));
    }
    function collapse() {
      root.classList.add('is-collapsed');
      setWidth(COLLAPSED_W);
    }
    function expand(w) {
      root.classList.remove('is-collapsed');
      setWidth(w || DEFAULT_W);
    }
    /* 拖动分栏 */
    gutter.addEventListener('pointerdown', function (e) {
      if (root.classList.contains('is-collapsed')) return;
      dragging = true;
      root.classList.add('is-dragging');
      gutter.classList.add('is-dragging');
      if (gutter.setPointerCapture) { try { gutter.setPointerCapture(e.pointerId); } catch (err) {} }
      e.preventDefault();
    });
    gutter.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var box = root.getBoundingClientRect();
      var w = box.right - e.clientX;
      var maxW = box.width - LEFT_MIN;
      if (w > maxW) w = maxW;
      if (w < 0) w = 0;
      /* 第 24 轮第 4 项：拖到 100px 以下立刻折叠成窄条（实时反馈）；
         继续向左拖回 100px 以上则恢复跟随鼠标。松手时以 curW 判定最终状态。 */
      if (w < MIN_W) {
        curW = w;                                  /* 记录真实拖拽宽度，便于反向恢复 */
        root.classList.add('is-collapsed');
        setWidth(COLLAPSED_W);
      } else {
        root.classList.remove('is-collapsed');
        setWidth(Math.round(w));
      }
    });
    function endDrag() {
      if (!dragging) return;
      dragging = false;
      root.classList.remove('is-dragging');
      gutter.classList.remove('is-dragging');
      if (curW < MIN_W) collapse();          /* 过窄 -> 自动折叠 */
      else root.classList.remove('is-collapsed');
    }
    gutter.addEventListener('pointerup', endDrag);
    gutter.addEventListener('pointercancel', endDrag);
    /* 键盘可达：← 变宽 / → 变窄（到阈值即折叠） */
    gutter.addEventListener('keydown', function (e) {
      var step = 24;
      var maxW = root.getBoundingClientRect().width - LEFT_MIN;
      if (e.key === 'ArrowLeft') { expand(Math.min(curW + step, maxW)); e.preventDefault(); }
      else if (e.key === 'ArrowRight') {
        var nw = curW - step;
        if (nw < MIN_W) collapse(); else expand(nw);
        e.preventDefault();
      }
    });
    /* 折叠态：点击整列恢复默认宽度比例 */
    right.addEventListener('click', function (e) {
      if (!root.classList.contains('is-collapsed')) return;
      e.preventDefault();
      expand(DEFAULT_W);
    });
  }

  /* 外壳页签：本页归属研发工作台。React 外壳按「文件名 → 路由」判页签
     （task-detail.html 不在映射表内 → 被判成「基础工作台」）。外观（轨道底/游标/文字色）
     已由 CSS 覆盖；这里把页签的**文案与图标**也还原成 shell 自己的 dev 态：
     未选中 = 无图标 + 前 2 字；选中 = 图标 + 完整文案（与 shell 内 `r?label:label.slice(0,2)` 一致）。 */
  var DEV_ICON = '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" class="mr-1.5 size-4 shrink-0" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.08 4.315a3 3 0 012.328.01l17.769 7.576A3 3 0 0145 14.661v19.645a3 3 0 01-1.951 2.81L25.28 43.745a3 3 0 01-2.074.008L4.974 37.12A3 3 0 013 34.299V14.668a3 3 0 011.848-2.77l18.231-7.582zm1.146 3.855L7 15.334V33.6l17.227 6.27L41 33.61V15.32L24.226 8.17zm3.498 17.623L21.608 18l-6.377 4.723h-6.19L9 26.37h7.367l4.376-3.051l6.34 7.68 6.307-4.63H39l-.02-3.647h-7.117l-4.139 3.07z" fill="currentColor"></path></svg>';
  function setTabLabel(btn, text) {
    for (var i = btn.childNodes.length - 1; i >= 0; i--) {
      if (btn.childNodes[i].nodeType === 3) btn.removeChild(btn.childNodes[i]);
    }
    btn.appendChild(document.createTextNode(text));
  }
  function syncShellTab() {
    var tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
    if (!tl) return false;
    var base = tl.querySelector('[data-tab="base"]');
    var dev = tl.querySelector('[data-tab="dev"]');
    if (base) {
      base.setAttribute('aria-selected', 'false');
      var bi = base.querySelector('svg');
      if (bi) base.removeChild(bi);
      setTabLabel(base, '基础');
    }
    if (dev) {
      dev.setAttribute('aria-selected', 'true');
      if (!dev.querySelector('svg')) dev.insertAdjacentHTML('afterbegin', DEV_ICON);
      setTabLabel(dev, '研发工作台');
    }
    return true;
  }

  function inject() {
    var main = document.querySelector('main');
    if (!main || main.querySelector('.td-root')) return false;
    var wrap = document.createElement('div');
    wrap.className = 'td-wrap';
    wrap.innerHTML = KB_HTML;
    main.appendChild(wrap);
    bindDetail(wrap);
    return true;
  }
  /* 注意：两个动作都要执行，不能短路（页签在 React 挂载后才出现，可能晚于注入） */
  function ready() {
    var injected = inject();
    var tabbed = syncShellTab();
    return injected && tabbed;
  }
  if (!ready()) {
    var mo = new MutationObserver(function () { if (ready()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
