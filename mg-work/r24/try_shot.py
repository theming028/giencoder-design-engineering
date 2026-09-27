# -*- coding: utf-8 -*-
"""只拉画板截图（带多次重试），用于核对边框色 / 行距。"""
import json
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"


def call(name, args, timeout=200):
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


for i in range(5):
    try:
        txt = call("get_screenshot", {"projectDir": PROJ, "targetNodeId": "622:13950", "scale": 2})
        print("attempt %d: %s" % (i + 1, txt[:300].replace("\n", " ")))
        if "❌" not in txt:
            open("mg-work/r24/shot.txt", "w", encoding="utf-8").write(txt)
            print("SAVED")
            break
    except Exception as e:
        print("attempt %d 异常: %s" % (i + 1, e))
    time.sleep(3)
