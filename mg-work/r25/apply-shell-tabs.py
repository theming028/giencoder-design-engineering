# -*- coding: utf-8 -*-
"""把公共片段 mg-work/shell-tabs.snippet.html 注入所有页面（幂等 + 可升级）。

背景：外壳源码不在本仓库（由外部 Vite 工程 build.sh 构建成 viteSingleFile 产物），
     顶栏页签的导航逻辑只存在于各页内联 bundle 里，因此只能在产物上打补丁。

幂等/可升级：页面里已有 `<!-- SHELL-TABS-FIX ... -->` … `<!-- /SHELL-TABS-FIX -->` 区块时
     整块替换为新片段（片段版本升级后直接重跑本脚本即可）；没有则在 `</body>` 前插入。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SNIP = os.path.join(ROOT, "mg-work", "shell-tabs.snippet.html")
PAGES = os.path.join(ROOT, "pages")
START = "<!-- SHELL-TABS-FIX"
END = "<!-- /SHELL-TABS-FIX -->"

snip = io.open(SNIP, encoding="utf-8").read().rstrip("\n")


def patch(name):
    path = os.path.join(PAGES, name)
    s = io.open(path, encoding="utf-8").read()
    a = s.find(START)
    if a >= 0:
        b = s.find(END, a)
        if b < 0:
            return "FAIL  (open marker without close)"
        b += len(END)
        new = s[:a] + snip + s[b:]
        if new == s:
            return "SKIP  (already latest)"
        io.open(path, "w", encoding="utf-8", newline="").write(new)
        return "REPLACED  %+d chars" % (len(new) - len(s))
    idx = s.rfind("</body>")
    if idx < 0:
        return "FAIL  (no </body>)"
    new = s[:idx] + "  " + snip + "\n" + s[idx:]
    io.open(path, "w", encoding="utf-8", newline="").write(new)
    return "PATCHED  %+d chars" % (len(new) - len(s))


def main():
    for n in sorted(x for x in os.listdir(PAGES) if x.endswith(".html")):
        print("%-22s %s" % (n, patch(n)))


if __name__ == "__main__":
    main()
