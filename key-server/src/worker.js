/* Máy chủ key kích hoạt của Ôn Luyện Nha Khoa
   - App gọi /api/activate (lần đầu nhập key) và /api/check (kiểm tra lại mỗi lần mở app khi có mạng).
   - Trang quản lý ở /admin: tạo key, xem máy đang dùng, khoá / mở khoá, đổi hạn, gỡ máy.
   Dữ liệu nằm trong D1 (xem schema.sql). Mật khẩu quản lý là secret ADMIN_PASSWORD. */
import ADMIN_HTML from './admin.html';

const ORIGINS = [
  'https://tunaasieunhat.github.io',      // bản web
  'https://appassets.androidplatform.net' // app Android (WebView)
];
const ALPHA = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'; // bỏ 0 O 1 I L cho khỏi nhầm
const MAX_FAILS = 10, FAIL_WINDOW = 15 * 60 * 1000;
const CHECK_EVERY = 6 * 60 * 60 * 1000; // app kiểm tra lại tối đa mỗi 6 giờ
const OFFLINE_GRACE = 14 * 24 * 60 * 60 * 1000; // không có mạng: vẫn dùng được 14 ngày kể từ lần kiểm tra cuối

function cors(req, env) {
  const o = req.headers.get('Origin') || '';
  const extra = (env.EXTRA_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  const ok = ORIGINS.includes(o) || extra.includes(o) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(o);
  return ok ? { 'Access-Control-Allow-Origin': o, 'Access-Control-Allow-Methods': 'GET,POST,OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type,Authorization', 'Access-Control-Max-Age': '86400', Vary: 'Origin' } : { Vary: 'Origin' };
}
const json = (data, status = 200, h = {}) => new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...h } });

export function normKey(s) {
  const raw = String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  const body = raw.startsWith('NK') && raw.length === 14 ? raw.slice(2) : raw;
  if (body.length !== 12 || [...body].some(c => !ALPHA.includes(c))) return null;
  return `NK-${body.slice(0, 4)}-${body.slice(4, 8)}-${body.slice(8)}`;
}
export function newKey() {
  const out = []; const buf = new Uint8Array(32);
  while (out.length < 12) {
    crypto.getRandomValues(buf);
    for (const b of buf) { if (b < 248 && out.length < 12) out.push(ALPHA[b % 31]); } // 248 = 31*8: không lệch xác suất
  }
  const s = out.join('');
  return `NK-${s.slice(0, 4)}-${s.slice(4, 8)}-${s.slice(8)}`;
}
const clean = (s, n) => String(s ?? '').replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, n);
const ipOf = req => req.headers.get('CF-Connecting-IP') || 'local';

async function tooMany(env, id) {
  const r = await env.DB.prepare('SELECT n, since FROM fails WHERE ip = ?').bind(id).first();
  return !!(r && Date.now() - r.since < FAIL_WINDOW && r.n >= MAX_FAILS);
}
async function fail(env, id) {
  const now = Date.now();
  await env.DB.prepare(`INSERT INTO fails (ip, n, since) VALUES (?1, 1, ?2)
    ON CONFLICT(ip) DO UPDATE SET n = CASE WHEN ?2 - since > ?3 THEN 1 ELSE n + 1 END, since = CASE WHEN ?2 - since > ?3 THEN ?2 ELSE since END`).bind(id, now, FAIL_WINDOW).run();
}

// Kiểm tra key + máy. register = true: cho phép thêm máy mới (lần kích hoạt đầu)
async function verify(env, req, body, register) {
  const ip = ipOf(req);
  if (await tooMany(env, ip)) return json({ ok: false, error: 'too_many' }, 429);
  const code = normKey(body.key), device = clean(body.device, 80);
  if (!code) { await fail(env, ip); return json({ ok: false, error: 'invalid' }, 404); }
  if (device.length < 8) return json({ ok: false, error: 'bad_request' }, 400);
  const k = await env.DB.prepare('SELECT * FROM keys WHERE code = ?').bind(code).first();
  if (!k) { await fail(env, ip); return json({ ok: false, error: 'invalid' }, 404); }
  const now = Date.now();
  if (k.revoked) return json({ ok: false, error: 'revoked' }, 403);
  if (k.expires_at && now >= k.expires_at) return json({ ok: false, error: 'expired', expires_at: k.expires_at }, 403);
  const d = await env.DB.prepare('SELECT last_at FROM devices WHERE code = ? AND device = ?').bind(code, device).first();
  const label = clean(body.label, 80);
  if (d) {
    if (now - d.last_at > 60 * 60 * 1000) await env.DB.prepare('UPDATE devices SET last_at = ?, label = CASE WHEN ? = \'\' THEN label ELSE ? END WHERE code = ? AND device = ?').bind(now, label, label, code, device).run();
  } else {
    if (!register) return json({ ok: false, error: 'device_removed' }, 403);
    const c = await env.DB.prepare('SELECT COUNT(*) AS n FROM devices WHERE code = ?').bind(code).first();
    if ((c?.n || 0) >= k.max_devices) return json({ ok: false, error: 'device_limit', max: k.max_devices }, 403);
    await env.DB.prepare('INSERT INTO devices (code, device, label, first_at, last_at) VALUES (?, ?, ?, ?, ?)').bind(code, device, label, now, now).run();
  }
  return json({ ok: true, key: code, name: k.name, expires_at: k.expires_at || null, check_every: CHECK_EVERY, offline_grace: OFFLINE_GRACE, now });
}

// So sánh mật khẩu không lộ thời gian
async function same(a, b) {
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([a, b].map(s => crypto.subtle.digest('SHA-256', enc.encode(String(s)))));
  const u = new Uint8Array(x), v = new Uint8Array(y); let r = 0;
  for (let i = 0; i < u.length; i++) r |= u[i] ^ v[i];
  return r === 0;
}
async function isAdmin(req, env) {
  const h = req.headers.get('Authorization') || '';
  const pw = h.startsWith('Bearer ') ? h.slice(7) : '';
  return !!(env.ADMIN_PASSWORD && env.ADMIN_PASSWORD.length >= 8 && pw && await same(pw, env.ADMIN_PASSWORD));
}

async function admin(req, env, path) {
  const ip = 'admin:' + ipOf(req);
  if (await tooMany(env, ip)) return json({ ok: false, error: 'too_many' }, 429);
  if (!await isAdmin(req, env)) { await fail(env, ip); return json({ ok: false, error: 'unauthorized' }, 401); }
  const DB = env.DB;
  if (path === '/api/admin/keys' && req.method === 'GET') {
    const keys = (await DB.prepare('SELECT * FROM keys ORDER BY created_at DESC').all()).results;
    const devs = (await DB.prepare('SELECT * FROM devices ORDER BY last_at DESC').all()).results;
    const by = {}; for (const d of devs) (by[d.code] ||= []).push(d);
    return json({ ok: true, now: Date.now(), keys: keys.map(k => ({ ...k, devices: by[k.code] || [] })) });
  }
  const body = await req.json().catch(() => ({}));
  if (path === '/api/admin/keys' && req.method === 'POST') {
    const name = clean(body.name, 80);
    if (!name) return json({ ok: false, error: 'name_required' }, 400);
    const max = Math.max(1, Math.min(10, parseInt(body.max_devices, 10) || 1));
    const exp = body.expires_at ? Number(body.expires_at) : null;
    if (exp !== null && !(exp > Date.now())) return json({ ok: false, error: 'bad_expiry' }, 400);
    const n = Math.max(1, Math.min(50, parseInt(body.count, 10) || 1));
    const out = [];
    for (let i = 0; i < n; i++) {
      const code = newKey(), nm = n > 1 ? `${name} ${i + 1}` : name;
      await DB.prepare('INSERT INTO keys (code, name, note, max_devices, expires_at, revoked, created_at) VALUES (?, ?, ?, ?, ?, 0, ?)').bind(code, nm, clean(body.note, 200), max, exp, Date.now()).run();
      out.push({ code, name: nm });
    }
    return json({ ok: true, created: out });
  }
  if (path === '/api/admin/key' && req.method === 'POST') {
    const code = normKey(body.code);
    if (!code) return json({ ok: false, error: 'invalid' }, 400);
    const a = body.action;
    if (a === 'revoke' || a === 'unrevoke') await DB.prepare('UPDATE keys SET revoked = ? WHERE code = ?').bind(a === 'revoke' ? 1 : 0, code).run();
    else if (a === 'update') {
      const max = Math.max(1, Math.min(10, parseInt(body.max_devices, 10) || 1));
      const exp = body.expires_at ? Number(body.expires_at) : null;
      await DB.prepare('UPDATE keys SET name = ?, note = ?, max_devices = ?, expires_at = ? WHERE code = ?').bind(clean(body.name, 80) || 'Không tên', clean(body.note, 200), max, exp, code).run();
    } else if (a === 'remove_device') await DB.prepare('DELETE FROM devices WHERE code = ? AND device = ?').bind(code, clean(body.device, 80)).run();
    else if (a === 'delete') { await DB.batch([DB.prepare('DELETE FROM devices WHERE code = ?').bind(code), DB.prepare('DELETE FROM keys WHERE code = ?').bind(code)]); }
    else return json({ ok: false, error: 'bad_action' }, 400);
    return json({ ok: true });
  }
  return json({ ok: false, error: 'not_found' }, 404);
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url), path = url.pathname.replace(/\/+$/, '') || '/';
    const ch = cors(req, env);
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: ch });
    try {
      if (path === '/admin') return new Response(ADMIN_HTML, { headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Frame-Options': 'DENY', 'Referrer-Policy': 'no-referrer' } });
      if (path.startsWith('/api/admin/')) return await admin(req, env, path);
      if (req.method === 'POST' && (path === '/api/activate' || path === '/api/check')) {
        const body = await req.json().catch(() => ({}));
        const r = await verify(env, req, body, path === '/api/activate');
        for (const [k, v] of Object.entries(ch)) r.headers.set(k, v);
        return r;
      }
      if (path === '/') return json({ ok: true, service: 'onluyen-key' }, 200, ch);
      return json({ ok: false, error: 'not_found' }, 404, ch);
    } catch (e) {
      return json({ ok: false, error: 'server' }, 500, ch);
    }
  }
};
