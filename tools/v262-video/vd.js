/* @@VD-JS: Video bài giảng (Version 2.6.2) */
var VIDEOS = __VD_DATA__;
const VD_ICON = '<svg class="i" viewBox="0 0 24 24"><rect x="2.5" y="5" width="14" height="14" rx="2.5"/><path d="M16.5 10l5-3v10l-5-3z"/></svg>';
const VD_REMOTE = 'https://tunaasieunhat.github.io/on-luyen-nha-khoa/';
const VD = { id: null, built: null, cur: -1, cue: -1, remote: false, track: null, saveAt: 0 };
function vdData(id) { return (typeof VIDEOS === 'object' && VIDEOS) ? VIDEOS[id] || null : null; }
function vdStore(k, v) { try { if (v === undefined) return localStorage.getItem('vd:' + k); localStorage.setItem('vd:' + k, String(v)); } catch { return null; } }
const vdClock = t => { t = Math.max(0, Math.floor(t || 0)); const m = Math.floor(t / 60), s = t % 60; return `${m}:${String(s).padStart(2, '0')}`; };
function vdReader(l) {
  const v = vdData(l.id);
  $('#th-tab-vd').hidden = !v;
  $('#th-tab-vd-n').textContent = v ? `${Math.round(v.dur / 60)} phút` : '';
  $('#vd-title').textContent = `${l.no}: ${l.title || ''}`;
  if (VD.id !== l.id) { vdPause(); VD.id = l.id; VD.built = null; VD.cur = -1; VD.cue = -1; }
}
function vdPause() { const el = document.getElementById('vd-video'); if (el && !el.paused) { try { el.pause(); } catch {} } }
function vdVtt(v) {
  const f = t => { const ms = Math.round(t * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60;
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`; };
  return 'WEBVTT\n\n' + v.cues.map((c, i) => `${i + 1}\n${f(c[0])} --> ${f(c[1])}\n${c[2]}\n`).join('\n');
}
function vdSrc(v) { return (VD.remote ? VD_REMOTE : '') + v.src; }
function renderVD() {
  const v = vdData(VD.id); if (!v) return;
  const el = $('#vd-video');
  if (VD.built !== VD.id) {
    VD.built = VD.id; VD.remote = !!window.AndroidApp; VD.cur = -1; VD.cue = -1;
    if (VD.track) { try { URL.revokeObjectURL(VD.track); } catch {} }
    VD.track = URL.createObjectURL(new Blob([vdVtt(v)], { type: 'text/vtt' }));
    el.innerHTML = `<track kind="subtitles" srclang="vi" label="Tiếng Việt" default src="${VD.track}">`;
    el.src = vdSrc(v); el.preload = 'metadata';
    const sl = slData(VD.id);
    $('#vd-ch').innerHTML = v.ch.map((c, i) => `<button type="button" data-vdto="${i}"${sl ? '' : ' class="noimg"'}>${sl ? `<img src="${slSrc(sl, i)}" alt="" loading="lazy" decoding="async">` : ''}<span><b>${i + 1}. ${esc(c[1])}</b><small>${vdClock(c[0])}</small></span></button>`).join('');
    $('#vd-meta').textContent = `${v.ch.length} slide · ${vdClock(v.dur)} · ${v.mb} MB`;
    $('#vd-dl').href = VD_REMOTE + v.src;
    const pos = Number(vdStore('pos:' + VD.id)) || 0;
    $('#vd-resume').hidden = !(pos > 20 && pos < v.dur - 30);
    $('#vd-resume-t').textContent = vdClock(pos);
    el.addEventListener('loadedmetadata', () => { vdRate(); vdCC(); }, { once: true });
  }
  vdSync();
}
function vdSeek(t, play) {
  const el = $('#vd-video');
  const go = () => { try { el.currentTime = Math.max(0, t); } catch {} if (play) { const p = el.play(); if (p && p.catch) p.catch(() => {}); } };
  if (el.readyState >= 1) go(); else { el.addEventListener('loadedmetadata', go, { once: true }); try { el.load(); } catch {} }
  $('#vd-resume').hidden = true;
}
function vdRate(r) {
  if (r) vdStore('rate', r);
  const rate = Number(vdStore('rate')) || 1, el = $('#vd-video');
  try { el.playbackRate = rate; el.defaultPlaybackRate = rate; } catch {}
  $$('#vd-rate [data-vdrate]').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.vdrate) === rate)));
}
function vdCC(flip) {
  let on = vdStore('cc') !== '0';
  if (flip) { on = !on; vdStore('cc', on ? 1 : 0); }
  const el = $('#vd-video'), tr = el.textTracks && el.textTracks[0];
  if (tr) tr.mode = on ? 'showing' : 'hidden';
  $('#vd-cc').setAttribute('aria-pressed', String(on));
}
function vdSync() {
  const v = vdData(VD.id); if (!v) return;
  const el = $('#vd-video'), t = el.currentTime || 0;
  let i = 0; while (i + 1 < v.ch.length && v.ch[i + 1][0] <= t + .05) i++;
  if (i !== VD.cur) {
    VD.cur = i;
    const box = $('#vd-ch');
    box.querySelectorAll('button').forEach((b, k) => b.setAttribute('aria-current', String(k === i)));
    const b = box.children[i];
    if (b && !$('#th-vd').hidden) { try { const T = b.offsetTop - box.offsetTop, H = box.clientHeight; if (T < box.scrollTop || T + b.offsetHeight > box.scrollTop + H) box.scrollTo({ top: T - (H - b.offsetHeight) / 2, behavior: reduced ? 'auto' : 'smooth' }); } catch {} }
    $('#vd-now').textContent = `Slide ${i + 1} / ${v.ch.length}: ${v.ch[i][1]}`;
  }
  if (t > 5 && Date.now() - VD.saveAt > 4000) { VD.saveAt = Date.now(); vdStore('pos:' + VD.id, t > v.dur - 15 ? 0 : Math.floor(t)); }
}
(function () {
  const el = $('#vd-video');
  el.addEventListener('timeupdate', vdSync);
  el.addEventListener('seeked', vdSync);
  el.addEventListener('error', () => {
    const v = vdData(VD.id); if (!v || !el.getAttribute('src')) return;
    if (!VD.remote) { VD.remote = true; const t = el.currentTime; el.src = vdSrc(v); if (t) vdSeek(t); return; }
    toast('Chưa tải được video. Video cần có mạng, hãy kiểm tra kết nối rồi thử lại.');
  });
  el.addEventListener('pause', () => { const v = vdData(VD.id); if (v && el.currentTime > 5) vdStore('pos:' + VD.id, Math.floor(el.currentTime)); });
  document.addEventListener('keydown', e => {
    const p = $('#th-vd'); if (!p || p.hidden || $('#th-read').hidden) return;
    if (e.target && /^(INPUT|TEXTAREA|SELECT|VIDEO|BUTTON)$/.test(e.target.tagName)) return;
    if (e.key === ' ' || e.key === 'k') { e.preventDefault(); if (el.paused) { const q = el.play(); if (q && q.catch) q.catch(() => {}); } else el.pause(); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); vdSeek((el.currentTime || 0) + 10); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); vdSeek((el.currentTime || 0) - 10); }
  });
})();
/* @@VD-JS-END */
