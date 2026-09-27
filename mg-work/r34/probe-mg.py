# -*- coding: utf-8 -*-
"""单发探测 MasterGo MCP：先 version(短超时)，再对目标节点各发一次 get_selection_node(90s)。"""
import json, sys, time, urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"

def call(name, args, timeout=90):
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

def one(name, args, timeout=90):
    t = time.time()
    try:
        content = call(name, args, timeout)
        txt = "\n".join(c.get("text", "") for c in content)
        imgs = [c for c in content if c.get("type") == "image"]
        return {"ok": True, "sec": round(time.time() - t, 1), "len": len(txt),
                "imgs": len(imgs), "head": txt[:180].replace("\n", " ")}
    except Exception as e:
        return {"ok": False, "sec": round(time.time() - t, 1), "err": "%s: %s" % (type(e).__name__, e)}

rep = {}
rep["version"] = one("get_version", {}, 30)
rep["page_263_05935"] = one("get_selection_node", {"projectDir": PROJ, "targetNodeId": "263:05935"}, 90)
rep["main_1345_18487"] = one("get_selection_node", {"projectDir": PROJ, "targetNodeId": "1345:18487"}, 90)
rep["chat_1345_18502"] = one("get_selection_node", {"projectDir": PROJ, "targetNodeId": "1345:18502"}, 90)
print(json.dumps(rep, ensure_ascii=False, indent=1))
