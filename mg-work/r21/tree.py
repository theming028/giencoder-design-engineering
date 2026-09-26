# -*- coding: utf-8 -*-
"""把 MasterGo 节点代码文本转成精简结构树：name + 关键几何 + 文本。"""
import re
import sys

KEY = ("width", "height", "left", "top", "background", "border-radius",
       "font-size", "color", "font-weight", "border-color", "border-width",
       "gap", "padding", "position", "border-style")


def parse(path):
    raw = open(path, encoding="utf-8").read()
    i = raw.find("代码内容：")
    body = raw[i:] if i >= 0 else raw
    lines = body.split("\n")
    out = []
    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            continue
        indent = (len(s) - len(s.lstrip(" "))) // 2
        st = s.strip()
        # 元素开始
        m = re.match(r'<(div|span|ui-component|img|button|p)\b', st)
        if m:
            out.append((indent, "OPEN", st))
        elif st.startswith("data-name="):
            out[-1] = (out[-1][0], out[-1][1], out[-1][2] + " " + st) if out else None
        elif st.startswith("style="):
            if out:
                out[-1] = (out[-1][0], out[-1][1], out[-1][2] + " || " + st)
        elif st.startswith("text="):
            if out:
                out[-1] = (out[-1][0], out[-1][1], out[-1][2] + " ## " + st)
        elif st.startswith("props="):
            if out:
                out[-1] = (out[-1][0], out[-1][1], out[-1][2] + " $$ " + st)
        elif st.startswith("data-node-id="):
            if out:
                out[-1] = (out[-1][0], out[-1][1], out[-1][2] + " @" + st.split('"')[1])
        elif st in ("</div>", "</span>", "</ui-component>", "</button>", "</p>"):
            out.append((indent, "CLOSE", ""))
        elif re.match(r'^[^<>=]*$', st) and len(st) < 40:
            # 纯文本内容
            if out:
                out[-1] = (out[-1][0], out[-1][1], out[-1][2] + " ~~ " + st)
    return out


def brief(st):
    """只保留关键 style 与 name。"""
    nid = ""
    m = re.search(r'@(\S+)$', st)
    name = ""
    m2 = re.search(r'data-name="([^"]*)"', st)
    if m2:
        name = m2.group(1)
    sty = ""
    m3 = re.search(r'style="([^"]*)"', st)
    if m3:
        parts = []
        for kv in m3.group(1).split(";"):
            kv = kv.strip()
            if any(kv.startswith(k + ":") for k in KEY):
                parts.append(kv)
        sty = " ".join(parts)
    txt = ""
    m4 = re.search(r'text=\'([^\']*)\'', st)
    if m4:
        txt = " TEXT=" + m4.group(1)
    m5 = re.search(r'props=\'([^\']*)\'', st)
    if m5:
        txt += " PROPS=" + m5.group(1)
    return "%s [%s] %s%s" % (name, nid, sty[:170], txt[:120])


if __name__ == "__main__":
    path = sys.argv[1]
    nodes = parse(path)
    cur = []
    for indent, kind, st in nodes:
        if kind == "CLOSE":
            if cur:
                cur.pop()
            continue
        line = "  " * indent + brief(st)
        print(line)
        cur.append(indent)
