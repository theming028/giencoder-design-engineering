# -*- coding: utf-8 -*-
"""探测设计稿画板结构：拉取指定节点的权威数据（名称 / 尺寸 / 子节点 / 填充色）。"""
import json
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
TARGETS = sys.argv[1:] or ["553:06620"]


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
    return "\n".join(out)


for nid in TARGETS:
    got = False
    for i in range(5):
        try:
            txt = call("get_selection_node", {"projectDir": PROJ, "targetNodeId": nid})
            if txt.strip() and "❌" not in txt:
                print("=" * 24, nid, "(attempt %d, len=%d)" % (i + 1, len(txt)), "=" * 24)
                print(txt[:6000])
                got = True
                break
            print("FAIL %s attempt %d: %s" % (nid, i + 1, txt[:200].replace("\n", " ")))
        except Exception as e:
            print("ERR %s attempt %d: %s" % (nid, i + 1, e))
        time.sleep(3)
    if not got:
        print("=" * 24, nid, "FAILED", "=" * 24)
print("DONE")
