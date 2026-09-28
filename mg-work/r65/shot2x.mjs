/**
 * shot2x.mjs —— 以 deviceScaleFactor=2 截图（CDP）
 *
 * 用法：node shot2x.mjs "<ws-url>" <url-suffix> <out.png> [exactUrl] [probeJs]
 *
 * ⚠️ 同一 URL 可能同时存在多个 page target（例如带/不带 ?fresh 的两个标签页），
 *    必须优先用 exactUrl 精确匹配，否则会截到另一个标签页的状态。
 *
 * ⚠️ 全文 JS 用普通字符串拼接，**不要**改成模板字符串（\s / \d 会被吞成转义）。
 */
import fs from 'node:fs';

const [, , wsUrl, urlSuffix, outPng, exactUrl, probeJs] = process.argv;

const send = (ws, id, method, params = {}, sessionId) =>
  new Promise((res, rej) => {
    const handler = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id === id) {
        ws.removeEventListener('message', handler);
        m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify(sessionId ? { id, method, params, sessionId } : { id, method, params }));
  });

const main = async () => {
  const ws = new WebSocket(wsUrl);
  let id = 0;
  await new Promise((r) => ws.addEventListener('open', r));
  const { targetInfos } = await send(ws, ++id, 'Target.getTargets');
  const cands = targetInfos.filter((t) => t.type === 'page' && t.url.includes(urlSuffix));
  if (!cands.length) throw new Error('找不到目标页面: ' + urlSuffix);
  let page = cands.find((t) => exactUrl && t.url === exactUrl);
  if (!page) page = cands[cands.length - 1];
  console.log('targets:', cands.map((t) => t.url).join('  ||  '));
  console.log('picked :', page.url);

  const { sessionId } = await send(ws, ++id, 'Target.attachToTarget', { targetId: page.targetId, flatten: true });
  await send(ws, ++id, 'Emulation.setDeviceMetricsOverride',
    { width: 1440, height: 900, deviceScaleFactor: 2, mobile: false }, sessionId);
  await new Promise((r) => setTimeout(r, 500));
  if (probeJs) {
    const r = await send(ws, ++id, 'Runtime.evaluate', { expression: probeJs, returnByValue: true }, sessionId);
    console.log('probe  :', JSON.stringify(r.result && r.result.value));
  }
  await new Promise((r) => setTimeout(r, 400));
  const shot = await send(ws, ++id, 'Page.captureScreenshot', { format: 'png' }, sessionId);
  fs.writeFileSync(outPng, Buffer.from(shot.data, 'base64'));
  console.log('saved  :', outPng);
  ws.close();
};

main().catch((e) => { console.error('ERR', e.message); process.exit(1); });
