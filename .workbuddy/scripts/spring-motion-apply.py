#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全局显示/隐藏动效 → 弹性 spring（对齐 FF Motion）
规则：进入（展开/打开）用 spring 曲线 var(--transition-timing-function-spring)，
     opacity 保持 standard（透明度无过冲概念），退出方向保持 standard 且快一档。
    dry-run: python3 spring-motion-apply.py --dry
    apply:   python3 spring-motion-apply.py
"""
import sys, pathlib

ROOTS = [
    pathlib.Path("/Users/shaoyuming/Documents/Nutstore/我的坚果云/YuanqiDesignSystem/yuanqi"),
    pathlib.Path("/Users/shaoyuming/Documents/Nutstore/我的坚果云/YuanqiDesignSystem/yuanqi-delivery"),
]

SPRING = "var(--transition-timing-function-spring)"
STANDARD = "var(--transition-timing-function-standard)"

# 文件级规则：(文件名, [(old, new, 说明), ...])
RULES = {
    "component-select.html": [
        ("translate .2s cubic-bezier(0.34, 0.69, 0.1, 1), scale .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"translate .2s {SPRING}, scale .2s {SPRING}", "弹层展开 translate/scale → spring"),
    ],
    "component-dropdown.html": [
        ("translate .2s cubic-bezier(0.34, 0.69, 0.1, 1), scale .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"translate .2s {SPRING}, scale .2s {SPRING}", "弹层展开 translate/scale → spring"),
    ],
    "component-tooltip.html": [
        ("translate .2s cubic-bezier(0.34, 0.69, 0.1, 1), scale .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"translate .2s {SPRING}, scale .2s {SPRING}", "弹层展开 translate/scale → spring"),
    ],
    "component-popover.html": [
        ("translate .2s cubic-bezier(0.34, 0.69, 0.1, 1), scale .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"translate .2s {SPRING}, scale .2s {SPRING}", "弹层展开 translate/scale → spring"),
    ],
    "component-popconfirm.html": [
        ("translate .2s cubic-bezier(0.34, 0.69, 0.1, 1), scale .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"translate .2s {SPRING}, scale .2s {SPRING}", "弹层展开 translate/scale → spring"),
    ],
    "component-trigger.html": [
        ("translate .2s cubic-bezier(0.34, 0.69, 0.1, 1), scale .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"translate .2s {SPRING}, scale .2s {SPRING}", "弹层展开 translate/scale → spring"),
    ],
    "component-cascader.html": [
        ("transform .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"transform .2s {SPRING}", "弹层展开 transform → spring"),
    ],
    "component-auto-complete.html": [
        ("transform .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"transform .2s {SPRING}", "弹层展开 transform → spring"),
    ],
    "component-mentions.html": [
        ("transform .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"transform .2s {SPRING}", "弹层展开 transform → spring"),
    ],
    "component-tree-select.html": [
        ("transform .2s cubic-bezier(0.34, 0.69, 0.1, 1)",
         f"transform .2s {SPRING}", "弹层展开 transform → spring"),
    ],
    "component-color-picker.html": [
        ("transform var(--transition-duration-2) var(--transition-timing-function-standard)",
         f"transform var(--transition-duration-2) {SPRING}", "弹层展开 transform → spring"),
    ],
    "component-date-picker.html": [
        ("transform var(--transition-duration-2) var(--transition-timing-function-standard)",
         f"transform var(--transition-duration-2) {SPRING}", "弹层展开 transform → spring"),
    ],
    "component-menu.html": [
        ("transform var(--transition-duration-2) var(--transition-timing-function-standard)",
         f"transform var(--transition-duration-2) {SPRING}", "子菜单展开 transform → spring"),
    ],
    "component-modal.html": [
        ("transition: transform var(--transition-duration-3) var(--transition-timing-function-standard);",
         f"transition: transform var(--transition-duration-3) {SPRING};", "modal 打开 scale → spring（关闭态 duration-2 保持 standard）"),
    ],
    "component-drawer.html": [
        ("transition: transform var(--transition-duration-3) var(--transition-timing-function-standard);",
         f"transition: transform var(--transition-duration-3) {SPRING};", "drawer 打开 transform → spring"),
        (".yuanqi-drawer-mask-motion-hide { opacity: 0; }",
         ".yuanqi-drawer-mask-motion-hide { opacity: 0; transition-duration: var(--transition-duration-2); }",
         "drawer 关闭 0.3s→0.2s 快一档"),
    ],
    "component-collapse.html": [
        ("max-height 0.2s var(--transition-timing-function-standard)",
         f"max-height 0.2s {SPRING}", "collapse 展开 max-height → spring"),
    ],
    "component-message.html": [
        (".pv-message-enter { animation: pv-message-in 0.25s var(--transition-timing-function-standard); }",
         f".pv-message-enter {{ animation: pv-message-in 0.25s {SPRING}; }}", "message 进入动画 → spring"),
    ],
    "component-notification.html": [
        ("transition: opacity var(--transition-duration-3) var(--transition-timing-function-standard),\n                  transform var(--transition-duration-3) var(--transition-timing-function-standard);",
         f"transition: opacity var(--transition-duration-3) {STANDARD},\n                  transform var(--transition-duration-3) {SPRING};",
         "notification 进入 transform → spring（opacity 保持）"),
    ],
    "component-image.html": [
        (".pv-img-anim-in { animation: pv-img-in 0.3s var(--transition-timing-function-standard) both; }",
         f".pv-img-anim-in {{ animation: pv-img-in 0.3s {SPRING} both; }}", "image 预览打开 scale → spring"),
    ],
    "component-checkbox.html": [
        ("animation: yuanqi-checkbox-check-pop 0.15s var(--transition-timing-function-standard);",
         f"animation: yuanqi-checkbox-check-pop 0.15s {SPRING};", "checkbox 勾选 pop → spring"),
    ],
    "component-alert.html": [
        ("transition: opacity 0.2s var(--transition-timing-function-standard),\n                  max-height 0.2s var(--transition-timing-function-standard),",
         "transition: opacity 0.2s var(--transition-timing-function-standard),\n                  max-height 0.2s var(--transition-timing-function-spring),",
         "alert 收起 max-height → spring"),
    ],
}

def process(root, dry):
    hits = 0
    for fname, rules in sorted(RULES.items()):
        p = root / "preview" / fname
        if not p.exists():
            print(f"  [SKIP] {p.relative_to(root)} 不存在")
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        for old, new, desc in rules:
            if old not in text:
                print(f"  [WARN] {fname}: 未找到 → {desc}")
                continue
            text = text.replace(old, new)
            hits += 1
        if text != orig:
            if not dry:
                p.write_text(text, encoding="utf-8")
            print(f"  [{'DRY' if dry else 'OK '}] {p.relative_to(root)}")
    return hits

def main():
    dry = "--dry" in sys.argv
    mode = "DRY-RUN" if dry else "APPLY"
    print(f"== {mode} ==")
    total = 0
    for root in ROOTS:
        print(f"== {root.name} ==")
        total += process(root, dry)
    print(f"total replacements: {total}")
    if dry:
        print("dry-run 完成；确认无误后去掉 --dry 执行。")

if __name__ == "__main__":
    main()
