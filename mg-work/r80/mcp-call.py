import json,sys,urllib.request
URL="http://127.0.0.1:20678/mcp"
def call(method,params,timeout=300):
    body=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    req=urllib.request.Request(URL,data=body,headers={
        "Content-Type":"application/json",
        "Accept":"application/json, text/event-stream"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        raw=r.read().decode("utf-8","replace")
    if "data: " in raw:
        raw=raw.split("data: ",1)[1].strip()
        raw=raw.split("\n")[0]
    d=json.loads(raw)
    if "error" in d: raise SystemExit("MCP error: "+json.dumps(d["error"],ensure_ascii=False)[:600])
    return d["result"]
def tool(name,args,timeout=300):
    r=call("tools/call",{"name":name,"arguments":args},timeout)
    return r
if __name__=="__main__":
    name=sys.argv[1]; args=json.loads(sys.argv[2]); out=sys.argv[3] if len(sys.argv)>3 else None
    r=tool(name,args)
    txt=json.dumps(r,ensure_ascii=False,indent=1)
    if out:
        open(out,"w",encoding="utf-8").write(txt); print("saved",out,len(txt),"chars")
    else: print(txt[:3000])
