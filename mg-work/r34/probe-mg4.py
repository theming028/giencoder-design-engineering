# -*- coding: utf-8 -*-
import json, os, time, urllib.request
MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"

def call(name, args, timeout=150):
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

for nid, pref in (("1345:18487","main"), ("1345:18502","chat")):
    t = time.time()
    try:
        content = call("get_frontend_code", {
            "projectDir": PROJ, "targetNodeId": nid,
            "frontendFramework": "json", "outDir": "mg-work/r34/design",
            "fileName": "avatar-%s.json" % pref, "writeToFile": True}, 150)
        txt = "\n".join(c.get("text","") for c in content)
        print("[%s] sec=%.1f len=%d" % (nid, time.time()-t, len(txt)), flush=True)
        print(txt[:400].replace("\n"," "), flush=True)
    except Exception as e:
        print("[%s] ERR %s sec=%.1f" % (nid, type(e).__name__, time.time()-t), flush=True)
