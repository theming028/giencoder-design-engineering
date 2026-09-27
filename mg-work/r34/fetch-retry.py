# -*- coding: utf-8 -*-
"""后台低频重试：每 90s 试一次 get_selection_node，成功即落盘，最多 8 次（约 12 分钟）。"""
import json, io, os, time, urllib.request
MCP = "http://127.0.0.1:20678/mcp"
PROJ = "E:/GienCoder/giencoder-design-engineering"
TARGETS = [("1345:18487", "mg-work/r34/design/avatar-main"),
           ("1345:18502", "mg-work/r34/design/avatar-chat")]

def call(name, args, timeout=120):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": name, "arguments": args}}).encode("utf-8")
    req = urllib.request.Request(MCP, data=body, headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")

def fetch(nid, out):
    raw = call("get_selection_node", {"projectDir": PROJ, "targetNodeId": nid})
    out_l = []
    for line in raw.splitlines():
        if line.startswith("data: "):
            d = json.loads(line[6:])
            for c in d.get("result", {}).get("content", []):
                out_l.append(c)
    txt = "\n".join(c.get("text", "") for c in out_l)
    if txt.strip() and "❌" not in txt:
        io.open(out + ".txt", "w", encoding="utf-8").write(txt)
        return len(txt)
    return 0

for i in range(8):
    ok = 0
    for nid, out in TARGETS:
        if os.path.exists(out + ".txt"): continue
        try:
            n = fetch(nid, out)
        except Exception as e:
            n = 0
            print("attempt %d %s ERR %s" % (i+1, nid, type(e).__name__), flush=True)
        if n:
            print("attempt %d %s OK len=%d" % (i+1, nid, n), flush=True); ok += 1
        else:
            print("attempt %d %s no-data" % (i+1, nid), flush=True)
    if all(os.path.exists(o + ".txt") for _, o in TARGETS):
        print("ALL_DONE", flush=True); break
    time.sleep(90)
print("EXIT", flush=True)
