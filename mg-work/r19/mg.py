# -*- coding: utf-8 -*-
"""读 MasterGo 节点：把 get_selection_node / get_screenshot 的返回落盘，避免 shell 截断。"""
import json
import sys
import urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"


def call(name, args, timeout=60):
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


if __name__ == "__main__":
    name = sys.argv[1]
    args = json.loads(sys.argv[2])
    print(call(name, args))
