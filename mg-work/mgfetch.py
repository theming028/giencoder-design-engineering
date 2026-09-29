# -*- coding: utf-8 -*-
"""
mgfetch · MasterGo 设计节点取数（一次调用搞定，含超时自愈）

为什么要它（第 82 轮踩过的坑）：
  1. MCP 的 get_selection_node 走的是**画布当前页**。目标图层不在当前页时，
     传「裸图层 ID」会立刻返回 TargetNodePageMismatch —— 但传**完整 goto 链接**时
     服务端仍会去取（跨页可用），只是经常 90~120s 才回，甚至 HTTP 读超时。
  2. HTTP 读超时 ≠ 没数据：`~/.mgmcp/artifacts/sessions/as_*.json` 里会留下
     这次请求的 Asset Session（含 sha256），SVG 就在 `artifacts/blobs/sha256/<前2位>/<后62位>`。
     → 所以超时后**不要重试**，直接去 blob 捞，秒级拿到结果。

用法：
  python mg-work/mgfetch.py <链接或图层ID> [更多...] \
      [--out mg-work/rNN/raw] [--timeout 300] [--since 600]

  <链接或图层ID>   给 MasterGo 的 goto 链接最好（能解析出 page_id + layer_id）；
                   纯图层 ID 只有在画布正好停在那一页时才可用。
  --out            落盘目录（默认 mg-work/mgfetch）
  --timeout        单节点 HTTP 等待秒数（默认 300）
  --since          只认这个秒数之内新建的 asset session（默认 900，避免捞到旧产物）

产物：
  <out>/node_<ID>.json     MCP 原文（成功时）
  <out>/asset_<ID>.<ext>   从 blob 解出的素材（成功时，无论 HTTP 是否超时）
  <out>/fetch.log          过程日志
退出码：0 全部拿到；2 有节点没拿到（细节见 log 与 stdout 的处置建议）
"""
import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.request

MCP_URL = 'http://127.0.0.1:20678/mcp'
MGMCP = os.path.join(os.path.expanduser('~'), '.mgmcp')
SESSIONS = os.path.join(MGMCP, 'artifacts', 'sessions')
BLOBS = os.path.join(MGMCP, 'artifacts', 'blobs', 'sha256')

LAYER_RE = re.compile(r'layer_id=([0-9]+:[0-9]+)')
PAGE_RE = re.compile(r'page_id=([0-9a-zA-Z]+:[0-9]+)')


def log(msg, fh=None):
    line = str(msg)
    print(line)
    if fh:
        fh.write(line + '\n')
        fh.flush()


def call(method, params, timeout):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode()
    req = urllib.request.Request(MCP_URL, data=body, headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode('utf-8', 'replace')
    if 'data: ' in raw:
        raw = raw.split('data: ', 1)[1].strip().split('\n')[0]
    return json.loads(raw)


def node_id_of(spec):
    m = LAYER_RE.search(spec)
    if m:
        return m.group(1)
    if re.fullmatch(r'\d+:\d+', spec.strip()):
        return spec.strip()
    m = re.search(r'([0-9]+:[0-9]+)', spec)
    return m.group(1) if m else None


def canvas_page():
    """从 mgmcp.log 尾部读画布当前激活页，用于给出『该切到哪一页』的处置建议。"""
    p = os.path.join(MGMCP, 'mgmcp.log')
    try:
        with open(p, 'rb') as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 400000))
            tail = f.read().decode('utf-8', 'replace')
    except OSError:
        return None, None
    ids = re.findall(r'\\"documentPageId\\":\\"([^"\\]+)\\",\\"documentPageName\\":\\"([^"\\]+)\\"', tail)
    if not ids:
        return None, None
    return ids[-1][0], ids[-1][1]


def blob_for(sha):
    # ⚠ 目录名 = sha 前 2 位，文件名 = **完整 sha**（不是去掉前 2 位的部分）
    return os.path.join(BLOBS, sha[:2], sha)


def harvest_assets(nid, since, out, fh):
    """从 asset session 捞这次请求的素材（HTTP 超时也能拿到）。"""
    got = []
    seen = set()
    cutoff = time.time() - since
    for f in glob.glob(os.path.join(SESSIONS, 'as_*.json')):
        try:
            if os.path.getmtime(f) < cutoff:
                continue
            d = json.load(open(f, encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if nid not in (d.get('targetNodeIds') or []):
            continue
        for a in d.get('assets') or []:
            sha = a.get('sha256')
            bp = blob_for(sha) if sha else None
            if not bp or not os.path.exists(bp):
                continue
            if sha in seen:          # 同一节点短时间内多次请求 → 多个 session 含相同素材，去重
                continue
            seen.add(sha)
            lp = a.get('logicalPath') or ''
            base = os.path.basename(lp) or ('asset_%s' % (nid.replace(':', '-')))
            # ⚠ 同一节点的多个素材必须用**各自主文件名**（默认 svg_xxxxxxxx.svg），
            #   否则会被后写覆盖成只剩最后一件（r83 踩到：5 件只剩 1 件）。
            dest = os.path.join(out, '%s__%s' % (nid.replace(':', '-'), base))
            with open(bp, 'rb') as src, open(dest, 'wb') as dst:
                dst.write(src.read())
            got.append((dest, a.get('size'), lp))
            log('    ↳ asset %s (%s bytes) ← blob %s' % (dest, a.get('size'), sha[:12]), fh)
    return got


def fetch_one(spec, args, fh):
    nid = node_id_of(spec)
    log('── %s  (node %s)' % (spec[:96], nid), fh)
    if not nid:
        log('   !! 解析不出图层 ID，跳过', fh)
        return False
    t0 = time.time()
    raw = None
    try:
        raw = call('tools/call', {'name': 'get_selection_node',
                                  'arguments': {'projectDir': args.root, 'targetNodeId': spec}},
                   args.timeout)
    except Exception as e:                                    # noqa: BLE001
        log('   HTTP %.1fs → %s（继续走 asset 兜底）' % (time.time() - t0, type(e).__name__), fh)
    if raw is not None:
        try:
            txt = raw['result']['content'][0]['text']
        except (KeyError, IndexError, TypeError):
            txt = json.dumps(raw, ensure_ascii=False)[:300]
        if raw.get('result', {}).get('isError') or 'TargetNodePageMismatch' in txt:
            log('   ✗ %s' % txt.strip()[:200], fh)
            cid, cname = canvas_page()
            log('   ⇒ 处置：让画布切到目标页再跑（当前画布页 = %s %s）；'
                '或本仓历史落盘 mg-work/r80/raw/sel_*.json 里按 documentPageId 找旧导出。'
                % (cid, cname), fh)
            harvest_assets(nid, args.since, args.out, fh)
            return False
        path = os.path.join(args.out, 'node_%s.json' % nid.replace(':', '-'))
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(raw, f, ensure_ascii=False, indent=1)
        log('   ✓ %.1fs → %s (%d bytes)' % (time.time() - t0, path, len(json.dumps(raw))), fh)
    assets = harvest_assets(nid, args.since, args.out, fh)
    if assets:
        log('   ✓ 通过 asset 兜底拿到 %d 件素材' % len(assets), fh)
        return True
    if raw is not None:
        return True
    log('   ✗ 既无 HTTP 结果、也无 asset 兜底。判定：该页解析失败或画布不在目标页。', fh)
    cid, cname = canvas_page()
    log('   ⇒ 当前画布页 = %s %s' % (cid, cname), fh)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('targets', nargs='+')
    ap.add_argument('--out', default='mg-work/mgfetch')
    ap.add_argument('--root', default=None)
    ap.add_argument('--timeout', type=float, default=300)
    ap.add_argument('--since', type=float, default=900)
    args = ap.parse_args()

    args.root = args.root or os.getcwd()
    os.makedirs(args.out, exist_ok=True)
    fh = open(os.path.join(args.out, 'fetch.log'), 'a', encoding='utf-8')
    log('==== mgfetch %s ====' % time.strftime('%Y-%m-%d %H:%M:%S'), fh)
    ok = 0
    for spec in args.targets:
        if fetch_one(spec, args, fh):
            ok += 1
    log('结果：%d/%d 拿到' % (ok, len(args.targets)), fh)
    fh.close()
    sys.exit(0 if ok == len(args.targets) else 2)


if __name__ == '__main__':
    main()
