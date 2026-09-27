# -*- coding: utf-8 -*-
"""拉取左栏 / 右栏 / 折叠态 三个设计稿节点的权威数据（含描边色、投影、圆角）。"""
import json
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
TARGETS = ["1343:18534", "1343:18535", "1343:18532", "1343:18530"]


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


buf = []
for nid in TARGETS:
    for i in range(6):
        try:
            txt = call("get_selection_node", {"projectDir": PROJ, "targetNodeId": nid})
            if "❌" not in txt and txt.strip():
                buf.append("=" * 30 + " " + nid + " " + "=" * 30)
                buf.append(txt)
                print("OK %s (attempt %d) len=%d" % (nid, i + 1, len(txt)))
                break
            print("FAIL %s attempt %d: %s" % (nid, i + 1, txt[:160].replace("\n", " ")))
        except Exception as e:
            print("ERR %s attempt %d: %s" % (nid, i + 1, e))
        time.sleep(3)
    else:
        buf.append("=" * 30 + " " + nid + " (FAILED) " + "=" * 30)

open("mg-work/r24/nodes.txt", "w", encoding="utf-8").write("\n".join(buf))
print("DONE len=%d" % sum(len(b) for b in buf))
