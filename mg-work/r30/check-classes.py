# -*- coding: utf-8 -*-
"""契约类名自检：抽取页面 HTML 里用到的全部 `giencoder-*` 类名，
与「DS 已定义」集合取差集 —— 差集必须为空（不允许自造同义类名）。

「已定义」= 
  1) giencoder-design-system/components.css 里的选择器类名
  2) giencoder-design-system/gienx-templates/*.css 里的选择器类名
  3) giencoder-design-system/components/*.json 的 anatomy[].element 声明里的类名

用法: python check-classes.py [page.html ...]
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DS = os.path.join(ROOT, "giencoder-design-system")

PAGES = sys.argv[1:] or [os.path.join(ROOT, "pages", p)
                        for p in ("task-detail.html", "avatar.html")]

CLASS_RE = re.compile(r'class=\\?"([^"\\]+)\\?"')
GNC_RE = re.compile(r"\bgiencoder-[A-Za-z0-9_-]+")
SEL_RE = re.compile(r"\.(giencoder-[A-Za-z0-9_-]+)")


def css_files():
    out = []
    for dirpath, _dirs, files in os.walk(DS):
        if "preview" in dirpath.split(os.sep):
            continue          # preview/ 是演示页，不作为「已定义」来源
        for f in files:
            if f.endswith(".css"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


defined = {}

for p in css_files():
    txt = io.open(p, encoding="utf-8").read()
    # 只取选择器段落里的类名（去掉 /* */ 注释，避免注释里提到的类名被当作已定义）
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    for m in SEL_RE.finditer(txt):
        defined.setdefault(m.group(1), []).append(os.path.relpath(p, ROOT))

comp_dir = os.path.join(DS, "components")
for f in sorted(os.listdir(comp_dir)):
    if not f.endswith(".json"):
        continue
    try:
        d = json.load(io.open(os.path.join(comp_dir, f), encoding="utf-8"))
    except Exception:
        continue
    for part in d.get("anatomy", []) or []:
        for cls in GNC_RE.findall(json.dumps(part, ensure_ascii=False)):
            defined.setdefault(cls, []).append("components/%s (anatomy)" % f)

fail = 0
for page in PAGES:
    txt = io.open(page, encoding="utf-8").read()
    used = set()
    for m in CLASS_RE.finditer(txt):
        for cls in m.group(1).split():
            if cls.startswith("giencoder-"):
                used.add(cls)
    missing = sorted(c for c in used if c not in defined)
    print("=" * 96)
    print("PAGE %s" % os.path.relpath(page, ROOT))
    print("  页面用到 giencoder-* 类名: %d 个" % len(used))
    print("  DS 已定义(含契约 anatomy): %d 个" % len(defined))
    if missing:
        fail += len(missing)
        print("  !! 契约未定义的类名 %d 个:" % len(missing))
        for c in missing:
            print("     - %s" % c)
    else:
        print("  虚构类名差集: NONE  → OK")
    # 额外提示：DS 定义了但页面没用的，只在 verbose 下输出
    if os.environ.get("VERBOSE"):
        unused = sorted(c for c in defined if c.startswith("giencoder-image") and c not in used)
        print("  (参考) DS 里 Image 相关但本页未用: %s" % ", ".join(unused))

print("=" * 96)
print("RESULT: %s" % ("ALL_OK" if fail == 0 else "HAS_FAIL(%d)" % fail))
sys.exit(0 if fail == 0 else 1)
