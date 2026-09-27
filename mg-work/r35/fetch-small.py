# -*- coding: utf-8 -*-
"""逐个小节点截图（小节点快、且能直接读出文案）。
用法: python fetch-small.py <outDir> "1345:18473|rowA" "1345:18478|rowB" ...
每个节点独立重试；成功的立即落盘，失败的继续下一个（可重复运行补漏，已存在的跳过）。
"""
import base64
import json
import os
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
OUTDIR = sys.argv[1]
JOBS = [a.split("|", 1) for a in sys.argv[2:]]


def call(name, args, timeout=150):
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
                out.append(c)
    return out


os.makedirs(OUTDIR, exist_ok=True)
for nid, name in JOBS:
    dst = os.path.join(OUTDIR, name + ".png")
    if os.path.exists(dst):
        print("SKIP %s (exists)" % name, flush=True)
        continue
    ok = False
    for i in range(3):
        try:
            content = call("get_screenshot", {"projectDir": PROJ, "targetNodeId": nid, "scale": 2})
            for c in content:
                if c.get("type") == "image" and c.get("data"):
                    with open(dst, "wb") as f:
                        f.write(base64.b64decode(c["data"]))
                    print("SAVED %s <- %s bytes=%d" % (name, nid, len(c["data"])), flush=True)
                    ok = True
                    break
                print("FAIL %s attempt %d: %s" % (name, i + 1, (c.get("text") or "")[:140]), flush=True)
        except Exception as e:
            print("ERR %s attempt %d: %s" % (name, i + 1, e), flush=True)
        if ok:
            break
        time.sleep(5)
print("DONE", flush=True)
