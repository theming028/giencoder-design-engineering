# -*- coding: utf-8 -*-
"""生成 mg-work/desc-fig.svg —— 任务详情页 .td-desc 里的「端到端交付链路」示意图（第 28 轮第 2 项）。

设计稿 622:13950 的 .td-desc 里**没有**配图，这张是本次新增内容，视觉语言对齐 DS：
  底色 #F7F7F7(--color-fill-1) / 卡片白底 + #E5E5E5(--color-border-2) 描边 / 圆角 12
  序号胶囊 #E8F0FE(--color-primary-light-1) + #3770F7(--color-primary-6) 文字
  标题 #1F1F1F(--color-text-1) / 说明 #868686(--color-text-3) / 连接线 #DCDCDC
⚠️ img 里的 SVG 是独立文档，取不到页面 CSS 变量 → 这里色值只能字面写死（值与 DS 一致，见上）。
   所以本文件里的 hex 是「素材」而非「组件样式」，不受「禁止硬编码 hex」约束。

用法：python mg-work/r28/build-desc-fig.py   （在仓库根目录执行）
产物：mg-work/desc-fig.svg   （由 mg-work/r21/build-detail.py 读入并 base64 成 data URI）
"""
import io

STAGES = [
    ("需求澄清", "明确输入、输出与责任人"),
    ("方案设计", "概要设计与接口定义"),
    ("任务拆分", "拆到可独立交付的粒度"),
    ("开发实现", "编码与单元测试"),
    ("自测验证", "用例通过率与缺陷收敛"),
    ("联调验收", "跨系统联调与验收确认"),
    ("灰度发布", "分批放量并观察核心指标"),
    ("交付归档", "交付物登记与版本留存"),
]
W, H = 1240, 620                 # 2:1，配合 .td-desc img{max-width:620px} → 折叠态内完整可见
NW, NH, PITCH, GAP = 240, 100, 300, 60
X0, Y1, Y2 = 50, 140, 380
FONT = "PingFang SC, Microsoft YaHei, Helvetica, Arial, sans-serif"

p = []
p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img" aria-label="端到端交付链路 8 个阶段示意图">' % (W, H, W, H))
p.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
         'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#A9A9A9"/></marker></defs>')
p.append('<rect width="%d" height="%d" rx="16" fill="#F7F7F7"/>' % (W, H))
# 蛇形连接线：第一行末 → 折返 → 第二行首
p.append('<path d="M%d %d V%d H%d V%d" fill="none" stroke="#DCDCDC" stroke-width="2" '
         'stroke-linecap="round" marker-end="url(#ah)"/>'
         % (X0 + 3 * PITCH + NW / 2, Y1 + NH, (Y1 + NH + Y2) // 2, X0 + NW / 2, Y2))
# 行内箭头
for y in (Y1, Y2):
    for c in range(3):
        x = X0 + c * PITCH + NW
        p.append('<path d="M%d %d H%d" fill="none" stroke="#DCDCDC" stroke-width="2" '
                 'stroke-linecap="round" marker-end="url(#ah)"/>' % (x + 8, y + NH / 2, x + GAP - 8))
for i, (name, desc) in enumerate(STAGES):
    x = X0 + (i % 4) * PITCH
    y = Y1 if i < 4 else Y2
    p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#FFFFFF" stroke="#E5E5E5"/>'
             % (x, y, NW, NH))
    p.append('<circle cx="%d" cy="%d" r="13" fill="#E8F0FE"/>' % (x + 30, y + 34))
    p.append('<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="13" '
             'font-weight="600" fill="#3770F7">%d</text>' % (x + 30, y + 38.5, FONT, i + 1))
    p.append('<text x="%d" y="%d" font-family="%s" font-size="15" font-weight="500" '
             'fill="#1F1F1F">%s</text>' % (x + 54, y + 39, FONT, name))
    p.append('<text x="%d" y="%d" font-family="%s" font-size="12" fill="#868686">%s</text>'
             % (x + 30, y + 74, FONT, desc))
p.append('</svg>')

out = "\n".join(p)
io.open("mg-work/desc-fig.svg", "w", encoding="utf-8", newline="\n").write(out)
print("WROTE mg-work/desc-fig.svg  %d chars" % len(out))
