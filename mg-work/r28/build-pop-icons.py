# -*- coding: utf-8 -*-
"""生成 mg-work/pop-icons.json —— 对话框三个弹层用到的 5 个图标（第 28 轮第 4 项）。

来源：mg-work/r28/base-dumps/ 里从 pages/base.html 实际 DOM 抽出的三份弹层快照（原样落盘，未改）。
      base.html 是 Vite/React 单文件产物，路径是 MasterGo 导出的高精度浮点，
      这里统一 round 到 1 位小数（14/24 单位下的最大误差 0.05 ≈ 0.4%，肉眼不可见），
      体积从 ~8.7KB 压到 ~2.6KB。
产物：mg-work/pop-icons.json（由 mg-work/r21/build-detail.py 读入）
用法：python mg-work/r28/build-pop-icons.py   （在仓库根目录执行）
"""
import io
import json
import re


def load(name):
    s = io.open("mg-work/r28/base-dumps/%s" % name, encoding="utf-8").read()
    # dump 是 JSON 字符串形态，引号被转义过
    return s.replace('\\"', '"')


def shrink(d):
    def r(m):
        t = ("%.1f" % float(m.group(0))).rstrip("0").rstrip(".")
        return t if t not in ("-0", "") else "0"
    return re.sub(r"-?\d+\.\d+", r, d)


def paths(html):
    return [(shrink(d), extra.strip()) for d, extra in re.findall(r'<path d="([^"]+)"([^>]*)>', html)]


add = paths(load("add-menu.html"))
skl = paths(load("skills2.html"))

out = {
    # 「添加」菜单两项：14×14 fill #6B6B6B
    "add_file": add[0][0],          # 添加本地文件
    "add_kb": add[1][0],            # 知识库
    # 技能面板：Goal 行图标 14×14 fill #7766FD
    "skill_goal": skl[0][0],
    # 技能面板：普通技能行图标 12×12 fill #6B6B6B + transform matrix(-1,0,0,1,26,0)
    "skill_row": skl[2][0],
    # 技能面板：右上角关闭 X 12×12 fill #A9A9A9
    "skill_x": skl[1][0],
}
io.open("mg-work/pop-icons.json", "w", encoding="utf-8", newline="\n").write(
    json.dumps(out, ensure_ascii=False, indent=1))
print("WROTE mg-work/pop-icons.json  %d bytes" % sum(len(v) for v in out.values()))
for k, v in out.items():
    print("  %-11s %d chars" % (k, len(v)))
