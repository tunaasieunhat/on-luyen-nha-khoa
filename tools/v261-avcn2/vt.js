/* @@VT-JS */
/* Version 2.6.1: AVCN2 cho người mất gốc – nút loa đọc từ, bài U0 / Gốc từ, Luyện từ 5 bậc */
var TH_EXTRA = { AVCN2: [
  { id: 'avcn2-u0', name: 'U0', title: 'Bắt đầu từ đây – Cách học cho người mất gốc', file: 'Glossary.pdf' },
  { id: 'avcn2-ugoc', name: 'Gốc từ', title: 'Gốc từ – Đoán nghĩa từ lạ', file: 'Glossary.pdf' }
] };
var VT_WORDS = __VT_DATA__;
const VT_ICON = '<svg class="i" viewBox="0 0 24 24"><path d="M4 20h4V12H4zM10 20h4V8h-4zM16 20h4V4h-4z"/></svg>';
const VT_LV = [
  ['Nghe và chọn nghĩa', 'Nghe từ rồi chọn nghĩa tiếng Việt đúng'],
  ['Nghĩa → từ', 'Từ tiếng Anh nào có nghĩa là'],
  ['Keyword → từ', 'Trong đề thấy keyword này, chọn từ nào?'],
  ['Định nghĩa → từ', 'Chọn từ điền vào chỗ trống (giống đề thi)'],
  ['Điền vào câu', 'Chọn từ điền vào câu']
];
const VT_DAY = 864e5, VT_INT = [0, 0, VT_DAY, 2 * VT_DAY, 4 * VT_DAY, 7 * VT_DAY];
const VT = { st: null, run: null };
const vtKey = () => 'vt_' + (typeof exPlayerKey === 'function' ? exPlayerKey() : 'guest');
function vtLoad() { VT.st = store.get(vtKey(), {}) || {}; return VT.st; }
function vtSave() { store.set(vtKey(), VT.st || {}); }
function vtUnitOf(id) { const m = /^avcn2-u(\d+)$/.exec(String(id || '')); return m ? m[1] : ''; }
function vtPool(u) { u = Number(u) || 0; return VT_WORDS.filter(w => !u || w.u === u); }
function vtStats(u) {
  const st = VT.st || vtLoad(), c = { n: 0, learn: 0, done: 0, all: 0, lv: [0, 0, 0, 0, 0, 0] };
  vtPool(u).forEach(w => { c.all++; const s = st[w.t]; if (!s) { c.n++; return; } c.lv[s.l]++; if (s.l >= 5) c.done++; else c.learn++; });
  return c;
}
/* ---------- giọng đọc ---------- */
let vtVoice = null;
function vtPickVoice() {
  try {
    const vs = speechSynthesis.getVoices() || [];
    vtVoice = vs.find(v => /^en[-_]US/i.test(v.lang) && /google|samantha|aria|jenny/i.test(v.name)) || vs.find(v => /^en[-_]US/i.test(v.lang)) || vs.find(v => /^en/i.test(v.lang)) || null;
  } catch { vtVoice = null; }
}
try { if (window.speechSynthesis) { vtPickVoice(); speechSynthesis.onvoiceschanged = vtPickVoice; } } catch {}
function vtSpeak(text, slow) {
  text = String(text || '').trim(); if (!text) return;
  try { if (window.AndroidApp && typeof AndroidApp.speak === 'function') { if (!AndroidApp.speak(text, slow ? .7 : .9)) toast('Đang mở giọng đọc tiếng Anh, bấm lại sau giây lát.'); return; } } catch {}
  try {
    if (!window.speechSynthesis || typeof SpeechSynthesisUtterance === 'undefined') throw 0;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    if (!vtVoice) vtPickVoice();
    if (vtVoice) u.voice = vtVoice;
    u.lang = vtVoice ? vtVoice.lang : 'en-US'; u.rate = slow ? .7 : .9;
    speechSynthesis.speak(u);
  } catch { toast('Máy này chưa có giọng đọc tiếng Anh. Hãy xem dòng “Đọc gần giống” bên cạnh.'); }
}
/* ---------- tiến độ trong bài ---------- */
function vtProgHTML(u) {
  const c = vtStats(u), pct = x => (c.all ? (x / c.all * 100) : 0).toFixed(1);
  const seg = [0, 1, 2, 3, 4, 5].map(l => c.lv[l] ? `<i class="l${l}" style="width:${pct(c.lv[l])}%" title="Bậc ${l}: ${c.lv[l]} từ"></i>` : '').join('');
  return `<div class="vtp-bar" aria-hidden="true">${seg}</div><p class="vtp-t"><b>${c.done}</b>/${c.all} từ đã thuộc · <b>${c.learn}</b> đang học · <b>${c.n}</b> chưa học</p>`;
}
function vtReader() {
  vtLoad();
  document.querySelectorAll('#th-body .vt-prog').forEach(el => { el.innerHTML = vtProgHTML(el.dataset.vtu); });
}
/* ---------- phiên luyện ---------- */
function vtQuestion(w) {
  const s = (VT.st || {})[w.t], l = s ? Math.min(s.l, 5) : 0, type = l >= 5 ? 3 : l;
  const same = VT_WORDS.filter(x => x.t !== w.t && x.u === w.u), other = VT_WORDS.filter(x => x.t !== w.t && x.u !== w.u);
  const pref = (type >= 3 ? shuffle(same.filter(x => x.p === w.p)) : []).concat(shuffle(same), shuffle(other));
  const seen = new Set([type === 0 ? w.m : w.t]), dis = [];
  for (const x of pref) { const k = type === 0 ? x.m : x.t; if (!seen.has(k)) { seen.add(k); dis.push(x); } if (dis.length === 3) break; }
  const opts = shuffle([w, ...dis]);
  return { w, type, lv: l, opts, ans: opts.indexOf(w) };
}
function vtStart(u) {
  vtLoad(); u = Number(u) || 0;
  const now = Date.now(), pool = vtPool(u), st = VT.st;
  const due = pool.filter(w => st[w.t] && st[w.t].d <= now).sort((a, b) => st[a.t].l - st[b.t].l || st[a.t].d - st[b.t].d);
  const fresh = pool.filter(w => !st[w.t]);
  let q = due.slice(0, 10);
  q = q.concat(fresh.slice(0, Math.min(6, 10 - q.length)));
  if (q.length < 10) {
    const rest = pool.filter(w => !q.includes(w)).sort((a, b) => ((st[a.t] || {}).l || 0) - ((st[b.t] || {}).l || 0) || ((st[a.t] || {}).d || 0) - ((st[b.t] || {}).d || 0));
    q = q.concat(rest.slice(0, 10 - q.length));
  }
  VT.run = { u, q: q.map(vtQuestion), i: 0, ok: 0, up: 0, again: new Set(), done: false, picked: null, total: q.length };
  vtOpen(); vtRender();
}
function vtOpen() {
  let ov = document.getElementById('vt');
  if (!ov) {
    ov = document.createElement('div'); ov.id = 'vt'; ov.className = 'vt'; ov.hidden = true;
    ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-labelledby', 'vt-h');
    ov.innerHTML = '<div class="vt-card"><div class="vt-top"><h2 id="vt-h"></h2><button class="icon-btn sm" type="button" data-vtx="1" aria-label="Đóng"><svg class="i" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div><div class="vt-bar"><i></i></div><div class="vt-main" id="vt-main" aria-live="polite"></div></div>';
    document.body.appendChild(ov);
  }
  ov.hidden = false; document.body.classList.add('mm-lock');
}
function vtClose() {
  const ov = document.getElementById('vt'); if (ov) ov.hidden = true;
  document.body.classList.remove('mm-lock'); VT.run = null;
  try { speechSynthesis.cancel(); } catch {}
  if (S.screen === 'theory') vtReader();
}
const vtSay = (t, cls) => `<button class="vw-say${cls ? ' ' + cls : ''}" type="button" data-say="${esc(t)}" aria-label="Nghe đọc ${esc(t)}"><svg class="i" viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg></button>`;
function vtRender() {
  const R = VT.run; if (!R) return;
  $('#vt-h').textContent = `Luyện từ 5 bậc · ${R.u ? 'Unit ' + R.u : 'tất cả Unit'}`;
  $('#vt .vt-bar i').style.width = `${Math.round(Math.min(R.i, R.q.length) / R.q.length * 100)}%`;
  const main = $('#vt-main');
  if (R.done) {
    const c = vtStats(R.u);
    main.innerHTML = `<div class="vt-end"><div class="vt-score">${R.ok}<small>/${R.q.length} câu đúng</small></div>
      <p>${R.up ? `<b>${R.up}</b> từ vừa lên bậc. ` : ''}${R.ok === R.q.length ? 'Tuyệt vời, không sai câu nào!' : 'Những từ sai sẽ được hỏi lại ở buổi sau.'}</p>
      <div class="vt-prog-end">${vtProgHTML(R.u)}</div>
      <ol class="vt-lv">${VT_LV.map((x, i) => `<li><b>Bậc ${i + 1}</b> ${esc(x[0])}<span>${c.lv[i]} từ</span></li>`).join('')}<li><b>Đã thuộc</b> qua đủ 5 bậc<span>${c.lv[5]} từ</span></li></ol>
      <div class="vt-act"><button class="btn btn-scrub" type="button" data-vtgo="${R.u}">Luyện tiếp 10 câu</button><button class="btn" type="button" data-vtx="1">Đóng</button></div></div>`;
    return;
  }
  const Q = R.q[R.i], w = Q.w, ans = R.picked !== null;
  let prompt = '';
  if (Q.type === 0) prompt = `<div class="vt-word">${vtSay(w.t, 'big')}<div><b lang="en">${esc(w.t)}</b><span>${esc(w.ipa)}</span></div></div>`;
  else if (Q.type === 1) prompt = `<p class="vt-big">“${esc(w.m)}”</p>`;
  else if (Q.type === 2) prompt = `<p class="vt-big" lang="en">${esc(w.kw)}</p>`;
  else if (Q.type === 3) prompt = `<p class="vt-def" lang="en">“${esc(w.d)}”</p>`;
  else prompt = `<p class="vt-def" lang="en">“${esc(w.x)}”</p><p class="vt-sub">Nghĩa của câu: ${esc(w.xv)}</p>`;
  const opts = Q.opts.map((o, i) => {
    const cls = ans ? (i === Q.ans ? ' right' : i === R.picked ? ' wrong' : ' dim') : '';
    return `<button class="opt${cls}" type="button" data-vtopt="${i}"${ans ? ' disabled' : ''}><span class="k">${'ABCD'[i]}</span><span${Q.type ? ' lang="en"' : ''}>${esc(Q.type === 0 ? o.m : o.t)}</span></button>`;
  }).join('');
  const fb = !ans ? '' : `<div class="vt-fb ${R.picked === Q.ans ? 'ok' : 'bad'}"><b class="vt-fh">${R.picked === Q.ans ? 'Đúng rồi!' : 'Chưa đúng.'}</b>
      <div class="vt-mini">${vtSay(w.t)}<div><b lang="en">${esc(w.t)}</b> <span class="vw-ipa">${esc(w.ipa)}</span><br><span>${esc(w.m)}</span></div></div>
      <p class="vt-k">Keyword trong đề: <b lang="en">${esc(w.kw)}</b></p>
      <button class="btn btn-scrub btn-sm" type="button" id="vt-next" data-vtnext="1">${R.i + 1 >= R.q.length ? 'Xem kết quả' : 'Câu tiếp'}</button></div>`;
  main.innerHTML = `<div class="vt-meta"><span class="vt-chip l${Q.lv}">${Q.lv >= 5 ? 'Ôn lại từ đã thuộc' : `Bậc ${Q.type + 1}/5 · ${esc(VT_LV[Q.type][0])}`}</span><span class="vt-n">${R.i + 1}/${R.q.length}</span></div>
    <p class="vt-ask">${esc(VT_LV[Q.type][1])}${Q.type === 1 ? ':' : ''}</p>${prompt}<div class="opts vt-opts">${opts}</div>${fb}`;
  if (!ans && Q.type === 0) setTimeout(() => { if (VT.run === R && R.picked === null) vtSpeak(w.t); }, 250);
  if (ans) { const n = document.getElementById('vt-next'); try { n.focus({ preventScroll: true }); } catch {} }
}
function vtAnswer(i) {
  const R = VT.run; if (!R || R.done || R.picked !== null) return;
  const Q = R.q[R.i], w = Q.w, st = VT.st, now = Date.now(), s = st[w.t] || { l: 0, d: now, n: 0 };
  R.picked = i; s.n = (s.n || 0) + 1;
  if (i === Q.ans) {
    R.ok++;
    if (!R.again.has(w.t)) { const nl = Math.min(5, s.l + 1); if (nl > s.l) R.up++; s.l = nl; s.d = now + (s.l >= 5 && Q.lv >= 5 ? 14 * VT_DAY : VT_INT[s.l]); }
  } else {
    s.l = Math.max(0, s.l - 1); s.d = now;
    if (!R.again.has(w.t)) { R.again.add(w.t); R.q.push(vtQuestion(w)); }
  }
  st[w.t] = s; vtSave(); vtRender();
}
function vtNext() {
  const R = VT.run; if (!R || R.picked === null) return;
  R.i++; R.picked = null;
  if (R.i >= R.q.length) R.done = true;
  vtRender();
}
document.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  if (t.dataset.say) { e.preventDefault(); vtSpeak(t.dataset.say); return; }
  if (t.dataset.vt !== undefined) { e.preventDefault(); vtStart(t.dataset.vt); return; }
  if (!t.closest('#vt')) return;
  if (t.dataset.vtx) vtClose();
  else if (t.dataset.vtopt !== undefined) vtAnswer(Number(t.dataset.vtopt));
  else if (t.dataset.vtnext) vtNext();
  else if (t.dataset.vtgo !== undefined) vtStart(t.dataset.vtgo);
});
document.addEventListener('keydown', e => {
  const ov = document.getElementById('vt'); if (!ov || ov.hidden || !VT.run) return;
  if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); vtClose(); return; }
  const R = VT.run;
  if (!R.done && R.picked === null) { const k = { 1: 0, 2: 1, 3: 2, 4: 3, a: 0, b: 1, c: 2, d: 3 }[String(e.key).toLowerCase()]; if (k !== undefined) { e.preventDefault(); vtAnswer(k); } }
  else if (!R.done && e.key === 'Enter') { e.preventDefault(); vtNext(); }
}, true);
window.__vt = { VT, stats: vtStats, open: id => openLesson(id) };
/* @@VT-JS-END */