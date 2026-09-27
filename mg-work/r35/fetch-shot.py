# -*- coding: utf-8 -*-
"""只补抓截图（txt 已有）。用法: python fetch-shot.py <nodeId> <outPrefix> [scale]"""
import base64
import json
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
NID = sys.argv[1]
OUT = sys.argv[2]
SCALE = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5


def call(name, args, timeout=280):
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


for i in range(12):
    try:
        content = call("get_screenshot", {"projectDir": PROJ, "targetNodeId": NID, "scale": SCALE})
        got = False
        for c in content:
            if c.get("type") == "image" and c.get("data"):
                with open(OUT + ".png", "wb") as f:
                    f.write(base64.b64decode(c["data"]))
                print("SAVED %s.png bytes=%d (attempt %d)" % (OUT, len(c["data"]), i + 1), flush=True)
                got = True
                break
            print("FAIL img attempt %d: %s" % (i + 1, (c.get("text") or "")[:180]), flush=True)
        if got:
            break
    except Exception as e:
        print("ERR img attempt %d: %s" % (i + 1, e), flush=True)
    time.sleep(4)
