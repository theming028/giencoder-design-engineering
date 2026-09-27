# -*- coding: utf-8 -*-
"""拉取设计稿节点：先 get_selection_node（全量文本），再 get_screenshot（落盘 png）。
用法: python fetch.py <nodeId> <outPrefix> [scale]
"""
import base64
import json
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
NID = sys.argv[1] if len(sys.argv) > 1 else "1345:18366"
OUT = sys.argv[2] if len(sys.argv) > 2 else "mg-work/r31/design/dispatch"
SCALE = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0


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


def node_text():
    for i in range(8):
        try:
            content = call("get_selection_node", {"projectDir": PROJ, "targetNodeId": NID})
            txt = "\n".join(c.get("text", "") for c in content)
            if txt.strip() and "❌" not in txt:
                with open(OUT + ".txt", "w", encoding="utf-8") as f:
                    f.write(txt)
                print("SAVED %s.txt len=%d (attempt %d)" % (OUT, len(txt), i + 1), flush=True)
                return True
            print("FAIL txt attempt %d: %s" % (i + 1, txt[:200].replace("\n", " ")), flush=True)
        except Exception as e:
            print("ERR txt attempt %d: %s" % (i + 1, e), flush=True)
        time.sleep(3)
    return False


def shot():
    for i in range(8):
        try:
            content = call("get_screenshot", {"projectDir": PROJ, "targetNodeId": NID, "scale": SCALE})
            for c in content:
                if c.get("type") == "image" and c.get("data"):
                    with open(OUT + ".png", "wb") as f:
                        f.write(base64.b64decode(c["data"]))
                    print("SAVED %s.png (attempt %d)" % (OUT, i + 1), flush=True)
                    return True
                print("FAIL img attempt %d: %s" % (i + 1, (c.get("text") or "")[:200]), flush=True)
        except Exception as e:
            print("ERR img attempt %d: %s" % (i + 1, e), flush=True)
        time.sleep(3)
    return False


ok1 = node_text()
ok2 = shot()
print("DONE txt=%s img=%s" % (ok1, ok2), flush=True)
