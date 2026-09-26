# -*- coding: utf-8 -*-
"""带重试地读取 MasterGo 当前选中节点，落盘到文件。"""
import json
import os
import sys
import time
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"


def call(name, args, timeout=110):
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


if __name__ == "__main__":
    out_path = sys.argv[1]
    tool = sys.argv[2]
    args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {"projectDir": PROJ}
    attempts = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    for i in range(attempts):
        try:
            txt = call(tool, args)
            if txt and "❌" not in txt[:40] and len(txt) > 200:
                open(out_path, "w", encoding="utf-8").write(txt)
                print("OK attempt %d, len=%d -> %s" % (i + 1, len(txt), out_path))
                sys.exit(0)
            print("attempt %d 返回异常: %s" % (i + 1, txt[:120]))
        except Exception as e:
            print("attempt %d 异常: %s" % (i + 1, e))
        time.sleep(2)
    print("ALL_FAILED")
    sys.exit(1)
