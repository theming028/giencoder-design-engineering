# -*- coding: utf-8 -*-
"""拉取设计稿画板的完整节点代码（get_frontend_code 更省，get_selection_node 全量文本）。"""
import json
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
NID = sys.argv[1] if len(sys.argv) > 1 else "553:06620"
OUT = sys.argv[2] if len(sys.argv) > 2 else "mg-work/r27/design-full.txt"


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
                out.append(c.get("text", ""))
    return "\n".join(out)


for i in range(8):
    try:
        txt = call("get_selection_node", {"projectDir": PROJ, "targetNodeId": NID})
        if txt.strip() and "❌" not in txt:
            with open(OUT, "w", encoding="utf-8") as f:
                f.write(txt)
            print("SAVED %s len=%d (attempt %d)" % (OUT, len(txt), i + 1))
            raise SystemExit(0)
        print("FAIL attempt %d: %s" % (i + 1, txt[:180].replace("\n", " ")), flush=True)
    except SystemExit:
        raise
    except Exception as e:
        print("ERR attempt %d: %s" % (i + 1, e), flush=True)
    time.sleep(2)
print("FAILED")
