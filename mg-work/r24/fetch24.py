# -*- coding: utf-8 -*-
"""第24轮：从 MasterGo 画布桥拉取详情页画板（结构 + 截图）。"""
import json
import sys
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"


def call(name, args, timeout=240):
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": name, "arguments": args},
    }).encode("utf-8")
    req = urllib.request.Request(MCP, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8")
    out = []
    for line in raw.splitlines():
        if line.startswith("data: "):
            d = json.loads(line[6:])
            for c in d.get("result", {}).get("content", []):
                out.append(c.get("text", ""))
            if "error" in d:
                out.append("ERROR: " + json.dumps(d["error"], ensure_ascii=False))
    return "\n".join(out)


JOBS = [
    ("mg-work/r24/board.txt", "get_selection_node",
     {"projectDir": PROJ, "targetNodeId": "622:13950"}),
    ("mg-work/r24/board-shot.txt", "get_screenshot",
     {"projectDir": PROJ, "targetNodeId": "622:13950", "scale": 2}),
    ("mg-work/r24/collapse2.txt", "get_selection_node",
     {"projectDir": PROJ, "targetNodeId": "1343:18532"}),
]

for path, tool, args in JOBS:
    try:
        txt = call(tool, args)
        open(path, "w", encoding="utf-8").write(txt)
        print("OK  %-28s %-20s len=%d" % (path, tool, len(txt)))
        print("    head: " + txt[:220].replace("\n", " "))
    except Exception as e:
        print("FAIL %-28s %s: %s" % (path, tool, e))
