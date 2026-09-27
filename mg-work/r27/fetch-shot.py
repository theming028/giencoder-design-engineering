# -*- coding: utf-8 -*-
"""拉取设计稿节点截图（get_screenshot），把 base64 落盘为 png。"""
import base64
import json
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
NID = sys.argv[1] if len(sys.argv) > 1 else "553:06620"
OUT = sys.argv[2] if len(sys.argv) > 2 else "mg-work/r27/design-board.png"
SCALE = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0


def call(name, args, timeout=300):
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


last = None
for i in range(6):
    try:
        content = call("get_screenshot", {"projectDir": PROJ, "targetNodeId": NID, "scale": SCALE})
        for c in content:
            t = c.get("type")
            if t == "image" and c.get("data"):
                raw = base64.b64decode(c["data"])
                with open(OUT, "wb") as f:
                    f.write(raw)
                print("SAVED %s bytes=%d (attempt %d)" % (OUT, len(raw), i + 1))
                raise SystemExit(0)
            if t == "text":
                last = c.get("text", "")
                print("TEXT[%d]: %s" % (i + 1, last[:300].replace("\n", " ")))
        time.sleep(3)
    except SystemExit:
        raise
    except Exception as e:
        print("ERR attempt %d: %s" % (i + 1, e))
    time.sleep(3)
print("FAILED last=%s" % (last or "")[:400])
