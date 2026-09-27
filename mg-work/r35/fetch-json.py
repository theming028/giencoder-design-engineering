# -*- coding: utf-8 -*-
"""导出设计稿 JSON（含文案）。用法: python fetch-json.py <nodeId> <outPrefix>"""
import json
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
NID = sys.argv[1]
OUT = sys.argv[2]


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


for i in range(10):
    try:
        content = call("get_frontend_code", {
            "projectDir": PROJ, "targetNodeId": NID,
            "frontendFramework": "json", "writeToFile": False,
        })
        txt = "\n".join((c.get("text") or "") for c in content)
        if txt.strip() and "❌" not in txt[:200] and len(txt) > 500:
            with open(OUT, "w", encoding="utf-8") as f:
                f.write(txt)
            print("SAVED %s len=%d (attempt %d)" % (OUT, len(txt), i + 1), flush=True)
            break
        print("FAIL attempt %d: %s" % (i + 1, txt[:200].replace("\n", " ")), flush=True)
    except Exception as e:
        print("ERR attempt %d: %s" % (i + 1, e), flush=True)
    time.sleep(4)
