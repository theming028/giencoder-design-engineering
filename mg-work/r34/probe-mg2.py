# -*- coding: utf-8 -*-
"""诊断：逐个试触及文档的 MCP 工具，看是全部无响应还是个别工具。"""
import json, time, urllib.request

MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"

def call(name, args, timeout=45):
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

def one(name, args, timeout=45):
    t = time.time()
    try:
        content = call(name, args, timeout)
        txt = "\n".join(c.get("text", "") for c in content)
        imgs = len([c for c in content if c.get("type") == "image"])
        return {"ok": True, "sec": round(time.time()-t,1), "len": len(txt), "imgs": imgs,
                "head": txt[:150].replace("\n"," ")}
    except Exception as e:
        return {"ok": False, "sec": round(time.time()-t,1), "err": "%s" % type(e).__name__}

tests = [
    ("get_variables",        {"projectDir": PROJ}, 30),
    ("get_frontend_code",    {"projectDir": PROJ, "targetNodeId": "1345:18487"}, 45),
    ("get_screenshot",       {"projectDir": PROJ, "targetNodeId": "1345:18487", "scale": 1}, 45),
    ("get_selection_node",   {"projectDir": PROJ}, 45),
]
rep = {}
for n, a, t in tests:
    rep[n] = one(n, a, t)
    print(n, "->", json.dumps(rep[n], ensure_ascii=False), flush=True)
