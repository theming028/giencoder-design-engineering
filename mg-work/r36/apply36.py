# -*- coding: utf-8 -*-
"""第 36 轮 —— 组件级规范收敛：Card 头部浅灰底色。

用户口述：「`giencoder-card-header` 少了浅灰底色，请对比设计稿」。
设计稿（MasterGo 1345:18487，2x 导出逐像素实测）：
  · 卡头底色 = #F7F7F7 = `--color-fill-1`（y 309–378 平色带，计数 25808）
  · 卡头下分隔 = #F2F2F2 = `--color-border-1`
  · 卡本体底色 = #FFFFFF = `--color-bg-2`
→ 结论：底色属于 **Card 组件本体**，不该由各页适配层各自补，故在 DS 层收敛。

同时给 `.giencoder-card` 补 `overflow: hidden`：卡头底色是方块，卡体有圆角，
不裁切时浅灰会从圆角外溢出（DS 圆角 medium=4 / 页面 large=8 都会露角）。

⚠️ 页面是外部 Vite 的 `viteSingleFile` 产物，内联的 `components.css` 是**压缩版**
（属性顺序与 DS 源文件不同），故两处都要改：
  · DS 源：giencoder-design-system/components.css（美化版）
  · 9 个页面内联压缩版（逐字替换固定串）
幂等：检测到新串即跳过。

用法：C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe mg-work/r36/apply36.py
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DS = os.path.join(ROOT, "giencoder-design-system", "components.css")
PAGES = os.path.join(ROOT, "pages")

# ---------- (1) DS 源文件（美化版） ----------
DS_CARD_OLD = (".giencoder-card { background: var(--color-bg-2); border: 1px solid "
               "var(--color-border-2); border-radius: var(--border-radius-medium); }")
DS_CARD_NEW = (".giencoder-card { background: var(--color-bg-2); border: 1px solid "
               "var(--color-border-2); border-radius: var(--border-radius-medium); "
               "overflow: hidden; }")
DS_HDR_OLD = (".giencoder-card-header { display: flex; align-items: center; "
              "justify-content: space-between; padding: 8px 16px; "
              "border-bottom: 1px solid var(--color-border-1); }")
DS_HDR_NEW = (".giencoder-card-header { display: flex; align-items: center; "
              "justify-content: space-between; padding: 8px 16px; "
              "background: var(--color-fill-1); "
              "border-bottom: 1px solid var(--color-border-1); }")

# ---------- (2) 9 个页面内联的压缩版 ----------
MIN_CARD_OLD = (".giencoder-card{background:var(--color-bg-2);border:1px solid "
                "var(--color-border-2);border-radius:var(--border-radius-medium)}")
MIN_CARD_NEW = (".giencoder-card{background:var(--color-bg-2);border:1px solid "
                "var(--color-border-2);border-radius:var(--border-radius-medium);overflow:hidden}")
MIN_HDR_OLD = (".giencoder-card-header{border-bottom:1px solid var(--color-border-1);"
               "justify-content:space-between;align-items:center;padding:8px 16px;display:flex}")
MIN_HDR_NEW = (".giencoder-card-header{border-bottom:1px solid var(--color-border-1);"
               "justify-content:space-between;align-items:center;padding:8px 16px;display:flex;"
               "background:var(--color-fill-1)}")

# ---------- (3) 契约 ----------
JSON_OLD_TOKENS = '    "--color-text-1",\n    "--color-text-2"\n  ],'
JSON_NEW_TOKENS = '    "--color-text-1",\n    "--color-text-2",\n    "--color-fill-1"\n  ],'
JSON_OLD_STATE = '"visual": "背景 --color-bg-2，边框 --color-border-2"'
JSON_NEW_STATE = ('"visual": "背景 --color-bg-2，边框 --color-border-2；'
                  '头部底色 --color-fill-1（与卡体区分层级）"')


def patch(path, pairs, label):
    src = io.open(path, encoding="utf-8").read()
    acts = []
    for old, new in pairs:
        if new in src and old not in src:
            acts.append("skip")
            continue
        if src.count(old) != 1:
            raise SystemExit("!! %s 出现 %d 次（应为 1）：%s" % (label, src.count(old), old[:60]))
        src = src.replace(old, new)
        acts.append("done")
    io.open(path, "w", encoding="utf-8", newline="").write(src)
    print("  %-46s %s" % (label, ",".join(acts)))


print("=== 36-2 Card 头部浅灰底色（组件级） ===")
patch(DS, [(DS_CARD_OLD, DS_CARD_NEW), (DS_HDR_OLD, DS_HDR_NEW)],
      "giencoder-design-system/components.css")

names = sorted(n for n in os.listdir(PAGES) if n.endswith(".html"))
for n in names:
    patch(os.path.join(PAGES, n),
          [(MIN_CARD_OLD, MIN_CARD_NEW), (MIN_HDR_OLD, MIN_HDR_NEW)],
          "pages/" + n)

patch(os.path.join(ROOT, "giencoder-design-system", "components", "card.json"),
      [(JSON_OLD_TOKENS, JSON_NEW_TOKENS), (JSON_OLD_STATE, JSON_NEW_STATE)],
      "components/card.json")
print("完成。")
