# -*- coding: utf-8 -*-
import json, time, urllib.request
MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"

def call(name, args, timeout=120):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": name, "arguments": args}}).encode("utf-8")
    req = urllib.request.Request(MCP, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8")
    out = []
    for line in raw.splitlines():
        if line.startswith("data: "):
            d = json.loads(line[6:])
            for c in d.get("result", {}).get("content", []):
                out.append(c)
    return out

txt = "\n".join(c.get("text","") for c in call("get_frontend_code", {"projectDir": PROJ, "targetNodeId":"1345:18487"}, 60))
print("=== FULL ASK ===")
print(txt)
# 也把 tools/list 里的 schema 打出来（若支持）
body = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}).encode()
req = urllib.request.Request(MCP, data=body, headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
try:
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    for line in raw.splitlines():
        if line.startswith("data: "):
            d = json.loads(line[6:])
            for t in d.get("result", {}).get("tools", []):
                if t["name"] in ("get_frontend_code","get_selection_node","get_screenshot"):
                    print("\n=== %s schema ===" % t["name"])
                    print(json.dumps(t.get("inputSchema", {}), ensure_ascii=False)[:1500])
except Exception as e:
    print("tools/list err", e)
