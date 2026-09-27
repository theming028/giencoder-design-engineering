# -*- coding: utf-8 -*-
"""从 pages/task-detail.html（已构建产物，模块内占位符都已填好）抽「AI 对话栏」模块：

  · CSS  —— 页面 <style> 里的顶层规则，选择器命中白名单前缀的整条取出
  · HTML —— KB_HTML（JS 字符串数组）里的 `<aside class="td-right" …>` … `</aside>`
  · JS   —— bindDetail() 里对话框三段弹层的绑定（add / skill / select）

产物：mg-work/r34/composer-module.{css,html,js}（供 build-avatar.py 内联）
用法：python pre-extract-composer.py
"""
import io
import json
import re

SRC = "pages/task-detail.html"
OUT = "mg-work/r34/composer-module"

# 组成 AI 对话栏所需的类名前缀（视图适配层，复用详情页同名类，不改名）
PREFIXES = (
    ".td-right", ".td-chat", ".td-msg-", ".td-ai-", ".td-composer",
    ".td-add-", ".td-skill", ".td-round-btn", ".td-sep", ".td-ico-",
)

s = io.open(SRC, encoding="utf-8").read()


# ---------------- CSS：顶层规则切分 ----------------
def top_rules(css):
    """按「花括号配平」切出顶层规则文本列表（含 @media 整块）。"""
    out, buf, depth, i = [], [], 0, 0
    while i < len(css):
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            if j < 0:
                buf.append(css[i:])
                break
            buf.append(css[i:j + 2])
            i = j + 2
            continue
        c = css[i]
        buf.append(c)
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append("".join(buf).strip())
                buf = []
        i += 1
    if "".join(buf).strip():
        out.append("".join(buf).strip())
    return out


styles = re.findall(r"<style[^>]*>(.*?)</style>", s, re.S)
page_css = [x for x in styles if ".td-right" in x]
assert len(page_css) == 1, "页面 CSS 段定位异常：%d 个" % len(page_css)
page_css = page_css[0]

keep, seen = [], set()
for r in top_rules(page_css):
    if r.startswith("@media"):
        continue                      # 全屏态等 @media 规则本模块用不到
    if any(p in r.split("{")[0] for p in PREFIXES):
        if r in seen:
            continue
        seen.add(r)
        keep.append(r)
css_out = "\n".join(keep)

# ---------------- HTML：从 KB_HTML 的 JSON 行里取 aside ----------------
opener = '"  <aside class=\\"td-right\\" aria-label=\\"AI 会话\\">",'
start = s.find(opener)
assert start > 0, "找不到 AI 会话 aside"
m_end = re.compile(r'</aside>",\n').search(s, start)
assert m_end, "找不到 aside 的收尾"
block = s[start:m_end.end() - 2]          # 去掉行尾的  ",

lines = []
for ln in block.split("\n"):
    t = ln.strip()
    if t.endswith(","):
        t = t[:-1]
    if t.startswith('"') and t.endswith('"'):
        lines.append(json.loads(t))       # 还原 \\" → "
    else:
        lines.append(t)
html_out = "\n".join(lines)

# ---------------- JS：对话框三弹层绑定 ----------------
JS_A = "/* ================= 对话框三个弹层"
JS_B = "var gutter = wrap.querySelector('[data-td-gutter]')"
# ⚠️ JS_A 在页面 CSS 里也有一条同文案注释（占位说明），必须从 bindDetail 之后开始找
_anchor = s.find("function bindDetail(")
assert _anchor > 0, "找不到 bindDetail"
js_start = s.find(JS_A, _anchor)
assert js_start > 0, "找不到对话框三弹层绑定段"
js_end = s.find(JS_B, js_start)
assert js_end > js_start, "找不到绑定段结尾"
js_out = s[js_start:js_end].rstrip()
assert len(js_out) < 6000, "绑定段长度异常：%d" % len(js_out)

io.open(OUT + ".css", "w", encoding="utf-8").write(css_out)
io.open(OUT + ".html", "w", encoding="utf-8").write(html_out)
io.open(OUT + ".js", "w", encoding="utf-8").write(js_out)

print("CSS 规则 %d 条 / %d chars" % (len(keep), len(css_out)))
print("HTML %d chars / %d 行" % (len(html_out), len(lines)))
print("JS   %d chars" % len(js_out))
print("含骨架占位符？", "__" in html_out and [x for x in re.findall(r"__[A-Z]+__", html_out)])
