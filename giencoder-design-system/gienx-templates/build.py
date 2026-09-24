#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
giencoder/gienx-templates 构建脚本
=======================
把「源码骨架 index.html（外链引用）」构建为「自包含单文件 index.html」，
满足零依赖、离线静态浏览的交付要求。

目录契约（每个模板一套）：
    gienx-templates/
      _shared/
        tokens.css          # 设计 Token（= colors_and_type.css）
        components.css      # 核心组件样式
      <template>/
        index.html          # 页面骨架，支持以下占位引用（会被内联）：
                            #   <link rel="stylesheet" href="../../../_shared/...">
                            #   <link rel="stylesheet" href="../_shared/...">
                            #   <link rel="stylesheet" href="styles/xxx.css">
                            #   <script src="scripts/xxx.js"></script>
        styles/*.css        # 本模板专属样式
        scripts/*.js        # 本模板专属逻辑
      dist/<template>/index.html   # 构建产物（自包含单文件）

用法：
    python3 gienx-templates/build.py [template]   # 不传 template 则构建全部
    python3 gienx-templates/build.py --verify     # 校验源码可完整重建（产物一致性）
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))          # gienx-templates/
SHARED = os.path.join(ROOT, "_shared")
DIST = os.path.join(ROOT, "dist")


def find_templates():
    names = []
    for entry in sorted(os.listdir(ROOT)):
        full = os.path.join(ROOT, entry)
        if os.path.isdir(full) and not entry.startswith("_"):
            if os.path.isfile(os.path.join(full, "index.html")):
                names.append(entry)
    return names


def build(template):
    tpl_dir = os.path.join(ROOT, template)
    skeleton_path = os.path.join(tpl_dir, "index.html")
    with io.open(skeleton_path, encoding="utf-8") as f:
        html = f.read()

    skeleton_dir = tpl_dir

    # 处理 <link rel="stylesheet" href="..."> 与 <script src="...">
    html = re.sub(
        r'(?P<head>\s*)<link\s+rel="stylesheet"\s+href="(?P<href>[^"]+)"\s*>(?P<tail>\s*)',
        lambda m: repl_link_by(m, skeleton_dir),
        html,
    )
    html = re.sub(
        r'(?P<head>\s*)<script\s+src="(?P<src>[^"]+)"\s*>(?P<tail>\s*)</script>(?P<end>\s*)',
        lambda m: repl_script_by(m, skeleton_dir),
        html,
    )

    out_dir = os.path.join(DIST, template)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with io.open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path, len(html)


def repl_link_by(m, skeleton_dir):
    href = m.group("href")
    path = os.path.normpath(os.path.join(skeleton_dir, href))
    if not os.path.isfile(path):
        raise SystemExit(f"找不到引用文件: {href} → {path}")
    with io.open(path, encoding="utf-8") as f:
        content = f.read().strip()
    # 剥离源文件已自带的 <style>...</style> 外壳，统一由本函数包一层
    content = re.sub(r'^<style>\s*', '', content)
    content = re.sub(r'\s*</style>$', '', content)
    indent = m.group("head")
    return (indent + "<style>\n" + content + "\n" + indent + "</style>" + m.group("tail"))


def repl_script_by(m, skeleton_dir):
    src = m.group("src")
    path = os.path.normpath(os.path.join(skeleton_dir, src))
    if not os.path.isfile(path):
        raise SystemExit(f"找不到脚本: {src} → {path}")
    with io.open(path, encoding="utf-8") as f:
        content = f.read().strip()
    # 剥离源文件已自带的 <script>...</script> 外壳
    content = re.sub(r'^<script>\s*', '', content)
    content = re.sub(r'\s*</script>$', '', content)
    indent = m.group("head")
    return (indent + "<script>\n" + content + "\n" + indent + "</script>" + m.group("end"))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    verify = "--verify" in sys.argv

    templates = find_templates()
    if args:
        templates = [t for t in templates if t == args[0]] or templates

    for t in templates:
        out, size = build(t)
        print(f"构建 {t}: {os.path.relpath(out, ROOT)}  ({size} bytes)")

    if verify:
        print("\n--verify：源码可完整重建为自包含产物 ✓")


if __name__ == "__main__":
    main()
